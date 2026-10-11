# Command and payload guide

Run from any directory using the actual skill path. Examples below use `S` for that path and `R` for an explicit disposable or authorized run directory. `--input` takes a JSON file. State commands also accept `-` for stdin. JSON input is data, never authorization by itself.

## Inspect and test the package

```
python3 "$S/scripts/gauntlet.py" --help
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s "$S/tests" -v
python3 "$S/tests/run_control.py" --help
```

The unit tests create isolated temporary files and exercise real local CLI behavior. Their fake host receipts test validation; they do not qualify real host isolation or model quality. They contain complete executable payload examples in `test_state_controls.py` and `test_engine_lifecycle.py`.

## Plan and initialize

`inspection.py brief --input brief.json` checks required intake and a file-backed bar. Fields: goal, done_means, domain, execution_shape, out_of_scope, non_negotiables, bar_rationale; success_criteria string array; inspection_methods; bar_files as `{path, sha256}` objects; output_paths; and budget. Supported methods: run, test, measure, render, screenshot, read, reader-proxy, claim-audit, source-reach, red-team. Bar files must exist, be nonempty and not overlap intended output. Knowledge work cannot use read alone.

State initialization calls this gate too, before creating state. Initial JSON fields:

- explicit_invocation: true, task, mode: artifact/project/verification-only, project_root.
- capabilities: observed booleans, including fresh_context and artifact_inspection. Include relevant optional capabilities such as command execution/network/parallel_helpers; false optional observations mark degraded.
- Optional peer_probe, peer_active, fable_requested, handled before any state creation.
- scope: write_roots absolute paths and allowed_actions string list. Review helpers have no artifact write paths.
- budget: positive max_launches, max_iterations, max_concurrency, max_critic_rounds_per_workstream, max_seconds; nonnegative finite max_cost. The embedded brief budget must match it.
- brief: the fields above. Its bar file contents are frozen as well.
- frozen: four paths named plan, bar, criteria, reader_questions. For a code-only run the last can contain an explicit non-applicability record; for knowledge work it holds the actual immutable question set.
- source_paths: actual external reference/test/source files. verification-only also requires artifact_paths to freeze finished work. The current finalization API certifies one exact frozen target. Multiple approved targets are refused as unverifiable rather than silently certifying a subset; use separate per-target verification runs for separate artifacts.
- review: criteria_ids, required_criteria_ids defaulting to all criteria, at least three required_perspectives, policy. Policy fields are quality_count and integrity_count, each at least 2; quality_rule `strict-majority`; integrity_rule `all-pass`; cannot_verify_rule `blocks`; consecutive_wins at least 2. Use `review.default_policy()` for the exact supported policy if uncertain.
- Optional normalized program from the planner. completion_mode is blind-consecutive by default; measured-plus-independent is available only for a program with an integration gate and an approved measured done condition.

```
python3 "$S/scripts/gauntlet.py" precheck --input init.json
python3 "$S/scripts/gauntlet.py" init --run-dir "$R" --input init.json
python3 "$S/scripts/gauntlet.py" verify --run-dir "$R"
```

Initialization returns run_id and contract_hash. Approval JSON binds that contract_hash, host_verified true, host, actual message_id, actor, verified_by and timezone-aware verified_at. Check the actual user approval, then:

```
python3 "$S/scripts/gauntlet.py" approve --run-dir "$R" --input approval.json
```

## Dependency program

`planning.py validate|compile --program program.json --project-root <project>` validates or computes waves. Program fields: goal; budget with max_elapsed_minutes, max_agent_launches, max_concurrency, max_critic_rounds_per_workstream, max_cost and extension_requires_user_approval true; workstreams; integration_waves; verification_panel, at least three distinct perspective strings. A workstream has id, objective, owner, dependencies, write_targets, acceptance_criteria, evidence_required, builder_charter, critic_charter, critic, max_critic_rounds and stop_conditions. Arrays hold strings except waves, which name `workstreams` lists. Protected paths, external_bar file references and reader_questions file reference are optional extra guards; initialization's bar gate is mandatory.

Program and state budget spellings differ for compatibility with the donor contract. Initialization verifies max_agent_launches equals max_launches, max_elapsed_minutes times 60 equals max_seconds, and concurrency/critic/cost ceilings match. Never exploit the two representations to widen a budget.

