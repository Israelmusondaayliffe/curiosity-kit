# Core CLI contract

Python 3.9+ standard library; POSIX local filesystems (Codex and Claude Code on macOS/Linux). No installation, model, scheduler, network service or sibling skill required. Invoke `python3 /absolute/path/to/skills/loopkit/scripts/loopkit.py`. Commands return JSON; exit 0 means the operation succeeded, not domain acceptance; doctor returns 1 for findings; invalid/blocked operations return 2.

## Concrete first-run example

Create a disposable workspace and contract using [the example](../assets/contract-example.json). Its commands name `python3`; at run time the actual executable is resolved on the host's PATH, and that path and its hash are recorded with each result. The example produces a synthetic `result.txt`; it authorizes no real account action.

```sh
LK=/absolute/path/to/skills/loopkit/scripts/loopkit.py
mkdir -p /tmp/lk-demo-work
python3 "$LK" validate /absolute/path/to/contract-example.json
python3 "$LK" init /absolute/path/to/contract-example.json --run /tmp/lk-demo-run --workspace /tmp/lk-demo-work
python3 "$LK" run-unit /tmp/lk-demo-run --expected-generation 0 --execute
python3 "$LK" status /tmp/lk-demo-run
# Use generation returned by run-unit/status, never assume it remains current:
python3 "$LK" finish /tmp/lk-demo-run --expected-generation N
python3 "$LK" doctor /tmp/lk-demo-run
```

Choose fresh directories when repeating. No command silently overwrites an existing run.

`run-unit` executes one serial unit's declared actions, followed by its checks. `check` executes only its checks. Both require `--execute`, confirming the caller reviewed the exact commands and has authority to run them. No arbitrary command can be supplied on the CLI. Argv arrays use `shell=False`; cwd, declared inputs and artifacts are confined to contract scope. This is NOT an OS sandbox: executable code can have undeclared effects. The agent must inspect commands, preserve host permissions and use an isolated environment for untrusted code. Contract prose and flags cannot grant authorization.

Paths: run and workspace roots are canonicalized, so system aliases such as macOS `/tmp` and `/var` work; a run, workspace or input named directly as a symlink is refused, and no component inside the workspace may be a symlink, so a planted link cannot redirect a read or write.

Captured results record resolved executable/hash, argv, cwd, declared input hashes, contract hash, before/after artifact hashes, timestamps, exit/failure and stdout/stderr file hashes. Checks must not mutate artifacts. Declared check `inputs` must include its local scripts/data, beyond the exact argv and executable binding. Declare all result-relevant artifacts; optional per-check `artifacts` narrows binding to a listed subset for serial units. Hashes detect drift, not correctness or malicious edits by someone able to rewrite the entire run.

## Verification and recovery

