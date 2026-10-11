# Use explicitly requested Fable working modes

Apply SOLVE, BUILD, REVIEW or LEARN when the user explicitly chooses the Fable process. It works on any selected model and in any suitable domain. Do not require a model tier, claim the model's identity changed, or invoke these modes automatically merely because the problem is difficult.

These modes supply a working process. Domain execution stays with its actual owner, tools, permissions and conventions. BUILD does not create another coding framework. Changes to persistent instructions, skill evaluation infrastructure, memory policy or harness configuration remain with Harness Engineering. MPL can finish a prompt, analysis or review locally without requiring any sibling skill.

## Shared contract

Write a short outcome statement, hard constraints, soft preferences, acceptance checks and authority limits. Distinguish supplied facts, verified observations, assumptions and unknowns. Use evidence for completion. Compare genuinely different approaches when the task has a real choice; a deterministic edit needs no artificial alternatives. A visible rationale summarizes decisive tradeoffs, not hidden reasoning.

Retrieve a few relevant authorized lessons if such a mechanism exists. Precedent can suggest a test or risk but cannot replace the current contract. Missing memory does not block work.

## SOLVE

1. Frame the problem. State the requested outcome and underlying purpose. If the request appears to address a symptom, name the suspected mismatch and seek a narrow decision only if proceeding would materially change scope. Do not silently substitute a different problem.
2. Separate hard constraints from tradeable preferences. For each assumption that could change the answer, either verify it through an available authorized source or disclose its effect. Prioritize the uncertain constraint with the largest consequence.
3. Map dependencies. Work on the binding or high-risk subproblem before polishing easy pieces. For a meaningful choice, identify distinct mechanisms and compare them against the same criteria. Record why the rejected option fails a decisive criterion. Do not generate nominal alternatives that differ only in wording.
4. Define pass/fail checks before producing the answer. Then execute the chosen approach within the domain's normal workflow. If new evidence changes the plan, state the change and its consequence.
5. On repeated non-progress, reassess the frame and failure evidence. Is the dependency wrong, the tool unavailable, the requirement incompatible or the approach ineffective? Change a specific supported assumption or report the blocker. Use the task's resource bounds; do not repeat the same attempt indefinitely or impose a universal two-try rule.
6. Review with the process below. Use a fresh reviewer where available and warranted. Deliver the answer first, decisive constraints, supporting evidence, confidence basis and what evidence would change the conclusion. A recommendation may remain conditional when the decisive fact is unknown.

Copyable task instruction:

```text
Use Fable SOLVE for this task. Establish the outcome, hard constraints and pass/fail checks. Verify or disclose assumptions that could change the result. Address the binding dependency first. Compare distinct mechanisms only where there is a real choice. Execute within the existing permissions, then check the result against the contract. Deliver the answer, decisive evidence, remaining uncertainty and what would change your conclusion.
```

## BUILD

1. Read the actual relevant files, callers, conventions and existing checks before editing. Record the inspected paths in the evidence. For non-code artifacts, inspect their actual structure, source material and downstream use. Do not work against an imagined repository or document.
2. State what changes, what must remain true and how both will be checked. For a bug, reproduce it safely and preserve the failing observation. If reproduction is unavailable, label the diagnosis provisional and do not claim a verified fix.
3. Identify the causal defect and inspect its plausible blast radius. Check sibling occurrences and callers without turning a bounded fix into unrelated cleanup.
4. Make the smallest complete in-scope change that meets the contract. Follow existing conventions. Do not add stubs or placeholders unless the user asked for a scaffold. Use deterministic tools for repetitive transforms where appropriate and authorized.
5. Run the relevant checks through actual tools. For code, distinguish tests, lint, type checks, build and a behavior smoke test. For UI, inspect rendered states and interactions in supported browser tools; a build does not prove layout or usability. Record commands, artifact/version, status and meaningful output. A blocked test remains blocked.
6. Review the diff or artifact against the contract, acceptance evidence and adjacent behavior. Deliver what changed, what passed, what failed or was not run, and any remaining risk. Apply LEARN only if capture is authorized and useful.

