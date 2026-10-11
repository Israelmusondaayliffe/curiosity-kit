# Design a long-running task

Use this method when the requested task must continue across many tool calls, asynchronous jobs or context transitions. Design a task-level contract that the actual host can carry out. Writing a persistence instruction does not create background execution, a scheduler, a memory store or a delivery channel.

MPL owns the proposed prompt and task contract. Persistent instruction-chain changes, tool installation, global memory policy, configuration application and guarded rollback belong to Harness Engineering. Domain work remains with its existing owner. Do not apply those changes merely because this design would benefit from them.

## Establish the execution envelope

Read the user's goal, existing specification, authority and stopping condition. Infer settled details from supplied context. Ask only for a missing decision that changes the contract or permission. Record:

- The outcome, artifact locations, acceptance checks and exclusions.
- Supervised or unattended operation, and how interruptions arrive.
- Actual read, write, execution, job-status, wait, cancellation, review and delivery tools. Record their real names and return shapes in the delivered contract. An unavailable tool stays unavailable.
- Duration, spending and resource limits. Include retry and verification costs. If a necessary bound is unknown, prepare the design and mark execution blocked at that step.
- The evidence the host exposes: output files, receipts, exit statuses, screenshots or job records. Do not require hidden reasoning or private transcript directories.
- Existing memory ownership and any writable location already authorized for this task.

Test prerequisites using harmless checks where authorized. Check that the specification can be read, output can be persisted and retrieved, a started job can be observed, and the user can see the intended communication channel. Tool availability alone does not prove the renderer displays its output. Keep provider-specific state, output budgets and timeout support in the relevant branch of [provider guide](../references/provider-guide.md).

## Build all five pillars

### 1. Truthful progress

Give each acceptance item a status: not started, active, blocked, failed or verified. Associate status changes with an addressable result. For written analysis, a saved artifact and cited source can be evidence; a tool call is not the only possible proof. Prior-run evidence keeps its origin and freshness limitation.

Use this instruction near progress reporting:

```text
Report completed work only when you can identify its artifact or observed result. Distinguish produced, checked and accepted. State failed checks and skipped steps. A plan, dispatched job or tool acknowledgement is not a completed result. Use earlier evidence only with its provenance intact.
```

Before saying a percentage or count, derive its numerator and denominator from the item ledger. If scope is still being discovered, give the known count and say the total is not established. Never use elapsed time as evidence of progress.

### 2. Interval verification

Store the specification in an addressable artifact. Choose checks at meaningful boundaries, such as each completed module, source batch or approved decision. Do not impose a universal wall-clock interval. Choose checks before building so they cannot silently weaken after failures.

When an independent reviewer is available and authorized, supply the specification, artifact version and allowed evidence. Do not supply the builder's persuasive account of why it should pass. Request per-criterion pass, fail or unverified results with evidence locations. A reviewer may report no findings. Fresh context is a review method, not a claim of statistical independence.

```text
At each declared milestone, check the artifact against the recorded acceptance criteria. Give an available independent reviewer the specification and artifact, without the builder's narrative. Resolve consequential failures before dependent work. Keep the failed result and the retest result. Do not replace a required check with a claim that the model normally self-verifies.
```

If no reviewer exists, use independent deterministic checks, fixtures, source comparisons or a separately performed manual review when available. Label same-context self-review accurately. If independent review is a hard acceptance condition, complete feasible preparation but report that condition blocked. If it is optional, deliver with the reduced assurance stated. Do not invent a reviewer or require approval for every harmless omitted capability.

### 3. Active work and turn endings

Maintain two linked records: acceptance items and started work. A job record needs its host/job identifier, owner, dependency, output location, last observed status, remaining action and applicable cancellation rule. Keep queued, running and terminal states distinct. A tool returning an identifier means the job started, not that it succeeded.

```text
Continue authorized work while it can advance the acceptance criteria. Before ending, inspect all acceptance items and every started job. Collect and check terminal outputs; wait through the real host mechanism for running work. Do not report completion while a required job or review remains active. If input, permission or an external prerequisite blocks progress, state the exact blocker and preserve a resumable checkpoint.
```

For supervised work, respond to user interventions promptly, reconcile the new request against in-flight work, and stop or redirect only through supported controls. For unattended work, do not replace a required confirmation with an assumption because no one is watching. Stop the dependent action and preserve state. Continue unrelated authorized work if it remains useful.

