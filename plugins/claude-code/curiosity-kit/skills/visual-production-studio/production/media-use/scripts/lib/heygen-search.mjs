import { execFileSync } from "node:child_process";

export function heygenSearch(subcommand, query, { type, limit = 5, minScore } = {}) {
  const allowed=new Set(["audio sounds list","asset search"]);
  if(!allowed.has(subcommand))throw Error("unsupported HeyGen operation");
  const parts=["--headers","X-HeyGen-Client-Source: media-use",...subcommand.split(" "),"--query",query];
  if(type)parts.push("--type",type);
  parts.push("--limit",String(limit));
  if(minScore!=null)parts.push("--min-score",String(minScore));

  let out;
  try {
    out = execFileSync("heygen", parts, {
      encoding: "utf8",
      timeout: 15000,
      stdio: ["pipe", "pipe", "pipe"],
    });
  } catch (err) {
    // Don't swallow a broken command / auth failure as "no results" — that turns
    // a typo or expired key into a silent dead end. Surface it, then give up.
    const detail = err.stderr?.toString().trim() || err.stdout?.toString().trim() || err.message;
    console.error(`media-use: \`heygen ${subcommand}\` failed: ${detail}`);
    return null;
  }

  let parsed;
  try {
    parsed = JSON.parse(out);
  } catch {
    console.error(`media-use: \`heygen ${subcommand}\` returned non-JSON output`);
    return null;
  }
  if (parsed?.error) {
    const e = parsed.error;
    console.error(`media-use: \`heygen ${subcommand}\` error: ${e.message ?? JSON.stringify(e)}`);
    return null;
  }

  const data = parsed?.data;
  return Array.isArray(data) && data.length > 0 ? data : null;
}