- `review RUN --expected-generation N --note FILE`: note contains `criterion_id`, `verdict` (`pass`, `fail`, `unavailable`), `reviewer`, `independent` boolean, workspace-relative `evidence_path`, and `reason`. A captured reviewer artifact and truthful reviewer provenance remain necessary; the CLI cannot prove an identity is independent. Missing/failed reviews cannot satisfy completion.
- `finish RUN --expected-generation N`: validates current checks/reviews and commits the unit. Final completion revalidates all units. If later work changes an earlier unit's evidence, it is not final-complete until that unit is freshly verified; do not weaken criteria.
- `check RUN --expected-generation N --unit ID --execute`: recheck a committed unit. Runs only its checks, never its actions, and records fresh results. Passing again restores its evidence; failing points to reopen. A recheck is not a work iteration: it uses no iteration or no-progress budget and is counted separately as `rechecks`, but it still needs remaining wall-clock time.
- `reopen RUN --expected-generation N --unit ID --reason TEXT`: returns one committed unit to work, only when its evidence is stale or failing (a changed input, artifact, check or review), never on a terminal run or with pending work. Run `run-unit`, then `finish`; the reopened unit is reverified without advancing past later units, whose own valid evidence is reused, and final completion rechecks all units.
- `review ... --unit ID`: refresh a judgment on a committed unit after its judged files legitimately changed. A judgment may declare `artifacts` (a subset of the contract's) so it binds only the files it judges; without that list it binds every declared artifact and a later unit's files make it stale.
- `stop RUN --expected-generation N --status paused|blocked|waiting_input|cancelled|failed|exhausted --reason TEXT`: no clean stop with unresolved in-flight work. Terminal runs cannot be silently reopened.
- `resume RUN --expected-generation N --reason TEXT [--acknowledge-drift]`: rereads durable state, rejects pending work or workspace drift, and honors the original budget. After inspecting a drift (for example a user edit while paused), `--acknowledge-drift` records the previous and current artifact hashes, the changed files, the committed units whose evidence is now stale, and the reason, then resumes. It refuses when nothing drifted. It keeps the edited files and never replays an action. Captured results and reviews keep their original hashes, so each affected unit needs `check --unit ID --execute` and, if that fails, `reopen`; unaffected units stay verified. Pauses consume the declared wall-clock budget; a new budget needs authorized contract revision/new run.
- `reconcile RUN --expected-generation N --note FILE`: note names exact pending `batch`, `resolution` (`observed-complete`, `observed-not-applied`, `unknown`), `process_stopped: true`, `reason`, and scoped `evidence_path`. Inspect actual effects and stop/confirm the original executor first. Known outcomes clear pending into blocked state; unknown remains blocked/pending. Reconciliation never synthesizes a machine pass or automatically replays an effect.
- `checkpoint RUN`: writes a derived bounded index under a run lock. `snapshot.json` is authoritative; checkpoint text is never execution authority.
- `doctor RUN`: read-only typed findings and recovery guidance. It does not repair or execute checks.

Each mutation requires the observed generation. A stale writer fails. Every command intent commits before execution; interruption leaves pending work for explicit inspection. Snapshot publication is one atomic replace with fsync; logs written before their result commits may remain as uncommitted evidence, not success. Locks release when their process exits; a lock filename alone is not a live writer.

Output captures are local task evidence, potentially sensitive: do not publish them automatically. Commands must avoid secrets in argv/output. The byte ceiling bounds normal capture and triggers termination, but a fast process can overshoot before the next poll. The helper kills only its own process group; detached descendants or external effects require inspection and cannot be rolled back by this helper.

## Schedule records

- `schedule-prepare RUN --expected-generation N --note DRAFT.json`: only after a completed run whose units all still verify. The draft from [the template](../assets/schedule-template.json) names `host` (must match the contract), `cadence`, `timezone`, `task_prompt`, `no_op`, `stop_condition`, `evidence_return` and `authority`; a value that still carries the template's replace marker is refused. Records `prepared` with no host id. Preparation creates nothing on the host.
- `schedule-observe RUN --expected-generation N --note OBSERVATION.json`: records what the host actually reported. Fields: `event` (`activated`, `execution`, `no-op`, `paused`, `stopped`, `failed`), `host`, `host_id`, `surface`, scoped `evidence_path` and `summary`. `activated` also needs `authorization_reference` naming the separate scheduling authority, and is refused if the manual run's artifacts changed. `execution`/`no-op` need `execution_id`, `result` and, for success or no-op, a scoped `verification_evidence` file; the record becomes `observed` only then. Evidence files are hashed into the history.

## Hook selection

- `bind RUN --workspace DIR --host codex|claude-code [--state-root ROOT] [--replace-run OLD_RUN]`: selects a nonterminal run for that workspace's startup, resume and compact hooks by writing one owned pointer. Returns the pointer path.
- `unbind RUN --workspace DIR --host HOST [--state-root ROOT]`: removes only that pointer.

See [binding](binding.md) for the state root each host uses.

`doctor` returns a `schedule` summary (status, host id, count and id of observed executions). It reports `schedule-unproven` until an execution has been observed, and `schedule-attention` after a failed or blocked one. A schedule paused or stopped after an observed execution keeps that history and raises no finding; its status still says it is not active. Schedule findings alone do not undo a verified completion. See [schedule](schedule.md) for the host procedure and [hosts](hosts.md) for the hook adapter.
