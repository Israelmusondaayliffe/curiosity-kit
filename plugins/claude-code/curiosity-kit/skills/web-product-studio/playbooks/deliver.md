# Deliver the requested result

Load after the applicable [verification](verify.md), or when the user asks for a handoff, pause or release. Match the actual requested result: diagnosis, recommendation, image/reference, complete implementation, local preview, private artifact or authorized deployment. Do not add a commit, PR, merge, publication or account change as an automatic finishing step. The entry's authority rules still control those actions.

## Check the exact deliverable

Compare the current output with the original request and accepted changes. Count the promised files, views, controls and formats. Deliver the complete requested implementation rather than a scaffold with omitted functions. Split a large artifact at useful file boundaries if necessary, retaining a precise resume point and truthful incomplete status. Do not silently reduce scope to fit a message.

Before claiming completion:

1. Reconcile the frozen requirement list with the actual artifact. Each requirement has passing current evidence, an explicit exclusion agreed with the user, or a named gap.
2. Finish authorized writers and generators. Inspect the actual final source, including relevant staged, unstaged, untracked, fixture, configuration and dependency inputs. A commit SHA alone does not identify a dirty build.
3. Run the appropriate final build/package step and compare it with the reviewed candidate. A generator that changes runtime output invalidates affected earlier proof. Reuse unchanged checks only after checking their inputs.
4. Preserve distinct technical, functional, visual, access and operational outcomes. A strong screenshot cannot cover a broken journey; a clean test run cannot establish design quality.
5. Verify that delivered files, media and links exist, represent the stated version and open for the intended recipient. Do not expose private source locators, credentials, authenticated URLs or local machine paths as public destinations.

Use one small task record for scope, version, checks, unresolved work and delivery receipts. Reference existing artifacts rather than duplicate a plan into several logs. Machine validation checks supported structures and bindings; actual browser observations and review establish the remaining claims.

When the change affects setup, run commands, APIs, configuration or user guidance, compare the relevant existing documentation with the exact implemented candidate. For a consequential handoff, give an independent reviewer the frozen candidate and specifically permitted documentation files. Check the returned findings, actual edited paths and their version bindings. Record the documents they reviewed, omissions and blocked access. A self-grade of "docs current" is insufficient. Refresh the affected documentation review if a later change alters those instructions; do not launch a second general audit for an unrelated copy edit.

Save new deliverables with an exclusive, non-overwriting operation or equivalent safe host versioning, unless replacing that exact artifact is authorized. A prior existence check alone can race with another writer. Suffix a colliding name, retain staged generated output if its final save fails, and report the actual saved path. Preserve accepted versions, prior source media and decision evidence. Reusing an output name must never make an earlier screenshot or approval look current.

## Report at the correct level

Lead with the artifact or result and the useful link or file. State what was actually checked and any material limitation. Put long evidence in the task's existing receipt, not a wall of build output. Examples of accurate scope:

- "The local catalog is ready. Search, dialog keyboard use and reload persistence passed on the recorded local build; no hosted deployment was requested."
- "The private preview is ready for your account. Public access has not been enabled."
- "The new revision deployed, but its checkout flow failed the live smoke test. The release is degraded; the failed transaction did not persist."
- "The deployment is still pending. The existing site is reachable, but that does not show the new revision is live."

Follow the current host's attachment, messaging and Sites access-wording rules. For a private Site, state its actual access level and explain that sharing can be changed if requested. Mention only sharing options the current account supports. Invitation eligibility requires its own evidence. A preview URL is not automatically public, durable or production-ready.

No deployment, field performance, mobile hardware, external integration, native host or security-certification claim follows from local tests. Name the limits that matter to this user's acceptance rather than listing unrelated things that were never requested.

## Authorized release

Use this section only when the request and applicable permissions cover the actual destination and effects. Inspect the existing project's release procedure rather than importing a donor's CLI, branch conventions, automation or provider. If a prerequisite is missing, preserve the verified candidate and ask for the specific decision or authority needed.

### Readiness and side effects

Establish the exact repository/project, candidate and base, target environment, artifact, audience and release mechanism. Read the real CI/deploy configuration. A merge might deploy production automatically. If staging-first was requested, verify that a staging trigger, revision selection, production hold and promotion gate actually exist before taking a production-triggering action.

Read all relevant checks and review pages, including pagination. Missing fields, unavailable services, unknown mergeability or a pending check are not passing evidence. Separate no configured tests from configured tests that could not run. Confirm required tests and reviews apply to the current inputs. Resolve scope changes before release; do not bypass branch protections or treat a platform warning as permission.

If the user requested only PR preparation, provide the complete proposed change and stop before submission. If submission is authorized, verify exact recipient/repository, title/body, included files, links and issue-closure wording. Close an issue only when the requested action is authorized and every bound criterion is complete; partial work can link the issue without claiming closure.

