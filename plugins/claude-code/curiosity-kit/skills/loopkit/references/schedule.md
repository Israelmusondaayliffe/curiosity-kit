# Schedule data and module contract

`lk_schedule.prepare(run, generation, draft)` and `lk_schedule.observe(run, generation, observation)` use the same generation-checked snapshot writer as the core and return updated state. They never contact a host scheduler. The integrated CLI exposes these commands:

```text
python3 scripts/loopkit.py schedule-prepare RUN --expected-generation N --note DRAFT.json
python3 scripts/loopkit.py schedule-observe RUN --expected-generation N --note OBSERVATION.json
```

Run these from the skill directory, using the current generation returned by `status`. They prepare or record local state; a successful record write is not a host scheduling operation.

## Draft

Required fields: `host` matching the run; nonempty `cadence`, IANA `timezone`, self-contained `task_prompt`, `no_op`, `stop_condition`, `evidence_return` and `authority`. The module requires a completed, currently verified manual run before preparing. The agent verifies timezone/cadence interpretation through the actual host; accepting a JSON string does not validate a schedule expression.

Use [the draft template](../assets/schedule-template.json) only after replacing its markers with actual authorized values; unresolved template markers are rejected. Preparation keeps `host_id` null. The local record status begins `prepared` and retains its manual-run/artifact binding.

## Host observation

Required: `event`, matching `host`, actual `host_id`, actual `surface`, workspace-relative `evidence_path`, and `summary`. Evidence must be a saved host response/inspection artifact within authorized scope. Read it, do not merely create a file with a desired assertion. The recorder checks presence and hashes it; the agent/reviewer establishes what it proves.

- `activated`: requires separate `authorization_reference`; accepted after prepared or paused, with unchanged manual-run artifacts. Records `active-unobserved`, not scheduled success
- `execution` or `no-op`: requires actual `execution_id` and `result` (`success`, `no-op`, `failed`, `blocked`). Success/no-op requires `verification_evidence`, a scoped artifact inspecting the actual scheduled result. Successful observation gives `observed`; failure/block gives `attention-required`
- `paused` or `stopped`: requires actual host confirmation for the matching schedule id
- `failed`: records a host fault requiring attention

History retains observations and evidence hashes. Later recurrence uses fresh run instances so prior terminal outcomes remain intact. Unknown host responses need read-only reconciliation before another create/activation attempt. Never forge an execution id or reuse the manual run as proof of a scheduled invocation.
