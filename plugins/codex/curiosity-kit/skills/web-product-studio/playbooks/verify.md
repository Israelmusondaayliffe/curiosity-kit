# Verify the requested web outcome

Use this playbook for implemented work, diagnosis, QA and independent review. The entrypoint owns authority and delivery boundaries. Select checks from the accepted task and affected risks; do not convert a one-control fix into a whole-site certification campaign. The product, technical and visual verdicts are distinct. A clean build or an attractive screenshot cannot substitute for the other axes.

## 1. Freeze what will be judged

Read the accepted brief/reference and current changed files, their callers, relevant tests and the actual running page. Identify the exact base and candidate, source snapshot, served build, fixtures/roles, environment/configuration, route, viewport, states and required outcomes. Preserve protected user changes. For supplied-reference work read [reference-to-code](reference-to-code.md); the reference's identity and allowed interpretations are inputs to review, not things the reviewer may silently replace.

Use the task's existing acceptance notes/feature map. If meaningful evidence would otherwise be ambiguous, use the optional [acceptance contracts](../references/acceptance-contracts.md) and planned [flow example](../assets/acceptance-flow.json). State required observations before implementation results are visible. Separate happy, invalid, denied, cancelled and recovery outcomes where material. Each outcome needs an owner, an observable check and a real evidence source; an unsupported/unrun check remains open.

For an existing verification map, compare it with actual user entry points. A feature may be reached through a button, keyboard shortcut, direct URL or persisted session. Do not cover only the easiest entry when the task depends on another. If the map describes intended but broken behavior, report a product defect; do not edit the map to erase the failure. A map/harness correction must itself be re-driven.

Choose a bounded scope: the requested surfaces plus dependencies and adjacent paths plausibly affected by the change. For exploratory QA, state the time/coverage boundary and prioritize core outcomes. After each meaningful observation choose the next probe from what it taught you; avoid blind checklists, repeated setup and arbitrary issue quotas. At a deadline report unfinished coverage while retaining already confirmed defects.

## 2. Establish a trustworthy running baseline

Use [browser and evidence](../references/browser-and-evidence.md) for the selected adapter, ownership, readiness and fresh observation loop. Confirm the exact app/build/profile/fixture before driving it. If the page surprises you, recheck that identity before diagnosing product code. A port answering or a tab in the expected position is insufficient.

Run available project-native parser, lint, type, build and focused test commands, recording the command, result and actual coverage. A regex scan, balanced delimiters or a successful helper invocation is not type/undefined-variable/security proof. Missing tools or unsupported languages remain untested. If a baseline already fails, preserve its output and determine whether the candidate causes a new failure; do not claim that a pre-existing failure disappeared without a same-condition retest.

Exercise one known-successful journey to show the fixture/environment is usable before challenges. Observe its actual result, not just page load. Then run the critical and negative cases through the normal user path. Arrange preconditions using isolated seed data, roles, supported flags or mock service boundaries; never inject the reported symptom with hidden state setters or DOM edits and call it a reproduction.

## 3. Functional acceptance

For each material flow: establish its starting state → perform one action → wait for the current outcome → observe fresh state → compare with the frozen expectation → read any durable effect. Record a pass, fail or blocked result with the evidence and missing prerequisite. Never promote “the click succeeded,” an unchanged URL, an old results container or a toast into task success.

Check the applicable slices below, not every conceivable feature:

- Navigation and forms: correct route/history/back behavior; input survives expected validation; errors identify the field and next action; submit uses current input; success reveals the actual result.
- Data states: loading, empty, one item, many items, error, partial and stale results; changed filters/reset; no-results differs from unavailable data; request cancellation and stale-response ordering where concurrent requests exist.
- Persistence: inspect the named result ID/value after reload and from another consumer if persistence/sharing is part of the requirement. The visible saved state and source-owned data must agree.
- Roles and trust: a synthetic denied actor cannot obtain the forbidden data or create the effect through the normal endpoint. Test the server boundary as well as hidden/disabled UI. Harmless untrusted text remains text; submitted IDs, ownership, redirects and uploads obey their declared boundaries. This is bounded fixture verification, not a penetration test of real accounts.
- Repetition/recovery: double activation, retry after a failure, interrupted request, reopen/cancel/reopen and back/forward follow the specified semantics. A duplicate click must not cause duplicate persistence when one effect is required. Read effect state before retrying an ambiguous mutation.
- External integration: mocks prove the app-owned seam only. Name the real provider/account path that remains unrun. A dry-run label does not prove no side effects; inspect what it actually touched within scope.

### Worked isolated catalog check

Freeze two seeded catalog items: C-12 belongs to “Lighting”; C-25 belongs to “Seating.” The editor can save, the viewer cannot. Search “lamp” plus category Lighting must return the exact agreed C-12 result, not merely a nonempty list. Reset must restore both IDs. An unmatched query shows a helpful zero-results state; a simulated unavailable service shows a retry explanation without claiming zero catalog items.

