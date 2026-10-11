# Refactor and migrate safely

Use this method to change structure while preserving behavior, or to carry an approved compatibility migration through all relevant consumers and retained data. A refactor is complete when the new structure works against the preserved contract and the claimed simplification is real. Renamed symbols and a successful build are insufficient.

Read [the host contract](../references/host-contract.md). Local editing authority does not authorize a production migration, data deletion, deployment, account change, or published-history rewrite. Use [implement.md](implement.md) for work ownership and integration, and [debug.md](debug.md) if an unexplained failure emerges.

## Inputs and decision boundary

Identify the requested structural outcome, accepted behavior, relevant source and tests, affected consumers, retained data, and allowed operations. Read applicable design decisions. Preserve unrelated edits and staged work before changing files.

Name the concrete difficulty the refactor will remove. Examples include duplicated domain rules that diverge, a state owner split across callers, repeated conversion logic, or an interface that forces every caller to understand transport details. A file being long or a pattern feeling unfashionable is weak evidence on its own.

If the user requested an architecture assessment, produce grounded options and a recommendation before editing. If they authorized a specific refactor, do not restart a general design interview. Separate a newly found feature or bug from the behavior-preserving task. Do not silently fix it or pin a disputed behavior as intended merely because it currently exists.

## 1. Record the behavior that must survive

Trace the affected entry points to their state and external effects. Include normal results, errors, ordering, permissions, configuration, serialization, and any performance or resource constraint the existing contract actually promises.

Run relevant existing checks on the starting state. Add characterization coverage, a replay, a snapshot of meaningful output, or an old-versus-new comparison when coverage is inadequate. A typecheck or lint run can catch structural mistakes but does not preserve behavior by itself.

Choose the comparison carefully:

- Use independently specified expected values for accepted business behavior.
- Use differential comparison for a wide transformation when the prior implementation is an appropriate reference.
- Normalize only irrelevant variation such as a disposable path. Do not normalize away ordering, timestamps, identifiers, or errors that are part of the contract.
- Keep negative cases, including denied access, stale updates, malformed accepted-boundary inputs, and interruption where they matter.

A characterization records what happens, which can include a known bug. Label that limit. If the requested structural work can preserve the known behavior safely, keep the bug separate. If proceeding would make the defect worse or invalidate the accepted change, raise the concrete conflict.

Record pre-change evidence before moving structure. It cannot be recovered merely by inspecting the final patch.

## 2. Design a smaller responsibility boundary

Write realistic caller examples before moving types and files. Identify what each caller should know and what the implementation should hide. Include error and state handling, not only the happy-path function signature.

Ask where each invariant belongs. Parse untrusted input at the boundary that receives it. Keep one owner for a shared business rule. Prefer derived values to lists or flags that callers must synchronize manually. Use a state model when it removes invalid combinations, rather than adding a state framework by default.

Consider dependencies in their actual categories:

- In-process computation can usually be tested directly through the resulting interface.
- A local database or filesystem can use isolated real instances or faithful project-supported substitutes. Verify the substitute represents the behaviors the refactor depends on.
- An owned remote service may need a narrow transport boundary so domain behavior can be tested without network setup, plus integration evidence for the real transport.
- A true third party can use an injected substitute for local checks, with real integration remaining a separate claim.

A test double does not justify exposing internal seams to every production caller. Nor does an arbitrary number of adapters prove a design is useful. Add a boundary because it hides needed complexity or supports real substitution, and keep it as narrow as the task allows.

For a costly unresolved interface change, compare a few genuinely different approaches. Evaluate caller effort, ownership, hidden complexity, change locality, failure handling, and migration cost. Skip the panel for a settled mechanical change. The selected design should explain what becomes easier in this project, not promise abstract elegance.

## 3. Inventory the compatibility boundary

Search code references, then inspect consumers that text search can miss:

- Public exports, imports, generated clients, reflection, registration tables, string keys, configuration, commands, and documentation used as operational instructions.
- Independently deployed services, older background workers, scheduled jobs, cached browser clients, plugins, and consumers in other repositories or languages.
- Stored rows, saved JSON, files, queue messages, persisted caches, exports, replay logs, and schema versions still supported.
- The previous binary or configuration retained for backout.

Record each relevant consumer's owner, version or format, read/write behavior, ability to change together, and cutover evidence. Use an existing plan or a short migration note. Do not create a registry for a small local rename.

Establish semantics as well as spelling. Renaming `allocated_count` to `reserved_count` can hide a change in units or meaning. Compare identity, null/default behavior, enum values, rounding, ordering, timezones, and lifecycle transitions when affected.

Choose the change strategy from this inventory:

- Change callers and remove the old internal interface together when the entire relevant set can change atomically and no retained data or supported runtime consumer needs the old interpretation.
- Use a compatibility period when callers or data outlive the checkout, release independently, or need a usable backout version.
- If the consumer set is unknown, investigate or keep the affected contraction blocked. Unknown external usage is not proof that deletion is safe.

The smallest correct plan can retain a temporary compatibility path. It should have a specific reason and a removal condition, rather than becoming permanent duplication by accident.

## 4. Expand, migrate, then contract when needed

### Expand without breaking the current contract

Add the new representation or entry point while old supported consumers still work. Define how readers handle old and new forms, how writers select a form, and what happens if both disagree. Avoid uncontrolled dual writes that create two sources of truth.