Use dependency-aware parallelism. Assign disjoint artifact ownership, provide each worker its inputs and return contract, and reserve integration ownership. Reuse a context-bearing worker for its workstream when useful; keep verification fresh. Intervene when evidence shows drift, missing context or overlapping edits. More agents are not inherently faster or more reliable. End an ensemble once the declared comparison or synthesis outcome is established; creating another candidate is a new bounded step, not an endless search for agreement.

Recover an accidental early stop by listing the actual open items and resuming the next authorized action. A generic continuation message must not replay a side effect with an uncertain outcome. Retry only after checking the previous attempt, the failure category, idempotency and remaining budget. Define the retry bound per operation, together with a terminal failure state. Do not add an infinite persistence loop.

### 4. Authorized durable memory

Separate task checkpoints from reusable learning. A checkpoint records current requirements, completed artifacts, open jobs and next actions. A lesson records a reusable correction or method with its evidence. Neither contains hidden reasoning, credentials or unnecessary personal data.

```text
Use the existing authorized capture mechanism. Retrieve relevant precedent before a repeated problem. Save only reusable outcomes, corrections and next-time procedures, with source and scope. Update an existing record where appropriate rather than adding a duplicate. If no memory write is authorized, include a resumable task summary in the deliverable and continue without persistent learning.
```

Name the concrete store and its owner. Do not bootstrap from unrelated history, create global memory policy or delete records without authority. Correct or supersede a mistaken note through the existing mechanism and its permissions. A missing memory store does not invalidate an otherwise completed one-off task.

### 5. Final and mid-run delivery

These are different requirements. A final report must make sense to someone who saw none of the work. Mid-run delivery requires a real tool or visible host channel and a clear instruction to use it. A fictional tool definition in a prompt does not make that tool callable.

```text
Use the verified user-delivery channel for a ready partial deliverable, a direct answer received during work, or a decision the user must make. Send the actual content or an accessible artifact link. Keep internal reasoning and routine tool narration out of it. At the end, lead with the outcome, then give the evidence, remaining limitations and any decision needed in ordinary language.
```

If no mid-run delivery exists, persist partial artifacts where allowed and return them at the next supported response boundary. Do not promise immediate notification. If timely delivery is essential, mark that part of the design blocked and identify the missing host capability. Never claim raw tool output is user-visible without checking.

## Context and interference controls

Before compaction or a context transfer, save the current contract version, authority limits, artifact identities, verified versus unverified work, open job identifiers, unresolved decisions and next executable action. Preserve source locations rather than replacing exact evidence with a loose summary. On resume, read that record, check artifact versions and job status, and resolve changes before restarting work.

Opaque provider state is not editable prose. Preserve or transfer it only through the supported interface and documented direction. If compatibility is unknown, use an allowed visible-state handoff and disclose lost continuity. Do not request hidden reasoning as a substitute. Keep stable instructions separate from volatile progress where the host supports caching. Do not invent a universal compaction threshold or reassure the model that unlimited context exists.

On a topic change, explicitly identify the active task and applicable state. Do not let an earlier draft, cached fact or worker instruction override a newer user decision. Lock or partition shared files when available; otherwise assign one writer. A reviewer reads a specified artifact version, and a later edit invalidates affected review evidence. A user cancellation overrides a continuation prompt.

Check infrastructure before treating silence as a prompt defect. Inspect supported streaming, client timeout, message block handling and output budget. A tool-wait period can be legitimate. A final answer truncated by a token cap needs a budget or delivery repair and a completeness check, not a claim that generation succeeded.

## Deliver and qualify

Fill [the long-run template](../assets/long-run.template.md). Deliver the complete task prompt separately from host prerequisites and proposed configuration changes. Include the actual readiness state of each pillar, milestone checks, item/job records, context transition and stop rules, and a worked recovery path.

Exercise at least the applicable cases with isolated artifacts: ordinary completion; a required job still running; failed verification; permission blocker; missing review/delivery/memory capability; context transfer with an open job; intervention that changes scope; duplicate side-effect risk after timeout. Record expected and observed outcomes separately. These are design tests unless an authorized runtime actually executed them. See the complete degraded-host specimen in [examples](../references/examples.md).

Stop this design task when the user has a usable contract and honest prerequisite/qualification status. A long-run design request does not itself authorize a long-running model campaign.
