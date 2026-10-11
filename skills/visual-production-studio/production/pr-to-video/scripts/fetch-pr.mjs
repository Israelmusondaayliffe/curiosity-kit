#!/usr/bin/env node
// Step 1 — PR fetch (deterministic; runs gh; large-PR-safe; NO scratch dir).
//
// Replaces a bare `gh pr view … > capture/pr.json` in the orchestrator. It folds
// the PR into the two artifacts ingest.mjs consumes:
//   capture/pr.json    the gh pr view core (title, body, author, refs, commits,
//                      reviews, comments, assignees, +/− stats, …) with its `files`
//                      list COMPLETED via a paginated `gh api .../pulls/N/files`
//                      call — `gh pr view --json files` truncates at ~100 files, so a
//                      big PR would otherwise lose the tail. Commits keep gh pr view's
//                      rich `authors[]` (co-authors) — only `files` needs the override.
//   capture/diff.patch the full unified diff (`gh pr diff`).
//
// gh runs HERE so auth / not-found / private-repo errors surface with gh's own stderr
// and exit 1 (the orchestrator then stops). Intermediates are held in memory — this
// writes ONLY the two files above, so there is no `_ingest_tmp/` scratch to clean up
// (the previous "let the agent fetch in pieces" approach polluted videos/ and was
// non-deterministic). ingest.mjs stays a pure offline transform downstream.
//
// Usage:
//   node fetch-pr.mjs --pr "<url | owner/repo#N | N>" [--out-dir ./capture]
//
// Exit 0 = capture/pr.json + capture/diff.patch written + summary on stdout.
// Exit 1 = gh not authenticated / PR not found / pr view failed.

import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync, renameSync, rmdirSync } from "node:fs";
import { join, resolve } from "node:path";

import {randomUUID,createHash} from "node:crypto";
const argv = process.argv.slice(2);
const flag = (name, def) => {
  const i = argv.indexOf(`--${name}`);
  return i >= 0 && i + 1 < argv.length ? argv[i + 1] : def;
};
function die(msg) {
  if(globalThis.__captureStatus) {globalThis.__captureStatus.status.errors.push(msg); writeFileSync(join(globalThis.__captureStatus.outDir,"capture-status.json"),JSON.stringify(globalThis.__captureStatus.status,null,2));}
  console.error(`✗ fetch-pr.mjs: ${msg}`);
  process.exit(1);
}

const prRef = flag("pr", null);
if (!prRef) die('--pr "<url | owner/repo#N | N>" is required');
const outDir = resolve(flag("out-dir", "./capture"));
mkdirSync(outDir,{recursive:true});
const lock=join(outDir,".fetch.lock");try{mkdirSync(lock);}catch{throw Error("capture busy; serialize PR fetches");}
process.on("exit",()=>{try{rmdirSync(lock);}catch{}});
const captureStatus={session:randomUUID(),complete:false,pr:prRef,errors:[],captured_at:new Date().toISOString()};
globalThis.__captureStatus={status:captureStatus,outDir};
writeFileSync(join(outDir,"capture-status.json"),JSON.stringify(captureStatus,null,2));
const sessionDir=join(outDir,"sessions",captureStatus.session);mkdirSync(sessionDir,{recursive:true});

// Run gh, capture stdout. Returns { ok, stdout, stderr } — never throws (callers
// decide whether a failure is fatal). 64 MB buffer covers large diffs / file lists.
function ghTry(args) {
  try {
    const stdout = execFileSync("gh", args, { encoding: "utf8", timeout:120000, maxBuffer: 64 * 1024 * 1024 });
    return { ok: true, stdout, stderr: "" };
  } catch (e) {
    return {
      ok: false,
      stdout: (e.stdout || "").toString(),
      stderr: (e.stderr || e.message || "").toString().trim(),
    };
  }
}

// ── 0. auth — fail fast with gh's own hint ───────────────────────────────────
if (!ghTry(["auth", "status"]).ok) {
  die("gh is not authenticated — run: gh auth login");
}

