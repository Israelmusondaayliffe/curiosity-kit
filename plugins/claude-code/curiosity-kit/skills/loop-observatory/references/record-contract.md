# Evidence and record contract

There are three distinct versions: manifest/supplied input schema `"1.0"`, normalized result schema `"2.0"`, and a parser version identifying the actual reader/metric implementation. Producer schema versions are separate. Never infer that a `v2` reader-profile name changes a producer's own schema.

## Manifest

A JSON object:

```json
{
  "schema_version": "1.0",
  "sources": [
    {
      "id": "checkout-export",
      "path": "input/checkout.json",
      "profile": "supplied-v1",
      "namespace": "checkout",
      "coherence": "frozen-export"
    }
  ]
}
```

`sources` is a nonempty list. Each ID is unique, nonempty text. Paths may be absolute or relative to the manifest's directory. Profile is one of the five documented in [source profiles](source-profiles.md); namespace is nonempty. Coherence is `best-effort` by default or `frozen-export` when the source owner supplies that assertion. This is a claim about capture, not about outcome correctness.

An optional `limits` object may reduce these defaults, never increase them:

| Limit | Default | Meaning |
| --- | ---: | --- |
| max_files | 1000 | source file bound; also bounds source count |
| max_file_bytes | 8388608 | 8 MiB per file |
| max_total_bytes | 67108864 | 64 MiB across the selected manifest (also enforced per capture) |
| max_depth | 24 | directory traversal depth |
| max_json_depth | 64 | JSON nesting depth |
| max_records | 10000 | supplied records per export and normalized records across the manifest |

Directory traversal also bounds visited entries to four times max_files. Every path component must be free of symlinks. All captured content must be regular files. Output and sources must be disjoint in both directions: no output inside a source and no source inside the chosen output root. Duplicate JSON keys and nonfinite numeric constants are rejected.

A supplied export with `records: []` can establish a valid empty cohort. A missing root cannot. Registration writes only the explicit local manifest; it does not scan producer homes or schedule a future run.

## Supplied records

A supplied-v1 source is one JSON file:

```json
{"schema_version": "1.0", "records": []}
```

Every record requires:

| Field | Type | Meaning |
| --- | --- | --- |
| producer | nonempty string | actual producer namespace, not the parser profile |
| run_id | nonempty string | native logical run ID |
| revision | nonnegative integer | source-authoritative evidence revision for this logical run |
| status | nonempty string | native state retained verbatim |
| terminal | boolean | explicitly mapped producer terminality |

The manifest supplies `namespace`. Logical identity is `(producer, namespace, run_id)`. Equal run IDs in different projects remain distinct. `revision` is neither a trial number nor a charge. A later label/cost correction changes evidence about the same run. A copied source location is not a new identity. Do not invent a revision order to make conflicts disappear.

Optional analytical fields retain their source meanings:

- `event_time`: timestamp for the run event being reported;
- `known_time`: time this evidence became available under the source's declared knowledge basis;
- `cohort`: explicit text used by the cohort filter;
- `goal`, `model`, `version`: evidenced descriptive dimensions;
- `iteration`: nonnegative integer count under the producer's iteration definition;
- `duration_seconds`: finite nonnegative explicit measured seconds, converted to a cumulative duration observation when no duration measurement is supplied;
- `conditions`: supplied comparison-condition metadata, retained as part of descriptive strata;
- `execution_owner`: optional owner label for unresolved handoffs;
- `supersedes`: optional exact derived record IDs replaced by a bound correction of the same logical run;
- `process_completion`, `machine_completion`: distinct boolean/null observations where supplied;
- `judge_verdict`, `human_label`: raw source labels, not implicit typed acceptance;
- `stop_reason`, `escalation_reason`: raw reasons retained independently of any exact mapped exhaustion classification;
- `task`, `artifact`, `criterion`, `rubric`: exact judgment target identifiers;
- `judgments`: bound observations described below;
- `measurements`: typed observations described below;
- `measurement_coverage`: explicit complete-scope assertions described below.

Unknown optional information remains missing/null with an explanatory warning where relevant. It is not false or zero. A valid status string and `terminal: true` do not manufacture completion, acceptance or cost evidence.

Times are RFC3339/ISO-style strings with explicit timezone; the helper normalizes them to UTC. Naive local timestamps are rejected. Native epoch conversion occurs only in the documented producer profile. Do not use filesystem modification time or ingestion time as an unannounced event-time fallback. A known-time assertion from an export is not independently verified proof of when a human actually saw the information.

## Judgment observations

A judgment object has the following shape:

```json
{
  "id": "review-a",
  "kind": "human",
  "label": true,
  "task": "checkout-error-state",
  "artifact": "sha256:artifact-a",
  "criterion": "required-state",
  "rubric": "ui-review@3",
  "purpose": "output-acceptance",
  "reviewer": "reviewer-1",
  "event_time": "2026-10-09T10:00:00Z",
  "known_time": "2026-10-09T10:00:00Z"
}
```

