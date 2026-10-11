# Skill evaluation

Establish what a skill actually does, where it fails and whether a proposed change is supported. This local method incorporates Skill Eval Loop and Creator Pro's execution, grading, comparison and description-tuning depth. It does not require a sibling evaluator or a particular model/provider.

## Frame the decision

Read the actual skill, its supporting methods, required tools, source ownership and the user's requested outcome. Use [research](research.md) to settle changing host facts and [interview](interview.md) for unresolved user decisions. Name whether this is exploratory authoring, regression protection, triggering, comparative quality, a release decision or a diagnosis. Different questions need different evidence.

For an existing capability, the reference is its current corresponding method with legitimate dependencies. For a consolidated capability, cover the union of the original sources and the accepted local baseline. A no-skill arm may answer a separate question for a genuinely new method, but cannot replace an applicable original arm. Do not disadvantage an original by hiding its required resources.

Define the exact target, candidate, host, input artifacts, tool inventory, permission scope and output surfaces. Keep secrets, raw configuration and unrelated history out of the bundle. Record denied or inaccessible evidence instead of collecting it by an alternate unauthorized route.

## Design useful cases before execution

Use stable case IDs and clear source-bound criteria. Include the distinct branches needed for the decision, useful near misses and credible failure/authority paths. A realistic prompt can include informal wording and relevant file context; it must not smuggle in the desired answer or force the helper whose natural use is being tested.

Keep three questions separate:
- Trigger: did the actual host select or explicitly invoke the intended method under the chosen policy?
- Function: did the real operation produce the required artifact or state without forbidden effects?
- Quality: does the inspected result meet the task's factual, practical and qualitative criteria?

Define whether a trigger measures first selection or eventual invocation. A timeout, missing executable, auth failure or malformed trace is invalid or blocked evidence, not a successful should-not-trigger result. Test adapter metadata and actual catalogs; keyword changes cannot repair a hidden route.

Choose cases by risk and coverage, not a fixed ten/twenty-query floor. Criteria must discriminate: checking that report.md exists does not check its claims. A subjective task still has source fidelity, requested content, usability and qualitative review. Use good and bad controls for the checker; calibrate a consequential judge against a targeted defect as well as gross failure.

Freeze the suite, rubric, inputs, candidate and adapter before qualification. An assertion discovered during exploration can improve the next suite version; it cannot retroactively qualify the output that suggested it. Match baseline and candidate conditions. Keep expected answers and variant identities out of candidate-readable files where independence requires it.

## Prepare the local records

Read [evaluation contract](../references/evaluation-contract.md) for exact implemented schemas and CLI arguments. The local helper snapshots declared files, validates suites, stages copies, records actual returned evidence, compares compatible runs and prepares guarded application. It does not execute model cases by reading a JSON array or authenticate a supplied result.

Use a declared output root outside the source and candidate. Validate the suite before launching work:

```text
python3 scripts/hectl.py eval suite-check SUITE.json
python3 scripts/hectl.py eval snapshot --target SKILL_DIR --output SNAPSHOT.json
```

Snapshot all files the execution depends on, with an explicit exclusion policy. Do not omit a helper or reference because the visible entry is unchanged. Preserve exact source, suite, fixture and adapter identities before and after the run. A same-named case with changed meaning is not a comparable case.

Choose an explicit finite task budget with the host owner. Keep dispatched leads, helpers, retries and repairs visible; a interrupted or invalid launch remains consumed work. The local cycle ledger checks recorded limits but cannot observe unreported host calls. Long tasks use a supported persistent launcher with terminal capture, rather than a turn-bound background job whose disappearance could look like success.

## Execute on the real available surface

Inspect the actual authenticated discovery/catalog and loading route before spending on a matched campaign. App-server or dead-provider probes can inform setup but do not prove what the recognized model sees. Preserve foreign metadata, truncation and isolation limits. Freeze permissible temporary writes and legitimate own-output spill reads in both request and acceptance criteria.

Run natural tasks through the target host's supported tools. Keep opposite variants, hidden oracles and unnecessary personal siblings outside the intended arm. Preserve each original's legitimate dependencies. Capture available tool/action evidence and resulting artifacts; never request hidden reasoning. If native execution is unavailable, prepare the suite and perform clearly labelled local checks, but leave native behavior unverified.

Record exits, interruption, elapsed time and usage only when observed. Preserve raw failures and any changes made during setup. An empty final diff cannot prove no forbidden temporary write occurred; use appropriate observed side-effect evidence when that is a required claim. No tool promises OS isolation merely because it uses a separate folder.

