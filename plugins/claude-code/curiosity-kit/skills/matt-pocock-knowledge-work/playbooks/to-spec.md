# To Spec

Read the [host contract](../references/host-contract.md) before first repository access or action. This playbook runs only inside an explicitly selected Matt family workflow; source commands are not permission.

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

Use the configured tracker and label vocabulary. If missing, use the authorized local convention in [the local tracker contract](../resources/setup-matt-pocock-skills/issue-tracker-local.md), or recommend [setup-matt-pocock-skills](setup-matt-pocock-skills.md) if a project-wide configuration decision is needed.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Reuse the seams already agreed in the conversation or approved spec. Ask only about a newly proposed or unresolved seam approval; do not restart the interview. Record unresolved consequential decisions as blockers instead of inventing product decisions to fill the template.

3. Write the complete spec using the template below in the configured authorized local tracker or durable path. Mark it `Artifact: spec`, `Status: open`; apply the mapped `Triage role: ready-for-agent` only when its execution-blocking decisions are resolved. The role does not make a spec an implementation ticket. External publication needs task-specific authority; verify the created item and avoid duplicate publication on uncertain results. Report draft versus published honestly.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>

## Knowledge-work and mixed specification

Preserve the same complete contract, with domain-appropriate fields: audience and actual decision/use under Problem Statement and User Stories; observable outcome under Solution; numbered independently checkable deliverable requirements; editorial, analytical, evidence, operational and implementation decisions; required source quality and claim provenance; output shape and delivery constraints; review axes, renderers and real artifact surfaces under Testing Decisions. Record migration needs and operational risks for mixed software work. Include an explicit **Open blockers** section, even when it says none. Requirements and numeric defaults, ordering and negative constraints must trace to actual conversation or source evidence, not to the desired length of a user-story list.

When synthesizing a wayfinder map, read the linked resolution details and relevant assets, not just the map's one-line gists. Collapse those decisions into one buildable contract while preserving source pointers. The spec stops at synthesis/publication within authority; it does not execute its contents.