- `id` identifies the observation; `kind` is `machine` or `human`.
- `label` is strictly boolean or null. Strings such as `"pass"`, `"approved"` or `"false"` need an explicit mapping before this interface; broad truthiness is forbidden.
- `task`, `artifact`, `criterion`, `rubric` bind the exact question. Include versions in those immutable identities. All four must match for an eligible pair; record-level targets can identify what is current but cannot excuse mismatched observation targets.
- `purpose: "output-acceptance"` distinguishes output judgment from approval to run, upload or spend. Human reference evidence with another purpose cannot establish output acceptance.
- `reviewer` is a required nonempty observer identity. Missing reviewer identity excludes the observation from eligible acceptance/pairing.
- Event and known times support temporal eligibility. Missing temporal evidence must remain visible for historical queries.

Use one eligible machine/reference observation per exact target/rubric stratum under the declared selection policy. Optional `supersedes` lists exact observation IDs of the same kind and binding being replaced. Explicit reviewer flags can select a declared reference/judge. The helper conservatively excludes unresolved multiplicity; it does not invent adjudication, majority voting or observation ordering. Null labels remain unpaired. The raw observations remain available for a human/owner to resolve.

Human acceptance and calibrated pairing are separate eligibility questions: an output label may be visible without an eligible machine counterpart. A stale artifact or wrong-purpose human label must not become current acceptance merely because the run ID matches. See [audit](../playbooks/audit.md) for exclusions and diagnosis.

## Measurement observations

A measurement object identifies exactly what was measured:

```json
{
  "id": "charge-a1",
  "metric": "cost",
  "value": 2,
  "unit": "USD",
  "basis": "measured",
  "scope": "run",
  "aggregation": "incremental",
  "attempt_id": "attempt-1",
  "operation_id": "call-1",
  "revision": 1,
  "covers": []
}
```

- Metric is `cost`, `tokens` or `duration`.
- Value is a finite nonnegative JSON number. Numeric strings and booleans are invalid; counts/revisions require integers where specified. A measured zero is valid evidence, unlike an absent observation.
- Unit names currency for costs, `tokens` for token counts and `seconds` for duration. Keep currencies separate; no implicit conversion.
- Basis is `measured`, `estimated` or `reserved`. Estimates and budgets are not measured charges.
- Scope identifies the compatible run/measurement scope. `attempt_id` and `operation_id` identify distinct charges/operations beneath it.
- Aggregation is `incremental` or `cumulative`. Incremental observations accumulate only when their identities show distinct charges. Revised cumulative observations replace the prior observation for that scope, rather than adding another charge.
- Measurement `revision` orders that measurement's evidence; it is separate from the run revision.
- `covers` explicitly identifies measurements included in an authoritative aggregate. Covered components must not also be added to the total.

Do not combine parent totals with covered children, or inclusive tokens with cached/reasoning subsets. The helper can only deduplicate/replace relationships declared by the supported identity and coverage contract. If the underlying billing/usage scope is unknown, preserve raw observations and withhold the total rather than inventing a covers relationship.

Incremental charges alone establish known spend, not complete run cost. Declare complete incremental coverage only when the source evidence actually covers every relevant charged operation:

```json
{
  "measurement_coverage": [{
    "metric": "cost",
    "unit": "USD",
    "basis": "measured",
    "complete": true,
    "observation_ids": ["charge-a1", "charge-a2"]
  }]
}
```

The assertion must bind the exact effective and covered observation IDs for that series. A cumulative observation with `scope: "run"` explicitly claims the complete run total. Neither form may be invented to fill absent billing evidence. Without a complete-scope assertion, report known partial spend but withhold full-run cost coverage and cost/acceptance ratios that require it. Mixed-currency costs retain currency-specific known spend but cannot claim complete single-currency run cost.

All relevant distinct charged attempts must remain represented when a run's evidence revision is updated. Merely selecting the latest run record is not proof that previous attempt spending vanished. [Worked examples](worked-examples.md#attempts-and-cumulative-spend) distinguishes replacement from accumulation and partial costs from total costs.

## Derived record and provenance

A normalized record preserves the logical identity and supported input fields, plus its reader `profile`, raw source values, `field_pointers`, warnings and source IDs. Field pointers bind normalized values to captured file locations; source capture retains relative filenames, byte sizes and SHA-256 values. The overall captured-source digest identifies the selected bytes, not an external artifact's quality.

The result keeps immutable revision/history evidence and a defensibly selected current view. Revision conflicts, unsupported transitions, unreadable sources and invalid records have explicit exclusions/issues. Do not edit a derived record to disguise a source defect; correct the mapping or ingest new bound evidence as a new result.

