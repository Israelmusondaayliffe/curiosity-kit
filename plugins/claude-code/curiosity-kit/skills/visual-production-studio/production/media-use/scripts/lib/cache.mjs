import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync, rmdirSync } from "node:fs";
import { join, basename, resolve } from "node:path";
import { createHash } from "node:crypto";
import { homedir } from "node:os";
import { readManifest, appendRecord } from "./manifest.mjs";

import {inside} from "../../../shared-storyboard/scripts/lib/safety.mjs";
const SCHEMA_PREFIX = "mu-v1-";
const KEY_HEX_CHARS = 16;
const COMPLETE_SENTINEL = ".hf-complete";

export function globalMediaDir() {
  if(!process.env.MEDIA_CACHE_DIR) throw new Error("cross-project cache requires explicit MEDIA_CACHE_DIR");
  return resolve(process.env.MEDIA_CACHE_DIR);
}

export function contentHash(filePath) {
  const bytes = readFileSync(filePath);
  return createHash("sha256").update(bytes).digest("hex");
}

function cacheEntryDir(rootDir, sha) {
  return join(rootDir, SCHEMA_PREFIX + sha.slice(0, KEY_HEX_CHARS));
}

function isComplete(entryDir) {
  return existsSync(join(entryDir, COMPLETE_SENTINEL));
}

function markComplete(entryDir) {
  writeFileSync(join(entryDir, COMPLETE_SENTINEL), "", "utf8");
}

function readGlobalManifest() {
  return readManifest(globalMediaDir());
}

function validateCacheHit(match) {
  if (!match?.sha || !match.cached_path || !existsSync(match.cached_path)) return null;
  if (!resolve(match.cached_path).startsWith(resolve(globalMediaDir())+"/")) return null;
  if(contentHash(match.cached_path)!==match.sha)return null;
  return isComplete(cacheEntryDir(globalMediaDir(), match.sha)) ? match : null;
}

export function cacheGet(prompt, type) {
  return validateCacheHit(
    readGlobalManifest().find(
      (r) => r.reusable && r.provenance?.prompt === prompt && (type == null || r.type === type),
    ),
  );
}

export function cacheGetByEntity(entity) {
  const lower = entity.toLowerCase();
  return validateCacheHit(
    readGlobalManifest().find((r) => r.reusable && r.entity && r.entity.toLowerCase() === lower),
  );
}

export function cachePut(filePath, record) {
  const root=globalMediaDir();mkdirSync(root,{recursive:true});const lock=join(root,".write.lock");
  try{mkdirSync(lock);}catch{throw new Error("cache busy; serialize promotion and retry");}
  try {
  const sha = contentHash(filePath);
  const dir = globalMediaDir();
  const entryDir = cacheEntryDir(dir, sha);
  mkdirSync(entryDir, { recursive: true });

  const dest = join(entryDir, basename(filePath));
  copyFileSync(filePath, dest);
  markComplete(entryDir);

  const globalRecord = {
    ...record,
    sha,
    reusable: true,
    cached_path: dest,
  };
  appendRecord(globalMediaDir(), globalRecord);
  return { sha, cached_path: dest };
  } finally { rmdirSync(lock); }
}

export function importFromCache(cacheRecord, projectDir, localId, localPath) {
  const sha = cacheRecord.sha;
  const entryDir = cacheEntryDir(globalMediaDir(), sha);
  if (!isComplete(entryDir) || !validateCacheHit(cacheRecord)) return null;

  const cachedFile = cacheRecord.cached_path;
  if (!cachedFile || !existsSync(cachedFile)) return null;

  mkdirSync(join(projectDir, ".media"), { recursive: true });
  const fullDest = inside(projectDir, localPath);
  mkdirSync(join(fullDest, ".."), { recursive: true });
  copyFileSync(cachedFile, fullDest);

  const projectRecord = {
    ...cacheRecord,
    id: localId,
    path: localPath,
    provenance: {
      ...cacheRecord.provenance,
      imported_from: sha,
    },
  };
  delete projectRecord.sha;
  delete projectRecord.reusable;
  delete projectRecord.cached_path;

  return projectRecord;
}

export function promote(projectDir, id) {
  const records = readManifest(projectDir);
  const record = records.find((r) => r.id === id);
  if (!record) throw new Error(`asset not found in project manifest: ${id}`);

  const filePath = inside(projectDir, record.path);
  if (!existsSync(filePath)) throw new Error(`asset file not found: ${filePath}`);

  return cachePut(filePath, record);
}
