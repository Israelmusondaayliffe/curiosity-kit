# Resume from canonical evidence

Read the initial frozen goal/plan and canonical state, then the newest generated handoff, saved rounds, workstream evidence, integration and verification. A handoff is a reading aid; the ledger and current bytes determine truth. Report discrepancies rather than silently choosing the more flattering narrative.

Run `gauntlet.py verify --run-dir <run>` before dispatch. Check actual host capabilities against the frozen snapshot, remaining time/cost/launch/round capacity, approval scope and peer status. Check pending launch receipts against the host. If a process died, its OS file lock releases; do not delete a lock file to override a live holder. A reservation that survived the crash still counts. `recover` records uncertainty and retains cost; reusing its request ID cannot authorize another launch.

Accepted work is not rebuilt without a concrete recorded gap or changed dependency. Rehash its artifact/evidence. Changed upstream bytes invalidate descendants and affected integration even when the former status says accepted. Resume a paused run only after pending reservations are reconciled. A changed capability, exhausted budget or changed frozen plan requires diagnosis and an explicit new contract where needed, not a force flag.

Generate a handoff at material boundaries and before ending a session. It must retain run identity, contract/approval, status and gaps, accepted work and evidence, unresolved or interrupted launches, decisions not to reopen, exact next action, read-first paths, budget and capabilities. Script-generated facts stay separate from any clearly labelled unverified judgment note. Never overwrite prior canonical handoff records.

When useful, ask a fresh read-only helper to recover the objective, status, accepted work, unresolved risk, next command, forbidden repetition and assumptions solely from the saved state/handoff. This comprehension check authorizes no continuation or artifact edits. Fix confusing handoff generation, not history.

## Exhausted runs and successor contracts

There is no budget-extension command. An exhausted run cannot silently resume, reset counters or become verified. Export its evidence and handoff, leave its ledger intact, and state the exact remaining outcome and cost/authority change needed.

If the user approves continuation under a new contract, create a different run directory. Record the predecessor run ID, ledger/evidence paths and hashes in the new plan and source inputs. Inspect existing artifact bytes and retain useful completed work; do not rebuild it merely to manufacture a new receipt. Scope the successor program to remaining work, treating preserved predecessor artifacts and evidence as frozen external inputs. Declare that changed decomposition and any revised budget/criteria in the approved successor plan. Old acceptance is historical evidence, not automatic acceptance under changed criteria. Recheck affected dependencies and the final integrated outcome. Never edit or reset the predecessor's usage ledger, approvals, gaps or verdict.

When an essential preserved artifact or evidence hash no longer matches, record the discrepancy and seek the smallest repair/decision; do not quietly import a stale pass. A successor can complete the remaining goal, but its report must identify both runs and avoid relabelling the exhausted predecessor as successful.
