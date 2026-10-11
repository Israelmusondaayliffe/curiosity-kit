# Strategy

## Unit and bar

Inspect distinct options, load-bearing assumptions, the recommendation, and risks or reversibility. Options must be genuine alternatives, with costs and foreclosed choices, rather than a favorite surrounded by straw men.

Freeze a concrete decision rubric and any reference memo before work starts. Include evidence-to-choice reasoning, assumptions with justified confidence, observable falsifiers, consequences, reversible steps, and conditions for abandoning the recommendation. Thresholds belong to the approved decision context. Do not invent a default score or rewrite the rubric to fit the result.

## Inspection recipe

A fresh adversary reads only the memo and tries to overturn its recommendation using its own evidence. Save each objection, the affected assumption or criterion, and whether the memo answers it. Unanswered material objections become named gaps, not rhetorical disagreements to dismiss.

An independent reader answers the frozen questions: What is the decision? What is the strongest counterargument? What would change the decision? Require locations in the memo and record every guess. Validate the saved reader record with `python3 scripts/inspection.py reader --input payload.json`. Factual premises also require `python3 scripts/inspection.py claims --input payload.json` and semantic source review.

## Worked rubric and integrity

For build versus buy, compare implementation and operating costs, dependency risk, exit options, and assumptions about demand. Ask which observation would reverse the choice and who will notice it. For a pricing decision, attack the assumptions most responsible for the projected result; uniformly high confidence is not evidence.

Blindness is usually weak because unrelated decisions are not fair comparators. Record that limitation and use the frozen rubric plus adversarial review. A genuine prior memo on the same decision can supplement this check. Separate known facts from judgment. A changed rubric requires stopping for renewed approval; a detected hash mismatch cannot be passed over. Use research to establish facts and prose or deck to improve presentation.
