# Ask Matt

Read the [host contract](../references/host-contract.md) before first repository access or action. This playbook runs only inside an explicitly selected Matt family workflow; source commands are not permission.

You don't remember every skill, so ask.

Before stating what a method does or recommending a step be skipped, read its complete linked playbook and applicable resources: the summaries here are for orientation only. Recommend the smallest useful route, explain why, then stop. Do not execute it unless the user also requested execution. Direct named-method execution is dispatched by the family entry, not by this recommendation method.

A **flow** is a path through the skills. Most paths run along one **main flow**, and several **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **[grill-with-docs](grill-with-docs.md)** sharpens the idea by interview. Recommend this when you have a **durable workspace and authorized document capture**: it's stateful, retaining what it learns in `GLOSSARY.md` and ADRs. (No working directory? Use [grill-me](grilling.md#grill-me) instead, covered under Standalone. Both run the same [grilling](grilling.md) primitive; `grill-with-docs` is the one that leaves a paper trail, which makes it useful when a paper trail is wanted and authorized.)
2. **Branch: can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **[handoff](handoff.md)** in both directions (a prototype lives in its own directory, which is exactly what [handoff](handoff.md) is for; see Phase boundaries):
   - **[handoff](handoff.md)** out, then open a fresh session against that file,
   - **[prototype](prototype.md)** to answer the question with throwaway code,
   - **[handoff](handoff.md)** back what you learned, and reference it from the original idea thread.
3. **Branch: is this a multi-session build?**
   - **Yes** → **[to-spec](to-spec.md)** (turn the thread into a spec), then **[to-tickets](to-tickets.md)** to split it into tracer-bullet tickets, each declaring its **blocking edges**. Then work the tickets one of two ways:
     - **[implement](implement.md)** per ticket, **`/clear`ing context between each one**. On a local tracker that's one file per ticket under `.scratch/<feature>/issues/`, worked blockers-first by hand; on a real tracker the edges become native blocking links, so any ticket whose blockers are done can be grabbed. Each ticket is self-contained, so the last one's context is disposable.
     - **[implement-spec](implement-spec.md)** for the whole spec in one run. It reads the tickets as a **task graph**, runs implementer subagents across the ready **frontier** in parallel, and lands everything on one **integration branch**. Reach for it when you'd rather orchestrate the build than drive each ticket yourself.
   - **No** → **[implement](implement.md)** right here, in the same context window.

   Either way, the code gets built by driving **[tdd](tdd.md)** (one red-green slice at a time) and closes out with **[code-review](code-review.md)**, a two-axis review (Standards + Spec) of the diff. [implement](implement.md) runs both per ticket; [implement-spec](implement-spec.md)'s implementers each drive [tdd](tdd.md), and it runs one [code-review](code-review.md) over the integration branch. Reach for **[tdd](tdd.md)** on its own when you just want to build a concrete behaviour test-first without a full spec, and **[code-review](code-review.md)** on its own whenever you want to review a branch or PR against a fixed point.

   When the work goes up as a pull request, **[pr](pr.md)** shapes the body: the smallest visual that shows the change, before/after evidence that it works, and a one-way or two-way door call. Within an explicitly selected Matt workflow, read it when drafting the requested PR body. It does not authorize publication.

4. **[retro](retro.md)** closes the loop. After a build, and especially one that went sideways, it looks back over the session and suggests changes to the agent's **environment**, not the code: navigation pointers, automated checks, the coding standards [code-review](code-review.md) enforces, steering files, tooling. Mechanical mistakes become deterministic checks; judgement calls become coding standards. The next build then starts from a better environment.

### Context hygiene

Keep steps 1–3 in **one unbroken context window** (don't compact or clear until after [to-tickets](to-tickets.md)) so the grilling, spec, and tickets all build on the same thinking. Each [implement](implement.md) then starts fresh, working from the ticket. Recommend [retro](retro.md) in the session it is looking back on before clearing; after clearing, use an accessible authorized session record, never restricted logs.

The source calls this the **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)** and suggests roughly 150k tokens. Treat that as a source heuristic, not a measured capacity guarantee for the current model; use actual host context availability and observed quality. If a session approaches it before [to-tickets](to-tickets.md), don't push on degraded; `/compact` at the nearest phase boundary and carry on (see Phase boundaries).

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → **[triage](triage.md)**. It moves issues through triage roles and produces agent-ready issues, which **[implement](implement.md)** later picks up.

  Triage is only for issues **you didn't create**: bug reports, incoming feature requests, anything that arrives raw. Tickets that [to-tickets](to-tickets.md) produced are already agent-ready, so **don't triage them**.

