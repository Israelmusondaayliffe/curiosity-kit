# Diagnose, repair, refactor or redesign an existing web product

Use for an existing web surface that needs explanation, debugging, a bounded visual improvement, structural refactoring or measured performance work. These are distinct outcomes. An audit or “what is wrong?” request returns findings without code changes. A requested repair authorizes its scoped repair under [the entry](../SKILL.md), not an unrelated redesign.

Use the [protected working-state baseline](build.md#protect-the-existing-working-state) before any edits. Read [architecture and errors](../references/architecture-and-errors.md) for a relevant technical mechanism, [visual craft](../references/visual-craft.md) for the affected design details, and [browser and evidence](../references/browser-and-evidence.md) for actual observation or interaction. [Verify](verify.md) owns final review, evidence freshness and acceptance; this method owns causal diagnosis and bounded change.

## 1. Inspect before choosing a treatment

Record the request, actual version, affected route/component, actor, data and expected result. Inspect the current page and the source path that produces it. Read the relevant framework/styling configuration and versions, imports, component state, data flow and adjacent working examples. Use relevant history and design decisions to explain constraints without inventing original intent.

Separate these problem classes:

- **Job/content:** the page emphasizes the wrong task, omits necessary information, uses unsupported claims or cannot explain its result.
- **Visual:** hierarchy, density, composition, type, alignment, imagery or surfaces fail the accepted direction.
- **Interaction:** unclear affordance, hidden or dead action, awkward navigation, missing feedback, broken keyboard path, interruption or recovery.
- **Behavioral defect:** an operation produces the wrong result, corrupts state, loses data or violates an access boundary.
- **Refactor:** the external behavior is acceptable but its internal shape is difficult to change safely.
- **Performance:** the completed user task is too slow or costly under a specified workload.
- **Version/environment:** the observed artifact, configuration, network, fixture or tool does not match the assumed source.

A page may have more than one issue, but do not mix their pass criteria. Fixing navigation does not establish visual fidelity. A font change does not resolve a broken save. Split unrelated findings and keep unrequested work as recommendations.

For visual redesign, preserve the existing accepted content, brand, structure and working behavior unless the request includes changing them. For a bug, preserve the exact symptom before simplifying the scenario. For a refactor, pin current accepted behavior before moving structure. If the claimed defect is actually a documented product decision, explain that evidence and resolve the discrepancy before changing it.

## 2. Build a discriminating reproduction

Write the expected versus observed outcome in terms a user or public caller can verify. Establish the starting data, identity, route/history state, browser/device and conditions that matter. Save the original reproduction before minimizing it.

Choose the cheapest real signal that reaches this bug, typically:

1. An existing public-seam regression test
2. A request to the actual local API with a known fixture
3. A fixture-driven command or small isolated harness
4. A browser sequence with visible/DOM/network assertions
5. Replay of an already supplied trace or captured input
6. Controlled differential, property-based or historical comparison when the failure requires it

These are alternatives, not a mandatory toolchain. Prefer the available project path. Do not invent a harness that replaces the suspected boundary with a mock, or test only a helper when the failure requires multiple consumers or a full event chain.

Run the reproduction and confirm the user's symptom appears. “The command failed” is insufficient if it failed during setup. “No console error” is insufficient if the user sees incorrect data. For an intermittent issue, record the observed frequency and conditions; use controlled timing or repeated isolated trials to increase the signal without calling it deterministic. Keep repetition bounded by the diagnostic question and its side effects.

Minimize one variable at a time while retaining the same failure. Remove unnecessary inputs, steps, configuration or callers and rerun after each removal. Keep the original full scenario for later replay. Stop minimizing when further reduction loses the mechanism or would turn the check into a different bug.

If the surface cannot be reached, distinguish unavailable environment, denied authority, missing fixture and product failure. Continue useful source or supplied-artifact analysis with calibrated conclusions. Ask for the exact missing prerequisite only when needed. Do not perform a speculative fix and report it as proven.

## 3. Test causes before editing the treatment

Trace from the actual entry point through each relevant transformation, state write, await and response. Use [architecture and errors](../references/architecture-and-errors.md#error-diagnosis-catalog) to generate candidates, not automatic patches.

For a non-obvious issue, rank a small set of competing hypotheses. Each needs a prediction: “If the stale request wins, delaying the older response until after the newer one will restore the older results.” An obvious local defect can have one discriminating hypothesis; do not manufacture alternatives to meet a count.

Select the next probe that best separates plausible causes. Prefer debugger/state inspection when available, otherwise narrowly placed, uniquely tagged logs. For each probe record the hypothesis, intervention, expected distinction, actual result and next decision. Change one variable at a time. Remove task-owned instrumentation and changes motivated only by disproven hypotheses.

Examples of useful discrimination:

- Correct server result but old UI: compare response identity with the component's current query and accepted-result identity.
- Save toast without durable change: compare the write response, a fresh authorized application read and a second consumer; inspect whether only optimistic state changed.
- Dialog closes immediately: observe the opening event, document listeners and dismissal reason; do not merely add an arbitrary delay.
- Repeated event after remount: inspect subscription setup/cleanup and stable listener identity; do not disable the effect to hide the symptom.
- Works locally but fails in preview: confirm build/origin/base-path/config identities before altering business logic.

When hypotheses repeatedly fail, revise the mental model and reproduction. Look for a wrong version, hidden writer, unexpected lifetime or missing observation. Escalate a concrete scope/authority need, not an arbitrary file-count threshold. Do not stack several “might help” changes and lose the causal signal.

## 4. Apply the relevant bounded change

### Bug repair

1. Put the observed failure into the closest appropriate regression seam before the production fix. Preserve its failing result. If no sound durable seam exists, retain the executable reproduction and identify that gap.
2. Change the mechanism supported by the probe. Address shared policy at its actual owner after reading all callers; do not paste guards into every consumer.
3. Include the necessary validation, ordering or recovery change, but do not add unrelated defensive machinery.
4. Run the regression and then the original full reproduction. Exercise nearby legitimate and negative behavior that the change could affect.
5. Recheck protected working state. Record what changed, why it works, remaining uncertainty and the evidence.

An isolated test can prove a local mechanism; it does not automatically prove the browser path is fixed. If the original environment remains unavailable, report a repair candidate with that exact limit.

### Behavior-preserving refactor

First define what must remain unchanged: public outputs, routes, storage effects, failures, timing bounds, accessibility behavior and relevant rendered states. Capture characterization, equivalence or snapshot evidence against the actual baseline. Typecheck and lint do not pin user behavior.

Name the concrete structural improvement: one authoritative state owner, a coherent operation behind a smaller public interface, fewer invalid states, removed duplicated policy, or reduced mutable scope. Count how many decisions and layers a caller must understand, not just lines or files. If the proposed abstraction adds reader burden without a real benefit, keep the simpler code.

Move in small steps while the pin stays green. Search every caller, export, dynamic string, configuration entry, fixture and documentation reference for a renamed or moved contract. Migrate all current callers before removing a superseded API. Prefer one completed migration; use a bounded expand–migrate–contract sequence from [plan](plan.md) only when compatibility requires it. Do not leave permanent two-way APIs merely to avoid finishing caller migration.

Preserve meaningful tests. Replace obsolete implementation-coupled tests only after the new public checks cover their requirements; do not delete a failing test to make the refactor green. Keep discovered feature changes or bug corrections separate from the parity claim. For pixel-preserving refactors, freeze fonts, browser, viewport, data, state and capture conditions; a new screenshot baseline is not proof of parity.

### Performance repair

Define the user-visible work and measure its baseline before optimizing. Identify actual workload, build, warm/cold state, browser/runtime, fixture and relevant cache/network conditions. Use the measurement that matches the symptom:

- CPU trace for a hot loop, main-thread blocking or repeated render work
- Heap/retainer evidence for a leak across repeated use
- Network waterfall for sequential requests, overfetching or delayed assets
- Query logs/plans for N+1 patterns or missing useful indexes
- Frame/timeline inspection for jank, layout thrash or expensive effects

Reduce the profile to the cost-bearing path and attribute it to source. Test a single causal change, such as batching the measured query, virtualizing a demonstrated large list, eliminating a leaked listener, avoiding repeated layout reads/writes, or caching an actually repeated stable computation with a defined invalidation policy. Do not add memoization, debouncing, lazy loading or caching merely because they sound faster.

Repeat the same completed work under matched conditions, preferably interleaving baseline/candidate trials when noise matters. Compare distributions or repeated observations appropriate to the task, including regression risk and memory/interaction costs. If the baseline lacks the feature, use a defined absolute budget and isolate added work; do not claim a speed ratio between different tasks. Instrumented coverage may perturb performance. Local measurements do not establish field Core Web Vitals or real-device behavior.

### Conflict or structural migration repair

When a requested repair includes merge conflicts, read the base and both sides where available. Recover each change's intent and invariant before choosing combined code. Resolve one coherent cluster, then test both intended behaviors. Compiling whichever side is easiest does not settle incompatible product policy. Surface genuine semantic conflicts. Respect the entry's authority for any branch, index or history operation; this procedure does not authorize destructive Git cleanup.

## 5. Run a targeted visual and interaction redesign

Use this branch for authorized appearance/experience improvement. Start with matched before renders of the real surface and preserve the selected visual authority. Audit only the relevant page/flow unless a broader sweep was requested.

Read the applicable parts of [visual craft](../references/visual-craft.md), then connect each proposed change to an observed problem:

- **Hierarchy and content:** what gets attention first, whether the primary job is visible, whether prose/data density supports scanning, and whether required content is missing or misleading
- **Type and alignment:** actual font/weights, line lengths and wraps, numeric alignment, label/value relationships, shared baselines and optical centering
- **Layout and surfaces:** grid, spacing, responsive reflow, unnecessary containers, grouping, contrast, depth and image framing
- **Controls and states:** action priority, navigation/current location, hover/press/focus, loading/empty/partial/error/success, cancellation and back paths
- **Inclusive use:** meaningful semantics, names and alternatives, keyboard path, focus visibility, zoom/reflow, touch targets and non-hover access
- **Implementation fit:** actual dependency availability, styling-system consistency, reusable components, z-order/portal behavior, route/asset integrity and page metadata when applicable

Do not treat a familiar font, a card, symmetry or a particular color as a defect by itself. A font swap can change wrapping and layout, so it is not automatically the safest first fix. Do not add legal links, cookie banners, metrics, imagery or features whose content/need has not been established. Missing required states and inaccessible controls outrank decorative novelty.

Rank improvements by observed user impact, accepted visual-contract importance, breadth and risk. Fix the load-bearing issue first: hierarchy or broken structure before optical polish. Keep unrelated working data and navigation intact. Use surgical changes in the existing stack, not regeneration of the entire page or framework migration.

For each nontrivial change, state the current evidence, intended result, affected component/token, protected scope and how the before/after will be compared. Use exact project values when they matter; link the authoritative craft recipe rather than invent a new parallel token system. A changed direction must return to [design](design.md), not drift into the implementation unnoticed.

### Motion audit and improvement

For motion-specific work, first map framework/library, where motion lives, shared tokens, product personality and interaction frequency. Review eight applicable dimensions: purpose/frequency, easing/timing, physical origin, interruption, performance, accessibility, coherence and genuinely useful missing feedback. The contextual recipes and exceptions belong in [motion and mobile](../references/motion-and-mobile.md).

Re-read every finding at its current location. Discard duplicates, wrong attribution, settled intentional tradeoffs and exempt cases. A code search locates candidates; it cannot judge a spring's feel. Separate corrective defects from optional additions. For an opportunity sweep, each proposed animation needs a named purpose and must not delay frequent/functional use. Report the small set that survives that test; zero useful additions is a valid outcome.

An audit-only request stops with vetted findings. An authorized implementation plan names current version/location, target values, existing token exemplars, ordered edits, excluded scope, drift condition and mechanical plus live-feel proof. Use one current task record. Reconcile it against later code so already-fixed issues do not become duplicate work.

After edits, use the relevant live review criteria in [motion and mobile](../references/motion-and-mobile.md), including contextual exceptions and static alternatives. Endpoint screenshots alone cannot prove temporal quality.

## Delivered-artifact and trace diagnosis

Use this conditional branch when the complete source is unavailable, a delivered build disagrees with it, or the user supplied a trace/bundle for explanation. Ordinary complete-source work does not require reconstruction tooling.

### Supplied trace

Identify the format and capture conditions before parsing: CPU profile, browser performance trace, heap snapshot, network capture or event log. Preserve the original artifact and inspect it as data; do not execute embedded scripts. Query or summarize large artifacts using an available parser, keeping exact source/capture pointers.

Find the significant hot frames, repeat scheduler, retainer chain, request dependency or observed event sequence. Map it to file/symbol/location using the artifact's actual symbols or explicitly paired source map. State unresolved symbol gaps. A paired before/after capture may support a causal hypothesis; a single hot frame or correlation alone does not establish cause.

### Delivered script or bundle

1. Establish exact artifact bytes/version, origin and capture context. Preserve query/fragment variants and duplicate candidates rather than selecting by a familiar filename or module ordinal.
2. Inspect delivered code inertly. Recovered routes, endpoints, imports and literal strings suggest probes; static reachability is not executed behavior. Retain missing dependencies, computed imports and parse limitations as unknowns.
3. If using an already captured script export, retain its capture-to-file identity. Do not refetch a same-URL asset and call it the original version.
4. Pair source maps explicitly with the selected generated script and location. Preserve one-based line versus zero-based UTF-16 column conventions supported by the tool. A declaration or embedded original text does not independently authenticate deployed source.
5. Compare source/runtime identities with the browser evidence method. Loaded bundle residence does not prove module initialization, branch execution or UI causality. Keep multiple matching candidates ambiguous.
6. If active coverage or instrumentation is genuinely needed and authorized, scope it to the selected owned environment and interaction. Confirm it was armed, preserve frame/document/default-world identity, and invalidate attribution when that identity changes. Do not present timing collected under intrusive instrumentation as an unperturbed performance measurement.

Return the strongest supported conclusion, relevant counterevidence, exact artifact/source pointers and the smallest next discriminating observation. Do not install an engine, borrow a live authenticated session, broaden origins/actions, or patch a live process merely because a donor procedure suggests it. [Browser and evidence](../references/browser-and-evidence.md) owns capture authority, privacy and adapter lifecycle.

## 6. Recheck the whole affected outcome

For every repair, replay the original case, the focused regression and the adjacent behavior the change could break. For redesign, capture the new real render under the same relevant conditions as before and replay the affected flows. For refactor, keep the agreed parity criterion; for intentional redesign, compare with the selected design tolerances rather than demand unchanged pixels.

Remove only this task's temporary instrumentation/experiments and verify protected changes survived. Pass the exact candidate, findings, before/after artifacts, checks and gaps to [verify](verify.md). Explain the symptom, supported cause, scoped change, actual result and remaining qualification in plain language. A read-only diagnosis can be complete without a patch; an unobserved repair cannot be called a verified fix.
