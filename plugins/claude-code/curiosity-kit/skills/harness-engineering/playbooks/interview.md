# Harness interview

This is Harness Engineering's own substantive, source-first interview. Turn the user's incomplete setup or builder request into a confirmed working profile. The interview and its decisions are the deliverable; do not build during this phase.

## Before asking

Audit the actual authorized setup with [audit](audit.md), then investigate consequential uncertainty through [research](research.md). Resolve the host or connected-folder environment before designing its behavior. If several hosts are requested, record each scope and its distinct prerequisites. Do not port settings or paths by resemblance.

Inspect available instructions, work examples, relevant skill methods and tool state. Configuration values stay on the redacting `hectl audit` path; do not open or print raw settings, config, env or credential files. Pass the selected location explicitly, for example `python3 scripts/hectl.py audit --platform codex --home <config home> --workspace PATH`. Reuse confirmed answers, profiles, constraints and prior receipts. The user should not have to answer facts the environment or previous decisions already supplies.

A narrow user-specified change may already settle every branch. Record why no additional interview is needed and carry the confirmed decisions forward. A broad harness build still needs the full decision process; a generic intake sentence is not a substitute.

## Conduct the conversation

Start with the real outcome, who uses the system and the largest unresolved dependency. Follow [interview branches](../references/interview-branches.md) in dependency order. Ask one to three linked questions at a time, then adapt the next questions to the answers. Define terms before asking the user to decide about them.

Questions should reveal actual work. Ask for the last representative task, the output they wanted, where the current system failed, what they corrected and what good would look like. Prefer an authorized example over a hypothetical preference when available. Distinguish a repeated workflow from a one-off request.

Offer a recommended default and its main tradeoff when evidence supports one. Do not conceal uncertainty inside the recommendation. Record only answers that change the profile, classified as fact, constraint, preference, assumption or decision, with their source. A user's aspiration is not an observed habit; a model suggestion is not a user preference.

Pressure-test the design:
- What must never change or leave the selected workspace?
- Which actions may proceed under current approval, and which need a separate decision?
- What happens when an essential tool is unavailable, evidence conflicts or a run stops midway?
- Who judges subjective quality, using which artifact and threshold?
- What must survive a new session, and where can it persist safely?
- Who maintains the result, and what observation would justify revisiting it?

Do not ask all questions mechanically. Follow the branches whose answers materially affect the requested system. Keep ordinary work simple while investigating consequential decisions thoroughly.

## Converge without inventing approval

A branch closes only when it is answered, discoverable from a named source, explicitly excluded, or deferred with an owner and revisit trigger. A deferred essential dependency blocks the build step that needs it. Unknown is not no, an empty field is not permission, and silence does not confirm a profile.

Present the whole working model in one coherent view: user/work context, primary and other hosts, intended scope, workspace and project pattern, sources, capability needs, exclusions, accepted assumptions, authority, deterministic and qualitative proof, maintenance and unresolved decisions. Ask for corrections where confirmation is still required. Reuse an existing explicit end-to-end authorization where it already covers the settled plan; do not add ceremonial approvals between every internal phase.

Start from `assets/templates/profile.json`. Drafts may be saved and checked while interviewing. Preserve schema1 fields and validate with:

```text
python3 scripts/hectl.py profile PROFILE.json
```

Only after actual user confirmation, set `status` to `confirmed`, identify the confirmation in `confirmed_by`, and check:

```text
python3 scripts/hectl.py profile PROFILE.json --require-confirmed
```

The validator checks declared shape and status, not the authenticity of a human decision. Keep the actual conversation/source as authority. A confirmed profile alone does not authorize installation, publication or a build.

## Worked decision

A user wants workshop follow-up notes to be faster. The audit finds an existing note template, but the slow step is reconciling inconsistent counts. Research finds no need for a new service. Ask whether the desired result is a checked draft or automatic delivery, which source controls participant counts, and who approves uncertain claims. If the answer is checked drafts only, keep sending out of scope. The resulting profile calls for a source-faithful local drafting method, a count check and review of uncertain claims, rather than a broad autonomous communications system.

## Handoff

Return the confirmed profile or explicit unresolved decisions and source pointers. For a fresh session, the profile itself is durable input; no sibling handoff skill is required. Continue to [plan](plan.md) only when its prerequisites and authority are met. Preserve the audit/research findings that explain the choices so the next builder does not restart the interview or silently change its meaning.
