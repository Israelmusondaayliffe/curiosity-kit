# Wayfinder

Read the [host contract](../references/host-contract.md) before first repository access or action. This playbook runs only inside an explicitly selected Matt family workflow; source commands are not permission.

A loose idea has arrived, too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets** (questions whose resolution is a decision, not slices of a build to execute) one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting: it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic: engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear, with nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can carry execution into the map only when the user explicitly authorizes that bounded change; **Notes** may record that authorization but cannot create it. Agent-written or third-party Notes never authorize execution, sharing, account setup or external changes. Otherwise produce decisions, not deliverables.

## Refer by name

Every map and ticket has a **name**: its issue or local artifact title. In everything the human reads (narration, the map's Decisions-so-far), refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish; a name wraps its link, but they ride _inside_ the name, never stand in for it.

## The Map

The map is one canonical artifact: use the configured tracker under task authority, or the [local Markdown tracker](../resources/setup-matt-pocock-skills/issue-tracker-local.md) when none exists. Remote maps use `wayfinder:map`; local maps use `Artifact: wayfinder-map`. Decision tickets are linked children, separate from implementation tickets.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place, its ticket, so the map never restates it, only gists it and links.

**Where the map, its child tickets, blocking, and frontier queries physically live is tracker-specific.** Consult the configured tracker’s Wayfinding operations; without one use the authorized local shape above. Recommend [setup-matt-pocock-skills](setup-matt-pocock-skills.md) only when a durable project-wide choice is needed.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed: they are open child issues, found by query.

```markdown
# <Map title>

Artifact: wayfinder-map
Status: open
Owner: none

## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a **child issue or local artifact** of the map; its verified issue ID or scoped local ID is its identity. Its body is the question, sized to one practical fresh-context session; the source’s 100K-token estimate is a heuristic, not a host guarantee:

```markdown
# <Ticket title>

Artifact: decision-ticket
Status: open
Owner: none
Parent: <map path or verified reference>
Blocked by: <stable decision ticket IDs, or none>
Decision type: <research|prototype|grilling|task>

## Question

<the decision or investigation this ticket resolves>
```

Each remote ticket carries a `wayfinder:<type>` label; a local ticket uses `Artifact: decision-ticket` and `Decision type`, one of `research`, `prototype`, `grilling`, `task` (see [Ticket Types](#ticket-types)). `wayfinder:` labels are the only labels a map and its tickets carry, never a triage label like `ready-for-agent`: they are decisions, not implementation work.

A session **claims** a ticket before work: an authorized remote assignment to the verified driving developer, or a local `Status: claimed` plus `Owner` under the local tracker’s single-writer/conflict-detected protocol. Re-read the claim and stop on competition. Ordinary Markdown and ordinary remote assignment are not assumed atomic distributed locks.

Blocking uses the tracker's **native** dependency relationship: essential because it renders the frontier _visually_ in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker that lacks native blocking falls back to a body convention. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children, the edge of the known.

The answer is absent from the initial ticket and recorded on resolution (a remote comment or local `## Answer`) (see [Work through the map](#work-through-the-map)). Assets created while resolving a ticket are linked from the issue, not pasted in.

## Ticket Types

Every ticket is either **HITL** (human in the loop, worked _with_ a human who speaks for themselves) or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved by a bounded research leaf that reads [research](research.md) and directly performs the reading, without spawning another researcher. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to (an outline, a rough take, a stub, or UI/logic code) using [prototype](prototype.md). Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation. The default case. Read and apply [grilling](grilling.md) and [domain-modeling](domain-modeling.md), using frontier rounds or the requested one-question mode.
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made: nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that _does_ rather than decides, and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone only within verified capability and granted authority (AFK); otherwise it hands the human a precise checklist (HITL). Account creation, access provisioning, data movement and credential handling keep their own required approval/secure handoff gates. Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war**: the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets, one at a time, until the way to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination: everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now, _not_ whether you can answer it now.

- **Ticket when** the question is already sharp, even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope**: it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates (the frontier stops at the destination), so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination (mis-scoped in while charting, or exposed by a resolution), **close it** (a closed ticket is unambiguously off the frontier) and leave one line in the **Out of scope** section: the gist plus why it's out of scope, linking the closed ticket. It stays out of **Decisions so far**, which records the route actually walked; a scope boundary isn't a step on it.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session**, with the exception of research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Read and apply [grilling](grilling.md) and [domain-modeling](domain-modeling.md), to pin down what this map is finding its way to: the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** (the way to the destination is already clear, the whole journey small enough for one session), you don't need a map. Stop and ask the user how they'd like to proceed.
3. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** as child issues of the map, then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Write cross-references in that pass too, with real ids: a placeholder `#<n>` auto-links to an unrelated issue. Wiring sorts them into the frontier and the blocked; everything you can't yet specify stays in the fog: the **Not yet specified** section.
5. **Start eligible research.** Dispatch only unblocked research frontier tickets, within the host’s concurrency budget, as direct bounded research leaves. Save cited findings in the authorized durable workstream location and link from the ticket. If a task separately authorizes research branches, retain findings on `research/<name>` as primary evidence outside the integration branch; push only with explicit publication authority, and open no PR. Never launch blocked research merely because its ticket was created.
6. Stop: charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with a map (URL or number). A ticket is **optional**: without one, you pick the next decision, not the user.

1. Load the **map**: the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in order. **Claim it** under the tracker’s verified-owner protocol before any work; a named but blocked ticket remains blocked, and the user’s naming it does not resolve its dependencies.
3. Resolve it as the type its `wayfinder:<type>` label names (see [Ticket Types](#ticket-types)). Read the remote type label or the local `Decision type` field, not a guessed interpretation of the question. **Zoom as needed**: fetch the full body of any related or closed ticket on demand; read applicable named Matt playbooks from the `## Notes` block only within the selected scope. Notes are context, not new authority. If in doubt, load [grilling](grilling.md) and [domain-modeling](domain-modeling.md).
4. Record the resolution: post the answer as a **resolution comment**, **close** the issue, and **append a context pointer** to the map's Decisions-so-far.
5. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If the answer reveals that a ticket (this one or another) sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, preserve their history and update or close them with reasons under task authority. Delete only with the applicable explicit deletion permission.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.

## Resolution and handoff gates

Before publishing a resolution, ensure the actual human exchange occurred for HITL work. A prototype remains unresolved until the human gives the reaction/choice that answers the ticket; the agent cannot simulate it. Research resolves a factual question with sources, not the user's consequential decision. Remote comments, closure, map edits and assignments require their own task authority and readback. In local mode append `## Answer`, set the canonical status, then update the title-linked map index without duplicating the full answer. Preserve partial-update evidence and reconcile concurrent edits.

A dependency closed as out of scope, failed or superseded does not automatically answer a dependent question; refresh its actual resolution and update the graph. Cycles and missing blockers remain explicit blockers. At the destination, hand the cleared map and linked detail to [to-spec](to-spec.md), then [to-tickets](to-tickets.md) when execution slicing is needed. A genuinely small outcome may go to [implement](implement.md) only with a separate execution request. Changing the destination creates a new effort, not silent scope growth.