`planning.py ready|integration --program program.json --state records.json --project-root <project>` checks current evidence-bound accepted predecessors. `invalidate` additionally takes `--changed <id>` for changed workstreams. It reports descendants needing new evidence. These functions do not launch agents, run a scheduler or grant substantive acceptance.

## Reserve, observe and record

Launch JSON: unique request_id, actor, role builder/smoother/critic/reader/quality/integrity, workstream_id, action from approved allowed_actions, write_paths, fresh_context true, estimated_cost and current capabilities. Critic, quality and integrity dispatches also require evidence_paths mapping evidence IDs to actual files, hashed before dispatch. Blind critics additionally require packet_hash and sealed_map_hash from the prepared objects. Record explicit model/effort choice and actual host observations with the dispatch. Read-only roles use empty write_paths. A launch command returns may_launch; invoke the actual host helper only when true. A builder launch is refused when the workstream's remaining critic capacity, which counts interrupted critic reservations, cannot cover the independent reviews its new bytes need to be accepted; pause and use an approved successor contract instead.

```
python3 "$S/scripts/gauntlet.py" launch --run-dir "$R" --input launch.json
python3 "$S/scripts/gauntlet.py" complete --run-dir "$R" --input completed-launch.json
```

Completion JSON has launch_id, actual_cost and host_receipt: author_id, session_id, host_record, fresh_context, inherited_turns=0, forbidden_context_seen=false, role, verification_id and assigned perspectives. Builder/smoother receipts also require write_observations_complete true and write_observations with path, before_sha256 and after_sha256 for each observed change, with null for absence/deletion. The engine binds these to prelaunch snapshots and current bytes within approved output roots; the host still audits writes outside those roots. Values must describe actual host evidence. Repeated request/completion data is idempotent; conflicting replay is rejected.

`inspection.py check --input check.json` takes authorized true, argv string array, cwd, timeout_seconds and optional output artifact paths. It captures actual exit/stdout/stderr and hashes. `reader` takes artifact path/hash, questions_file/hash, exact questions array, and answers with original question, answer, location, guessed boolean and answerable boolean. `claims` takes artifact path/hash and claims with id, claim, location, support, reason, sources_checked `{path,sha256,quote}`. Supported claim statuses are supported/contradicted/unsupported/cannot-verify. Even unsupported rows list the sources actually checked.

## Blind packets and review bindings

```
python3 "$S/scripts/review.py" blind --ours candidate-output --reference bar-output --contract contract.json --packet neutral/packet.json --sealed-map sealed/map.json --seed 19
```

The seed is coordinator-only randomization input, never part of the critic packet. The contract is the full frozen state contract, not an abbreviated replacement. The coordinator validation envelope stays private from the blind critic. Send only the neutral packet to that critic; after receiving the unedited response, attach the coordinator identity/hash/evidence bindings to the recorded verdict. Do not send a candidate fingerprint that could reveal which neutral item is ours. Critic context binds piece_id, verification_id, artifact_hash, contract_hash, excluded_authors, used_sessions, criteria_ids, evidence_manifest and expected_sessions. Verifier contexts add eligible and required_perspectives. Evidence manifest maps coordinator evidence IDs to current SHA256 labels. Expected sessions are actual host receipts keyed by session ID.

Each verdict binds the same generation/identity fields, author_id and session_id; verifier_type for panel votes; perspectives; plan_hash_matched; reason; evidence_inspected objects `{id,sha256,observation}`; criteria_checked. Critics additionally return winner, confidence, one largest_gap and gap_is_actionable. A passing or winning result may record no material gap with gap_is_actionable false; a failing, losing or blocked result needs a concrete gap. Panel result is pass/fail/cannot-verify. A non-pass vote must include criterion_results mapping every criterion to its individual result. Required failures veto a quality majority; only explicitly nonmaterial failures can become preserved dissent. The worker cannot set candidate identity or its own trusted host receipt.

`review.py validate-critic|unseal|consensus --input review.json` validates those records. Consensus input contains verdicts, context and frozen policy. Unseal contains verdict, context, packet and sealed_map. `hash`, `freeze-contract`, `check-frozen` and `check-hash` expose contract integrity controls; inspect their `--help` for exact arguments.

Round JSON contains evidence_id, completed critic launch_id, contract_hash, artifact_path/hash, report_path, gap, expected verdict and review packet. The review packet carries the validated context, verdict, packet and sealed_map for blind mode. acceptance_evidence binds actual acceptance files for program workstreams. `round` recomputes the decision; a claimed win does not override it. See the executable lifecycle tests for a complete construction.

