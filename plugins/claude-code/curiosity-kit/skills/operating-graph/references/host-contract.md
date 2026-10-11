# Host contract and evidence boundaries

Last checked: 9 October 2026. Read for worker/effect execution, host portability or qualification. Stable graph semantics do not depend on a named model or provider. Tool availability and exact argument schemas must come from the current session, not this document's examples.

## What this package can and cannot do

The standard-library CLI manages a selected local graph run: validation, readiness, packet/evidence records, bounded lifecycle, rewrites, recovery and verification. It does not acquire credentials, install a plugin, start a paid API client, send a message to an external recipient or authenticate a human decision. Actual worker/effect tools belong to the invoking host/controller.

Before dispatch, establish the concrete available launch, wait/inspect, interrupt/stop and result-reading operations. Determine capacity from that surface, including its current parent/sibling use. If an essential operation or requested model/context setting is unavailable, block that execution mode and report the exact gap. Design and read-only inspection remain possible. Do not invent equivalent model availability from a provider name.

## Normalize the actual launch deliberately

The runtime packet describes intent; it is not a tool call. Translate it to the actual host schema field by field. Preserve fresh context, bounded goal, accessible inputs, allowed/forbidden writes, criteria, counters, deadline, canonical return location and authority denials. Pass no parent transcript or hidden reasoning. A node worker may not spawn children, approve, integrate canonical state, answer for the controller or issue terminal acceptance.

Honor explicit user requirements for model and context. If the required selection is unavailable, report and block the affected launch unless the user already authorized a compatible fallback. When no exact selection is required, choose a suitable available model by capability and record the setting actually observed; do not infer unknown effective-model fields from an alias. Effort settings and model routing differ across hosts. Package metadata cannot establish which model ran.

Capture the actual launch request and host response, then persist the run's launch binding. A unique string invented for a fixture is a simulated identity. A real invocation ID must come from the observed tool channel. If a request may have been issued but the response is missing, retain an unknown launch obligation and reconcile before any retry. Do not reuse a child as a supposedly fresh attempt.

The controller validates returned scope and evidence, opens the artifacts, and commits eligible outputs. A worker's declaration of its writes is not a complete filesystem audit. Where hard containment matters, use a separately authorized supported sandbox and test it; a directory prefix, shared workspace or instruction is not that sandbox.

## Approval and effect adapters

A trusted controller receives the actual verified user/authority decision through the permitted channel, checks action/destination/content/conditions, and records its provenance and ordering. An imported `granted` JSON value alone is not authentication. Revocation controls future work; it cannot undo an effect already issued. Platform-required handoff/action-time confirmation remains required even when a graph has a standing grant.

Before an effect, record intent and stable operation identity, revalidate scope/decision at the final invocation boundary, and capture actual outcome. If the adapter supports lookup or idempotency, use it within its documented scope. Without either, a lost response means unknown outcome and blocks automatic retry. No local journal can promise exactly-once execution across an unqueryable external system. Use inert effect adapters for sample tests.

## Stop and settlement

Record a cancellation request separately from observed worker termination. Interruption may change what a worker does without killing it. When the host has no reliable stop/lookup evidence, keep the obligation unresolved. No clean terminal completion or rewrite while live/uncertain work is hidden. Late results may be recorded as non-activating settlement; they cannot revive cancelled output or upgrade a terminal verdict.

## Dated host guidance

### Codex

The official subagent guide describes delegated parallel work and warns about concurrent writers. It distinguishes worker threads from the main integrating agent. Current tool details must still be inspected in the actual environment. A supported launch surface exposing `fork_turns` can express a fresh-context request; that field is not assumed to exist on every Codex surface. This package's original collaboration launch schema is normalized intent, not a universal native API. [Official guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents).

For a target-host qualification, verify actual fresh-context behavior, returned identity, completion/stop observations, permitted output paths and model/request facts using that host. The cloud author's collaboration tool is not proof of Codex CLI or desktop parity.

### Claude Code

The official guide distinguishes non-fork subagents with their own context from conversation forks that inherit parent history. Its current documentation says fork behavior varies with interactive/non-interactive mode and configuration. Select and verify a non-fork execution path deliberately; do not infer isolation from “subagent” or background execution alone. The Agent tool's available parameters and agent type must be checked in-session. [Official guidance](https://code.claude.com/docs/en/sub-agents).

Do not change user configuration, install agent definitions, broaden tools, alter permissions or switch billing arrangements as an implicit adaptation. If the current surface cannot supply the required non-fork/identity/return contract, qualify that limitation rather than silently downgrading it.

### Packaging and invocation

Agent Skills use a SKILL.md entry and optional local executable/reference/assets resources; progressive disclosure keeps specialist details off the initial path. [Specification](https://agentskills.io/specification). The maintained source preserves Claude explicit-only frontmatter; the existing packager emits Codex explicit-only policy in its generated metadata. Packaging checks establish those bytes and resource closure, not actual natural invocation or runtime execution.

## Evidence classes

- Structural check: definitions and records obey syntax/invariants.
- Deterministic sample: real local code operated on isolated fixture data.
- Simulated adapter: declared fake launch/effect responses exercise the protocol.
- Observed cloud worker: actual current cloud tool calls and artifacts were captured.
- Target-host qualification: that exact packaged candidate ran on the named supported host with independently inspected results.

One class never silently becomes another. Source dates, commands/tool references, immutable candidate/input/output identities, failures and unrun cases belong in the development receipt. Runtime users need the precise limits relevant to their selected job.