- **Something's broken** → **[diagnosing-bugs](diagnosing-bugs.md)**. For the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. It refuses to theorise until it has a **tight feedback loop** (one command that already goes red on *this* bug), then fixes with a regression test. Once the fix is in, run **[retro](retro.md)** in the same session to ask what would have prevented the bug; where the real finding is that there's no good seam to lock it down, that's a job for **[improve-codebase-architecture](improve-codebase-architecture.md)**.

- **A huge, foggy effort: a greenfield project or a huge feature build, too big for one session** → **[wayfinder](wayfinder.md)**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker and resolves them one at a time, producing **decisions, not deliverables**, until the fog is pushed back and the way is clear. Where **[grill-with-docs](grill-with-docs.md)** sharpens an idea you can hold in one session, wayfinder is for the idea you can't, and it's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **[to-spec](to-spec.md)**, which collapses the map's linked decisions into a buildable plan, then [to-tickets](to-tickets.md) and [implement](implement.md) as usual. Looping the map straight into [implement](implement.md) skips that collapse and throws the linked detail away, so go straight to [implement](implement.md) only when the effort turned out genuinely small.

## Codebase health

Not feature work, just upkeep.

- **[improve-codebase-architecture](improve-codebase-architecture.md)** can be recommended for explicitly requested codebase upkeep, to keep the codebase good for agents to operate in. It surfaces **deepening opportunities**; picking one _generates an idea_ you can take into the main flow at [grill-with-docs](grill-with-docs.md). It's the survey that finds the candidates; **[codebase-design](codebase-design.md)** (below) is the bench you design the chosen one on.

## Vocabulary underneath

Two explicitly loaded Matt references that run *beneath* the other skills, each the single source of truth for its vocabulary. Reach for them directly when the **words**, not the process, are the problem; or let the selected Matt methods above load them as dependencies.

- **[domain-modeling](domain-modeling.md)**: sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), record a hard-to-reverse decision as an ADR. It's the active discipline [grill-with-docs](grill-with-docs.md) drives to keep `GLOSSARY.md` a clean glossary.
- **[codebase-design](codebase-design.md)** is the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*: a lot of behaviour behind a small interface at a clean seam. [tdd](tdd.md) and [improve-codebase-architecture](improve-codebase-architecture.md) both speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the implementation, the QA. At the **boundary** between two of them you have five options, and picking between them is the fuzziest decision in this whole map:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window, when nothing here matters to what's next.
- **[handoff](handoff.md)** writes a portable markdown file. Narrow: only for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.
- **Subagent**: send a tightly-scoped task to its own window and get a report back.
- **`/compact`** compresses this context and seeds a fresh session with it. The **default**, at the bottom of the tree rather than the first reach.

Read [PHASE-BOUNDARIES.md](../resources/ask-matt/PHASE-BOUNDARIES.md) for the ordered tree: the five questions, the reasoning behind each branch, and why the primary-source cost makes **Continue** the one to rule out first. Make the decision **at** a boundary; mid-phase, continue or split the rest into subagents.

## Standalone

Off the main flow entirely.

