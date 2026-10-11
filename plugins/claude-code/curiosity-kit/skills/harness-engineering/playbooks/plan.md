# Plan

Turn a confirmed profile and a fresh audit into a plan a builder can apply without making a single design decision.

## Requirements before planning

A confirmed profile and a current audit, or a written reason one does not apply (for example a one-file fix the user specified exactly). Check the profile at this point with `python3 scripts/hectl.py profile PROFILE.json --require-confirmed`; a draft fails here because a draft never approves planning or building. The profile names the platform; plan only surfaces that platform has.

## What the plan decides

1. **Outcome.** The primary metric, the before state, the target state, the unresolved required-work count before and after, and how many primary outputs to expect. Execution against the target is the work; audits, receipts and reviews are support.
2. **Budget.** The legacy schema1 limits below apply to this operation-plan interface, not to all authoring workers or every native evaluation campaign. New evaluation uses its separately versioned, explicitly finite contract. A task-launch cap (above 6 needs the user's explicit cost approval and a written warning), a support-artifact cap, one final verification pass, and one low-yield wave: a wave that changes nothing in the target ends the run for re-planning.
3. **Qualitative acceptance.** When judgement carries acceptance (prose quality, visual fidelity, likeness), name the check and its owner. A plan whose acceptance is qualitative but whose checks are only functional is incomplete.
4. **Layers and placement.** Design the information, execution and feedback layers and place each requirement in its narrowest durable scope per [architecture](../references/architecture.md). On Cowork, durable means a connected folder, app instructions or an external system.
5. **Evidence-led changes.** Suspected compensation is a proposed subtraction experiment, not an automatic removal. Preserve useful safeguards and user policy. Put justified changes in their own approval group with evidence and a reason. Reuse installed capabilities before proposing a new skill or plugin. Prefer scripts, rules, hooks, sandbox settings and templates where behavior must be exact and the platform supports them.
6. **Approval groups** per [approvals](../references/approvals.md). Approving one group never approves another.
7. **Operations.** Each operation has an id, `create` or `update`, a target inside `allowed_roots`, an approval group, exactly one of `content` or `source`, a reason, and for updates the current `expected_sha256` from the audit. Add checks, failure stops and the rollback order.

Start from `assets/templates/operations-plan.json`, then validate:

```text
python3 scripts/hectl.py plan PLAN.json
```

Fix every error before showing the plan. Present the human summary and the machine plan together. Implementation waits for the user's acceptance or an explicit request for end-to-end execution.
