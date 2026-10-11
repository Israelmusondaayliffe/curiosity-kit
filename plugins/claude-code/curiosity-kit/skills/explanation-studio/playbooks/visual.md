# Make the relationship visible

Use for diagrams, visual ELI5, an algorithm walkthrough, causal explanation, standalone HTML or an educational simulation. A visual must answer a question. Decoration is not a teaching mechanism.

## Prepare the meaning

Ground the explanation with [explain](explain.md). Choose the relevant [pattern](../references/patterns.md). State the central relationship in one sentence for yourself. Identify what would become false if removed: a condition, direction, distinction, scale, uncertainty or boundary.

Use the requested medium directly. A small diagram can be enough. Do not build a website because the topic has several parts. Conversely, a requested HTML artifact needs an actual accessible file, not a description of what one could show.

Choose the visual grammar that carries the relationship:

- Arrows show an explicitly labeled flow, cause or handoff. Do not use the same arrow style for causation and mere association without a legend.
- Position/grouping shows containment, order or ownership. Keep a consistent direction.
- Before/after uses comparable scale and orientation, or labels the change.
- A sequence shows who acts, the condition and the returned result.
- An algorithm runs a concrete input through visible transformations.
- A tradeoff compares real alternatives against the same priorities, including the accepted cost.

For an analogy, use [bridge](bridge.md) first. The visual must show or explain where the mapping stops.

## Build only the necessary layers

Begin with the smallest complete relationship. For a complicated system, redraw known elements and add one meaningful relationship or part per stage. Keep labels and positions stable so the reader sees what changed. Stop adding frames when they stop teaching; a two-part fact does not need three staged pictures.

The first view should communicate the main point without a click. Deeper panels can add actual identifiers, implementation, metrics, assumptions or a failure branch. Map those details back to the visible concept. Do not hide a warning or essential qualification behind an optional disclosure.

Use large legible labels, sufficient spacing and direct connections. A central visual is usually better than a wall of equal-weight cards. Avoid tiny node maps, arbitrary animations and decorative statistics. When a picture cannot carry a condition, put a short sentence beside the relevant element.

Mark observed, inferred and unknown relations with words or line patterns, not color alone. Include a useful text equivalent of the visual for readers who cannot see it. That equivalent need not repeat every decorative mark.

## Construct a standalone artifact

[assets/standalone.html](../assets/standalone.html) is a working self-contained example and adaptable starting point. Inspect and replace its topic, labels, explanation, technical depth and limitation. It is not a template whose sample content can be left behind. You may write simpler HTML directly when that better fits the task.

Use semantic headings and a main landmark, an appropriate language, viewport metadata and a real title. Prefer inline CSS/SVG, system fonts and native controls. A promised standalone file must carry its required assets; a neighboring stylesheet or a CDN is a dependency even if it works on your machine. A normal source citation is navigation, not an automatically fetched display asset. Clearly label external source links and never follow or fetch them automatically from the artifact.

A native `details` disclosure often supplies all the interaction needed. Use JavaScript only when changing a variable or stepping a process genuinely teaches the idea. A live API or remote model call is unnecessary for a small deterministic illustration and may introduce costs or private-data exposure.

## Make controls explain something

For each control, define the input, allowed range, expected result and reset state before implementing it. Label units and assumptions. A slider that changes color but not the claimed mechanism is decoration.

Use a simple explicit model. If the model assumes constant arrival rate, unlimited storage or equal task duration, say so. Keep approximation distinct from measured system behavior. Compare at least two hand-computed cases with the displayed result. Test the minimum, maximum and reset. For step controls, check first, intermediate and terminal states and repeated clicks.

Use actual buttons and labels, visible focus, keyboard access and readable feedback. Respect reduced-motion preferences. The explanation should remain understandable when animation is paused or reduced. Never equate a control response with correct logic or learner understanding.

## Inspect what the reader receives

Read [review and tools](../references/review-and-tools.md). For HTML, run the local checker through its documented absolute path. Address structural findings and review warnings. Then open the actual saved file through an available browser, not a different draft.

Inspect a narrow phone-sized viewport and a wide one. Check labels, clipping, line crossings, reading order, scrolling and essential qualifications. Intermediate widths are useful if the layout changes. Do not claim a numeric viewport check unless that viewport was actually set or measured. Keyboard-test controls; inspect their results. Check relevant network behavior if claiming operation without external resources. Static detection is not exhaustive offline proof.

For a rendered image, inspect the pixels. Verify text, arrow direction, legends and cropping against the source. An image tool's completion status is not visual review. For editable formats, test that the promised elements are actually editable; an image embedded in a scene is not an editable diagram. Deliver source alongside rendering when requested and supported.

If the browser or renderer is unavailable, keep the useful authored artifact and perform available structural/content checks. State that rendering or interaction remains unverified. If the requested output cannot be produced, provide an honest partial explanation or plan, not a fake artifact link.

## Repair and finish

Repair a wrong relation before adjusting decoration. If the first view is crowded, remove secondary elements or separate them into another useful stage. If a label needs a paragraph, improve the underlying concept order rather than shrink the font. If a model result is wrong, fix its rule and rerun the affected cases.

Return the actual visual with a brief orientation and material limitation. Do not automatically publish, open external services, generate paid media or create a course. A complete artifact is not proof that the reader learned it; use actual learner evidence only when the task includes that check.