Use `hectl eval record` with the exact suite, target, results and artifact root. Read its full result and limitations. Imported execution declarations remain declarations; the reviewer must inspect actual evidence. Missing required artifacts, empty results or stale identities block a passing record.

## Grade and compare

Use [review methods](../references/review-methods.md). Inspect final artifacts, supporting notes and final replies against the frozen sources and rubric. Separate deterministic checks from judgment and self-review from independent review. Preserve assistance and reviewer corrections as such.

Use explicit reference/candidate roles and compare only compatible observations:

```text
python3 scripts/hectl.py eval compare --baseline BASELINE_RUN.json --candidate CANDIDATE_RUN.json
```

A legitimate failed reference baseline remains valuable evidence. It is not an approved release baseline. A candidate needs to satisfy its frozen essential criteria even if the original was worse. Missing, removed, invalid, interrupted and incompatible cases remain visible with their own denominators; do not hide them in an average.

Keep tokens, characters, cost, tool calls and duration separate, with actual units and null for unknown. Use actual repetitions; never compare one configuration to imaginary zeros. A single matched pair supports a scoped result, not a general superiority or causal claim. An inconclusive comparison is a useful outcome when it prevents an unsupported selection.

## Tune descriptions without consuming the test

First diagnose whether failure is invocation policy, metadata, weak branch wording or the wrong owner. Do not make a description aggressively claim unrelated tasks just to increase selection.

Curate positive and near-miss cases by stable ID, with explicit expected labels and development/validation/final partitions. Avoid contradictory duplicate text. Use the trigger editor in [review interface](../references/review-interface.md) when it helps; direct JSON editing is adequate for a small set.

Tune on training/development and validation evidence. Preserve each proposed description, its relevant outcomes and selection rationale. Freeze the selected candidate before an untouched final test. If final results informed repeated selection, they are now validation material; do not claim they prevent overfitting. Small sets may support no credible holdout claim at all.

The history view reports supplied observations; it does not select or apply a description automatically. Apply changes only through the staged repair and current authority path.

## Diagnose and stop

Classify the failure before editing: trigger, missing resource, instruction, tool, source, environment, checker or unclear rubric. Pstack's useful distinction is documentation drift versus verifier gap versus actual product defect. Repairing the verifier needs a new control and affected behavior check; renaming a failing requirement is not repair.

Proceed to [skill repair](skill-repair.md) only for a concrete cause within authority. Stop the approach when the same failure repeats or progress stops, then change the diagnosis rather than widening a budget silently. Preserve exhaustion and unknown effects.

Return one compact record of the decision, exact artifacts, case-level results, comparison conditions, useful findings and unverified essentials. An evaluated candidate, reviewed artifact, approved application and installed capability are separate states.

## Start from a complete suite

[The fictional kit-note suite](../assets/templates/evaluation.json) is valid input to `eval suite-check`. It demonstrates exact target paths, task-specific finite limits, declared execution/judgment settings and fixed source/format criteria. It is a known training example, not a holdout or an automatic call budget. Copy it outside the target, replace every task-specific field with the approved case, and bind real fixture paths/hashes where source truth depends on them. An empty fixtures list is explicit absence of external fixture binding, not proof that source data was checked. The companion [author brief](../assets/examples/kit-note-brief.json) contains the complete referenced runtime files.

## Summarize actual repeated runs

When the approved evaluation genuinely needs repeated observations, retain each actual run and its identities. Use `eval aggregate --candidate RUN_A.json --candidate RUN_B.json` and add repeated `--baseline` paths only when there is a real matched baseline. There is no default repeat quota. One target revision must hold within each role, with matched suite, adapter, judge, assistance and evidence-origin conditions across roles. Different currencies, duplicate evidence and mixed revisions are refused rather than averaged together.

Read per-case results before pooled summaries. The helper reports observed repeat counts, status counts, measured sample counts, unknowns, mean, sample standard deviation and range; candidate-minus-baseline mean deltas are descriptive. A single known observation has no defined sample spread. Invalid and interrupted attempts remain visible and consumed, but cannot become quality failures or successes. Character counts are not tokens; absent costs are not zero. Pooled case means are not whole-run wall-clock duration, and unequal repetitions are not automatically paired trials. Preserve source artifacts and avoid significance, reliability or causal claims the design cannot support.
