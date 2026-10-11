# Author one theme constitution

Read the chosen themes/<identity>.json only; it selects all default behaviors. For registry design/extension, consult themes/README.md and PORTING.md separately. Existing arbitrary cross-combinations are not automatically qualified.

The project theme.json accepts dna, width, height, fps, duration, lines (arrays of spoken words), optional minors, and optional hero. The compiler uses matte.fps when present. Transcript words must be nonempty, sequential and timed. Example shape:

    {"dna":"anchor","width":1280,"height":720,"duration":4,"lines":[["Make","every"],["word","read"]]}

For a selected climax:

    {"dna":"anchor","duration":4,"lines":[["Make","every"],["read"]],"hero":{"match":"word","occurrence":1,"text":"WORD"}}

The example is a schema illustration; actual durations and words come from the source transcript. Hero onset is the matched spoken token, its end follows the theme's hold and an optional hero.out. WordIndex is zero-based; occurrence is one-based. Omit hero entirely for pure-body output. Empty lines or all-hero/no-body are rejected because the preserved compiler needs a body endpoint. Inline setpieces require the hero in lines; embedded setpieces claim it independently, except panel redact linkage keeps it as hidden/revealed log text. Never duplicate a promoted word in the rail during its hero window.

The compiler's 23 body paradigms and 24 hero setpieces preserve timed entrance/hold/exit, deterministic seeds, foreground FX, linkages and post-composite plate behavior. Scene safe zones can position the hero and dock. Distinct fonts, fixed-slot paging, glyph metrics, short-word width fitting, body layer and theme parameters are artistic identity, not optional labels. Override only documented author fields and user-approved design choices; do not mutate bundled identity JSON to hide an engine gap.

Keep text separate from script, HTML, CSS, IDs and paths. Source text is script-safe serialized; display text can change spelling/case only through an explicit display override with source timing retained. Unavailable font/glyph metrics and external Nightcity licensing remain qualifications. Generated HTML expects pinned local _caption_gsap.js. Compiling HTML alone never establishes that browser animation, occlusion, alpha, color, motion or audio passed.
