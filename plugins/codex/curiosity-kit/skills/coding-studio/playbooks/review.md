# Review the actual candidate

Use this method for code, a plan, an implementation document, or an integrated change. Start with the requested result and the exact material to review. A review request authorizes findings. Applying findings, changing a remote document, posting comments, committing, and publishing are separate actions.

Read [the host contract](../references/host-contract.md) before relying on a tool, child, provider, or remote operation. One owner resolves scope and integrates findings. A small review can stay in one context. Add independent readers for a concrete risk or an explicit request, without creating a standing reviewer fleet.

## 1. Fix scope before judging

Record enough to identify the candidate again:

- The repository or document identity and the user's selected target.
- Candidate kind: selected index, working tree, commit, remote PR head, document revision, or built artifact. Staged and working-tree bytes may differ.
- For a diff, the actual comparison base and resolved base/head commits. For a PR, include forge host, base repository, PR identity, head repository and ref. Use its real target branch. Do not assume `main`, `origin`, or a same-named local branch.
- Included files, exclusions, relevant untracked inputs, and the approved behavior or selected plan. Record uncertain intent as uncertain.
- Material context outside the diff, including callers, configuration, generated inputs, runtime consumers, and applicable project standards.

Inspect the real diff before sizing the review. A title such as "docs only", a bot author, or a list of filenames cannot establish low risk. Instruction files, workflow files, manifests, and configuration can change runtime behavior. Binary or unreadable changes are unknown coverage, even when their extension resembles source code.

Review remote files at the reviewed head, including unchanged context and standards. A local checkout at a different revision cannot supply that evidence. Use the available exact-ref read or a safely prepared matching checkout; review-only does not silently switch branches. If only hunks are available, review those and name what remains unassessed.

Keep the inputs stable while a review runs. If a writer must continue, identify the snapshot each reader receives and reject stale conclusions about later changes. A source fingerprint alone does not prove which bytes a reviewer actually read. For sanitized or prepared copies, retain original identity, supplied-copy identity, excluded material, and relevant transformations separately.

## 2. Keep two acceptance axes

Assess both, even on the smallest path:

1. Engineering quality. Does the change work correctly and fit the project's standards, security boundaries, maintainability needs, and supported callers?
2. Requested outcome. Does it implement the accepted behavior, requirements, and constraints? What promised behavior lacks proof? What new user-visible rule has appeared without an accepted decision?

A standards-compliant implementation can miss the request. A feature that meets the request can still introduce a serious defect. State the results separately. When no accepted plan exists, use the current request and mark inferred intent. A discovered plan or PR-body link is context; it does not grant scope or establish that the user approved every linked requirement.

Reuse existing requirement and unit identifiers. Check both the promised behavior and any claimed implementation-unit completion. Do not invent missing unit obligations for a product-only brief. Preserve settled decisions as constraints. An independent reader may challenge their technical consequences, but a repair that reverses an accepted decision needs that decision reopened explicitly.

## 3. Size depth by consequences

Choose after inspecting the diff and context:

- Local and loud: a bounded review in the owner context may suffice when a mistake fails visibly at the edited site and there is no material hidden consumer or consequential boundary.
- Silent or uncertain: add a fresh independent read of the likely failure mechanism. Examples include retry behavior, stale state, background work, CI guards, implicit ordering, or a shared function whose failure appears elsewhere.
- Consequential or broad: use the necessary deeper checks for authorization, sensitive data, money, persistence, concurrency, public contracts, migrations, or wide integration. Explicit "full" or "thorough" requests set a depth floor. Missing scope or standards evidence prevents claiming full coverage.

Depth means the work performed. It does not prescribe a model, number of agents, report length, or provider. A broad task may need several focused readers, while a small consequential change may need one expert independent read and a strong reproduction. When independent review is required but unavailable, complete the owner review and report the missing independent result. Do not rename a self-review as independent acceptance.

## 4. Trace beyond the changed lines

Read each material change with its owning function, invariants, entry points, callers, and tests. Prefer supported symbol-reference tools, then structural search, then text search. Inspect aliases, re-exports, generated bindings, string-based routing, dependency injection, wire formats, saved records, jobs, and independently deployed consumers when relevant.

An empty search result does not prove absence of callers. Say "no callers found in the inspected scope" and name a material completeness limit. A wrong-checkout search is invalid evidence. Keep an existing issue separate only when evidence shows it predates the candidate and the candidate does not introduce or worsen its interaction. An unchanged test path does not make its failure pre-existing.

Select the checks that can change the decision:

- Correctness: concrete normal, boundary, error, denied, interrupted, and repeated paths. Trace values and effects through the actual call chain.
- Tests: whether the expected result comes from accepted behavior, whether tests distinguish a wrong implementation, and whether shared or alternative callers remain covered. Check that weakened assertions or deleted tests did not erase an obligation.
- Standards and maintainability: read the project's actual rules. Prefer existing abstractions and simple direct code. Flag duplication or indirection only when it imposes a concrete cost. Do not turn taste into a blocking defect.
- Security and data: validate trust boundaries, authorization before effects, secret handling, reachable evaluation or deserialization, network destinations, and sensitive-data exposure.
- State and reliability: verify transaction boundaries, races, partial failure, retries, idempotency, cache invalidation, ordering, timeouts, and recovery. A lock keyword or an accepted HTTP response is not behavioral proof.
- Contracts and release: check backward compatibility for retained data and running consumers, observable errors, rollout order, and whether the stated recovery actually restores the affected state.
- UI and accessibility: inspect the affected journey and acceptance evidence. Static code review alone cannot certify rendered layout, keyboard interaction, or native behavior. Use [verification](verify.md) for those claims.

