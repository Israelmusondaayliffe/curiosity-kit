# Complete synthetic worked deliverables

Every input, trace, output and result in this file is synthetic. These specimens demonstrate contracts and expected behavior. They are not model executions, measured provider scores or deployment evidence. Fixture references identify fictional test records, not external websites. Domain JSON below is not a lab.py plan or raw-results format. Use [evaluation contract](evaluation-contract.md) for helper artifacts and [provider guide](provider-guide.md) for native model configuration.

## 1. A complete plain chat prompt

Request: "Give me a prompt I can paste into my chosen chat model to turn rough project notes into a short update. Keep uncertain dates uncertain. I don't need API settings."

Deliverable:

```text
Turn the notes below into a project update for colleagues who know the project but have not followed this week's work.

Start with the current outcome or status. Then cover completed work, open blockers and the next action with its owner where stated. Use no more than 120 words. Preserve uncertainty: a proposed date is not a commitment, and planned work is not completed work. Do not invent owners, metrics, decisions or progress. If a required fact is absent, say it is not specified. Cut repetition before cutting a blocker or decision.

Return only the update. Do not send it anywhere.

Notes:
The import preview is implemented. Maya checked the three sample files; two passed. The third has duplicate column names and fails validation. We have not run the full test set. Luis will investigate the duplicate-column handling. Friday is a possible release date, pending that fix and the full test run.
```

Expected worked output:

```text
The import preview is implemented, but it is not ready for release. Maya checked three sample files: two passed, and one failed because it contains duplicate column names. The full test set has not run.

Luis will investigate duplicate-column handling. Friday is a possible release date, pending that fix and a successful full test run.
```

Why this is complete: it gives the actual pasteable task and input, preserves the missing verification and tentative date, and adds no API controls. No role paragraph, tool instructions, memory or multi-agent procedure is needed.

## 2. Extraction with success, missing data and an error

Request: "Extract four invoice fields. Missing values must be null. I need JSON only and a way to tell unreadable input from partial extraction."

Complete prompt:

```text
Extract invoice_number, invoice_date, vendor and total from the supplied invoice. Return only JSON matching the schema below. Use an ISO date only when the source states an unambiguous date. Currency amounts are numbers without symbols. Do not infer missing values, calculate an unstated total, or copy values from another invoice.

Every data key is present. Missing, ambiguous and illegible values are null and have an issue identifying the field. Use status "ok" only when all four values are supported and issues is empty. Use "partial" when the source is readable but at least one value is missing or uncertain. Use "error" when no usable source is available; then all four values are null and issues contains a $source entry. Return no extra fields, commentary or Markdown. Re-scan the source for missed fields and validate these status rules before returning.

Schema:
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["status", "data", "issues"],
  "properties": {
    "status": {"enum": ["ok", "partial", "error"]},
    "data": {
      "type": "object",
      "additionalProperties": false,
      "required": ["invoice_number", "invoice_date", "vendor", "total"],
      "properties": {
        "invoice_number": {"type": ["string", "null"]},
        "invoice_date": {"type": ["string", "null"], "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
        "vendor": {"type": ["string", "null"]},
        "total": {"type": ["number", "null"]}
      }
    },
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["field", "code", "detail"],
        "properties": {
          "field": {"enum": ["invoice_number", "invoice_date", "vendor", "total", "$source"]},
          "code": {"enum": ["missing", "ambiguous", "illegible", "unreadable_source"]},
          "detail": {"type": "string"}
        }
      }
    }
  }
}

The schema checks shape. Also check the status rules above, actual calendar validity and source support. A syntactically valid date is not necessarily a real date.

Invoice source:
[Insert the invoice text or supported attachment here.]
```

The placeholder is the intended input slot in a reusable prompt, not an unfinished instruction. Three complete synthetic calls follow.

Success input:

```text
Invoice INV-042
Vendor: North Pier Supplies
Invoice date: 2026-09-30
Total due: USD 128.50
```

Expected output:

```json
{"status":"ok","data":{"invoice_number":"INV-042","invoice_date":"2026-09-30","vendor":"North Pier Supplies","total":128.5},"issues":[]}
```

Missing/ambiguous input:

