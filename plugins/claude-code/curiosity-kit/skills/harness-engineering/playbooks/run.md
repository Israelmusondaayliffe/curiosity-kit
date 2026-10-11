# Run

Carry an approved multi-step harness build to a named terminal state, survive interruption, and never gain authority the plan did not grant.

## Requirements

An approved plan (validated with `hectl plan`), the allowed paths, caps and stop rules. Use Codex Goal mode only when explicitly requested. Otherwise stay in the current authorized task; use a supported long-running session only when needed. Chat/connected-folder work stores durable state only in an authorized persistent location. An installed loop framework may drive the iterations; the state below still records them.

## Loop

1. Create state once, next to the plan or in the connected folder:

```text
python3 scripts/hectl.py run init --state RUN.json --run-id ID --objective "..." \
  --plan PLAN.json --max-steps N --max-launches K
```

The plan must pass `hectl plan`; the launch cap cannot exceed the plan's `max_task_launches`, and the unresolved count starts from the plan's `outcome.unresolved_before` unless `--unresolved` sets it.

2. Observe fresh state and choose one bounded action inside an approved group. Apply it through [build](build.md).
3. Run the checks for that change and record the step:

```text
python3 scripts/hectl.py run step --state RUN.json --action "..." --group GROUP \
  --delta "observable change in the target" --unresolved U --check "command: result"
```

An empty `--delta` means the wave changed nothing; one such wave ends the run as `exhausted` for re-planning. Exceeding the launch cap or reaching the step cap with work unresolved also ends it. A changed plan file blocks the run.
4. Continue only while steps report progress and caps remain.

## Resume

A fresh session starts with `python3 scripts/hectl.py run status --state RUN.json`. It reports the last step, unresolved count, whether the plan is unchanged, and the next allowed move. Re-observe the target before acting; do not repeat a recorded step.

## Stop

End with `run stop --as STATE --reason "..."`, where STATE is `waiting-input`, `blocked`, `exhausted`, `failed`, `cancelled` or `completed`. A terminal state is never renamed. `completed` is refused while unresolved work remains and needs a receipt from [verification](verification.md) via `--verifier-receipt`, shaped like `assets/templates/verifier-receipt.json`. The run refuses a receipt for another run, a failed functional or qualitative result, unresolved required items, any non-passing check, or a receipt older than the last step. A passing receipt is still only as true as its evidence.
