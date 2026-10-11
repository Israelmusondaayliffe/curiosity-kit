# Short motion graphics

Make a design-led short graphic where motion communicates the idea: kinetic type, one number, charts, logo reveal, lower thirds, article/tweet/page highlights, asset-fusion or geographic shots. Often 3–10 seconds and sometimes up to roughly 30, with no required narration arc. Longer/narrated/reel work can use general-video or its source-specific specialist. Preserve the explicit brief even when it differs from a heuristic.

## Asset-aware production loop

Use one project with hyperframes.json (when that engine is selected), shot-plan.json, assets/index.md, compositions/index.html and requested renders/. The stages are draft direction → conditional sourcing → final design → build → inspect/repair → render/QC. Source before committing geometric design to an asset. On resume validate artifact identity and completeness, not simply file existence; an old render does not close a changed shot.

The [director](agents/director.md) explains both planning and asset-aware design passes. [Shot-plan IR](references/shot-plan-ir.md) is the exact editable handoff; [catalog map](catalog-map.md) and [motion vocabulary](references/motion-vocabulary.md) preserve the full recipe choices. Load the selected category module only:

- [Kinetic type](categories/kinetic-type/module.md): text scenes, emphasis, reading order and motion beats
- [Stat](categories/stat/module.md): value, prefix/suffix, label, ring/count-up with honest intermediate values
- [Charts](categories/charts/module.md): bars/line/pie/race/percentage with supplied data, axes and labels
- [Logo reveal](categories/logo-reveal/module.md): supplied mark and lockup, tagline/URL, appropriate hold
- [Lower thirds](categories/lower-thirds/module.md): names/roles/callouts/social overlays and safe placement
- [News](categories/news/module.md): real article content with keyword marker in place; retain centered 9:16 and full 16:9 article/photo/outlet/date branches
- [Tweet](categories/tweet/module.md): real author/handle/text/metrics, sourced avatar, accurate card
- [Webpage](categories/webpage/module.md): authentic captured page/UI plus target highlight region
- [Asset fusion](categories/asset-fusion/module.md): measured photo/object geometry becomes the chart/graphic
- [Maps](categories/maps/module.md): vector and real-basemap lanes, geographic projection, data fills, routes/pins/callout cards and attribution

## Draft shot-plan

Record category, positive duration_s/fps, canvas width/height/aspect, style, palette or derive-from-asset, font file/family/weight, beat units, export, source evidence and dominant motion idea. asset_needs is empty for asset-free form categories; otherwise each role has kind, query/source, treatment and required/optional status. User-supplied logo/image is a local source, not an excuse for a search. Basemap requests explicitly need map-bake; vector maps still need frozen geographic data/library availability.

The first question is whether the shot needs real source material. Form categories use provided content; source-led category choice may refine after retrieval. Use specific event/source queries for exact news/tweets, atomic queries for composable portraits/logos/objects; a failed exact query is not permission to substitute unrelated news. Preserve the request and report what remains unfilled.

[Source guide](phases/source/guide.md) specifies candidate review and actual adapter boundaries. The bundled media resolver handles local adoption and selected catalog image/icon/audio search. It does not implement news/web/tweet capture or a phases/source/resolve.mjs orchestrator. Use verified connectors/browser/capture capabilities for authentic text/screenshots and explicit adapters for transformations/generation. Availability is not authorization; do not silently change an asset-dependent category into asset-free output. An optional nonessential image can be omitted only consistently with the accepted plan.

## Ground and lock the design

Inspect kept candidates for use/maybe/reject and preserve path, provenance, rights and crop/treatment. Don't confuse the resolver's first result with curated selection. For asset-fusion, measure center/extent/safe/avoid zones, binding points and palette; use [grounding protocol](grounding/PROTOCOL.md) and its local overlay→region→final→mark helper. Always visually verify the marked box. Optional model localization requires an explicitly authorized supplied adapter; a key present in the environment is no permission.

Now finalize shot-plan around actual assets: named block plus customization, exact text/data, layout, focal geometry, motif, entrance/emphasis/exit, hold and beats. Top-level block/customize is canonical; source content.block/content.customize remains a recognized legacy alias with conflict resolution, never two competing values. Scene intervals partition [0,duration_s] without gaps/overlaps. Keep the main motion idea clear. A quick hook, ≥~0.3-second readable emphasis and small anticipatory beat offset are starting heuristics, not hard overrides of language/brief accessibility.

## Build under actual engine contracts

References to `hyperframes` or `npx hyperframes` mean a verified, already-installed executable; never use them to trigger an implicit package download.

[Builder](agents/builder.md) and [builder contract](references/builder-contract.md) retain layout-first rules, timing, deterministic seek behavior, palette discipline and render-critical details. Reuse installed registry blocks and actual animation recipes when they fit. The catalog is a selection reference, not proof that blocks are bundled. Author missing geometry/affordance behavior locally when suitable; do not invent a registry API. Installation requires its separate authority.

HyperFrames compositions use a sized root, exact composition ID, duration/fps/canvas, a paused registered finite GSAP timeline and source-local media. Delayed opacity/reveal and counters need arbitrary forward/backward seek tests under the selected host. Use fully visible static end-state first, then explicit entrances. Preserve planned duration on a repair. Transparent overlay export needs actual alpha-capable WebM support and alpha inspection; MOV support is version-dependent, not assumed. No native engine is bundled by the method.

Maps preserve both lanes. Vector work uses actual frozen D3/TopoJSON or supplied geometries. Basemap work needs puppeteer-core, browser, MapLibre/topojson/world-atlas and authorized tile/CDN retrieval, then FFmpeg. The helper validates coordinates/timing before loading dependencies, uses unique staging frames, refuses incomplete tiles/encode failure and writes provenance. It does not disable the browser sandbox by default. Inspect mainland/overseas filtering and antimeridian behavior; do not silently drop a politically/geographically important region. The screen-projected SVG overlay aligns only at the held camera. Keep on-screen attribution for current imagery terms; a provenance JSON is not visible attribution.

## Finish

Run actual lint/validate/inspect and headless snapshots at onset, hero, beat, transition and end, then draft render. [Finalizer](agents/finalize.md) performs bounded local repair; a fundamentally wrong concept returns to design, while small collisions/overflow/timing issues stay local. Verify readable content, values, source text, actual logo/path geometry, alpha and audiovisual timing. Re-render after edits and run delivery-QC. Share the actual current output and technical facts, with exact missing dependencies/UNRUN native checks. No title-card screenshot or generic montage proves full rendering parity.
