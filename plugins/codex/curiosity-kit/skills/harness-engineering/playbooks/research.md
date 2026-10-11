# Research before design

Resolve the uncertainties that could change a harness or skill design. Start after a scoped [audit](audit.md), before the substantive [interview](interview.md) and build decisions. If the target or permission is unknown, ask that narrow question first. Research does not authorize installation, account access or source mutation.

## Establish the questions

Read the user's actual outcome, existing instructions, approved scope, available capabilities and audit findings. List only design-changing unknowns: host support, resource format, current invocation policy, existing ownership, tool reliability, data access, failure modes, relevant source methods or licensing. Reuse verified facts that remain applicable. Do not launch broad research because an otherwise complete profile has an empty field.

Separate three kinds of evidence:
- User decisions and observed workflow define the desired behavior and authority.
- Actual source methods and current files establish what exists and how components work.
- Official host/tool documentation and real observations establish supported mechanisms. A donor's successful example does not prove this environment supports it.

For each consequential question, define what would settle it. For example, whether a skill can be model-invoked needs both the documented metadata contract and later observation of the actual catalog; a README alone cannot settle installed visibility.

## Read and trace

1. Inspect the corresponding existing skill/plugin entry and the supporting method it calls. Follow references, assets, scripts and actual dependencies for the behavior being changed. For a rebuild, account for the complete source family, including rare recovery paths and host variants.
2. Record repository or document identity, revision/date, exact path and read scope. A search result or tree listing is discovery, not a body read. Mark inaccessible or unread resources explicitly.
3. Read relevant benchmark methods as capability sources. Extract a useful mechanism, its prerequisites and limitations. Compare it with the user's requirements before adopting it. Do not import a donor's provider, bootstrap, shell command, standing schedule or authority merely because the source uses one.
4. Check current official documentation when a design depends on changing host/model facts. Keep dated facts dated. Inspect actual supported tools before promising their execution. Research exact claims; avoid unrelated release surveys.
5. Trace side effects in code before proposing execution. An audit-named or dry-run command may write state, start a service or call a provider. Reading source is not permission to execute unfamiliar software.
6. Where uncertainty is architectural, make the smallest safe disposable example that can answer it within authority. Separate source inspection, a synthetic prototype, actual helper behavior and native model execution. Never substitute invented receipts for an unavailable experiment.

## Reconcile into the interview

For each finding, record its source, applicability, confidence and decision consequence. Distinguish a proven defect from a hypothesis. Prefer the simplest adequate mechanism already in the project; preserve working interfaces and callers. A newer model or attractive donor pattern is a reason to investigate, not proof that safeguards can be removed.

Bring the user only the choices that remain theirs: outcomes, priorities, acceptable tradeoffs, risk, data scope and qualitative standards. Offer a recommendation grounded in the findings. Do not ask them to choose between implementation details the evidence already settles.

Example: the existing skill drafts workshop notes accurately but cannot inspect a required workbook. The research outcome is a declared workbook-reading prerequisite and a narrow question about whether workbook handling is essential, rather than pretending CSV-only output preserves it or installing a parser without authority.

## Finish

Return the resolved design questions, actual sources, remaining access limits and the questions for [interview](interview.md). A short task can carry this inline. A major rebuild needs a durable component/method map and implementation evidence plan, but not one separate essay per source. The phase is complete when the next design/interview decision is grounded and the unresolved essentials are explicit. If a required source is inaccessible, continue independent work and stop the dependent claim.
