Before acting, read [the host contract](../references/host-contract.md). It governs actual tools, authority, owned output roots, safe first Git reads, worker identity, and evidence.

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](../resources/prototype/LOGIC.md). Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](../resources/prototype/UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

- **“Will this evidence, structure, analysis, or explanation work?”** → [knowledge-work experiment](#knowledge-work-experiment). Build a source sample, worked analysis, draft fragment, or explicit audience simulation.

The branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules that apply to every branch

1. **Throwaway from day one, and clearly marked as such.** Set a question and observable success signal before building. Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user double-clicks. Either way, no thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No production test suite, no error handling beyond what makes the prototype _runnable_, no abstractions. Still execute a smoke/interaction check of the question being demonstrated; skip polish, not verification. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Capture it when done.** Save the verdict, question settled, evidence, and remaining uncertainty in an authorized durable decision artifact. Preserve the experiment as primary evidence in an owned artifact location. A throwaway branch/commit and issue pointer are optional when explicitly authorized, not automatic. Promote the validated decision or logic only within authorized implementation scope, with production tests and review; do not ship the throwaway shell. Preserve all user-owned files and variants pending a cleanup decision.

## Knowledge-work experiment

1. Write one question and the decision it will change. Choose the lowest-cost observable artifact: source sample for availability, worked analysis for method validity, outline for coverage, draft fragment for voice/structure, or audience test for comprehension. Define what would count as failure before producing it.
2. Select representative inputs including a difficult case. State selection limits and use original approved sources; keep raw source material intact. Record citations/locations beside the facts used. Sample size is a cost decision, not evidence of representativeness by itself.
3. Produce one small complete result rather than many unfinished headings. Expose the evidence, assumptions, intermediate calculations, or competing variants that determine the answer. Label invented sample data and simulated audiences. A simulated reaction is a hypothesis, never a real user test.
4. Inspect against the prior success signal and run a concrete check. For an analysis, independently work one result and examine units/denominators. For a draft, verify its claims against sources and test whether the intended reader can find the answer. For audience feedback, distinguish actual observed comments from your interpretation. Contacting other people or sharing a prototype requires separate authority.
5. Return a bounded verdict: proceed, change the approach, or insufficient evidence, with the observed reason. Capture what transfers to the durable deliverable and what does not. Stop when the question is answered; larger production work needs its own approved scope.

Example: “Can a one-page purchasing brief support a renewal decision?” Build one brief for one sanitized vendor case, with cost, constraints, and source-backed trade-offs. Success means every required decision input has a traceable source and the user can identify the trade-off; missing cancellation terms means the evidence question remains open. Do not generalize this single success to all vendors or fabricate customer feedback.

The user selects the winning UI variant or validates the domain decision. You may recommend and report test observations; never invent their preference or treat silence as a selection.

## Completion

Deliver the actual file or verified accessible local preview, one run/inspection instruction, observed checks, and the verdict or pending user decision. If browser/runtime access is unavailable, mark interactions UNRUN and give the exact prepared artifact; never imply the user has already tested it.