```text
Invoice INV-043
Vendor: North Pier Supplies
Invoice date: 03/04/2026
Total section is absent from the supplied page.
```

Expected output:

```json
{"status":"partial","data":{"invoice_number":"INV-043","invoice_date":null,"vendor":"North Pier Supplies","total":null},"issues":[{"field":"invoice_date","code":"ambiguous","detail":"03/04/2026 does not identify whether the month or day comes first."},{"field":"total","code":"missing","detail":"No invoice total appears in the supplied page."}]}
```

Error input: the caller supplies no readable text or accessible attachment.

Expected output:

```json
{"status":"error","data":{"invoice_number":null,"invoice_date":null,"vendor":null,"total":null},"issues":[{"field":"$source","code":"unreadable_source","detail":"No readable invoice source was supplied."}]}
```

Contract checks: each output has exactly the declared keys; null is allowed for all four fields; issues are legal rather than an invented extra key. The ambiguous date is not guessed. The source error does not pretend that only one field was missing. None of these outputs proves a real model followed the prompt.

## 3. Rank twenty tickets while accounting for all fifty

Request: "Collect the 50 open tickets in this fixed export and show the oldest 20 that can be checked. Do not change tickets. Account for missing records."

This is a full synthetic bounded-stage design. The real deployment must substitute its actual tool contracts and verify their support. These tool names are fixture interfaces, not claims of installed tools.

### Collection contract and complete task prompt

```text
Read the fixed export S1 using these fixture interfaces only:
- list_open({export_id:"S1", cursor:string|null}) returns either {status:"ok", ids:string[], next_cursor:string|null} or {status:"error", code:"transient"|"denied", detail:string}.
- ticket_details({ticket_id:string}) returns either {status:"ok", ticket_id:string, account_id:string|null, age_days:integer, summary:string, source:string} or {status:"error", code:"transient"|"denied"|"not_found", detail:string}.
- account_tier({account_id:string}) returns either {status:"ok", tier:"standard"|"premium"} or {status:"error", code:"transient"|"denied"|"not_found", detail:string}.

First finish pagination and establish the unique ID set. This export must contain 50 IDs. If pagination is incomplete or the set is not 50, stop with status "scope_incomplete", preserve discovered coverage and do not claim a complete ranking.

For each ID, get details, then use its account_id to obtain tier. Missing account_id blocks that ticket; do not guess one. Use at most 4 concurrent read calls. Retry only a transient error once, so each logical call has at most 2 attempts. Stop a denied call without retrying it. Reuse a completed account lookup for the same account. No write tool is allowed.

Return one domain JSON object with status, expected_count, discovered_ids, candidates and coverage. status is "complete" only when all 50 IDs are successful, "partial" when all 50 are accounted for but some failed or were blocked, and "scope_incomplete" if discovery failed.

candidates contains up to 20 successful rows sorted by age_days descending, then ticket_id ascending. Every row has ticket_id, customer_tier, age_days, summary and evidence_ref. coverage contains exactly one row per discovered ID, with ticket_id, status (ok, failed or blocked), evidence_ref and detail. An ok row has detail null. Evidence references identify the fixture record or failure log supporting that status. Keep the full raw tool/attempt log separately under the export's evidence location. Failed and blocked rows are never eligible for candidates.

Verify exact discovered-ID/coverage-ID set equality, unique IDs, candidate eligibility, ordering and all required fields. Return control after this single collection stage. Do not repeat completed calls, start a new export or make an escalation decision.

Final user delivery must retain all 20 selected ticket IDs, tiers, ages and evidence references, and report the complete coverage counts and named exceptions. Describe this as a ranking among checked tickets if any ticket was excluded. A top-20 list alone does not prove full coverage.
```

### Synthetic fixture definition

S1 has the exact IDs T01 through T50 listed in the output below. Its two pages contain T01–T25 and T26–T50. For T01–T48, ticket number N has age N days, summary "Unresolved ticket TN", account_id A1, tier standard and source fixture://S1/TN. A1 is looked up once. T49 returns a transient detail error on both allowed attempts; its evidence is fixture://S1/log/T49. T50 returns age 50 and a null account_id; its evidence is fixture://S1/T50. All fixture values are defined here; no real source was read.

### Complete expected intermediate artifact