Activate Save for C-12 as editor. Observe the result and then independently read the isolated server-owned saved list: C-12 once. Reload, reopen from a second authorized browser, and repeat the supported activation to verify the specified duplicate behavior. As viewer, attempt the same supported endpoint; observe denial and read unchanged saved data. Simulate one permitted transient service failure, retry through the user control, and verify exactly the intended result. These observations distinguish actual product behavior from a toast, a disabled button or a fixture asserting itself.

Record the real expected and observed IDs/counts. Do not obtain the expected answer from the same function under test. A regression test should fail when the feature returns a wrong result, not merely when a mocked helper's call count changes.

## 4. Inclusive rendered behavior and visual craft

Capture and actually open fresh renders under matched content, viewport, state and theme. Inspect the full composition first, then affected details in their real surrounding shell. If an artifact cannot be decoded/viewed, mark visual proof blocked. A suffix, magic-byte header or successful screenshot API call is not image inspection.

Evaluate hierarchy and the primary action against the brief; typography/line lengths and actual copy; alignment, spacing and density; materials/color/contrast; image crop/quality; section rhythm; control states; mobile rearrangement. Use [visual craft](../references/visual-craft.md) for relevant decisions. Report concrete consequences rather than generic “looks modern” or a self-awarded quality score.

Drive keyboard entry, logical tab order, visible focus, accessible names, Enter/Space activation and Escape/dismissal where applicable. For dialogs, verify focus moves inside, stays appropriately contained, background interaction is prevented and focus returns logically. Test 200% text/zoom, narrow reflow, long localized content, accented/tall glyphs, zero/one/large counts and missing imagery when relevant. A horizontally scrollable data table can be appropriate; hiding a required action to eliminate overflow is not a fix. Automated accessibility checks supplement these flows and do not certify accessibility.

For meaningful motion, inspect live or recorded time, not just before/after images: interruption, rapid reversal, repeated open/close, regrab, cancellation, finish and focus. Confirm actual reduced-motion behavior preserves information and feedback; a static alternative is valid. Use existing project motion tokens and task-specific budgets. Longer purposeful drawers/toasts/holds or measured small layout-property transitions are assessed in context, not rejected by a universal duration/property ban. A daily work surface may appropriately remain static.

Desktop emulation proves the layouts/states it observes. Claims about mobile hardware keyboards, browser chrome, safe areas, touch/gesture coexistence or installed-PWA behavior require representative hardware where those claims are acceptance requirements. Name unavailable hardware as a qualification gap.

## 5. High-stakes visual gate

Only apply this gate when the accepted picture/reference is load-bearing or explicitly requested. Ordinary CRUD, diagnostic and spacing work still receives proportionate visual review without mandatory scoring or a spike.

1. **Target-locked:** use [design](design.md) to settle the actual visual authority, inspect the task-appropriate references, freeze first-glance identity and all distinct load-bearing traits and forbidden failures, view/state coverage, framing, medium/rejected alternatives, observable switch condition and actual author/builder identities. Resolve conflicting requirements before locking. The [visual contract](../assets/visual-contract.json) begins planned and cannot self-pass.
2. **Hero-spike:** implement only the representative highest-risk surface/interaction under that contract. A dashboard, gallery or immersive tool need not gain a literal hero. Keep unrelated secondary features frozen. Capture the required proof-slice views and states at the exact accepted conditions. A static image cannot establish load-bearing motion or an extreme interactive state.
3. **Visual-passed:** a genuinely separate reviewer inspects actual reference and current render side by side at comparable size and the temporal evidence when relevant. Give them the frozen brief, contract, source/build/reference identities and view/state matrix, not the builder's preferred verdict. They may ask for missing evidence. A host/person identity and actual assignment/report establish the separation; a new display name or `independent: true` does not.
4. **Full-build:** only after an accepted initial review, record its exact identity and implement the remaining authorized product. Keep the accepted reference/traits; preserve the spike receipt. A method switch or changed governing target requires a new lock and proof. A review from another version cannot authorize expansion.
5. **Final-reviewed:** capture the complete candidate with all required views/states and run a fresh independent visual review plus the applicable functional checks. Bind this review to the prior accepted proof slice and actual full-build receipt. An initial spike pass cannot be relabeled final.

### Frozen rubric

Before runs, freeze these bands and the accepted traits; never alter a threshold after seeing the candidate:

- **9–10:** first-glance identity, composition, form, material/light/atmosphere and load-bearing motion/state cues convincingly match the target; only non-contract polish remains.
- **7–8:** the target reads clearly and every accepted load-bearing trait, view and state holds; remaining differences are P3 polish. Seven is the minimum, not automatic acceptance.
- **5–6:** recognizable idea, but at least one required trait, accepted framing/state or first-glance read is materially weak. Repair or switch before feature expansion.
- **3–4:** the mechanism runs but communicates the wrong subject, medium, mood, scale or motion. Prefer a method switch unless one observable repair plausibly closes the gap.
- **0–2:** the target is not meaningfully represented or usable comparison evidence is absent. Missing viewable proof cannot be scored into a pass.