## 5. Obtain genuine independent evidence when needed

Give each reader the target identity, comparison base, accepted behavior, relevant standards, bounded read scope, and the question it owns. Exclude other readers' conclusions until their first independent result is complete. Do not conceal a necessary requirement merely to make the reader "blind". Readers return findings, coverage, missing evidence, and terminal status; they do not apply changes or contact external parties.

Use an actually available child or review capability. Record its real invocation or task identity and terminal result. A role name, launch acknowledgment, generated receipt, or output schema is not proof that a separate review completed. Keep distinct:

- Requested reviewer or route and any strict selection constraint.
- Observed execution identity, input identity and supported isolation.
- Actual model or provider identity when available, otherwise unknown.
- Completed coverage, failures, findings and remaining uncertainty.

Same-host independent review can satisfy an ordinary independent-read request. A specifically required model or provider cannot silently fall back. External model CLIs are optional integrations, never package prerequisites. Before using one, verify current availability, the recipient and content authorization, actual endpoint/configuration, permitted reads and egress, bounded execution, output limits, and owned cleanup. Tool branding does not attest to the served model or endpoint. If isolated scratch creation fails, do not widen the reader's workspace. Do not substitute a recipient after failure without authority covering that recipient.

Collect every started reader's terminal outcome. Preserve failed or incomplete coverage. Validate a returned finding's fields and cited source before treating it as evidence. An empty valid completed result means no findings within that reader's coverage. An absent, malformed, cancelled, or failed result does not.

## 6. Validate and integrate findings

For each candidate finding, establish:

1. The exact location at the reviewed revision, with a short source quotation or other inspectable evidence.
2. The triggering condition and concrete consequence. Distinguish a demonstrated defect from a plausible risk needing a test.
3. Its relationship to the diff, including changed behavior that breaks unchanged callers.
4. Any independent observation or test, and the limit if the condition cannot be reproduced.
5. A proposed remedy and whether it changes accepted behavior, needs a decision, or is a bounded mechanical correction.

Reject findings contradicted by the actual source or supported behavior. Merge duplicates only when they share the same cause and remedy. Preserve case-sensitive paths and all covered evidence references. Group related findings for reading, but do not treat a thematic group as an authorized apply queue.

Severity describes consequence, not permission:

- Critical: exploitable exposure, corruption, data loss, or broad breakage.
- High: likely failure of a significant supported behavior or contract.
- Moderate: a meaningful edge-case defect or demonstrated maintenance/reliability cost.
- Low: a narrow improvement or nonblocking concern.

Keep confidence, severity, remedy class, owner, and action authority separate. A very certain defect can still require a product decision. A severe issue does not itself authorize an edit, release, or external message. Retain substantive dissent and state what evidence would resolve it. If an urgent preliminary finding is later disproved, withdraw that specific finding explicitly.

Keep defects, optional advice, missing coverage and completion separate in the report. For shared-code extraction advice, establish two real authored callers, compatible contracts, an existing-helper search, migration/test cost and a net reduction in maintenance work. Similar spelling, generated copies or a shorter line count alone do not justify extraction. Preserve it as advice unless there is a concrete defect or accepted requirement.

## 7. Apply only an authorized bounded repair

Report-only ends with findings. If local application is authorized, choose one bounded repair batch whose sites, intended behavior, and proof are clear. Recheck that the candidate and evidence still match. Preserve unrelated content and index state. Apply the smallest correction at the owning layer; do not append repeated special-case prose or broad cleanup unrelated to the defect.

After repair, run the affected checks against the actual new candidate and review its diff again. Revisit affected callers and both acceptance axes. Old passes do not cover new edits. A repair that reveals a different cause, reverses a decision, expands scope, or fails its discriminating test returns to diagnosis or a user decision. Do not iterate indefinitely to force a clean review. Additional passes need a clear new hypothesis and the existing task's authority.

Return local-uncommitted as a valid outcome when that is the approved scope. Use [delivery](deliver.md) only for separately authorized commit, publication, feedback, or release work.

## Document and plan review

Use the same two axes and evidence discipline on a document's current revision. First identify its purpose, audience, authority, and readiness question. Review the actual native structure and linked sources. Check unresolved decisions, contradictory requirements, missing failure/recovery cases, testability, and implementation dependencies. Separate substantive defects from editorial polish. A source citation proves only the claim it supports.

For proposed edits, preserve the native format and existing structure unless the request changes them. Mechanical wording repair still requires edit authority. Changes to commitments, product choices, approval rules, or scope need the corresponding decision. If remote commenting or editing is requested, bind the exact document and revision, preview the narrow operation, and reread after applying it. Do not publish a document or create provider credentials as part of a generic review.

## Return a useful review

Lead with the consequential findings or the scoped clean result. Include:

- Candidate and base identity, reviewed scope and exclusions.
- Separate engineering-quality and requested-outcome conclusions.
- Findings with evidence, consequence, confidence, remedy and owner.
- What actually ran, independent coverage, failed readers and untested boundaries.
- Applied changes and fresh retests, if authorized.
- Remaining decisions or release conditions.

Use "no findings in the inspected scope" when warranted. Do not turn partial coverage into "safe", a transport success into "reviewed", or a clean review into merge/deploy authorization. A concise result is enough when the work is small; keep larger evidence in the existing task artifact rather than create another review database.
