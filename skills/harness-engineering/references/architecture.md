# Architecture

## Three layers

1. **Information**: instructions, context, skills, tools, connectors, project references, memory.
2. **Execution**: workspace boundaries, plans, autonomous runs, scripts, rules, hooks, approvals, recovery.
3. **Feedback**: checks, receipts, reviews, failure records, maintenance, model-change audits.

A harness that lacks feedback does not get fixed by more information. Balance the three.

## Scope hierarchy

Names differ per platform (see [platforms](platforms.md)); the order does not:

- Thread prompt: one task.
- Global instruction layer: personal defaults everywhere.
- Workspace layer: shared layout, routing and output rules.
- Project or nested layer: the closest commands, constraints and checks.
- Skill: a repeatable workflow with its references, scripts and assets.
- Plugin: a distributable bundle of skills and optional lifecycle components.
- MCP server or connector: live external data or actions.
- Hook, rule or script: deterministic enforcement where the platform supports it.

Put a requirement in the narrowest scope that must always see it.

## Reliability order

Use the least free mechanism that fits: script, command rule, hook, sandbox or permission setting, template, prompt instruction, instruction file, inference. A correction needed twice moves down this list instead of being repeated. Cowork has no practical hooks, so a validator script run by contract is its top rung.

## Context shape

Default context is a compact kernel of stable invariants plus delta-only workspace and project overlays. Plugin front doors stay visible; specialists, detailed workflows, examples and recovery guidance load from the task that needs them. Exact behavior sits in mechanisms. Prompt size is a diagnostic: freeze behavior before subtracting, and keep only reductions that preserve authority, routing, stopping, formatting and verification ([subtraction protocol](subtraction-protocol.md)).

## A mature shape, for reference

One working example separates a global home from the working workspace; uses layered instruction files, a project registry, reusable templates and a dated output folder; routes capabilities by data owner; enforces with command rules, reviewed hooks and quality gates; runs bounded autonomous work with durable state; and checks discovery in fresh tasks. The lesson is the arrangement, not the specifics: identity and global policy stay small, workflows live in skills, exact behavior lives in scripts and rules, and completion needs evidence from the live surface. It is not a default installation.
