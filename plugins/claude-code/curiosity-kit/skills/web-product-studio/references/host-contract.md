# Host and collaboration contract

Load for tool selection, packaging questions or a bounded collaborator handoff.

## Capability discovery

Resolve resources relative to this skill's installed directory. Shared Markdown and standard-library helper files are model-neutral; do not hardcode a provider/model, home directory, hidden specialist name or subscription entitlement.

Inspect actual available tools and the project's existing run instructions. Select one suitable browser surface: host browser/computer tools, an already available Playwright interface, or an existing project browser test runner. Neither Codex nor Claude guarantees a particular browser pane or CLI in every environment. If the chosen tool is unavailable, use another permitted available route or report the affected check unrun. A source file describing a tool does not make it installed.

Use a repository-native lint/type/test/build command only after inspecting what it does and its scope. Existing tool availability does not authorize installation, package downloads, external calls or production mutations. In particular, `npx` may fetch software; it is not automatically a local-only wrapper. Do not import donor bootstrap, telemetry, cookie-copy, session reuse or daemon startup into this skill.

The browser execution method and evidence limits are defined in [browser and evidence](browser-and-evidence.md). A CLI-only environment can still perform source review and applicable local checks; it cannot infer rendered, hardware or native-host outcomes.

## Useful optional collaboration

Web retains acceptance ownership. Delegate only a separable task with the exact request, source/build identity, permitted paths/actions, expected artifact and stop condition. One writer owns each file or integration surface. Receive the actual artifact and observations, inspect them, and reconcile against the current request before integration.

- Coding Studio can investigate a bounded engineering problem; all essential Web engineering methods are local.
- Brand/design specialists can resolve an explicitly open identity decision. They cannot override an approved reference by default.
- Visual Production can supply an authorized asset with dimensions, reference role, rights/provenance and exact version. Site-level layout and acceptance remain with Web.
- A separately acting reviewer can inspect a frozen artifact. An assertion that a reviewer is independent is not proof of a separate review process.
- Sites, repository, database and deployment tools are optional execution capabilities for the requested destination, not universal dependencies.

When delegation is unavailable, complete feasible local work and disclose any unmet independent-review requirement. Do not imitate a second actor or turn one self-review into two signatures.

## Host packaging

The canonical unit is `skills/web-product-studio/`. In this library the existing selected-unit `build/package.py` copies it into Claude Code and Codex full/isolation packages; Codex UI metadata comes from the library adapter entry. Packaging does not install the skill, prove invocation, or qualify native behavior. Do not create a second nested plugin or duplicate front door inside the unit.

Report actual loaded resource paths when tracing is available. Keep archived research, source ledgers and eval evidence outside runtime. Loading one route should not pull the entire benchmark corpus into context.

## Returning work

Return the exact artifact/version, completed request scope, observed results, changes made, unresolved requirements and next permitted action. Distinguish authored code, executed tests, browser observations, independent review and native-host qualification. Each claim must name its actual evidence boundary rather than inherit the strongest status elsewhere in the workflow.