### Dispatch and authoritative readback

Immediately before a consequential action, recheck its destination and candidate identity. After the action, query the authoritative server state. Preserve the attempt, command/tool result and receipt. A timeout or nonzero client exit can follow a successful remote action. Do not blindly replay a push, PR creation, merge, deploy or access change.

For an uncertain merge, read the exact PR's current head, base, merged state, landed revision and any active queue/request before deciding what remains. A squash or rebase creates different commit identities; ancestry of the old head is not the sole merge test. For an uncertain deployment, find the deployment receipt for this artifact and environment. A failed lookup means unknown, not absent. Reconcile changed destinations or revisions before further action.

Dependent changes release in their actual dependency order. A tested dependent patch does not make an unverified prerequisite safe. Recheck the next candidate after the preceding merge changes its base. A request to queue one item does not grant permission to arm or retarget the rest.

### Deployment identity and live health

Keep these states separate in the receipt:

| Observation | Supported conclusion |
| --- | --- |
| Local or private preview passed | That artifact worked in the recorded environment |
| Server confirms a merge | The specified change landed; deployment remains separate |
| Platform reports success for the exact version and environment | The identified deployment succeeded |
| HTTP response or reachable old page | Reachability at that time; deployed revision may be unknown |
| Fresh intended-viewer smoke and required durable effects pass on the identified deployment | The required live health checks passed for that revision |
| Revert/rollback change exists | Recovery work exists; restoration remains unproved |
| Restored version is confirmed deployed and required live checks pass | The scoped restoration is verified |

Follow actual deployment state until success, failure, cancellation, a task-defined observation boundary or a genuine authority/access blocker. Pending or unchanged is not completion. Use a sensible status interval and preserve tool failures as unknown. When the user asked to finish or monitor, continue safe diagnosis and authorized recoverable steps; ask before a new consequential action outside scope. Do not inherit an arbitrary donor deadline or start a recurring automation merely to finish one deployment.

For the live check, identify the version, URL, route, environment, viewer role, time and browser conditions. Check meaningful content, critical assets, required interaction and durable effects, errors and relevant timing. For public artifacts, use an unauthenticated context and verify required routes and downloads. Compare to an actual pre-deploy baseline where needed; a monitor-start sample cannot be relabeled pre-deploy. Changed error identities matter even when their count is unchanged. A later recovery does not erase an earlier outage.

Report "deployed, verification incomplete" when deployment succeeded but live proof is missing. Report degraded when a required health check fails. Keep a failed deployment separate from the health of an old version that remains reachable. Do not turn a waived check into a passing score.

## Recovery and interruption

Before risky authorized changes, identify the existing recovery procedure and what data or service effects it does and does not undo. Use the project's real deployment history and data-migration rules. Do not invent a universal rollback script or assume reverting code restores a database, external message or customer transaction.

On failure, preserve the first failing evidence, exact candidate and current remote state. Diagnose before choosing another mutation. A repair within the accepted task can proceed under its existing authority; a new production rollback, broader data change, publication or account action needs whatever permission applies. Retest the affected behavior and dependent acceptance checks after the repair.

If a rollback is authorized, determine the actual landed topology and exact range. Protect dirty, staged and untracked user work. Unknown merge range, conflicts or a changed target require a pause rather than a forced reset. A rollback commit or PR is still recovery pending until the intended version is live and its required health checks pass. Do not automatically revert a failed rollback.

For a requested pause or unavoidable interruption, finish or stop at a safe atomic boundary. Save a concise checkpoint in the task's existing authorized location:

- original goal and current authorized scope;
- exact source/build/reference identities and working location;
- completed results with evidence links and honest gaps;
- current operation, any pending remote action and how to read its state;
- remaining ordered steps, blockers and the first resume action;
- owned processes/resources and what must stay available.

Do not create a WIP commit, push or read unrelated private transcripts merely to make a checkpoint. On resume, compare the saved record with actual local and authoritative remote state. Check late worker results before relaunching anything. Reuse still-current proof and rerun only affected checks. The old summary supplies context, not an automatic pass or new authority.

## Clean up only owned task resources

Retain useful evidence and the deliverable before cleanup. Stop only the exact task-owned server, browser context, job or temporary resource when it is no longer needed. Verify ownership by its recorded identity and current state; a matching port, filename or reused PID alone is insufficient. Confirm termination or removal rather than claiming it from a requested stop.

Preserve the user's existing tabs, processes, databases, credentials, environment settings and staged/unstaged/untracked work. Do not clear shared caches, reset branches, remove worktrees, delete remote branches or empty evidence folders as a default shipping tail. Apply current permission rules to deletion. If cleanup is blocked or a task resource must remain for the user's preview, report what remains and why without calling it complete.
