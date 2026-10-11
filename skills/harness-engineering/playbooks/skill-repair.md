# Evidence-led skill repair

Repair a specific skill failure in an isolated candidate and prepare an exact reviewed change. Evaluation does not itself authorize editing, and a passing candidate does not itself authorize source application or installation.

## Diagnose the required change

Read the failed or needs-review result, original request, frozen criteria, exact source/candidate and actual artifacts. Distinguish a real capability defect from a trigger miss, broken verifier, unavailable prerequisite or invalid environment. Use [review methods](../references/review-methods.md) to separate observation from causal hypothesis.

State the smallest coherent fix and what would show that it worked. Check existing mechanisms before adding a duplicate instruction. A recurring mechanical error may need a helper or repaired gate; a judgment error may need better criteria or a contrasting example. Do not encode a fixture answer into the runtime.

Preserve the original failure and current acceptance contract. A source that already fails may still serve as a reference baseline for repair. It cannot support a claim that a subsequent destructive simplification preserved previously working behavior.

## Stage safely

Read the [evaluation contract](../references/evaluation-contract.md). Choose a new candidate directory and evidence root disjoint from the protected source. Snapshot the complete execution dependency set and stage declared files through the local helper:

```text
python3 scripts/hectl.py eval stage --target SOURCE_DIR --output NEW_CANDIDATE_DIR --manifest STAGE.json --path SKILL.md --path references/rules.md --path scripts/check.py
```

`--path` is required and repeats once per file. Substitute your own absolute SOURCE_DIR, a new NEW_CANDIDATE_DIR and a new STAGE.json outside the source, then list the resource closure: SKILL.md plus every file it, its playbooks or its scripts read, load or execute, and any new file the repair will author (a declared absent path stays absent until you write it). Use the same list as the suite's `target_paths`. Directories are refused; name files. Check the closure against the source tree before qualifying: the run records the complete execution tree, and preparation refuses a candidate containing undeclared files. A missed dependency means restaging with the complete list, not promoting a partial copy. Preserve the source's `.git`, unrelated data, modes and accepted identity. The staged copy is unqualified; copying it is not a passing test. Never replace the entire source directory to promote selected changes.

One writer owns each candidate file. Optional workers receive the exact failing behavior, owned paths, protected material, limits and expected evidence; they cannot expand scope, approve their own work or publish. The parent inspects returned changes and remains responsible for the integrated result.

## Repair and prove

Change the diagnosed cause. Preserve all other useful behavior and source meaning. For factual outputs, check every count, qualifier, condition, promise and final-response format; a structurally valid evidence record can still contain a false statement.

Run the smallest affected deterministic checks and relevant regressions, then the frozen acceptance evidence required for the change. Use a real bad control where it matters. Recheck all touched callers and resources; changes to shared packaging/common APIs may require a full-library package check. Do not repeat sound unrelated model cases by default.

Record actual before/after artifacts, current source/suite/adapter identities, outcomes and limitations. A reviewer correction is assisted evidence, not a retroactive pass of the original model output. If the rubric legitimately changes, version it and collect the relevant matched evidence. If work is blocked or the finite budget is exhausted, retain an honest unfinished state.

Inspect a complete useful output after the repair. Helper tests alone do not qualify the generated skill or a subjective deliverable. Required independent review must use the actual final artifact; a previous review becomes stale when the relevant bytes change.

## Prepare an exact application

The local `hectl eval prepare` binds the stage record, source, candidate, suite, passing current run and explicit artifact review into a promotion envelope. Use `--help` and the exact schema in the evaluation contract; do not construct an approval token from an example.

Show the proposed per-file changes and any known limits. Actual user authorization comes from the current conversation or an applicable approved plan, not an imported JSON field. Bind the authorization record to that exact envelope and operations. The helper checks declared identity consistency; it cannot authenticate the human.

Before application, recheck source, candidate, suite, evidence, review and operation payload. Any material drift blocks the affected step. Do not regenerate an expected hash silently to make a stale decision look current. Do not bypass a failed promotion gate by passing the envelope to legacy apply or hand-running its writes.

The guarded application uses existing HE scoped create/update operations, approved groups, unique backups and write-ahead recovery. It preserves unrelated files and later user edits. If removing a source file is genuinely required, stop that part until a separately approved, implemented and tested delete/recovery contract exists. Whole-directory replacement and generic stale-cache cleanup are not substitutes.

## Recover and finish

Inspect actual applied state and the receipt. If a failure occurs, preserve partial evidence and use the recorded manifest's recovery path under [build](build.md). Rollback must not overwrite intervening user edits; report a protected conflict rather than forcing restoration.

Keep source application distinct from installation, public release, account changes and live execution. For an installed-result request, [verification](verification.md) must inspect the actual authorized host. Otherwise return the reviewed staged candidate or applied local files with their precise proof level.

Finish with the original defect, exact corrected artifact, observed checks, remaining requirements and recovery state. A patch is complete when it achieves the approved outcome without an unresolved essential regression, not when every status field has been made green.
