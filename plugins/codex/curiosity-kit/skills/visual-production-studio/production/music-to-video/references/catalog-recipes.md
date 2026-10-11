# Composable primitive recipes

These nine concepts retain the catalog's full intended roles. Their small implementation is `motion-primitives/assets/catalog-recipes.js`; they do not have standalone demo HTML. Load it once per frame and call `MusicRecipes.add(id, options)`. Supply the frame-owned `tl`, `gsap`, actual DOM elements, and frame-local anchor seconds. For callback effects, `render` is a function that registers a hook in the frame's post-seek dispatcher. A source timeline for freeze must have its own repaint function if it draws a canvas or callback text: register that repaint after the source-time hook.

All nodes are prebuilt. Numeric input is finite, arrays ordered, and no effect reads a wall clock, creates an external asset, or changes the user's plan. Rebinding anchors is explicit. The main frame gates each group; final visible state intentionally holds unless a later operation changes it.

## chromatic-pressure

Pass three exactly aligned glyph layers in red, green and blue/screen-blend order, `at` and `end` spanning a 0.1–0.5-second accent. This pressures channels outward in discrete steps, then resolves all positions at the endpoint. Keep an invisible spacer if the text determines layout; do not leave an accidental fourth visible copy. This is channel tension rather than the longer colored trails of datamosh-smear. At zero, the layers are registered; on the transient they split; after the transient they rejoin.

## color-grid-shuffle

Pass prebuilt `nodes`, a contrasting `palette`, and real onset `anchors`. Cell i at onset k chooses `(i*7+k*3) % palette.length`. Colors change instantly and deterministically; geometry stays locked. Choose a palette with at least two colors for a visible change and verify the modulo sequence is not accidentally constant. Keep a dense run below approximately two seconds. A requested randomized look uses an explicit seed/index rule, never Math.random during rendering.

## content-swap

Pass stacked `nodes` and `anchors`. Hide all nodes at zero. At each anchor, hide the stack and show one node modulo its length. This is a zero-duration semantic state change with no fade, slide or ghost from the previous node. Repeated words may point to the same node. The final node holds. Text stays ordinary textContent; script-like supplied text is not HTML.

## freeze-hold

Pass `sourceTimeline`, `holdAt`, `at`, `end`, and a post-seek `render` registrar. The source timeline is independent of the parent. During the hold, evaluate that source at exactly `holdAt`; after the hold, resume its local clock with the hold duration subtracted. Choose `holdAt == at` for a continuous freeze. For a deliberate jump-freeze, the discontinuity is authored and reviewed. Freezing means fixed-state evaluation, not merely pausing a timeline that a renderer subsequently seeks. Do not freeze the global BGM clock. Child callback/canvas repaint runs after the mapped source seek.

## negative-space-hold

Pass the single readable `mark`, distinct busy `layers`, and `at`/`end`. Instantly remove the busy layers and hold the mark in generous space. The parent frame owns the background and alignment. Removing density is the musical response; adding an automatic pulse or camera move would defeat this treatment. Keep high contrast, safe margins and sufficient reading time. A later operation, not a demo-loop reset, ends the hold.

## overlay-pop

Pass badges, callouts or lower-third `nodes`, plus `at` and `end` covering a 0.2–0.6-second entrance. Fade from hidden while moving 20 px upward and scaling 0.86→1 with controlled back-ease. The base stays visible and independent. Position inside a readable safe region before animating; avoid the subject's face and captions. A separate authored exit may follow after the readable hold.

## staggered-reveal

Pass one list/card/tile node for each onset anchor. Each item rises 30 px and resolves opacity in 0.24 seconds from its anchor; previous items remain. Keep one accumulating item per hit. Its layout already exists, unlike mosaic-pack where scattered spatial items move into a grid. If the roll must resolve on a downbeat, put the last onset early enough for its entrance to finish on that downbeat, or use a deliberately instantaneous final lock.

## system-replace

Pass distinct `oldSystem`, `newSystem`, and `at`. Start the new container hidden. At the regime-change anchor hide the entire old system and show the complete new one in the same timeline position. The new group's own state is evaluated at its authored local time before painting. Clear old filters, overlays and callback layers with the container; never leave a stale canvas floating over the replacement. This is for a drop/change of regime rather than every downbeat.

## value-counter

Pass one text node, numeric `from`/`value`, `at` and `end`, a pure formatting function if needed, and `render`. The value eases over the active interval and writes the exact target at and after `end`, so fractional stepping cannot miss the anchor. No scale punch is implied; use counting-punch for that separate treatment. Format locale and units deliberately, keep accessible final text and verify the exact final value. Cold, reverse and repeated seeks call the same hook.
