# Diagnose before adding instructions

Find the cause of a concrete prompt failure and make the smallest supported repair within the request. Keep the failing case and source prompt so the change can be tested and reversed. A plausible explanation without a matching observation is a hypothesis.

## Capture the failure

Read the full prompt and actual target/interface/configuration. Obtain a failing input, returned visible output, stop/error status and available authorized tool or client evidence. Record the desired outcome and what specifically differed. Use supplied traces rather than asking for hidden reasoning or private host logs. If no failed example is available, provide a provisional diagnosis and a small test that would distinguish causes; do not claim reproduction.

## Locate the cause

Separate these classes before rewriting:

| Observation | Evidence to inspect | First useful distinction |
|---|---|---|
| Too brief, too long, dense or wrongly formatted | Prompt output contract and actual final artifact | Missing requirements versus excessive brevity/voice instruction |
| Extra features, approvals or actions | User scope, stable authority and tool effects | Prompt ambiguity versus unpermitted expansion |
| Silence during tools | Actual response blocks, request display/streaming settings and renderer | Hidden progress versus absent model updates |
| Tool call written as text | Structured response items and dispatch | Plain text is not an executed call |
| 400 or rejected request | Native request and exact current endpoint docs | Unsupported configuration before behavioral tuning |
| Early stop, empty answer or partial batch | Stop reason, token budget, active work and item coverage | Truncation or unfinished job versus task completion |
| Correct program output, wrong final answer | Intermediate schema and final delivered content | Missing coverage/evidence in the handoff versus faulty reduction |
| Bad facts or citations | Retrieved sources, freshness and quotation boundaries | Retrieval/source failure versus prompt grounding |
| Context loss or stale assumptions | Actual history/compaction and state contract | Host state damage versus unclear retained requirements |
| High cost or slow response | Observed usage, cache writes/reads, attempts and timed region | Effort, retries, queue/tool overhead or genuine task difficulty |
| Refusal | Visible refusal category, task intent, provider constraints and any prompt instruction that itself triggers a category | Correct safety response versus unsupported framing or unavailable access |

Use the relevant [pattern](../references/prompt-patterns.md) and [dated profile](../references/provider-guide.md) after classifying the issue. Do not copy one provider's progress, effort or history workaround to another interface. A prompt cannot repair an absent tool or a parser that discards content blocks.

## Test a causal change

Choose one change group supported by evidence. Repair configuration or client behavior where it is causal; remove contradictions or redundant compensation where causal; otherwise add one task-specific instruction or example. There is no universal order requiring effort before prompt edits or three prompt blocks before effort.

State the hypothesis and matched test before observing the revised output. Hold relevant cases, parser, tools and scoring constant. Preserve the original failure and label whether the repair changed prompt, configuration, runner or scorer. If a scorer was wrong, fix it under the same criteria and rescore both sides; do not bend the criteria to pass the candidate.

When several revisions fail the same way, revisit the premise. Group failures by case family, language, run order, model/configuration, tool state or missing inputs. A candidate always run cold or without one tool is a confounded comparison. An even failure distribution can disconfirm an imbalance theory. Do not treat correlation as proof or remove real deployment constraints to make a table look balanced.

For refusal or permission failures, preserve the actual boundary. Clarify a legitimate intent when ambiguity is causal. Do not disguise prohibited work, extract hidden reasoning, repeat an identical refused request indefinitely or switch models without the user's choice. [Fallback](fallback.md) applies only to an explicitly selected permitted pair and its authorized triggers.

## Return the repair and its limits

Provide the failing input/symptom, diagnosis and confidence, exact scoped change, expected effect, actual test evidence or unrun status, rollback and remaining issues. If only diagnosis was requested, report the proposed change without applying it. For a changed prompt, include the complete revised artifact, not a fragment that loses its original requirements. For a comparison, use [benchmark](benchmark.md) and [normalize](normalize.md); a lint pass alone is not confirmation that the symptom is fixed.
