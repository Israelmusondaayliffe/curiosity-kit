# Local deterministic interface

Requires Python 3 and its standard library. No package installation, network, model API, scheduler or sibling runtime is required. Resolve `scripts/loop_observatory.py` relative to this skill directory. Commands below assume the working directory is the skill directory.

```bash
python3 scripts/loop_observatory.py --help
```

## Commands and options

```text
register-root PATH --manifest PATH --profile PROFILE --namespace NAME
              [--coherence best-effort|frozen-export] [--discover]

ingest|report|audit|handoff --manifest PATH --output DIRECTORY
              [--previous PRIOR_RESULT_JSON]
              [--as-of RFC3339] [--known-as-of RFC3339]
              [--cohort TEXT] [--group-by engine|model|version|time]
              [--reference-reviewer NAME] [--machine-reviewer NAME]
              [--scheduled]
```

The four analytical commands use the same capture/normalization and result contract. Each emits both JSON and Markdown; the operation name is recorded in context and affects no-new-result identity. Choose the operation matching the user's question and use the corresponding local playbook to interpret the result. `handoff` emits unresolved analytical cases; it does not invoke or message a repair owner.

`--manifest` is always explicit. `--output` is an observer-owned directory disjoint from sources and the manifest; the helper writes there only. `--previous` may refer to a prior matching schema/parser result to retain immutable history and compare context. It is never a producer state file. Corrupt or incompatible previous results fail visibly; do not delete them or quietly reset history.

- `--cohort` is exact equality against the record's `cohort` field, not substring search or a query language.
- `--as-of` is an inclusive event-time cutoff for run revisions, judgments and measurements. It is not a start/end-window pair or a filter only on run completion date.
- `--known-as-of` is an inclusive evidence-knowledge cutoff. Missing required timestamps exclude evidence from that historical query with a reason.
- There is no lower-bound window option. For a bounded interval, explicitly select/export the relevant source cohort and document its lower boundary; do not claim the helper applied a nonexistent flag.
- `--group-by` selects one context dimension, default `engine`. The result still emits all four engine/model/version/time views. Time groups are UTC calendar days with intervals `[00:00, next 00:00)` using event time. Unknown event times remain `unknown`.
- Reviewer flags restrict eligible observations to the exact reviewer identity; they do not resolve remaining same-reviewer multiplicity or authorize relabeling.
- `--scheduled` requests conditional no-new-result behavior against `--previous`. It creates no schedule and makes no background monitoring promise.

## Explicit registration and discovery

Register one supplied export:

```bash
python3 scripts/loop_observatory.py register-root /absolute/input/export.json \
  --manifest /absolute/observer-inputs/manifest.json \
  --profile supplied-v1 --namespace checkout --coherence frozen-export
```

Register one producer run directory using its actual profile. Add `--discover` only when the user explicitly selected a containing root for bounded discovery. Discovery looks for supported run markers beneath that named root and writes explicit discovered entries into the local manifest; it does not scan a host home. Inspect the resulting source list before reporting across it.

Registration is idempotent for the same path/profile/namespace. A repeat reports zero added roots. It does not silently change a previous entry's coherence assertion; edit the owned manifest explicitly when the source assertion legitimately changes. The manifest must remain outside source roots.

## Complete supplied-record example

This example creates isolated synthetic files only. Set `SKILL_DIR` to this skill's actual directory. It does not read a real account or execute a producer.

