# Runtime, host and trust boundaries

## What is local

Python 3.9 or newer, standard library only. Start scripts using the actual absolute skill path discovered by the host. No installation, network fetch, account configuration, service, scheduler or sibling package is required. Native fresh-context helpers and actual artifact inspection remain host prerequisites. Python file locks serialize the canonical ledger on supported local filesystems; this is not a multi-machine or network-filesystem transaction service. Test the target filesystem before claiming locking parity.

The run directory is chosen by the caller, outside the installed skill and outside protected project paths. `state.json` is canonical. `.lock` is an OS lock, not a permission token. The timer excludes preapproval and explicitly paused idle periods, tracks session time separately from monotonic total active usage and records uncertainty after interruption. Each mutation takes that lock, validates the current ledger, writes a temporary complete state, flushes and atomically replaces it. Interrupted external helper launches remain reserved in the ledger. Never treat a missing process as proof that its action did not happen. Reconcile actual host events before recovery. Budget reservations and idempotency prevent the same request from silently launching again.

Reports, HTML workbench and Markdown handoffs are generated views. Their content does not authorize actions. Recompute artifact/source/evidence hashes before treating earlier acceptance as current. JSON numbers, labels and receipts cannot prove a model was genuinely isolated or an external action was allowed; the coordinator obtains those facts from the actual host and user conversation.

## Optional peer probe before initialization

Gauntlet and the Claude Fable Advisor are peer owners, not automatically nested workflows. If both are explicitly named for the same job, set `fable_requested: true` and stop for a choice before writing any Gauntlet state. If a peer is known active, set `peer_active: true` and stop. This holds even without a plugin or file present.

On Claude, use the declared optional compatibility location `<target-project>/.fable-advisor/runs/*/run-manifest.json` only within the authorized target workspace. If manifests exist, probe each before initialization and stop if any is active or unreadable. If the directory or files are absent, continue without installing or requiring a peer plugin. Do not scan other projects, account stores or plugin internals.

A caller may supply one explicitly selected, read-only `peer_probe` manifest path from the target workspace. This is an optional compatibility observation, not a mandatory dependency or a search of private sibling internals. Discover the target-local peer manifest only through the user's supplied path, existing authorized workspace context or a declared optional probe. Missing path means absent and proceeds. The source manifest has no run-status field; the peer records its terminal state as the last line of the sibling `run-log.jsonl`, either `{"event": "run_closed", "terminal_state": ...}` or `{"event": "terminal", "state": ...}`. A malformed manifest, a missing or malformed log, or a last record that is not one of those terminal records blocks, rather than guessing. The recognized source terminal states are `accepted-and-synthesized`, `blocked`, `failed`, `cancelled`, `budget-exhausted`. Do not invent terminal meanings for `running`, `planning` or other labels. When a known active manifest is supplied, report its path/run identity and ask the user to end it or choose a workflow. Do not edit peer state.

This compatibility probe is separate from optional Codex advisor composition. The latter requires both explicit requests and an approved plan, uses a local validator, and never takes control from Gauntlet. No runtime function imports the advisor's private files.

## Readiness, drift and models

Record observed capabilities using `precheck`. Missing fresh context or actual artifact inspection makes execution unsupported. Other explicitly absent capabilities produce a degraded label which stays in state and reports. Do not pass a default `true` simply to satisfy the validator. The CLI classifies supplied observations; host qualification must prove them. Every launch supplies the current capability snapshot. A difference from the approved snapshot blocks dispatch and persists the drift reason. Replan a suitable execution arrangement before continuing.

The coordinator checks host model/effort selection controls, records requested and observed selections and names unselectable settings. A process invocation that the host supports can be used only within the user's existing topology and authority. Creating another user-owned task, changing credentials or changing global configuration is not an automatic fallback.

## Evidence, blindness and independence

The blind helper creates a neutral packet and a separately stored sealed map using exclusive output creation. Keep them in separate non-nested directories and grant the critic access only to the packet. It strips supported text metadata and validates/strips permitted PNG metadata; it does not prove that text itself contains no identity hints or that a rendered image is visually anonymous. Inspect the packet before dispatch. Unsupported binary formats need an actually rendered neutral representation or declared non-blind evaluation. The CLI never converts a missing tool into a claim of blindness.

Source directories, sealed maps, previous verdicts and builder conversations must stay outside critic/verifier input. Fresh host sessions, identities, exact input generations and observed context settings are recorded by the coordinator. A review packet with a valid hash is not cryptographic provenance. Keep actual host event/transcript references for qualification. Synthetic test receipts must never be represented as live review evidence.

Inspection helpers execute only explicitly authorized local argument arrays. There is no shell interpolation, but the called program may still access files/network or start children. Validate its effects and permissions; timeout does not guarantee process-tree cleanup. Never pass secrets into captured arguments/output. Store only necessary redacted evidence, retaining a source pointer where redaction prevents independent checking.