## Integrate, finalize and recover

`integrate` receives actual evidence_path pointing to an inspection.py check JSON result, exit_code, command and contradictions; all required workstreams must have current accepted evidence. `finalize` receives artifact_path, context and verdicts. In verification-only mode its resolved path and bytes must equal the single approved immutable artifact, even if a different path contains identical bytes. For knowledge work, inspection_reports maps reader and claims to the actual JSON outputs. A completed reader launch is required. The frozen question/source/artifact identities must still match. Finalize computes rather than accepts a terminal verdict.

```
python3 "$S/scripts/gauntlet.py" finalize --run-dir "$R" --input verification.json
python3 "$S/scripts/gauntlet.py" report --run-dir "$R"
python3 "$S/scripts/gauntlet.py" handoff --run-dir "$R"
```

`usage` accepts absolute nondecreasing totals only. `pause` takes reason and closes the active session interval before idle time; `recover` takes pending launch_id and reason after host reconciliation; `resume` takes current capabilities and peer status and starts a new session window while retaining total active usage. `stop` takes reason and produces an honest stop. None extends scope or resets budgets.

State CLI exits 0 on a successful operation, 1 for rejected/gated work or failed/unverifiable finalization, and 2 for argument syntax errors. An idempotent launch replay exits 0 but says may_launch=false. Planning exits 0 valid, 2 invalid. Review exits 0 accepted/matched, 1 invalid/failing. Inspection exits 0 passed, 2 invalid/failed/unverifiable. Always inspect the returned status as well as the exit code. `verify` is a structural ledger check, not a quality verdict.

## Non-blind threshold review

When a fair blind comparator does not exist, freeze review.judging with mode `rubric`, blind_feasible false, a nonempty reason and thresholds mapping every criterion ID to an operator/value. Supported operators are listed in review.validate_judging_policy. The critic returns criterion_observations with actual numeric values, evidence and a result, not an A/B winner. `review.py rubric --input rubric-review.json` derives the threshold result and rejects a claimed pass below the frozen bar. State rounds use this route only when it was approved in the contract; freshness, read-only role, artifact/evidence bindings and the independent final panel remain required. Do not switch modes to avoid an unfavorable comparison.

## Executable payload example

The following creates only a disposable synthetic fixture and proposes its plan. It launches no agent, grants no real approval and changes no user project. Run it from the skill directory:

```sh
DEMO=$(mktemp -d)
python3 - "$DEMO" <<'PYCODE'
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path('tests').resolve()))
from test_state_controls import state_fixture
root = Path(sys.argv[1])
(root/'init.json').write_text(json.dumps(state_fixture(root)))
PYCODE
python3 scripts/gauntlet.py precheck --input "$DEMO/init.json"
python3 scripts/gauntlet.py init --run-dir "$DEMO/run" --input "$DEMO/init.json"
python3 scripts/gauntlet.py verify --run-dir "$DEMO/run"
python3 scripts/gauntlet.py handoff --run-dir "$DEMO/run"
```

Expected: supported precheck, awaiting_approval state, no builder launches, and a generated handoff. The test helper is a fixture factory, not an alternative production entry. For actual work replace the synthetic brief, observations, files and budgets with the user's real scoped inputs, and obtain/record real approval before launch. Preserve this directory if needed to inspect the example evidence; cleanup is the caller's choice.

## Active time and write observations

The session timer starts at actual dispatch, not run creation or waiting approval. Call `pause` before a known idle gap and `resume` when active work restarts. Session elapsed and cumulative active seconds are separate; totals never decrease. Handoff closes the active segment. Uncertain interrupted time is retained conservatively and labelled uncertain rather than measured. A per-session ceiling does not authorize more launches, cost or rounds. Exhaustion needs the new approved successor procedure in playbooks/resume.md.

Writer completion compares observed before/after hashes with a bounded local snapshot of declared output roots. Unreported changed/deleted files inside those roots fail, unless a separately recorded concurrent writer owns them. Reported foreign writes always fail. This is not whole-filesystem surveillance or an OS sandbox; genuine host write-audit evidence remains required for effects outside the observed roots. The coordinator, not the builder's unsupported narrative, attests complete host observations. Narrow very large scopes before execution rather than silently truncating inspection.
