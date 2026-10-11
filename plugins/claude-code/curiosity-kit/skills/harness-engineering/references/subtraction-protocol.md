# Subtraction protocol

Use this when shortening a harness, adapting it to a different model, or changing which skills are visible. The goal is the smallest default context that keeps measured behavior, not the shortest prompt. A reported reduction elsewhere is direction, never a quota.

## Freeze first

Before editing, save in one dated run folder: the instruction files and their hashes; the full prompt input measured by section where the host lets you capture it; model, effort, run count, tools and task conditions; the installed listing, capability inventory, source and cache fingerprints and routing results; the behavior cases, scorer version, raw outputs and normalized baseline; and the operation plan with approval groups, backups and rollback order. Compare only runs with matching model, effort, tools, scorer and conditions. If the scorer changes, rescore the frozen raw outputs.

## Behavior cases

A small permanent set covering what universal context protects: authority and safety; routing to the source owner; real implementation outranking process artifacts; finite task shape and a forced stop when effort is high but the target is not moving; unresolved work reported as unfinished; file layers, output paths and evidence-backed completion. Keep only cases that protect a distinct failure mode; add a case when a newly observed risk needs one.

## Accept a subtraction batch only when

1. every critical case passes;
2. no category drops below baseline;
3. the overall pass rate meets or beats baseline;
4. the prompt is smaller for the intended reason;
5. duplicated guidance declines;
6. the installed environment passes the same cases after every context-affecting change.

Subtract one coherent group at a time. Restore a failed batch, then add only the smallest missing cue the failure shows. A generic phrase is not equivalent to a named source owner; when a reduction loses a route, restore a compact owner mapping, not the old manual.

## Measure the whole prompt

Track instruction words, total prompt size, skill-listing size, implicit skill entries, duplicate names, front doors present, hidden specialists absent and reachable, explicit invocation of a hidden skill, and source-cache parity. Fewer entries does not mean a smaller prompt: richer front-door descriptions can grow the listing while entries fall. `hectl listing-budget` estimates listing characters against the host rule; capture the real listing after the host truncates it before trusting the estimate.

## Visibility policy

- Front door: implicit discovery only where the approved workflow permits it.
- Owned specialist: reduce discovery only after proving the intended route under current host invocation rules. Do not equate a hidden menu entry with unavailable model invocation or the reverse.
- Explicit-only workflows: keep explicit invocation available using the host's supported metadata; prove it in the actual host.
- Exact loose mirror of a visible namespaced skill: hidden.
- Curated, runtime, connector and system skills: unchanged.

Roll out in reversible waves, smallest families first, stopping at the first route, parity, discovery or behavior regression. After each wave: run the routing cases and one front-door case per hidden specialist, validate and reinstall the affected plugins through the host's supported update flow, prove listing and parity, capture the fresh listing, run a real explicit invocation of a hidden skill, and rerun behavior cases if task-start context changed.

## Compacting one skill

Freeze positive and negative triggers, functional cases, an external rubric, the source fingerprint, script hashes and the command-line contract. A failing current version may be frozen as a reference baseline, with every failure retained. It cannot serve as a passing release baseline. Separate defect repair from subtraction and evaluate both against the frozen criteria; do not call unchanged failure preservation a successful release. Keep stable invariants, safety, the core flow and completion criteria in `SKILL.md`; move conditional operations, setup, recovery and annotated examples into linked files. Passing functional cases alone is not enough when a rubric fails.

## Stop immediately when

A hash precondition changes, conditions become incomparable, a critical or category regression appears, a front door cannot reach a specialist, an unexpected file enters a generated plan, new evidence invalidates the frozen baseline, or source and installed cache diverge. Roll back in reverse apply order and prove parity and discovery after a capability rollback.
