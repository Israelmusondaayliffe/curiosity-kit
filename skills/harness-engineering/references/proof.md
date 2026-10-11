# Proof

Completion needs fresh evidence from the environment the user actually runs. Verify what changed or what the task depends on; do not re-prove unchanged state. Progress is an observable change in the target plus a falling count of unresolved required work. A passing validator never outweighs a required item still marked needs-review, deferred or unfinished.

## Evidence ladder

From weakest to strongest: a statement; a pointer to the real file and line; a walk through the failure path showing the bad case cannot occur; a script run against the real artifact; reproduction in the running setup. Push each load-bearing claim as far up the ladder as is cheap, and say where it stopped.

## Structural evidence

Files at the approved paths; JSON, TOML, YAML and Markdown that parse or validate; the instruction chain resolving in the intended order; manifests and skills free of placeholders (`hectl skill-check`, `hectl plugin-check`); no secrets or user-specific sample data in generated files; source matching the installed copy (`hectl parity`).

## Behavioral evidence

A new session discovers the intended front doors and omits hidden specialists; each hidden specialist has a proven route and one real explicit invocation; a task whose answer depends on a supporting file shows that file was read; command policy allows safe examples and blocks forbidden ones; hooks run only after review and trust; connectors return an authenticated profile or a precise setup requirement. Optional bundles such as Browser or Computer Use are tested only when the harness depends on them.

## Functional versus qualitative

When judgement carries acceptance (prose quality, visual fidelity, likeness), report functional and qualitative results separately. Passing tests do not complete a task whose qualitative gate is missing, failed or below threshold. The rubric belongs to the task's owner.

## Receipts

List every required check once: the command or inspection, the fresh result, the evidence location, pass or fail. A missing or stale check is a failure. Summarize low-risk commands inline (command, exit code, one-line result); keep separate evidence files for destructive, security, release or installation steps.