```json
{
  "status": "partial",
  "expected_count": 50,
  "discovered_ids": ["T01","T02","T03","T04","T05","T06","T07","T08","T09","T10","T11","T12","T13","T14","T15","T16","T17","T18","T19","T20","T21","T22","T23","T24","T25","T26","T27","T28","T29","T30","T31","T32","T33","T34","T35","T36","T37","T38","T39","T40","T41","T42","T43","T44","T45","T46","T47","T48","T49","T50"],
  "candidates": [
    {"ticket_id":"T48","customer_tier":"standard","age_days":48,"summary":"Unresolved ticket T48","evidence_ref":"fixture://S1/T48"},
    {"ticket_id":"T47","customer_tier":"standard","age_days":47,"summary":"Unresolved ticket T47","evidence_ref":"fixture://S1/T47"},
    {"ticket_id":"T46","customer_tier":"standard","age_days":46,"summary":"Unresolved ticket T46","evidence_ref":"fixture://S1/T46"},
    {"ticket_id":"T45","customer_tier":"standard","age_days":45,"summary":"Unresolved ticket T45","evidence_ref":"fixture://S1/T45"},
    {"ticket_id":"T44","customer_tier":"standard","age_days":44,"summary":"Unresolved ticket T44","evidence_ref":"fixture://S1/T44"},
    {"ticket_id":"T43","customer_tier":"standard","age_days":43,"summary":"Unresolved ticket T43","evidence_ref":"fixture://S1/T43"},
    {"ticket_id":"T42","customer_tier":"standard","age_days":42,"summary":"Unresolved ticket T42","evidence_ref":"fixture://S1/T42"},
    {"ticket_id":"T41","customer_tier":"standard","age_days":41,"summary":"Unresolved ticket T41","evidence_ref":"fixture://S1/T41"},
    {"ticket_id":"T40","customer_tier":"standard","age_days":40,"summary":"Unresolved ticket T40","evidence_ref":"fixture://S1/T40"},
    {"ticket_id":"T39","customer_tier":"standard","age_days":39,"summary":"Unresolved ticket T39","evidence_ref":"fixture://S1/T39"},
    {"ticket_id":"T38","customer_tier":"standard","age_days":38,"summary":"Unresolved ticket T38","evidence_ref":"fixture://S1/T38"},
    {"ticket_id":"T37","customer_tier":"standard","age_days":37,"summary":"Unresolved ticket T37","evidence_ref":"fixture://S1/T37"},
    {"ticket_id":"T36","customer_tier":"standard","age_days":36,"summary":"Unresolved ticket T36","evidence_ref":"fixture://S1/T36"},
    {"ticket_id":"T35","customer_tier":"standard","age_days":35,"summary":"Unresolved ticket T35","evidence_ref":"fixture://S1/T35"},
    {"ticket_id":"T34","customer_tier":"standard","age_days":34,"summary":"Unresolved ticket T34","evidence_ref":"fixture://S1/T34"},
    {"ticket_id":"T33","customer_tier":"standard","age_days":33,"summary":"Unresolved ticket T33","evidence_ref":"fixture://S1/T33"},
    {"ticket_id":"T32","customer_tier":"standard","age_days":32,"summary":"Unresolved ticket T32","evidence_ref":"fixture://S1/T32"},
    {"ticket_id":"T31","customer_tier":"standard","age_days":31,"summary":"Unresolved ticket T31","evidence_ref":"fixture://S1/T31"},
    {"ticket_id":"T30","customer_tier":"standard","age_days":30,"summary":"Unresolved ticket T30","evidence_ref":"fixture://S1/T30"},
    {"ticket_id":"T29","customer_tier":"standard","age_days":29,"summary":"Unresolved ticket T29","evidence_ref":"fixture://S1/T29"}
  ],
  "coverage": [
    {"ticket_id":"T01","status":"ok","evidence_ref":"fixture://S1/T01","detail":null},
    {"ticket_id":"T02","status":"ok","evidence_ref":"fixture://S1/T02","detail":null},
    {"ticket_id":"T03","status":"ok","evidence_ref":"fixture://S1/T03","detail":null},
    {"ticket_id":"T04","status":"ok","evidence_ref":"fixture://S1/T04","detail":null},
    {"ticket_id":"T05","status":"ok","evidence_ref":"fixture://S1/T05","detail":null},
    {"ticket_id":"T06","status":"ok","evidence_ref":"fixture://S1/T06","detail":null},
    {"ticket_id":"T07","status":"ok","evidence_ref":"fixture://S1/T07","detail":null},
    {"ticket_id":"T08","status":"ok","evidence_ref":"fixture://S1/T08","detail":null},
    {"ticket_id":"T09","status":"ok","evidence_ref":"fixture://S1/T09","detail":null},
    {"ticket_id":"T10","status":"ok","evidence_ref":"fixture://S1/T10","detail":null},
    {"ticket_id":"T11","status":"ok","evidence_ref":"fixture://S1/T11","detail":null},
    {"ticket_id":"T12","status":"ok","evidence_ref":"fixture://S1/T12","detail":null},
    {"ticket_id":"T13","status":"ok","evidence_ref":"fixture://S1/T13","detail":null},
    {"ticket_id":"T14","status":"ok","evidence_ref":"fixture://S1/T14","detail":null},
    {"ticket_id":"T15","status":"ok","evidence_ref":"fixture://S1/T15","detail":null},
    {"ticket_id":"T16","status":"ok","evidence_ref":"fixture://S1/T16","detail":null},
    {"ticket_id":"T17","status":"ok","evidence_ref":"fixture://S1/T17","detail":null},
    {"ticket_id":"T18","status":"ok","evidence_ref":"fixture://S1/T18","detail":null},
    {"ticket_id":"T19","status":"ok","evidence_ref":"fixture://S1/T19","detail":null},
    {"ticket_id":"T20","status":"ok","evidence_ref":"fixture://S1/T20","detail":null},
    {"ticket_id":"T21","status":"ok","evidence_ref":"fixture://S1/T21","detail":null},
    {"ticket_id":"T22","status":"ok","evidence_ref":"fixture://S1/T22","detail":null},
    {"ticket_id":"T23","status":"ok","evidence_ref":"fixture://S1/T23","detail":null},
    {"ticket_id":"T24","status":"ok","evidence_ref":"fixture://S1/T24","detail":null},
    {"ticket_id":"T25","status":"ok","evidence_ref":"fixture://S1/T25","detail":null},
    {"ticket_id":"T26","status":"ok","evidence_ref":"fixture://S1/T26","detail":null},
    {"ticket_id":"T27","status":"ok","evidence_ref":"fixture://S1/T27","detail":null},
    {"ticket_id":"T28","status":"ok","evidence_ref":"fixture://S1/T28","detail":null},
    {"ticket_id":"T29","status":"ok","evidence_ref":"fixture://S1/T29","detail":null},
    {"ticket_id":"T30","status":"ok","evidence_ref":"fixture://S1/T30","detail":null},
    {"ticket_id":"T31","status":"ok","evidence_ref":"fixture://S1/T31","detail":null},
    {"ticket_id":"T32","status":"ok","evidence_ref":"fixture://S1/T32","detail":null},
    {"ticket_id":"T33","status":"ok","evidence_ref":"fixture://S1/T33","detail":null},
    {"ticket_id":"T34","status":"ok","evidence_ref":"fixture://S1/T34","detail":null},
    {"ticket_id":"T35","status":"ok","evidence_ref":"fixture://S1/T35","detail":null},
    {"ticket_id":"T36","status":"ok","evidence_ref":"fixture://S1/T36","detail":null},
    {"ticket_id":"T37","status":"ok","evidence_ref":"fixture://S1/T37","detail":null},
    {"ticket_id":"T38","status":"ok","evidence_ref":"fixture://S1/T38","detail":null},
    {"ticket_id":"T39","status":"ok","evidence_ref":"fixture://S1/T39","detail":null},
    {"ticket_id":"T40","status":"ok","evidence_ref":"fixture://S1/T40","detail":null},
    {"ticket_id":"T41","status":"ok","evidence_ref":"fixture://S1/T41","detail":null},
    {"ticket_id":"T42","status":"ok","evidence_ref":"fixture://S1/T42","detail":null},
    {"ticket_id":"T43","status":"ok","evidence_ref":"fixture://S1/T43","detail":null},
    {"ticket_id":"T44","status":"ok","evidence_ref":"fixture://S1/T44","detail":null},
    {"ticket_id":"T45","status":"ok","evidence_ref":"fixture://S1/T45","detail":null},
    {"ticket_id":"T46","status":"ok","evidence_ref":"fixture://S1/T46","detail":null},
    {"ticket_id":"T47","status":"ok","evidence_ref":"fixture://S1/T47","detail":null},
    {"ticket_id":"T48","status":"ok","evidence_ref":"fixture://S1/T48","detail":null},
    {"ticket_id":"T49","status":"failed","evidence_ref":"fixture://S1/log/T49","detail":"Both permitted detail attempts returned a transient error."},
    {"ticket_id":"T50","status":"blocked","evidence_ref":"fixture://S1/T50","detail":"No account_id was supplied; tier cannot be checked."}
  ]
}
```

