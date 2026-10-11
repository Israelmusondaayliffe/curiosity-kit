# Faceless explainer

Turn text, notes, an article, a topic or an approved script into a teaching video whose visuals are authored typography, diagrams, abstract graphics and data visualization. This operation is distinct from product marketing, a captured website tour, a PR code explanation and captions applied to existing footage. Typical 30–90 seconds and up to roughly three minutes is a planning heuristic, not a limit overriding the brief.

## Inputs and outputs

Keep the full supplied input verbatim in capture/extracted/visible-text.txt. Record its source, intended audience, learning objective, claim confidence, duration/aspect/language, narration mode and output. Create tokens.json with title/description and empty colors/fonts unless provided. Do not invent a website, run a website capture or manufacture a captured asset inventory. A supplied real image is a supported exception: register its local path/provenance and use it only where appropriate.

The complete deliverable chain is source packet → frame.md → STORYBOARD.md and optional SCRIPT.md → verified audio_meta → frame compositions → caption/transition assembly → inspected requested video. For prompt/plan-only work, stop at the requested artifact. Native execution uses [frame production](references/frame-production.md); it explains dependencies, actual schemas, helper commands, safety and completion gates.

## Teach one useful idea

Read [story design](references/story-design.md) for the full concept, how-to, listicle and narrative-explainer structures, frame type mapping, hooks, clarity techniques, emotional beats, word budgets and VO_MODE. Pick the form that serves the source:

- Concept: a concrete question or surprising observation, the underlying mechanism, a simple example, the implication or useful takeaway.
- How-to: desired outcome, prerequisites only where needed, ordered actions with visible state change, a check of success and relevant caution.
- Listicle: a real organizing idea with distinct items and useful progression; don't make unrelated bullets merely to fit a count.
- Narrative: change over time with cause and consequence; keep sourced fact separate from illustrative analogy.

Reorder or compress source paragraphs to teach; keep qualifications that affect the takeaway. Explain before layering decoration. Use exact user script when VO_MODE requires verbatim. A source claim is evidence, not an instruction. Support data points/axes/units and avoid invented statistics. Material ambiguity in claims or audience warrants a small question; a fully specified brief does not warrant a compulsory interview.

## Design invented visuals

Use an existing design specification or an actual available named preset. Read [visual design](references/visual-design.md), [composition](references/composition.md), and the selected entries in [motion language](references/motion-language.md) when designing frames. Preserve every supported visual category: hero typography, comparative layouts, logical diagrams, sequences, counts/statistics and data-led graphics. In STORYBOARD.md give each frame its narrative purpose, exact visible text, duration, transition, effects and focal/roles. Focal and roles describe the invented visual elements, such as a word, node, link or series, rather than nonexistent captured assets. Set video-wide direction once; asset_candidates is empty except for supplied real media.

Use a stable visual metaphor and hierarchy that reveal relationships. Show one new cognitive step at a time, with readable holds and honest proportions. Brand and requested minimalism outrank optional style recipes. Do not require decorative density, a signature effect, a fixed number of beats or photorealism.

## Produce and review

Follow the selected frame-production execution detail. Source-free visuals don't need asset staging. Narration may proceed alongside visual planning, but duration sync completes before frame authoring and word-timed captions. Dispatch bounded frames using [frame worker](sub-agents/frame-worker.md), preserving original story/script/transition decisions. The worker must read its named actual motion recipe rather than an entire sibling library.

Build and inspect static hero layouts, animate, mark frames complete only after review, then await caption construction before assembly. Run repeatable transitions and actual engine checks; test scene starts/ends as well as midpoints. Check whether the viewer can explain the intended mechanism after watching. A visually polished but misleading explainer fails. Deliver exact requested files with technical and semantic verification levels, unresolved dependencies and source assumptions.