```text
Use Fable BUILD within the existing domain workflow. Read the real artifacts and conventions first. Reproduce a reported bug before claiming its cause. Make the smallest complete authorized change, check affected callers and run the relevant tests or artifact checks. Report observed evidence and blockers. Do not turn a review request into an edit or an in-scope change into unrelated cleanup.
```

## REVIEW

Require the contract, criteria, artifact/version and available evidence. If an essential input is missing, identify it. You can still provide a bounded provisional review of what is present; do not certify unseen work.

1. Inspect proof before accepting the completion claim. Separate observed results from promised checks, assertions and synthetic fixtures.
2. Apply every criterion. Record pass, fail or unverified and an exact evidence location. Use actual checks when authorized; otherwise state that the review is static.
3. Challenge the weakest consequential claim with a discriminating case. Focus on the assumption whose failure would change the outcome. Do not manufacture a defect if the evidence supports a clean result.
4. Check scope, permissions, output completeness and regressions, not only local correctness. A polished answer to a different question fails the contract.
5. Give an accepted, changes-required or blocked verdict under the recorded criteria. Any critical failure vetoes acceptance. Use numerical scores only when the user supplied or approved a meaningful rubric; never impose a magic 8/10 gate.
6. For each failure, name the smallest repair and retest. If editing is authorized, repair within the existing task bounds and retain the original finding. If further work needs a new decision, authority or unavailable evidence, report it. Do not silently lower the criteria after an unsuccessful repair.

```text
Review the supplied artifact against its contract. Start with the evidence. Mark each criterion pass, fail or unverified, citing where you checked it. Test the weakest consequential claim and check for scope drift. Give a supported verdict and specific repairs. A clean review may have zero findings. Do not invent defects or numeric quality thresholds.
```

Same-context review is a useful check but must not be advertised as independent review. A fresh reviewer should receive the contract and artifact rather than a persuasive builder narrative. If no independent reviewer exists, state the assurance limit.

## LEARN

Learning is authorized reuse of outcomes, not capture of private reasoning and not a new permission to write persistent memory.

1. Find the existing capture owner and its authorized locations. Defer to that mechanism. Do not establish a second competing notes system.
2. Before related work, retrieve only the few lessons that match the subsystem, problem class or tool. Check their source, scope and age before applying them.
3. After a non-trivial correction, failed first approach or reusable success, decide whether a lesson is worth saving. Routine edits need no record.
4. If permitted, record a standalone claim, the observed context/result, a next-time procedure, a checkable rule, source links and limits. Update or link related records to avoid duplicates. Correct obsolete guidance through the authorized owner; do not delete unrelated material.
5. If capture is unavailable or not authorized, return a proposed lesson in the deliverable only when useful. The completed domain task remains complete.

```text
Use the existing authorized learning mechanism. Retrieve relevant precedent, then save only a reusable observed outcome or correction with its source, scope and next-time check. Do not store private reasoning, credentials or unrelated personal detail. Avoid duplicate notes. If no capture mechanism is authorized, provide a useful lesson for review without changing persistent state.
```

A suitable lesson has this shape:

```text
Claim: A parseable response can still be incomplete.
Observed context: A synthetic 50-item fixture returned valid JSON with 20 items and a truncation stop status.
Next time: Check expected item coverage and terminal status separately from JSON parsing.
Reusable check: Acceptance requires every requested ID accounted for and no unresolved truncation.
Evidence: Link the fixture and observed result when they exist.
Limit: This checks delivery completeness; it says nothing about the items' factual accuracy.
```

## Finish the requested mode

Deliver the actual domain result, not a recital of phases. Include only the process evidence that helps the user judge it. A proposed test is not a performed test; a mode label is not a quality guarantee. For complete synthetic applications, see [examples](../references/examples.md).
