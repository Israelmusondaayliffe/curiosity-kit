# Recall

## Establish scope

Identify the project/checkout and current host. Default `platformSource` to `codex` or `claude`; use the requested dates, types or terms. Confirm broader disclosure when the task does not establish it. Worktree aliases may share a project; inspect the returned project rather than guessing from a folder name.

Discover the engine's actual public tool names and accepted arguments using the [host contract](../references/host-contract.md). Do not call server-only `observation_*` tools against worker mode.

## Retrieve progressively

For a private marker, make one search using the exact full marker and all requested scope filters. An empty result means no searchable match in that scope, not global absence. Do not retry fragments, suffixes or fuzzy variants unless the user explicitly requests it and every scope restriction is retained.

1. Call `search` with the question's terms, project, host source and relevant time filters. Start with a small bounded result limit.
2. Read IDs, titles, dates, projects and types. Select useful matches; refine the query or page the index only when necessary.
3. If order or surrounding decisions matter, call `timeline` around a selected ID with explicit small before/after depths. Preserve project/source filters where the actual schema supports them.
4. Call `get_observations` once for the selected IDs. Check each returned record's scope. Do not assume filters from the first call carry forward automatically.
5. Only if a summary omits required literal evidence, use supported `get_tool_uses` for already identified calls. Keep project/session/source restrictions where supported. Summaries cannot stand in for an exact diff or command output.

Never invent arguments the installed tool rejects. If a required filter cannot be enforced, disclose that limit and choose a supported scoped route; do not silently broaden retrieval. Avoid `full` context by default.

## Check the answer

For a consequential fact, compare the recalled claim with the current file or source-owned system. Distinguish what was proposed, attempted, observed and completed. Later evidence can supersede an earlier decision; memory cannot authorize acting on either.

A truncation marker means detail is missing. Narrow IDs, fields, time window or page size through supported parameters; do not report complete history from a truncated response. Installed retrieval can truncate at 64 KiB, and generated observations may already omit or compress original detail.

For ordinary keyword searches where refinement is authorized, an empty result may justify an alternate term while preserving the established project, host/source and time filters on every retry. No matches never authorize dropping filters or broadening scope. Correct a mistaken scope value only from evidence within the user's established scope; ask before expanding it. A user-requested earlier-session scope also excludes the current session where supported. If that exclusion or another required filter cannot be enforced, disclose the exact limit and do not claim an earlier-only or fully scoped result. If the backend fails, report retrieval failure. SQLite-only fallback may be available when semantic search is disabled or unavailable; report the route actually observed, without claiming equivalent semantic coverage.

## Return

Answer concisely with record ID, date and project where supplied. Label current-source verification and remaining uncertainty. Omit secret values even if the engine returned them. An authorized handoff can include a few record IDs and unresolved attempts; do not copy the entire history into another store.

