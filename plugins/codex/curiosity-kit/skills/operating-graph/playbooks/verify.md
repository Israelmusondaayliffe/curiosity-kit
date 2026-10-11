# Verify the original outcome

## Decide whether to inspect or finalize

Use the selected run and immutable original goal. Read-only inspection may review existing evidence. The v2 `verify` operation is read-only; `finalize` commits the terminal result. This replaces the original verifier's combined judgment/audit-write/closure behavior. Use the requested operation from [CLI](../references/cli.md) and obtain the needed mutation authority before finalizing. Never repair evidence, change topology or relax criteria during judgment.

Read [runtime-protocol.md](../references/runtime-protocol.md) for exact record bindings and [host-contract.md](../references/host-contract.md) when real worker or approval provenance matters.

## Judge each necessary claim

1. Establish trusted context: original/current graph, every applied version, committed history, replayed projections, relevant receipt hashes and lifecycle. Stop on corruption or conversion-needed. An internally consistent event chain does not excuse a divergent snapshot.
2. Enumerate every original completion criterion and required deliverable. For each criterion identify its exact current output, actual evidence and independent judgment. A structurally valid graph, empty generic issue list or worker's `met` value cannot satisfy a semantic requirement.
3. Open and inspect the actual deliverables. Recompute recorded digests and check producer, invocation/epoch, declared output type, source/input lineage, active eligibility and provenance. Failed, provisional, stale, invalidated, superseded or wrong-producer artifacts cannot qualify merely because a file exists.
4. Check evaluator independence and binding. The reviewer must have evaluated these exact deliverable bytes against the relevant original criteria, with enough raw input to judge them. Separate produced output from independent check. A role name or different node ID alone does not prove an actual fresh independent reviewer where that is required.
5. For executed workers, reconcile task, dispatch intent, launch request/response, actual identity when observed, complete return, input/output hashes, criterion evidence and terminal accounting across every attempt. Retain failed attempts. Imported/mock receipts prove only their declared protocol properties; they do not establish native host execution.
6. Recheck effective action approvals, scope/content binding, revocations and prohibited mutations. A terminal verifier cannot retroactively make an unauthorized action permissible. Any uncertain external outcome remains explicitly uncertain; never infer “did not happen” from timeout.
7. Confirm all required critical work is resolved and integrated. Optional inactive and fully accounted work may be explicitly omitted under the frozen contract. Optional live or uncertain workers still need accounting; a cancellation request is not observed termination. No clean completion while children, reservations or partially committed operations remain unaccounted.
8. Inspect the integrated result against the user's intended job. Distinct branches may each pass while their combination conflicts or omits an input. Check the source facts, ownership, final audience/output requirements and the original success condition together.

## Verdict and failure contract

Use the actual runtime verdict vocabulary from the CLI contract. V2 returns pass or fail, with explicitly omitted optional work recorded as limitations rather than the original conditional-pass status. Preserve the distinction between those limitations, terminal lifecycle, cancelled/unknown outcomes and domain acceptance. Optional omissions cannot hide a missing essential check. If an essential criterion is unrun or cannot be established, qualification is blocked unless the user explicitly changes scope.

Give criterion-specific reasons and evidence, including precise unavailable data/host observations. Do not average away a failed requirement with successful checks elsewhere. Advice is separate from a required defect. If repair is authorized, hand the concrete cause and affected recheck to the appropriate run/rewrite method; verification itself must not rewrite the answer to get a pass.

## Return

Return the final artifact references and exact digests, criterion-level results, actual verification/finalization outcome, preserved failures, optional limitations and unaccounted obligations. State the evidence tier actually established: structural, deterministic sample, simulated adapter, observed cloud worker or qualified target host. Only the designated user/project acceptance owner decides acceptance; the graph's machine report is not that owner's consent.
