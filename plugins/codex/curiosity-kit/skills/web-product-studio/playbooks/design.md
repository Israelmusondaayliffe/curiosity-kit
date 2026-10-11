# Design a coherent web experience

Use this method when visual direction is open, a comp is the requested artifact, or a load-bearing visual idea needs a bounded proof. [The entry](../SKILL.md) owns task authority and scope. For an approved screenshot or comp, start with [reference-to-code](reference-to-code.md); do not reopen its design by habit. Read the relevant parts of [visual craft](../references/visual-craft.md) when choosing or diagnosing the system.

## 1. Establish what the design must accomplish

Inspect the actual brief, existing page, project tokens/components, supplied references and available content. Describe the intended use moment: who arrives, what they know, what they need to notice, and their next action. Distinguish the surface's mode:

- Persuade: communicate value, provide earned evidence, make the next step clear.
- Operate: help repeated work, comparison and decisions with predictable controls and appropriate density.
- Read: sustain comprehension, navigation and comfortable text rhythm.
- Experience: make an image, simulation, story or interaction itself carry the meaning.

These modes can coexist on different surfaces. An immersive landing page does not justify hiding controls in the product. Ground mood and material in the audience's actual world: the objects, publications, tools and visual language they know. Industry or region is context to investigate, not a palette stereotype.

Write a small design brief in the existing task record: audience/job, primary and supporting content, desired first impression, constraints, assets, key states, responsive needs, open decision and intended deliverable. Identify the most important content with real examples before arranging empty rectangles. Keep unknown copy and assets visible as unresolved inputs under the entry's content-honesty rule.

When prior art would settle an open decision, inspect a small relevant set of actual reference or competitor surfaces. For each, record the observed route, viewport/state, content hierarchy, useful pattern and its fit or cost for this task. Compare the same user job rather than collecting attractive homepages. Distinguish rendered observations from remembered examples, inferred behavior and inaccessible/authenticated areas. Research can inform the choice; it cannot silently become the project's new authority or imply that a copied asset is usable.

## 2. Select visual authority, then a direction

Follow the entry's source precedence. Record the selected reference or existing system and its exact version. If an additional constitution is useful, choose one or none, with positive evidence, rationale and rejected alternatives. A precise supplied design usually needs no additional constitution. An optional named style skill may help only if its actual body is available and compatible; this method works without it.

For an open brief, derive a coherent system rather than combining every attractive example. Make mutually reinforcing decisions about:

- Hierarchy and composition: what receives attention first, how a reader enters and crosses the page, where action sits.
- Typography: display/body/label/data roles, proportions, measure and tone; a family may serve several roles.
- Layout and density: grid, content widths, grouping, whitespace, compact versus expansive surfaces.
- Color and material: semantic contrast pairs, brand emphasis, background depth and image grading.
- Components and imagery: shared controls, framing/crop rules, icon vocabulary, content-specific modules.
- Motion: what needs continuity or feedback; static is a valid choice. Use [motion and mobile](../references/motion-and-mobile.md) only when relevant.

Separate familiar affordances that reduce effort from deliberate departures that create identity. Name the benefit and cost of each meaningful departure: an editorial headline can strengthen recognition while consuming the first viewport; a dense table can improve comparison while requiring stronger grouping. Do not add a quota of unusual details. Record intentional exceptions so review does not mistake them for inconsistency.

For fonts, inspect existing files and license first. For a new family, verify its exact name, required weights/styles, usable source, license and loading method using actual local files or official sources. Judge a specimen in its intended role using the product's words, numbers and scripts. If verification is unavailable, keep the role/proportions provisional and use an available acceptable face; do not invent a font URL or block all layout work.

Read an existing design/token document completely before editing. Change only the intended decisions; preserve format, metadata, unknown fields, custom prose and unrelated tokens. An unfamiliar shape is not permission to convert it to a preferred schema. Where tokens use aliases, resolve actual value references and reject missing targets, group-only targets or cycles with the offending chain; do not silently emit a fallback value and call it the accepted token. Recheck affected consumers after an authorized token change.

## 3. Explore only a decision that is still open

When one draft would prematurely lock in a consequential layout or interaction, compare a small set of genuinely different answers. Choose the number for the decision and request; do not pad the set. Each direction gets a name, a divergent axis, its best use and its cost. Different hierarchy, layout, density or primary affordance counts; recoloring the same card grid does not.

Freeze the shared brief, content, viewport and criteria before comparing. Every candidate must stand on its own against those criteria; beating a weak candidate is insufficient. If using independent input, give the same brief and source facts without the desired winner. Read all finished candidates, choose one base, incorporate only compatible improvements and verify the synthesis as a new version. Record unavailable input without inventing agreement.

Choose the smallest instrument that answers the question:

- Wireframe for information order, navigation or grouping. Keep it intentionally rough so polish cannot conceal a weak structure.
- Full-size rendered variants for appearance or interaction. Use the real project shell/tokens with representative synthetic data.
- A logic prototype for state or data questions. Use [plan](plan.md) rather than treating different colors as answers to a state-model problem.
- Image comps for composition/material exploration when that is the requested or authorized medium. Images cannot prove control behavior.

The default implementation prototype lives on an isolated, dev-only route with authentic surroundings, or in a self-contained local HTML artifact when no project exists. A dev-only experiment on an existing route is an explicit justified exception. Keep production imports and real mutations out; use memory or a named scratch store if persistence is the question. Cheap construction does not excuse an unusable comparison.

