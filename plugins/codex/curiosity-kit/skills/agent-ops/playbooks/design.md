# Design and tool interfaces

## Decide what is needed

Take the user's outcome, current workflow, available tools, source inputs, allowed changes and checkable result. Inspect an existing design before proposing another. Start with one call plus retrieval/examples or ordinary code. Move to a workflow only when its control structure helps; use autonomy only when action selection depends on unpredictable environmental feedback. Name the extra cost or latency and what it buys. Missing ground truth is a design gap, not permission for self-grading.

Keep a compact design artifact containing: outcome; chosen pattern and simpler alternative considered; target host; inputs/tools/memory; read/write/action boundaries; observable success and failure; checks; finite execution boundary; retry/blocked policy; necessary human decisions; and inherited project instructions. Do not duplicate the host instruction chain or invent an output-folder convention. If the user already chose a suitable pattern, reuse that choice without a fresh interview.

## Five workflow branches

For the selected branch, emit complete prompts or executable project artifacts, with concrete inputs, outputs and failure behavior. Do not merely name a pattern.

1. Chaining: ordered stages consume the preceding artifact. Name each intermediate check, who runs it and what a failure prevents. Example: source-grounded outline passes coverage checks before drafting; invalid citations return to the evidence stage.
2. Routing: define categories with discriminating examples, specialized handling and an explicit uncertain/unmatched fallback. State how a mistaken classification is detected and corrected. Cheap triage is optional, not a reason to silently downgrade an explicitly selected model.
3. Parallelization: choose partitioned work or competing attempts. Give each worker disjoint write targets and the same relevant baseline. Define integration or selection before dispatch. A vote cannot erase a required failure; missing required partitions remain incomplete. Avoid shared mutable files.
4. Orchestrator-workers: the parent decomposes variable work, names dependencies and ownership, gives bounded contracts, inspects returned artifacts and runs final checks. Dependent work waits for verified prerequisite results. Every child ends in an accounted state; a missing return is not success.
5. Evaluator-optimizer: define the rubric, generator, independent evaluator, finite rounds and acceptance rule before generation. Feedback addresses observed defects. Stop when the bar is met; do not force a revision of passing work. Neither numeric scores nor model confidence replace required evidence.

One optional coordination example is six cards: specification, build, independent review, conditional repair, parent verification, summary. Merge unnecessary cards; no board or scheduler is required. Supply concrete role briefs from [roles](../references/roles.md) only when actual delegation is useful.

## Autonomous agent and subagent branches

An autonomous design states how it acquires the task, chooses the next action from observed feedback, checks environmental ground truth, pauses for material decisions and stops on success, exhausted budget or a named blocker. State how retries change the approach. A budget must be finite and appropriate to this assignment; an exhausted agent cannot redefine its objective as complete.

A reusable subagent definition states its narrow trigger, inputs, minimum tools, read/write scope, output contract, checks, escalation and stop conditions. A reviewer gets read-only artifact access and a separately allowed receipt destination if it must write a report. Freshness requires a independent context, not a role title.

Use the [host contract](../references/host-contract.md) for the actual supported artifact shape. Deliver to the authorized project output destination, with the intended installation path clearly distinguished. Do not install, edit global settings or widen tool grants as a side effect. If exact host fields cannot be verified, provide a complete host-neutral brief and identify the unverified serialization instead of inventing working config.

## ACI branch

For each proposed tool, write its purpose, when not to use it, typed inputs, output shape, errors, side effects and approval boundary. Include one valid call, an edge case and a nearby operation owned by another tool. Describe every parameter in terms a caller can use without hidden implementation knowledge.

Start from actual call sites and observed mistakes. Prefer a direct interface that removes caller obligations over pass-through wrappers. Make repeated mistakes harder to express: for example, resolve paths against an explicit root rather than a changing shell directory, or separate preview from mutation. Avoid line-count bookkeeping and unnecessarily escaped payloads. Do not promise structural prevention when the interface merely adds a warning.

Inspect whether a failure comes from the tool shape, the caller, missing permission or a unavailable host capability before changing it. When no failure example exists, label the risk as a hypothesis. Use the smallest ordinary-path check that can distinguish correct use from the demonstrated error.

## Verification and delivery

Check that every branch contains its defining control, every action has authority, and every claimed tool/format exists on the intended host. Parse emitted structured artifacts using the actual supported parser when available. Exercise the specific meaningful success and failure behavior in an authorized disposable environment. A keyword checker is only a lint signal; it cannot prove correct stops or independent review.

Return the complete artifacts, pattern rationale, actual checks versus unrun host checks, and the next necessary action. If a more complex pattern fails its premise, move down to a simpler design rather than adding machinery.
