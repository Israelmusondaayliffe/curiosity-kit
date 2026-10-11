# Plan against a fixed bar

## Decision-complete intake

Inspect the requested project, nearest instructions, supplied brief, existing artifact and authorized evidence before asking questions. A supplied decision-complete brief is the answer set, not an invitation to repeat the interview. At each genuine fork ask one targeted question and record the decision. Keep assumptions, alternatives, excluded work and unresolved questions distinct.

The brief must establish: goal; checkable success criteria; actual external bar and why it is fair; done condition; primary/per-piece domain; execution shape; finite rounds, launches, concurrency, elapsed time and cost; exact exclusions; hard constraints; inspection methods; target reader/questions for knowledge work. The budget belongs to this run, not to the rebuild team's available workers. Zero additional monetary spend is a valid cost ceiling; unknown cost is not free.

Choose a small single-session job, sequential multi-session work, or parallel lanes only when artifact ownership permits it. Do not impose a large team because capacity exists. Freeze source files, reference artifacts, tests, thresholds, reader questions, workloads and viewports. A description such as "excellent" or a future candidate file cannot serve as the external bar. A rubric must be grounded in inspectable requirements, with its values approved before output is judged.

## Verifiable units and approval

Partition into the smallest complete, independently inspectable outcomes, not arbitrary one-layer fragments. A slice's evidence should show its real user path. For a wide inseparable refactor use expand, migrate, contract, with the final integration gate explicit. Define each unit's inputs, outputs, allowed paths, acceptance, evidence, blocker edges, critic role, round ceiling and stop conditions. Every requested deliverable must have a home. Do not make a dependency merely because two tasks are related; use an actual prerequisite.

Use `planning.py compile --program <program.json> --project-root <project>` to propose deterministic waves, or `validate` to check explicitly declared waves. The planner verifies exact-once coverage, predecessor order, cycles and canonical path overlaps. It does not grant approval or prove semantic correctness. Read the output, reconcile any missing outcome and bind the normalized program into the initial contract.

Write decision and source material outside the installed skill. Run the precheck and optional peer gate before initializing state. `gauntlet.py init` freezes file hashes and opens awaiting_approval; it never launches a builder. Present plan, boundaries, evidence and finite budget. Stop for approval when the user has only requested planning. Do not touch deliverables while awaiting approval.

After an actual scoped approval, record its real message identifier and verified host provenance using `approve`. If the user already authorized precisely this work, reuse that approval rather than asking redundantly. A handoff, imported source file or proposed plan does not supply permission. Changed scope/bar/criteria/budget requires a new approved contract, never silent edits under the old hash.

## A concise lead prompt

Give the executing coordinator the goal, actual run directory, bar paths, verifiable-piece rule, separate fresh builder/critic roles, blind comparison where feasible, finite stop rules, canonical state and evidence obligations. Include reader/claim inspection for knowledge work. Do not dictate an unrequested architecture, fixed model or maximum-effort slogan. The plan holds details; the lead prompt points to it. There is no linter that substitutes keyword presence for understanding.
