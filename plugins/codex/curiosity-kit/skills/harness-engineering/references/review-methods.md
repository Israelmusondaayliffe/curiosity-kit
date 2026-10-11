# Grading, comparison and diagnosis

Use the job that answers the actual question. A structural result, artifact judgment, independent comparison and diagnosis are different evidence. Preserve their identities and limits rather than blending them into one quality score.

## Evidence grading

Read the frozen request, sources, expected output, criterion definitions and the actual delivered artifacts. Inspect relevant permitted tool traces when the criterion concerns actions rather than text. Do not accept a filename, a self-issued PASS or a nonempty evidence string as proof.

For each criterion:
1. State what observable fact would satisfy it.
2. Locate the actual supporting or contradicting bytes, rendered feature or captured action.
3. Check whether the evidence refers to the final candidate, inputs and suite.
4. Return pass, fail, blocked, invalid or unobserved according to the contract, with a precise reason and evidence pointer.
5. Preserve executor caveats, assistance, unavailable metrics and unexpected side effects.

Inspect implicit claims too: a count in a caption, a promised investigation in customer copy, an assertion that a script ran, or a final reply's requested sentence count. Correct source facts must survive every supporting note and evidence record, not only the main artifact. A well-formed statement can still be false.

Critique the eval itself separately. Is an assertion trivially satisfied, implementation-coupled, ambiguous, dependent on hidden restrictions, or unable to detect a plausible defect? A weak criterion is a finding about the suite; do not quietly change it while grading the candidate. Version substantive changes and obtain fresh matched evidence where required.

A deterministic check should have a known bad control and a normal control. A judgment-heavy criterion needs an anchored rubric and an inspected artifact. When required judgment is unavailable, report needs-review rather than manufacturing a number.

## Blind artifact comparison

Before showing outputs, freeze the task-derived rubric and what information the reviewer may see. Randomly assign neutral labels and keep the variant-to-label key outside the reviewer's input. Remove identity clues from paths and headings where doing so does not change the work being judged; disclose any unavoidable clues. Do not give the reviewer the author's preferences or earlier grades.

Give both outputs the same relevant task/source context and comparable presentation. Ask the reviewer to assess each criterion before choosing A, B, tie or inconclusive. Require evidence from the artifacts, not guesses about the producing model. When both fail an essential criterion, neither qualifies even if one looks better.

If a reviewer can see variant identities or shares the author's context, label the review accordingly. A claim of blindness in the prompt does not create independent context. Automated identity checks cannot prove that a human or model was uninformed.

Preserve the review and only then reveal the key for diagnosis. One comparison can establish a scoped preference or defect; it does not establish a general success rate or statistical superiority. A no-skill baseline has no skill source to inspect. A tie has no loser to explain away.

## Post-hoc diagnosis

Use after grades and identities are fixed. Read the variants' actual instructions, artifacts and allowed traces. Classify the cause:
- The intended method never triggered or adapter metadata hid it.
- The right entry loaded but a required resource did not.
- The method was ambiguous, incomplete or contradicted by another rule.
- A correct instruction was ignored in this instance.
- A helper, environment, source or evaluator failed.
- The suite measured the wrong thing or imposed a rule absent from the request.

Separate observation from causal hypothesis. Quote or point to the relevant evidence and propose the smallest change that could test the hypothesis. Compare against existing instructions and checks before adding a duplicate reminder. A tooling failure usually needs a tool repair; a missing source does not become a model-quality defect.

Preserve the original failing output. A reviewed correction is assisted evidence; it never retroactively turns the native primary green. Recheck changed behavior and relevant regressions rather than repeating every sound case. If a new finding changes the acceptance contract, record the change explicitly.

## Descriptive benchmark analysis

This mode reports what the recorded runs show without recommending speculative source edits or inventing causes. Use explicit candidate/baseline roles and match case definition, inputs, suite, adapter, model/settings and relevant permissions. Mark incompatible rows separately.

Report per-case transitions and the selected, comparable, valid and scored denominators. Keep errors, invalids, interrupts, missing observations and deferred coverage visible. Removed required cases are unresolved coverage, not unchanged success. Do not average away an essential failure.

Use actual repetition counts. Preserve cost, elapsed time, tokens, characters and tool calls as distinct measurements with units and origin. Unknown values are not zeros. Show latency or cost deltas only when the same scope was measured on both sides. Fewer Markdown files or descriptions is not a measured context saving.

When repeated noisy observations matter, freeze the number and stopping rule before collecting them. Do not sample until a preferred variant wins. A used holdout becomes development/validation evidence. Record uncertainty and a no-decision result when the evidence cannot support selection.

## Human feedback and approval

Human comments can identify a defect or preferred outcome. Record the exact artifact/revision reviewed, the decision and its actual source. A blank comment, a visited page, exported JSON or a model's approval field is not authentic user consent. The [review interface](review-interface.md) checks identity and declared feedback consistency; the host conversation supplies authority.

Distinguish acceptance of an artifact from permission to apply, install, publish, send or expand access. A requested review may finish with findings only. Carry approved decisions forward within their scope, but stop if source bytes, candidate payload or consequential terms change.

## Useful controlled example

The source says 13 kits are reserved and attendance is unknown. Artifact A says 13 people attended; artifact B retains the reservation count and uncertainty. Both may pass JSON structure checks. The factual criterion fails A and passes B based on the supplied source, not on style or filename. If B's evidence note promises an unrequested follow-up email, that note still fails the authority/fidelity check. Review the complete delivered set.