Complete expected user result:

```text
These are the oldest 20 among the 48 tickets whose details and tier could be checked. All have standard tier and remain unresolved.

T48: 48 days. Evidence: fixture://S1/T48
T47: 47 days. Evidence: fixture://S1/T47
T46: 46 days. Evidence: fixture://S1/T46
T45: 45 days. Evidence: fixture://S1/T45
T44: 44 days. Evidence: fixture://S1/T44
T43: 43 days. Evidence: fixture://S1/T43
T42: 42 days. Evidence: fixture://S1/T42
T41: 41 days. Evidence: fixture://S1/T41
T40: 40 days. Evidence: fixture://S1/T40
T39: 39 days. Evidence: fixture://S1/T39
T38: 38 days. Evidence: fixture://S1/T38
T37: 37 days. Evidence: fixture://S1/T37
T36: 36 days. Evidence: fixture://S1/T36
T35: 35 days. Evidence: fixture://S1/T35
T34: 34 days. Evidence: fixture://S1/T34
T33: 33 days. Evidence: fixture://S1/T33
T32: 32 days. Evidence: fixture://S1/T32
T31: 31 days. Evidence: fixture://S1/T31
T30: 30 days. Evidence: fixture://S1/T30
T29: 29 days. Evidence: fixture://S1/T29

Coverage: all 50 exported IDs are accounted for. 48 succeeded, T49 failed after its two allowed detail attempts, and T50 is blocked by a missing account ID. T50 is 50 days old, so resolving its tier could change this list. T49's age is unknown. Failure evidence: fixture://S1/log/T49 and fixture://S1/T50. No tickets were changed.
```

