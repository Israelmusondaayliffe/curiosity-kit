# Watches, explicit runs, deltas and briefs

Use this route for saved topics, “check it once,” “what changed?” and daily/weekly digests. Read [local-store](../references/local-store.md) for exact commands and [evidence-contract](../references/evidence-contract.md) for interpretation. A saved topic, a completed research run, a registered schedule and a delivered message are four separate outcomes. Never imply one proves another.

## Save and manage a topic

Resolve the topic/entity, substantive constraints, queries, requested source lanes, absolute window/timezone and selection method/cap. Preserve all supplied queries, not only the first. Prepare the scope file using the canonical schema. Use the selected store, without ambient global configuration:

- `watch list --root STORE` reads configuration and its current global revision. Distinguish absent configuration from corruption. Inspect archived entries when resolving a removed topic.
- `watch add NAME --scope FILE --root STORE` creates the named topic; include `--schedule TEXT` only when the user requested a schedule description. Stored schedule text is an unactivated request.
- `watch update NAME --scope FILE --expected-revision N --root STORE` changes the selected scope. `watch pause NAME`, `watch archive NAME` and `watch restore NAME` require the same explicit revision flag. Use the freshly read revision and verify returned/read-back state; do not reuse a revision across later mutations.
- “Remove this watch” archives/deactivates the topic while retaining immutable research history. Restoring an archived item is an explicit operation. Do not delete shared findings or rewrite other topics.

If revision changed concurrently, reread state and reconcile the user's intended edit with the actual changes. Do not blindly increment, force overwrite or silently restore a paused topic. Report the requested state only after inspecting the committed configuration.

## Execute a requested one-shot check

1. Read the named watch and determine whether this is an explicit one-shot request or a previously authorized scheduled execution. Paused/archived entries do not run automatically. An explicit “check this paused topic once” can run once without changing its paused state.
2. The saved scope contains an absolute interval, not a rolling-window policy. For an explicitly requested rolling check (for example, “last 30 days today”), resolve a new absolute interval from that request and preserve the query/source/selection constraints; record its changed-scope relationship when binding. Otherwise use the saved absolute interval. Do not widen the default 30-day window to 90 days. Apply [research](research.md) with real native/manual source access and record each lane's actual outcome, including failures and clean zero results.
3. Save a new immutable run using `validate` and `ingest`, read it back, then bind it with `watch record NAME RUN_ID --expected-revision N --root STORE`. When scope changed, use the helper's explicit `--relationship TEXT` only to record a truthful relationship and reason; this does not make incomparable samples comparable.
4. Report the findings and coverage. Saving/binding an already supplied record is not proof that fresh network collection occurred. An attempted but failed lane remains failed. Do not fabricate completion because a JSON file exists.

A request to run several topics uses each topic's full scope and records outcomes separately. Share significant independent results without waiting for a blocked topic. No cost meter means cost is unknown, not zero. A saved budget is not a spending reservation or enforcement mechanism; paid work requires actual permitted limits and an available enforcing route.

## Compare exact observations

Select explicit BEFORE and AFTER run IDs. Do not choose “latest” by file modification time or silently compare against a different topic. Use `delta BEFORE AFTER --root STORE`, then inspect the records and material source passages before drawing conclusions.

Check entity identity, actual queries, source lanes and outcomes, selection/cap, date boundaries/timezone and whether the request deliberately moved the absolute interval. For rolling windows distinguish the shared observation interval from dates that have aged out. A changed query, lower cap or inaccessible lane can explain apparent absence. The output categories mean:

- Added: newly observed in the selected comparable evidence, not necessarily newly created in the world.
- Continuing: the same item appears again; this alone does not establish unchanged content.
- Changed: recorded body/datum differences require review to say what fact changed. Falling engagement is a real observation, not a reason to retain a previous maximum.
- Not observed: absent from this sampled retrieval, not deleted, closed or disproved.
- Aged out: outside the newer window by a supported date, not vanished.
- Unverifiable: scope/access/read/date/identity mismatches prevent the comparison. Explain the relevant mismatch, including partial lanes.

With fewer than two usable records say insufficient history and provide the available baseline. Item-count changes across noncomparable samples are not momentum, popularity or source-quality estimates. Distinguish same-event syndication from independent new evidence. Link each material change to both observed versions and their check dates.

## Build a useful daily or weekly brief

1. Resolve the requested period in the user's timezone and select explicit saved runs. Decide whether the user asked to collect first or only summarize existing research. Reading yesterday's saved brief must not run today's collection.
2. Inspect per-topic newest usable collection time, original source window, failed lanes, never-run/paused topics and historical imports. “Never checked” cannot appear as fresh. Freshness depends on the question and actual dates; do not silently impose a universal 36-hour truth threshold.
3. Use `brief RUN_IDS... --format md --out NEW_FILE --root STORE` to save a readable digest without clobbering, then read and semantically review that file. Stdout remains structured JSON; without `--out`, `--format md` does not produce Markdown. Deduplicate the same event/origin across runs without losing corroborating or conflicting source links. Per-topic membership must survive shared URLs.
4. Lead with the important changes and why they matter for this topic. Include exact evidence dates/links, the comparison basis, unresolved contradictions and coverage that could change the answer. A small digest can omit low-value repeated detail; it must retain consequential caveats.
5. For a weekly comparison, name both periods and count only comparable sampled observations. If the prior count is zero, say “from 0 to N observed items,” not an invented percentage increase. Do not sum Reddit votes, video views and repository stars as a common interest index.
6. Return the reviewed narrative and selected run identities. If saving a brief, use a new unique artifact and verify its bytes; do not overwrite another brief with the same date. Local assembly does not refresh sources or send anything externally.

## Schedule and delivery boundaries

Only a requested recurring/future action uses the host's actual supported scheduling tool under [host-contract](../references/host-contract.md). Verify its registered task identity, timezone, recurrence, source access, scope and authorized destination before saying it will run. If unavailable, leave the topic saved and state scheduling is unconfigured. No hidden daemon, cron installer, startup hook or provider webhook is supplied here.

External delivery needs the applicable recipient/content authorization and verified destination. A “silent” local watch performs no hidden HTTP request. Stored delivery text or an arbitrary webhook URL is not permission. For a requested send that partly succeeds, retain confirmed successes and unresolved failures; do not resend the batch to manufacture an all-success outcome.
