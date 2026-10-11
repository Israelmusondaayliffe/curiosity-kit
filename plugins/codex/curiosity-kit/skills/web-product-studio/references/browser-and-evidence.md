# Browser work and evidence

Load when a real browser observation or user interaction is needed. Reuse the current host's supported browser or existing project harness. This method does not install GStack, Playwright, PStack or REA, copy sessions, launch a debugging transport, or grant authority to real accounts. Host routing and permissions remain with [host contract](host-contract.md) and the skill entrypoint.

## Select one adapter and bind the instance

1. Identify available capabilities and read their current usage instructions. Prefer a supported host browser or the repository's already installed verification harness. Do not assume a donor CLI, wrapper path, browser binary, package manager or model exists here.
2. Confirm what the adapter can actually do: navigate/read snapshot; click/fill/select/check; keyboard/hover/drag/scroll; resize; inspect URL/DOM/accessibility; capture screenshot/video; read console/network/trace; manage owned tabs; reset isolated state. Select only capabilities required by the task. Include file inputs/uploads, form submission, native alert/confirm/prompt dialogs, popup/new-tab handling and PDF capture when the workflow needs them and the adapter supports them; these capabilities do not grant permission for their effects. A missing video API does not mean all browser work is unavailable.
3. Establish the app using its documented authorized start/build command. Record the process/session you own, exact origin/port, actual app marker and build ID, synthetic dataset/role and browser profile. A successful response from port 3000 is not proof it belongs to this checkout. Inspect a stable app/build marker and the owned server log or receipt. If another process owns the expected port, stop attribution and choose a scoped solution rather than driving an unknown app.
4. Read the relevant feature map or source-backed user route. Discover stable roles/labels and supported test hooks in this app. Do not copy generated CSS classes, hashes, child indexes or selectors from a different project.
5. Record the actual browser/version, viewport and device scale, locale/timezone, theme, motion preference, relevant font readiness, authentication role and fixture state. Keep baseline/candidate conditions matched. If the task needs service workers, storage or offline behavior, verify the adapter supports those conditions without silently resetting them.

Use a separate browser context/profile and separate server data for independently mutating tests. Browser isolation alone does not isolate a shared database; distinct tabs are not distinct identities. Parallelize independent source readers or isolated instances, not concurrent drivers of the same mutable session. Where a truly shared instance is necessary, one owner drives it.

## The smallest meaningful interaction loop

- **Baseline:** read the current route and fresh snapshot; capture before state when it matters. Confirm preconditions and readiness from this instance.
- **Action:** perform one user-visible structural action with a current role/label/ref. Coordinates require an immediately fresh screenshot and a visible target. Reacquire references after navigation, layout or DOM changes; never blindly reuse an old element token.
- **Wait:** wait for a bounded predicate belonging to this action: the current query's response marker, expected item ID/count, resulting route, a settled dialog, changed save revision or specified error. An already-visible results region and a generic network-idle wait may be unrelated to the current action. Choose explicit action/navigation/startup deadlines and an overall task boundary; a tool's zero timeout may mean unbounded, not immediate failure.
- **Observe:** take a new snapshot, relevant DOM/accessibility result and actual screenshot/temporal capture. Read the actual value, result or source-owned effect; avoid a stale cache or a status label used as its own proof.
- **Assert:** compare against the predetermined literal expectation or accepted source. Classify pass/fail/blocked with the scope of evidence. Capture the discriminating state, not just setup/loading.

When a tool batches a full flow in one session, retain per-action observations and stop dependent actions after a failed prerequisite. When a tool closes tabs between calls, keep a bounded complete flow in the supported session or reopen from known state. Verify its actual result contract: some wrappers return transport exit 0 even when the embedded operation failed. Require the tool's explicit success/complete receipt and check errors; do not invent a sentinel the tool never promises.

### Concrete search/save probe

From the seeded catalog's ordinary route, snapshot the filter controls. Enter the frozen query, activate Search, and wait for the response marker for that query, then assert the agreed result IDs. Capture that state. Open one result using its real control, Save, and observe its visible confirmation. Then use the source-owned read-only result endpoint or isolated store to confirm the saved ID/value, reload and reopen from the second consumer when sharing/persistence is required. The last screen alone does not prove persistence. A denied-write test repeats this public seam as the denied synthetic actor and verifies no effect.

## Readiness, failures and safe retry

When an unexpected observation occurs, first “doctor” the instance: process alive, correct build/origin/app marker, valid isolated role, correct fixture, browser still attached, readiness predicate appropriate. Preserve the first failed output before reset. Separate a product defect from setup failure, harness drift and unavailable account/hardware state.

A stale locator can justify a fresh snapshot and one newly targeted retry when no ambiguous effect occurred. An uncertain save/payment/message must first be read back; lack of a local receipt does not authorize duplicating the effect. Retries remain within the original action's authority and the task's bounded scope. Repeated unchanged failures call for a new hypothesis, not a timeout increase or clicking again.

For a confirmed defect, minimize the user path without removing the triggering condition. Reset the isolated fixture and independently reproduce it when practical. If a required environment is unavailable, a translated check is useful only when it tests the same mechanism; label desktop layout evidence separately from hardware-specific behavior. Re-run a harness fix live before relying on it. Preserve confirmed findings even when later capture/minimization is blocked.

## Choose the artifact that answers the question