Raw JSON values remain faithful evidence. Markdown escapes presentation-active source text; display escaping is not a change to the source or a universal CSV safety claim. The report template is illustrative, not a second parser schema; the emitted result and this contract define supported semantics.

## Metric contract

Every reported rate carries its numerator, denominator and relevant coverage. Zero denominator produces null, never 0% or 100%. Missing/conflicting labels do not become rejections. The core quantities are:

- acceptance among labeled runs: accepted / (accepted + rejected);
- label coverage: (accepted + rejected) / eligible runs;
- disagreement: directional disagreements / eligible comparable pairs;
- known measured spend: sum of supported non-overlapping measured costs in each currency;
- accepted-run mean: compatible measured cost of all accepted runs / accepted runs, when that cost coverage is complete;
- spend per currently evidenced acceptance: complete compatible cohort spend / currently known accepts, with label coverage visible;
- fully adjudicated cost per acceptance: the previous quantity only after every eligible human outcome is resolved.

The report and audit playbooks define interpretation and limits. A helper can count exact rows while the underlying cohort is confounded; metric computation does not establish a fair ranking or a causal diagnosis.

## Emitted result fields

Analytical operations emit one JSON object with these stable top-level fields:

| Field | Meaning |
| --- | --- |
| schema_version, parser_version | output contract and actual reader identity |
| status | `ok`, `partial`, `error` or `no-new-result`; intake state, never acceptance |
| generated_at, identity | UTC output time and digest of analytical identity |
| context | operation, inclusive event/knowledge cutoffs, cohort, selected group, UTC, reviewer selection and metric version |
| counts | discovered/read/failed sources, read/rejected/duplicate records, current/eligible/history/conflict counts, human-labeled runs, excluded evidence and new evidence revisions |
| manifest, source_manifest | explicit selection and captured hashes/coherence/status for each source |
| records | retained normalized evidence revisions, including previous history |
| current | one defensibly selected revision per currently supplied logical run |
| history | superseded or conflicted historical revisions considered by this analysis |
| conflicts | unresolved run identities, competing record IDs and reasons |
| eligible_record_ids | current terminal records eligible for outcome metrics |
| labels | selected primary human/machine label by record ID, including nulls |
| measurement_totals | non-overlapping measurement series, coverage and observation IDs by record |
| metrics | exact acceptance/coverage, costs, duration/tokens/iteration summaries, completion/judgment counts and reason frequencies |
| calibration | declared reference policy, selected reviewers, exact pairs/cells/disagreements, assessments and pair coverage |
| groups | engine, model, version and UTC-date views with IDs and the same metric contract |
| comparison | explicit descriptive-only limits and task/cohort/criterion/rubric/condition strata |
| handoffs | unresolved source-bound discrepancy handoffs; no repair action |
| exclusions | evidence ID, reason, optional detail and context |
| report_paths | actual JSON and Markdown locations |

A no-new-result response additionally contains `reason` and `previous_output_identity`. Preflight failure may instead return a compact error object with `status`, `reason` and `detail`; it is not a valid previous analytical result.

Ratios use `{numerator, denominator, value}`. The first two are exact counts; value is null at zero denominator. `metrics.costs` keys are currencies. Each currency exposes measured `known_spend`, `measured_run_coverage`, `mean_observed_cost_of_accepted_runs`, `spend_per_currently_evidenced_accepted_outcome`, `fully_adjudicated_cost_per_accepted_outcome`, plus separate measured/estimated/reserved `series`. The accepted-run mean requires all accepted runs to have complete compatible run costs despite its historical `mean_observed...` field name. Known spend may be partial; inspect its coverage before interpreting it. A basis with no valid observation for that currency has `known_spend` null (unknown), never 0; an observed measured zero is 0. Each cost basis distinguishes `observed_run_coverage` (any valid observed amount) from `run_coverage` (complete compatible run cost). Per-record measurement totals similarly separate `valid` from `complete`, with `coverage_basis`, effective `observation_ids` and `covered_observation_ids`. A valid partial charge is useful evidence without being a full-run bill.

`calibration.cells` contains pair-ID lists; `cell_counts` contains their exact lengths. `paired_denominator` counts eligible target/rubric pairs, while `paired_run_coverage` counts distinct paired runs over eligible runs. Multiple criteria can therefore create more pairs than runs; do not replace one denominator with the other. Exclusions can overlap by record and evidence type, so their row count is not a count of distinct excluded runs.

`counts.new_revisions` compares fresh record identities with the previous output; it is not a new-trial count. `records` preserves previous observations even when their source is absent; those rows are explicitly excluded from the current selection. Do not report `len(records)` as the current portfolio denominator.

[Report template](../assets/report-template.json) is a nonexecuted shape reference with null status/time/identity. It is not a successful report, previous-result input or validation substitute. A real result must come from actual input evidence and include the actual parser/metric identity.