Expected checks: 50 distinct discovered and coverage IDs; 48 ok, one failed, one blocked; exactly 20 candidates; ages 48 down to 29; no failed candidate; source reference on every record; final summary admits the incomplete ranking. The raw fixture attempt count would be 2 list calls, 51 detail attempts and 1 account lookup, totaling 54. This arithmetic follows the defined fixture; it is not an observed execution count. The stated concurrency limit does not prove a runtime respected it.

## 4. Diagnose invisible progress without rewriting the prompt

Request: "My model runs tools but the client shows no progress until the end. Fix the prompt if that is the cause."

Synthetic inputs:

- Prompt P1 already says: "Send a short visible update when a material result is ready. Keep working until the artifact is checked."
- Permitted trace fixture E1 contains event 1, commentary text "The first source is checked; two remain"; event 2, a read-tool invocation; event 3, its result; event 4, final text "All three sources are checked."
- Renderer fixture R1 displays only blocks tagged final. It discards commentary blocks. No model timing or provider performance is represented by the fixture.

Complete diagnosis deliverable:

```text
The supplied fixture points to the renderer, not a missing progress instruction. P1 already requests milestone updates, and E1 contains one. R1 discards that block because its type is commentary.

Recommended change: have the client render supported commentary events as interim user messages while preserving final events as completion. Keep P1 unchanged. This is a proposed client change; it has not been applied.

Discriminating test: replay E1 through the current and proposed renderers without another model request. The current fixture should show only the final message. The changed renderer should show the commentary message and final message in order, without exposing hidden reasoning or raw tool payloads. Then check a live authorized trace, including a turn with no commentary, before concluding the symptom is fully fixed.

Confidence: high for the supplied fixture's display defect; live frequency and provider emission behavior remain unknown. If a real trace contains no commentary, investigate that separate case rather than assuming R1 explains it.

Rollback: restore the previous renderer and its tests if the change misclassifies blocks or exposes private content. A prompt-only rollout is not justified by this evidence.
```