For a variant picker:

1. Render one candidate at full size, with the same surrounding content and viewport. Thumbnails can orient; they cannot settle spacing or usability.
2. Make selection instant, label the active direction visibly and accessibly, and persist only valid selection in a URL parameter. Normalize missing, malformed, negative and out-of-range values to a real default before mounting.
3. Keep comparison chrome distinct from the product and clear of the evaluated surface. Provide visible buttons; keyboard shortcuts must ignore editable controls, composition events and held modifiers, and must not steal the product's keys.
4. Reset candidate-local state predictably when switching; add replay only when motion is being evaluated. Do not mask a broken initial render with a replay button.
5. Drive every reachable candidate and its important controls, check console output, and capture matched views. Include required long-content, empty/error and narrow states in the comparison.

Present actual artifacts, tradeoffs and a recommendation grounded in the brief. Ask for selection only when that decision remains with the user; prior authority to choose is sufficient. Bind a choice and comments to the exact candidate/round/content/viewport. A modified candidate is a new version, not a silent extension of old approval. Promote only the selected design through the real build and verification path. Retain or clean up owned prototypes under the delivery policy, without automatically deleting evidence or creating branches/issues.

## 4. Make reference imagery only when useful and authorized

Keep output modes explicit:

- Image-only request: deliver the requested comps/assets in the requested count, orientation and aspect ratio. A portrait hero stays portrait. Do not add a site build.
- Working-page request: deliver implementation. Optional generation fills an actual asset/design gap and must not replace the requested working result or a supplied authority.
- Existing reference: inspect it faithfully. Zoom and crops help read original pixels; newly generated details are new proposals, never recovered facts.

Before generation, confirm the available capability and applicable budget/permission under the host contract. Set the output plan to the user's intent. Separate primary deliverables from exploratory attempts and inspection details. A section-by-section set can protect readable typography; a full-page image can show rhythm; a detail frame can clarify controls. Choose deliberately rather than forcing a fixed section count or horizontal-only format.

Give each generation a complete brief: output type/dimensions, section job and content, selected source/version, dominant composition, type relationships, palette/material, media crop, CTA hierarchy, states, continuity constraints and explicit unresolved text. If several sections are requested, plan their rhythm together and carry the same token/asset family into each prompt. Use the menus in visual craft as options, not a combinatorial checklist.

Inspect every returned image at useful size. Check legible text, content truth, intended hierarchy, buildable proportions, continuity and the requested format/count. Extracted tokens are estimates until checked against the image and actual font files. Count saved successful artifacts from tool receipts, not a directory containing old rounds. Keep attempts and selected versions distinct using [delivery's non-overwriting preservation rule](deliver.md); report failures and remaining requested items. Resolve a selected artifact through its exact recorded identity; if missing or changed, stop that dependent use rather than substitute a nearby file. Regenerate only to address a specific observed gap within the authorized budget. When generation is unavailable, use an authorized rendered prototype or return the precise limitation; do not invent a generated result.

## 5. Lock the chosen system and prove its risky part

Record one first-glance sentence and check it against a fresh render: what does the eye actually find first, second and third, and is that the intended order? Name each major area by its job. If its purpose cannot be explained from the content and hierarchy, fix the structure before decorating it.

The design handoff should be sufficient to build without guessing: selected version and sources, layout/grid and responsive rules, type roles, palette contrast pairs, component/media rules, state requirements, intentional exceptions and remaining unknowns. Store actual values once in the project's canonical tokens or design record; prose explains use and rationale.

When the entry declares high visual stakes, freeze the target through [acceptance contracts](../references/acceptance-contracts.md) and follow the high-stakes gate in [verify](verify.md). Supply its references/permissions, first-glance target, required traits, forbidden failures, viewport/state matrix, framing, chosen/rejected medium, observable method-switch condition, identities and source bindings. Build only the bounded highest-risk visual slice until its independent review permits broader work. This can be a hero, scientific view, data-dense surface or interaction. Do not invent a hero for a product that has none.

Choose medium from the needed picture: DOM/CSS for editable layout and ordinary controls; SVG for crisp structured vectors; canvas/WebGL or another available rendering method when the actual effect needs it; image/video for approved fixed imagery where lack of interaction is acceptable. Record the limitation that would make the method fail. Example: a required orbiting camera exposes a flat compositing trick, so switch from layered imagery to a real spatial scene. Review uses the frozen meaning and evidence rules; neither a promising spike nor a token extraction is final product acceptance.

## Worked decisions

**One startup hero to implement.** Existing approved screenshot controls the layout. Extract its headline, action, frame and type relationships; inspect rather than regenerate. If only a brief exists, compare a compact product-led split with a typographic proof-led direction only if this resolves a real choice. Use verified product evidence, not invented logos. Build the selected hero with real controls and inspect the small-laptop first view.

**Two portrait section comps.** Preserve two primary outputs at the requested aspect. A quiet introduction and denser explanatory section may share type and palette while changing scale. No extra anchors or images are required. Inspect both and return the images; the task does not imply implementation.

**An eight-section product page.** First assign each requested section a job and available content. Alternate concentrated explanation with calmer transitions where that aids reading. A missing testimonial stays missing or is replaced by an approved form of proof, never fabricated. Produce the agreed reference format if requested, then translate and verify all sections if implementation is in scope. The number of generation calls is not a quality criterion.

*Adapted and substantially revised from GStack's Apache-2.0-derived design methods; see [NOTICE](../NOTICE).*
