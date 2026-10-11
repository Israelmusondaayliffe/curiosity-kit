Before acting, read [the host contract](../references/host-contract.md). It governs actual tools, authority, owned output roots, safe first Git reads, worker identity, and evidence.

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Read [codebase-design](codebase-design.md) for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion, and don't drift into "component," "service," "API," or "boundary."
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`GLOSSARY.md`) and any ADRs in the area you're touching first.

Then use one available independent leaf explorer to walk the scoped codebase, or explore directly when delegation is unavailable. The leaf returns evidence and does not dispatch this method again. Don't follow rigid heuristics; explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** from codebase-design: if removing a pass-through makes complexity vanish, it was shallow; if its responsibilities reappear across callers, it was earning its keep. Deepening should concentrate real behavior behind a useful interface, not remove a useful module merely to reduce file count.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to a fresh owned output path, using the host contract's durable-versus-temporary rules. Do not assume an OS temp path or desktop opener is user-accessible. Render/inspect with an available actual browser; otherwise check file structure and explicitly mark visual verification UNRUN. Deliver a supported attachment or verified accessible artifact, not merely an inaccessible cloud path.

Use inline CSS and inline SVG/HTML diagrams by default so the report works offline and discloses no project content to CDNs. A locally available trusted Mermaid renderer may produce inline SVG; otherwise use the hand-built patterns in the resource. Never claim CDN-dependent HTML is self-contained. Each candidate gets a before/after visualization.

If evidence supports no worthwhile candidate, report that honestly; do not manufacture friction. Label low-evidence ideas Speculative and identify what would validate them.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram**: side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use GLOSSARY.md vocabulary for the domain, and the `/codebase-design` vocabulary for the architecture.** If `GLOSSARY.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](../resources/improve-codebase-architecture/HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, read and follow [grilling](grilling.md) to walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Within authorized documentation edits, record decisions as they crystallize; read [domain-modeling](domain-modeling.md) to keep the domain model current as you go:

- **Naming a deepened module after a new concept?** Propose the term in the existing glossary (including compatible CONTEXT.md); add it only within authorized documentation scope. Create GLOSSARY.md lazily when authorized.
- **Sharpening a fuzzy term during the conversation?** Update the canonical existing glossary when authorized, preserving user edits.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing; skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Read [codebase-design](codebase-design.md) and use its design-it-twice parallel sub-agent pattern.