- Screenshot: composition, crop, clipping, material, typography and visible state. Save fresh paths, bind build/viewport/state, then decode and open the image. A header or digest cannot establish viewability. Compare at equal intended sizes; screenshot dimensions alone do not reveal CSS viewport/DPR.
- DOM/accessibility snapshot: labels, roles, values and semantic state. Presence is not visibility; accessibility structure is not pixel appearance or complete accessible interaction.
- Live/recorded interaction: focus, timing, interruption, gesture, animation and transient states. Capture the full action through the discriminating result, not endpoints alone.
- Network evidence: exact transaction/request ID and current response matched to the triggering step. Two requests to the same URL are separate transactions; a late body belongs to its original event, not whichever step received it. Observe independently known fixture outputs. Do not refetch a missing original response and call it the captured response.
- Source-owned durable readback: stored row/file/result or response from the production seam under the synthetic fixture. It complements the user path; internal setters do not replace that path.
- Console/trace/profile: contextual diagnostics. Preserve enough trace around reproduction to locate the issue; a clean console does not prove the product works. A performance trace must correspond to the actual workload and candidate.

Record whether each selected surface is complete, limited to the attach window, filtered, truncated, unavailable or not requested. Absence before capture began is unknown. A completed URL-only capture says where the page ended, not whether search results rendered. Missing selected data prevents an equivalence claim; a witnessed difference can still be reported while other coverage remains unknown.

Network headers/bodies, DOM text, accessibility names, scripts, screenshots and URL queries can contain private data. Capture the minimum selected surface, use synthetic inputs, exclude secrets and authentication state, and inspect the actual export before sharing. Redaction changes the represented bytes: state whether a digest covers original, decoded or redacted content. Dedicated profiles and origin filtering are useful boundaries, not an OS/network sandbox.

## Freshness and comparison commitments

Use [acceptance contracts](acceptance-contracts.md) for exact optional record shapes. Keep the full action/locator/input/environment/fixture contract, source and reference identities, current served build and artifact identities. A timestamp or an unchanged filename cannot establish freshness. A capture receipt establishes only the claims the real capture tool actually provides; a locally filled metadata file is corroborating notes, not authenticated provenance.

For before/after comparison, align unique step IDs with identical action kinds, inputs, states and acceptance conditions. Check browser/version/origin plus the full experiment, not only outputs. Missing/duplicate step IDs or changed actions make that comparison invalid. Freeze any permitted normalization before seeing the results: exact value, artifact kind and reason, such as a synthetic fixed clock or randomized fixture ID. Do not remove whole DOM sections, error text or changed content to manufacture equality. Preserve raw evidence and normalized output separately.

Distinguish:

- **Refactor parity:** same frozen source behavior/pixels under controlled renderer, fonts, viewport/DPR and data. Pixel diffs may find changed areas; inspect them for intended versus unintended change. Baseline regeneration is an acceptance decision, not a test repair.
- **Reference recreation:** accepted composition/content/material with explicit tolerances and responsive interpretation. It need not be pixel-identical to an image from another rendering environment.
- **Behavioral comparison:** exact visible and durable results for the exercised contract. Equal screenshot hashes cannot prove equivalent focus, network, persistence or unobserved states.

Image metrics help locate differences; they do not judge image quality, likeness or whether a crop hides a required control. Review real images and interactions independently where the gate requires it. Change to source/reference/fixtures/settings invalidates affected receipts; review dependencies before reusing unaffected proof.

## Optional reconstruction when delivered behavior and source disagree

Ordinary complete-source web work does not need REA or a recovered graph. When a shipped bundle, missing source or unexplained delivered build makes reconstruction useful, use an already available authorized specialist only for the concrete question. Begin with bounded inventory and passive observation. Passive attachment does not authorize navigation, evaluation, clicking, state seeding, WebMCP invocation or browser control. Active scenarios need explicit target/action/data/lifecycle scope and the current host's authority.

Keep static evidence, runtime presence and causality distinct. A recovered route/import/endpoint is a hypothesis for a browser probe. A bundle observed as loaded does not prove each embedded module initialized, a feature ran or an endpoint was called. Prefer captured byte identity plus matching location. Unique exact bytes may reconcile identity; ambiguous duplicates stay ambiguous; mapped paths cannot override conflicting bytes. Source maps describe a mapping, not the original bytes executed. URL/path mappings never broaden filesystem/origin permissions.

Choose relevant captures once, reuse their explicit evidence IDs and inspect narrower projections rather than repeatedly rerunning broad analysis. Preserve contradictions and unresolved coverage. “Not observed in this complete scoped capture” never means globally absent. If optional instrumentation changes execution, report that condition and its time/window; it is not passive proof.

Before any optional adapter adoption, verify actual capabilities and liveness against its implementation/tool behavior. In particular, do not trust documentation that promises finite waits when configured timeouts are zero; provide a bounded wrapper/cancellation through supported host controls. Connect-mode adapters may change emulation/storage/service workers; confirm scope and restoration rather than claiming generic read-only attachment. A version discrepancy blocks the affected adapter claim, not ordinary supported Web work.

## Teardown and durable result

Stop only owned processes, tabs, profiles, sessions and debug transports, using their actual handles. Never kill by process name or close unrelated user tabs. Cleanup applies after failed iterations as well as success, but evidence survives it. Inspect the named output files after teardown. Report any still-running/unknown resource and why; do not claim cancellation succeeded from an issued request alone.

For a reusable verification recipe, test its own launch → identity check → real mapped feature → evidence → cleanup path before calling it operational. Reuse an existing maintained recipe rather than generating a new skill/controller by default. Return the exact candidate, performed actions, observed result/effect, evidence and limitations to the single Web owner.