This preserves audit/diagnosis scope. No client file is actually edited, and a synthetic replay is not reported as a live model test.

## 5. A bounded migration with stable authority

Request: "Prepare this task prompt for my selected target model. Preserve its approval rule. Do not run either model yet."

Complete source prompt P0:

```text
You inspect support tickets and draft a reply. Think very carefully. Be exhaustive. Think very carefully. Summarize the issue, quote the supporting ticket ID, and write one reply draft under 100 words. Never send a reply or change a ticket without the user's approval of that exact action. If policy context is missing, say so and do not invent it.
```

Complete target prompt P1:

```text
Inspect the supplied support ticket and policy context. Summarize the issue with its ticket ID, then write one reply draft under 100 words. Preserve supported facts and state any missing policy context rather than inventing it. Never send a reply or change a ticket without the user's approval of that exact action.
```

Migration note:

```text
P1 preserves the job, ticket reference, 100-word reply limit, missing-policy behavior and exact-action approval rule. It removes the repeated "Think very carefully" instruction and the vague "Be exhaustive" direction, which conflicts with the bounded draft.

Keep P0 as the rollback artifact. Resolve the user's exact target and host before adding native configuration. First compare P0 on the source model with P0 on the target after only required compatibility changes. Then compare P0 and P1 on the target under matched settings. Treat effort changes as a separate axis.

Prepared cases: an ordinary ticket with policy; a missing-policy ticket; a request to send without approval; and a long ticket where the reply must stay under 100 words. Acceptance requires correct summary/ID, policy grounding, draft length and no unauthorized action on every case. Retain any failed output and restore the removed group only if it explains a regression.

No model ran. P1 is a prepared candidate, not a measured improvement. Rollback restores P0 and the recorded original configuration; it does not erase the comparison evidence.
```

## 6. Long-run design on a degraded host

Request: "Design an unattended run that checks three supplied CSV exports and writes a discrepancy report. This host has file read/write and synchronous commands, but no subagents, no direct-message tool and no persistent learning service."

Synthetic host contract: read_file and write_file access only `/task`; run_check runs a bounded local check synchronously and returns exit status and output. The host enforces a ten-minute whole-run deadline and includes remaining_seconds in each tool result, with enough reserved time to save a checkpoint. No background job or provider inference tool exists. These names describe the specimen host only. Three isolated inputs are a.csv, b.csv and c.csv. The user permits read-only input checks and writes to `/task/results`. Its acceptance condition is full row accounting, reported duplicate IDs and reconciled totals for each file; independent model review is optional. Without the host deadline mechanism, a hard runtime guarantee would remain unqualified.

Complete task prompt:

```text
Check /task/a.csv, /task/b.csv and /task/c.csv. Do not change the inputs. Write /task/results/report.md and /task/results/checkpoint.json. For each file, account for all rows, list duplicate IDs and compare the sum of row amounts with its stated total. Preserve missing or nonnumeric values as issues rather than treating them as zero.

Use only the host's read_file, write_file and synchronous run_check operations within /task. Stop after ten minutes or on a required permission/input blocker, keeping completed evidence. No background worker, reviewer, messaging or learning service is available.

Track each file as not started, active, blocked, failed or verified. A file is verified only after the coverage and arithmetic checks return usable results. Save the observed exit status and output next to the report. After each file, update the checkpoint with input identity, row counts, issues, result location and the next file. Do not call the complete report verified while a file remains unaccounted for.

Use deterministic row-count, duplicate-ID and arithmetic checks at each file boundary. Review the report against those outputs at the end. This is deterministic checking plus same-context review, not an independent model review.

If interrupted, read the checkpoint and verify input identities before resuming. A changed input invalidates its earlier result. All commands are synchronous; there are no ongoing jobs to poll. Do not create asynchronous work or promise a later notification. Save partial report content after each milestone and deliver it at the next supported final response.

Keep only this task checkpoint. Do not create a persistent learning store. End with a standalone account of which files were checked, discrepancies, evidence locations and any blocked criterion.
```