- **[grill-me](grilling.md#grill-me)**: the same relentless interview as [grill-with-docs](grill-with-docs.md), but **stateless**: it saves nothing locally and builds no `GLOSSARY.md`. Reach for it when you are **not working in a working directory** (sharpening a plan, a design, a piece of writing, anything with no repo under it). If durable, authorized recording is useful, recommend [grill-with-docs](grill-with-docs.md); a directory's existence alone does not require writing files.
- **[grilling](grilling.md)** is the interview primitive itself: rounds, the frontier, facts are the agent's job and decisions are yours. [grill-me](grilling.md#grill-me) and [grill-with-docs](grill-with-docs.md) are the two named ways in, and [triage](triage.md), [wayfinder](wayfinder.md) and [improve-codebase-architecture](improve-codebase-architecture.md) all run it internally. Reach for it directly only when you want the interview with no wrapper around it.
- **[prototype](prototype.md)** is a small, throwaway program that answers one design question: does this state model feel right, or what should this UI look like. Throwaway is a constraint on how the code is written, not a promise to destroy it: the answer folds into the real code, and the prototype itself is kept as a **primary source** on a `prototype/<name>` branch out of main, pointed at from the implementation issue. It's the detour in step 2 of the main flow, but reach for it any time a design question is hard to settle on paper.
- **[research](research.md)**: delegate reading legwork to a **background agent**: it investigates a question against **primary sources**, then leaves a cited Markdown file in the repo. Keep working while it reads. The file it produces is something to take *into* the main flow at [grill-with-docs](grill-with-docs.md), since research feeds the thinking rather than replacing it.
- **[to-questionnaire](to-questionnaire.md)** comes in when the thing blocking you isn't in your head or the codebase but in **someone else's**, and it writes them a questionnaire to fill in. It's the inverse of [grill-me](grilling.md#grill-me): instead of interviewing you about the subject, it interviews you about the **send** (who it's going to, what you need back) and aims the questions at the gap. What comes back is material for [grill-with-docs](grill-with-docs.md) or [to-spec](to-spec.md).
- **[wizard](wizard.md)** is for the steps only a **human** can take: provisioning infrastructure, setting up credentials or CI secrets, clicking through an unfamiliar third-party dashboard, running a one-off migration or cutover. It generates an interactive bash script that opens each URL, captures each value, and writes it into `.env` and GitHub secrets, so the procedure stops being something you re-explain to an agent every time. Within the selected Matt workflow, recommend it for a genuine human-required step. Real credentials are entered and submitted only by the human in their own secure terminal or supported secure handoff. If the agent could safely do it within granted authority, recommend that simpler route; this is for where a human is genuinely in the loop.
- **[wait-what](wait-what.md)** is the corrective for a message that didn't land. Use it mid-conversation, inside any other skill, and the agent re-pitches what it just said with the context you were missing, in plain English, using the `GLOSSARY.md` vocabulary. It works after the fact; [grill-with-docs](grill-with-docs.md) is the upfront cure, because a shared language agreed early is what stops the jargon arriving at all.
- **[teach](teach.md)**: learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **[writing-for-agents](writing-for-agents.md)** is the reference for writing documents agents consume: skills, AGENTS.md, pointed-at docs.

## Precondition

**[setup-matt-pocock-skills](setup-matt-pocock-skills.md)**: recommend when tracker, domain, output or verification conventions are missing. Reuse existing conventions; do not require setup ceremony for a small settled task. Local tracking is the default when no tracker is configured; custom trackers also work.

## Knowledge-work and mixed routing

Route a small, agreed, one-session result directly to [implement](implement.md); use [to-spec](to-spec.md) for a multi-session contract and [to-tickets](to-tickets.md) only when multiple execution slices help. For knowledge work, each slice crosses gathering, analysis, drafting and verification to produce one observable result, not one document heading. Preserve claim-to-source evidence and inspect the actual final artifact surface. For mixed work, one shared acceptance surface requires both software and evidence/artifact checks. No external review-owner skill is required for this library to complete that review.

Writing exploration starts at [writing-fragments](writing-fragments.md), then [writing-shape](writing-shape.md) or [writing-beats](writing-beats.md). Software-only tactics include TDD, codebase design, code review and [resolving-merge-conflicts](resolving-merge-conflicts.md); do not force code tests onto prose. Research answers factual gaps; knowledge-work prototypes can be worked examples, sample analyses, draft fragments or audience tests. Read those method bodies before advising.

A missing consequential decision blocks execution rather than becoming an assumption. Reuse exact approvals already given; spec approval does not grant publication, assignment, commits, purchases, deletions or other external actions. Close with fresh evidence against the originating brief and a readable next step.