// ── 1. core PR object (gh pr view) ───────────────────────────────────────────
const FIELDS = [
  "number",
  "title",
  "body",
  "author",
  "url",
  "baseRefName",
  "headRefName",
  "commits",
  "files",
  "additions",
  "deletions",
  "changedFiles",
  "labels",
  "reviews",
  "latestReviews",
  "comments",
  "assignees",
  "reviewDecision",
  "mergedBy",
].join(",");

const view = ghTry(["pr", "view", prRef, "--json", FIELDS]);
if (!view.ok) die(`gh pr view "${prRef}" failed (auth / not found / private?):\n${view.stderr}`);

let pr;
try {
  pr = JSON.parse(view.stdout);
} catch (e) {
  die(`gh pr view returned unparseable JSON (${e.message})`);
}

// ── 2. complete the files list via paginated gh api (the truncation fix) ──────
// gh pr view --json files caps at ~100 files; the REST endpoint is paginated; its service cap is checked against changedFiles. --jq runs per page, so the output is NDJSON (one file object per line).
const number = pr.number;
const m = /github\.com\/([^/]+)\/([^/]+)\/pull\/\d+/.exec(pr.url || "");
const owner = m?.[1];
const repo = m?.[2];
let filesNote = `${Array.isArray(pr.files) ? pr.files.length : 0} (from pr view)`;
if (owner && repo && number != null) {
  const apiFiles = ghTry([
    "api",
    "--paginate",
    `repos/${owner}/${repo}/pulls/${number}/files`,
    "--jq",
    ".[] | {path: .filename, additions, deletions, status}",
  ]);
  if (!apiFiles.ok) die("file pagination failed: "+apiFiles.stderr);
  let files;
  try {files=apiFiles.stdout.split("\n").filter(Boolean).map(JSON.parse);}catch(e){die("file pagination returned malformed data: "+e.message);}
  if(!Number.isInteger(pr.changedFiles)||files.length!==pr.changedFiles) die(`incomplete file evidence: fetched ${files.length}, expected ${pr.changedFiles}; provider caps may apply`);
  pr.files=files;filesNote=`${files.length} verified against changedFiles`;
} else {die("could not bind owner/repo/number from PR URL");}
const diff=ghTry(["pr","diff",prRef]);
if(!diff.ok || (pr.changedFiles>0 && !diff.stdout.trim()))die("diff retrieval failed or empty: "+diff.stderr);
pr._capture={session:captureStatus.session,complete:true};
const prBytes=JSON.stringify(pr,null,2)+"\n";
writeFileSync(join(sessionDir,"pr.json"),prBytes);writeFileSync(join(sessionDir,"diff.patch"),diff.stdout);
captureStatus.complete=true;
captureStatus.sha256={pr:createHash("sha256").update(prBytes).digest("hex"),diff:createHash("sha256").update(diff.stdout).digest("hex")};
writeFileSync(join(sessionDir,"manifest.json"),JSON.stringify(captureStatus,null,2));
const prJsonPath=join(outDir,"pr.json"),diffPath=join(outDir,"diff.patch");
for(const [path,bytes] of [[prJsonPath,prBytes],[diffPath,diff.stdout]]){const tmp=path+"."+captureStatus.session+".tmp";writeFileSync(tmp,bytes);renameSync(tmp,path);}
writeFileSync(join(outDir,"capture-status.json"),JSON.stringify(captureStatus,null,2));

// ── 4. summary ───────────────────────────────────────────────────────────────
const repoLabel = owner && repo ? `${owner}/${repo}` : "(repo?)";
console.log(
  [
    `✓ fetch-pr: ${repoLabel} PR #${number ?? "?"} — "${(pr.title || "").slice(0, 72)}"`,
    `  files: ${filesNote}; diff: ${diff.ok ? `${diff.stdout.length} chars` : "MISSING"}`,
    `  wrote ${prJsonPath}${diff.ok ? ` + ${diffPath}` : ""}`,
  ].join("\n"),
);