Complete expected checkpoint for an interruption after the second file:

```json
{
  "contract_version": "csv-check-v1",
  "evidence_class": "synthetic_specimen",
  "inputs": [
    {"path":"/task/a.csv","identity":"fixture-a-v1","status":"verified","rows":10,"duplicate_ids":[],"total_matches":true,"evidence":"/task/results/a-check.txt"},
    {"path":"/task/b.csv","identity":"fixture-b-v1","status":"verified","rows":8,"duplicate_ids":["B04"],"total_matches":false,"evidence":"/task/results/b-check.txt"},
    {"path":"/task/c.csv","identity":"fixture-c-v1","status":"not_started","rows":null,"duplicate_ids":null,"total_matches":null,"evidence":null}
  ],
  "active_jobs": [],
  "next_action": "Verify input identities, then check /task/c.csv.",
  "independent_review": "unavailable_optional",
  "mid_run_delivery": "unavailable",
  "persistent_learning": "not_configured"
}
```

The readable fixture identities above are not cryptographic hashes. A real run records actual supported file identities. "Verified" means the check completed against the acceptance definition; it does not mean the input has no discrepancies.

Complete expected report after the remaining fixture file is checked:

```text
All three synthetic exports were checked, covering 30 rows. Export b has a duplicate ID and a total mismatch.

a.csv: 10 rows; no duplicate IDs; row amounts total 100.00 and match the stated 100.00. Evidence: /task/results/a-check.txt.
b.csv: 8 rows; ID B04 appears twice; row amounts total 95.00, while the stated total is 90.00, a difference of 5.00. Evidence: /task/results/b-check.txt.
c.csv: 12 rows; no duplicate IDs; row amounts total 120.00 and match the stated 120.00. Evidence: /task/results/c-check.txt.

The discrepancy report is complete for the supplied fixture. Inputs were unchanged. Deterministic checks and same-context review were specified; no independent reviewer or mid-run delivery was available. No persistent learning record was created.
```

Qualification decision: the design is feasible with reduced review and delivery capability, provided the named host tools actually exist and the run is authorized. The document above does not claim that those tools or files exist here or that the checks ran. If independent review had been a hard condition, that condition would remain blocked.

## 7. Named-pair transition with incompatible opaque state

Request: "Design a Fable-primary, Opus-secondary fallback for a read-only document answer. Keep this pair. Use the secondary on one transport failure, never on a refusal. Do not deploy it."

Identity decision: retain the requested Fable/Opus names, but leave exact model IDs and interface unresolved until the user's host is known. No historical version or current account availability is assumed. The following state incompatibility is a fixture condition, not a claim about current provider support.

Complete shared prompt:

```text
Answer the user's document question from the supplied visible excerpts only. Return JSON with answer, evidence and unknowns. answer is a string; evidence is an array of objects with document_id, section and supporting_text; unknowns is an array of strings. Include every condition necessary to make the answer accurate. Do not infer facts from missing pages or claim to have read an inaccessible document. Do not change documents or contact anyone.

If a prior attempt is present, use only its visible supported observations. Preserve the current question and source references. Do not request or reconstruct private reasoning. If a required source is unavailable, state the gap in unknowns instead of inventing an answer.
```

Complete synthetic transition input:

```json
{
  "question": "When can the trial be extended?",
  "visible_sources": [{"document_id":"D1","section":"4.2","text":"The trial may be extended by 14 days if the request arrives before the original end date and both parties approve it in writing."}],
  "primary_visible_result": null,
  "completed_side_effects": [],
  "pending_jobs": [],
  "opaque_state_transfer": "unsupported_in_fixture",
  "primary_failure": "transport_error"
}
```

Routing contract: a client owns exactly one primary attempt and at most one secondary attempt for the transport-error category. No primary retry, recursion or return to primary is in scope. A permission denial, refusal, cancellation, schema error or unavailable required source does not trigger fallback. The example ceiling is 60 seconds total and an approved hypothetical USD 0.02; actual authority and observed usage must be established before execution.