Use the project's migration and compatibility facilities. When dual writing is required, state its consistency rule, failure handling, and reconciliation. Test mixed versions using the real affected serialization or storage boundary. A fake repository that accepts both shapes may conceal a real schema restriction.

Keep the expansion usable and reversible within its declared boundary. Verify that the supported old code can read data produced during expansion, or name the alternative recovery path. Do not promise code rollback if the new data makes that version unusable.

### Migrate in bounded units

Group code consumers or records so each batch has a clear owner, prerequisite, and proof. Preserve the accepted semantics. If the mechanical change cannot remain green between batches, use an explicitly isolated integration effort and name the final integrate-and-verify step. Do not represent partial batches as independently releasable.

For data conversion, inspect representative source records and expected transformed results. Validate relationships and invariants, not only row counts. Include empty or missing values, older versions, boundary values, and partially converted records when they occur in the supported data. Define how a rerun recognizes completed work and handles interruption without duplication or silent loss.

Run authorized data experiments on isolated copies or fixtures first. Verify what a dry run actually does before relying on its name. Live writes, backups containing sensitive data, and destructive cleanup remain governed by their own authority.

After each unit, run its behavior-preserving checks and inspect actual output. Recompute the next ready work from completed prerequisites. Two files using the same new name does not prove their data contract agrees.

### Contract only after the relevant consumers are gone

Before removing compatibility, establish all applicable conditions:

1. Supported code callers use the new interface.
2. Independently running consumers have actually cut over, or their continued compatibility is accounted for.
3. Retained data, queued work, and supported saved inputs can be read or were safely converted.
4. The agreed backout version remains valid, or an accepted different recovery procedure is ready.
5. Integrated behavior and the required mixed-version or recovery checks have passed against the candidate.

Closed tickets, zero symbol matches, and a successful migration command do not replace these observations. If a nightly job cannot be inspected, retain the compatibility it may still require and report that deletion is blocked. Safe completed expansion can remain useful.

Remove obsolete paths only within the approved deletion scope. Search again for operational references and generated artifacts. Verify the contracted result, including the absence of accidental fallback to the old behavior.

## 5. Preserve tests through the structural change

Move tests toward stable observable behavior when that improves them. Before retiring an old test, identify which relevant cases it protected and demonstrate equivalent coverage at the new interface. Keep cases for denied access, stale state, failure ordering, and interrupted operations even if the old test name described an internal module.

Do not retain brittle implementation assertions solely for their count, but do not delete them solely because the module moved. The question is which defects the resulting suite can catch. A valid-request interface test does not replace three deleted rejection tests.

Keep expected behavior independent of the new implementation. If the user approved a behavior change alongside the refactor, separate its expectation changes from the structural steps and point to that decision. Demonstrate the new expectation rejects the old behavior when practical. This makes regressions distinguishable from intentional changes.

After each coherent move, run the preserved behavior checks. After integration, run the broader affected set and the real original routes. Use [verify.md](verify.md) for interface and durable-effect acceptance. A source-only review cannot establish a runtime equivalence claim it did not observe.

## 6. Check that the refactor earned its cost

Inspect representative before-and-after caller paths. Name the concrete reduction, such as one domain validation instead of three, one state owner instead of competing writes, or an entry point that no longer exposes transport details. Count lines only when that answers the real maintenance question.

Remove abandoned experiments and unused transitional code whose removal conditions are proven. Preserve deliberate duplication when a settled decision or compatibility need justifies it. If a proposed abstraction adds navigation and coordination without removing meaningful complexity, simplify the candidate within scope or report that the attempted design did not meet the goal.

Use [review.md](review.md) for requested independent review. Any repair changes the candidate and needs affected verification again. Publication and deployment, if authorized, continue through [deliver.md](deliver.md); neither follows automatically from a cleaner diff.

## Example migration note

Illustrative change: rename the stored `allocated_count` field while the service and nightly exporter release independently.

Contract: Both names represent the same integer count. No unit conversion or behavior change is approved.

Expansion: The service accepts saved records with either supported name using a defined precedence and conflict rule. The chosen writer format remains readable by the current exporter and the backout service. Mixed reader/writer fixtures establish those combinations.

Migration: Update the service callers and exporter in separate verified units. Convert representative saved records using an interruption-safe operation. Check values and relationships after conversion, then replay both real routes on isolated data.

Contraction: Remove old-form support only after the deployed exporter cutover is observed, retained inputs are accounted for, and the agreed backout window or alternate recovery condition is met. If exporter identity is unavailable, report expansion and code migration as verified while contraction stays blocked.

Recovery: A code revert restores service code only. It does not restore converted records, undo an exported file already used by another system, or prove the previous exporter can read the new data. Name and test the applicable recovery separately.

## Return and resume

Report the structure changed, contract preserved, affected consumer/data set, actual before-and-after evidence, compatibility still retained, and any blocked contraction. Include the concrete maintenance improvement and limitations of substitutes or unobserved environments.

On resume, inspect current code, consumer versions, saved-data state, and migration outcomes before repeating a batch. Preserve completed work and its evidence. Reconcile possible external effects through stable operation identity. An absent local completion marker does not make a conversion or export safe to repeat.

If verification fails, preserve the failing evidence and locate the smallest responsible move. Undo only attributable owned changes when restoration is authorized and safe. A new binary, application data, governance record, and accepted external effect have different recovery requirements. Use [operate.md](operate.md) for an internal app's release and operational responsibilities, and [learn.md](learn.md) for an interruption handoff.