```bash
SKILL_DIR="$PWD"
DEMO="$(mktemp -d)"
mkdir "$DEMO/input" "$DEMO/observer"
cat > "$DEMO/input/run.json" <<'JSON'
{
  "schema_version": "1.0",
  "records": [{
    "producer": "demo-loop",
    "run_id": "run-a",
    "revision": 1,
    "status": "completed",
    "terminal": true,
    "process_completion": true,
    "event_time": "2026-10-09T09:00:00Z",
    "known_time": "2026-10-09T10:00:00Z",
    "cohort": "checkout-demo",
    "goal": "Show the required checkout error state",
    "model": "example-model",
    "version": "1",
    "iteration": 2,
    "task": "checkout-error-state",
    "artifact": "sha256:example-artifact-a",
    "criterion": "required-state",
    "rubric": "ui-review@3",
    "judgments": [{
      "id": "judge-a", "kind": "machine", "label": true,
      "task": "checkout-error-state", "artifact": "sha256:example-artifact-a",
      "criterion": "required-state", "rubric": "ui-review@3",
      "purpose": "output-acceptance", "reviewer": "example-judge",
      "event_time": "2026-10-09T09:00:00Z", "known_time": "2026-10-09T09:00:00Z"
    }, {
      "id": "human-a", "kind": "human", "label": true,
      "task": "checkout-error-state", "artifact": "sha256:example-artifact-a",
      "criterion": "required-state", "rubric": "ui-review@3",
      "purpose": "output-acceptance", "reviewer": "example-reviewer",
      "event_time": "2026-10-09T10:00:00Z", "known_time": "2026-10-09T10:00:00Z"
    }],
    "measurement_coverage": [{
      "metric": "cost", "unit": "USD", "basis": "measured", "complete": true,
      "observation_ids": ["charge-a"]
    }],
    "measurements": [{
      "id": "charge-a", "metric": "cost", "value": 2, "unit": "USD",
      "basis": "measured", "scope": "run", "aggregation": "incremental",
      "attempt_id": "attempt-1", "operation_id": "call-1", "revision": 1,
      "covers": []
    }, {
      "id": "duration-a", "metric": "duration", "value": 30, "unit": "seconds",
      "basis": "measured", "scope": "run", "aggregation": "cumulative",
      "revision": 1, "covers": []
    }]
  }]
}
JSON
cat > "$DEMO/manifest.json" <<'JSON'
{
  "schema_version": "1.0",
  "sources": [{
    "id": "demo-export", "path": "input/run.json", "profile": "supplied-v1",
    "namespace": "checkout-example", "coherence": "frozen-export"
  }]
}
JSON
python3 "$SKILL_DIR/scripts/loop_observatory.py" report \
  --manifest "$DEMO/manifest.json" --output "$DEMO/observer" \
  --cohort checkout-demo > "$DEMO/first-result.json"
python3 "$SKILL_DIR/scripts/loop_observatory.py" report \
  --manifest "$DEMO/manifest.json" --output "$DEMO/observer" \
  --cohort checkout-demo --previous "$DEMO/first-result.json" --scheduled \
  > "$DEMO/repeat-result.json"
printf 'Isolated example artifacts: %s\n' "$DEMO"
```

Expected substantive result: one current eligible terminal run; human acceptance 1/1 and label coverage 1/1; one positive-agreement pair and zero disagreements; measured USD2 with cost coverage 1/1; accepted-run mean, spend per currently evidenced acceptance and fully adjudicated cost per acceptance each USD2; measured duration 30 seconds; unknown tokens. The second identical report request returns `no-new-result`. Both invocations still write uniquely named evidence artifacts. The stdout JSON files are also valid prior-result inputs.

The example's artifact string is an explicit synthetic identity, not proof that a real file hash was verified. A normal user report needs the actual source-backed binding. To audit the same inputs, use `audit` instead of `report`; that is a different operation/context and cannot be suppressed by the previous report identity.

## Result files and exit behavior

Each analytical command prints the full result JSON to stdout and writes unique paired files:

```text
OUTPUT/OPERATION-UTC_MICROSECOND_TIMESTAMP-RANDOM12.json
OUTPUT/OPERATION-UTC_MICROSECOND_TIMESTAMP-RANDOM12.md
```

Use the returned `report_paths.json` and `report_paths.markdown`; do not guess a timestamped name. A repeated same-second request must not overwrite the previous report. No-new-result also has an evidence file and `previous_output_identity`.

- Exit 0: `ok` or `no-new-result`.
- Exit 1: `partial`, with usable evidence plus failed sources/rejected records.
- Exit 2: `error`; preflight/configuration failures are a structured error on stderr, while an all-source-read failure may also return an error result artifact.

`status: ok` describes successful intake, not artifact acceptance, complete human labels or absence of analytical exclusions. Always read `conflicts`, `exclusions`, coverage and unknowns. A report with no eligible runs has null ratios; it does not prove zero failures. Ordinary shell syntax/argument errors are handled by the Python argument parser and may use its standard stderr message.

## Do not improvise missing operations

There is no producer resume/repair command, billing lookup, judge execution, scheduler installation, remote upload, CSV export or automatic acceptance action. Use supplied evidence, return the useful missing-evidence request, and keep new owner actions separate. Avoid wrapping this small helper in a service solely to answer a one-off question.