Compare identity/silhouette; composition/framing/scale/depth; material/light/color/atmosphere; load-bearing motion/default/extreme state; artifacts such as stretching, clipping, faceting, banding, placeholders and fake detail. Do not score from code, feature count, telemetry or a label that tells the viewer what the image was meant to be.

Canonical severity is semantic:

- **P0:** unsafe/deceptive/unusable result or invalid proof that prevents a trustworthy comparison, such as missing viewable evidence, stale candidate or fabricated independence.
- **P1:** wrong first-glance identity, subject, medium or composition; an accepted core trait is absent or a decisive forbidden failure is present.
- **P2:** a material weakness in any other accepted load-bearing trait, framing, view or state, including a “secondary” state. Material lighting, geometry or motion failures count when the contract makes them load-bearing.
- **P3:** non-contract optical/detail refinement that changes neither recognition nor the accepted requirements.

Pass requires at least 7/10 and zero open P0–P2 gaps. A 9 overall cannot hide a clipped accepted mobile action or an extreme state that breaks the required silhouette. A one-pixel non-contract shadow preference can be P3; it does not block on taste alone. An original source's “secondary miss” remains blocking if it violates an accepted requirement; do not migrate old severity names mechanically.

Below the gate, choose exactly the applicable next move: repair the proof slice and re-review; record a method switch with the observed failure and new approach; or report visual incompleteness. Observable switch examples: the shader cannot reproduce the silhouette; surface sampling facets at the required closest view; procedural state range cannot reach the accepted extreme; an asset cannot retain its crop at the accepted aspect. “Try harder” and raising the score are not method switches. Scope/budget or unavailable review may block further work; preserve the artifact and honest result.

## 6. Independent technical/product review

Web can conduct this review without Coding Studio. Read the repository's actual standards (AGENTS, CONTRIBUTING, CODING_STANDARDS or their real equivalent) and the accepted specification separately. Label a missing spec or standard unreviewed rather than inventing requirements. Cite a standards finding as rule plus affected hunk; cite a product finding as accepted requirement plus counterexample. Provide the reviewer the exact base/candidate pair, approved spec, scope/protected paths, public entry points and raw check evidence. Start two questions: does the candidate satisfy the intended behavior, and is its implementation safe, maintainable and proportionate? A second reviewer or optional collaborator is useful for a different expertise boundary, not as a vote-count ritual.

Trace changed behavior through connected callers, data boundaries and error paths. When APIs, persistent data, migration overlap, trust boundaries or a measured hot path change, read the relevant [architecture and errors](../references/architecture-and-errors.md) section: check old/new client and schema coexistence, backward compatibility, validation/authorization before effects, and workload-specific performance rather than issuing a generic architecture verdict. Look for an actual counterexample: a broken role guard, stale input, unsafe output, missing recovery, unintended scope, unnecessary abstraction/dependency, changed contract or insufficient regression proof. Read enough adjacent code to test the concern; distinguish an intentional design change from a real keyboard/focus/contrast regression. Review assertions as well as product code. Avoid style-only findings dressed up as release blockers.

Each finding names the requirement and file/route/state, the observed or reproducible counterexample, impact, evidence, confidence and smallest bounded correction/retest. Keep genuine blockers even when numerous. Reject unsupported findings with a reason; do not accept an implementer's self-grade as evidence. Report technical, product and visual verdicts separately, with partial/blocked coverage explicit.

If a pre-existing fix/commit may already solve the reported issue, compare baseline and patched candidates with the same symptom, fixtures and environment before authoring a competing fix. If repair is authorized, use [redesign](redesign.md)'s diagnosis loop or [build](build.md)'s behavioral seam, then replay the exact failure and an adjacent unaffected path. If review-only, return findings without edits.

## 7. Measurements and closure

For performance work, freeze the workload, correct expected result, machine/browser/build/configuration and timer boundaries. Count successfully completed work; a faster failure is not an improvement. Compare end-to-end behavior, inspect the suspected limiter, interleave baseline/candidate repetitions and report variation. Profile evidence plus a paired change can support a mechanism; a source hypothesis alone cannot establish causality. Do not claim field Core Web Vitals from a local lab run or use an aggregate health score to conceal untested categories.

After a change, determine which evidence depended on changed source, data, reference or capture conditions. Refresh those checks; retain demonstrably unaffected proof. Keep the original failure and superseded receipts. Do not overwrite an accepted screenshot path with different bytes and keep its old verdict. A new helper pass is only fresh shape/binding evidence.

Close each requested obligation with observed pass, confirmed failure, or a concrete blocker/unrun reason and next prerequisite. For implementation completion, all applicable functional/product, technical and visual requirements must hold. A visually passed build with failed functional flows remains incomplete. A final report identifies the exact candidate, real executed checks, failures/repairs, remaining gaps and requested delivery status. Use [deliver](deliver.md); a private preview does not imply deployment, and deployment success does not imply observed live health.