Direction handling: primary-to-secondary opaque replay is unsupported in this fixture. Use a permitted fresh context containing the shared prompt, exact question and D1 excerpt above. Do not send opaque blocks disguised as text. Secondary-to-primary is not supported by this design and is never automatically attempted. Visible input and output requirements are identical. Both legs have no write tools and no broader data destination approval is inferred from the prompt.

Complete expected secondary output:

```json
{"answer":"The trial may be extended by 14 days if the request arrives before the original end date and both parties approve it in writing.","evidence":[{"document_id":"D1","section":"4.2","supporting_text":"The trial may be extended by 14 days if the request arrives before the original end date and both parties approve it in writing."}],"unknowns":[]}
```

Complete synthetic accounting record, conceptual rather than a helper input:

```json
{
  "evidence_class": "synthetic",
  "primary": {"requested_model":"Fable","attempts":1,"status":"transport_error","duration_seconds":2,"cost_usd":0.002},
  "secondary": {"requested_model":"Opus","attempts":1,"status":"success","duration_seconds":3,"cost_usd":0.004},
  "transition_seconds":1,
  "total_observed_region_seconds":6,
  "total_cost_usd":0.006,
  "timing_boundary":"Primary start through secondary output; includes the synthetic transition delay.",
  "billing_basis":"Invented fixture amounts only; not provider prices or charges."
}
```

Transition tests and expected decisions:

- Complete excerpt survives fresh-context transfer: answer includes 14 days, the pre-end-date request and both parties' written approval.
- Broken converter drops "before the original end date": reject the composite candidate even if both standalone prompts pass when given the full excerpt.
- Primary returns a correct refusal: stop after one attempt; no secondary call.
- Primary has a pending tool/action with unknown outcome: reconcile it through the real owner before any transition; do not duplicate it.
- Secondary fails or total deadline/budget is exhausted: return the actual failure and preserved evidence; do not loop back.
- Opaque state is unsupported and no exact visible source can be transferred: report blocked transition, not guessed continuity.

Complete design conclusion:

```text
The requested Fable/Opus pair has a bounded client-side design: one primary attempt and one secondary attempt only after a transport failure. The transition uses the visible question and source excerpt in a fresh context; opaque-state replay is excluded in the supplied fixture.

The intact synthetic example preserves every answer condition and accounts for both attempts. The broken-converter case shows why standalone model checks are insufficient. These are expected fixture outcomes, not observed provider results.

Execution remains blocked until exact model IDs, host support, source transmission authority and spending bounds are confirmed. No configuration was applied. Rollback is to disable the proposed secondary route and retain the primary's original failure reporting.
```

## 8. Explicit Fable SOLVE without a model-tier gate

Request: "Use Fable SOLVE to decide how to collect feedback for a 12-person internal workshop. We need input from everyone by Thursday; it is Tuesday. No new tools or public sharing."

Complete worked result based only on those synthetic facts:

```text
Use a short written questionnaire in an already approved internal channel, with the same questions for all 12 participants. Ask for a reply by Thursday and track whether each person has responded. This is a proposed collection plan, not a sent message.

The hard constraints are input from all 12 people, the Thursday deadline, existing tools and no public sharing. The main uncertainty is whether every participant can access and use the chosen internal channel. Verify that before sending.

Two workable approaches differ in how they collect input. A shared questionnaire allows asynchronous responses and makes coverage easy to check. Individual conversations allow richer follow-up but require scheduling 12 people within two days. The deadline and complete-coverage requirement favor the questionnaire. If anyone cannot use it, obtain their answers through another already approved internal channel and record them with the same questions.

Ask what was useful, what was unclear and what one change would improve the next workshop. Acceptance requires a response or an explicitly documented blocker for each of the 12 people, plus a summary that distinguishes common themes from isolated comments. Do not claim "everyone said" when only a subset responded.

Confidence is conditional on channel access. If several participants are unavailable until after Thursday, the complete-coverage deadline cannot be met as stated and needs a decision. No outreach or persistent learning capture has occurred.
```

Review: the result respects the deadline and tool constraints, compares genuinely different mechanisms, and identifies the access prerequisite. It does not invent participant names or send a message. Complete feedback from everyone remains an outcome of the later authorized collection, not something this plan has accomplished. No numerical quality score or persistent note is required to finish this planning request.
