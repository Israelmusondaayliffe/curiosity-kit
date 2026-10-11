# Skill mechanics

Conditional reference for [writing-for-agents](../../playbooks/writing-for-agents.md). The main playbook owns the universal concepts; this file owns packaging and invocation decisions. Inspect the actual target host’s documented frontmatter and loader before choosing fields. Source conventions are not portable guarantees.

## Invocation choice

- **Model-invoked:** an agent-visible description acts as a context pointer so the host may discover the skill; explicit user invocation remains possible. Write one meaningful trigger per genuine branch, front-load the leading word and omit redundant identity. This spends context load for discoverability. Shared reference may be reachable through this route when the host supports cross-skill invocation.
- **User-invoked:** explicit selection is required. The source host expresses this with `disable-model-invocation: true`; the description becomes a concise human-facing summary without broad ambient triggers. On hosts with different controls, use the supported explicit-only equivalent. Do not assume deleting the description makes a valid skill or that a flag removes all metadata from context.

Pick model invocation only when automatic discovery or composition is needed and authorized. User invocation spends cognitive load so people retain control over when the procedure runs. Document the actual host behavior rather than asserting zero context load or universal invisibility.

## Frontmatter and identity

Preserve the installed skill identity and required schema. For the source host, `name`, `description`, optional `argument-hint`, and `disable-model-invocation` describe a skill; supported fields vary. Check actual parser/loader behavior, including whether explicit-only skills can be composed. The current Matt package exposes one explicit library entry and ordinary local playbooks, so its internal links load references without needing another named skill or a donor `Skill` tool.

## Splitting by invocation

Split a separately discoverable skill only when a distinct leading word genuinely needs independent triggering or another workflow needs that entry, and the additional description earns its context load. A renamed synonym is not a new branch. For sequence-based splits, use the main playbook’s real-context-boundary test; moving text to an inline call does not clear later steps from memory.

## Router skills and shared reference

When user-selected skills become hard to remember, a router reduces cognitive load by naming methods and when each helps. A recommendation router stops at recommendations unless execution is authorized. A directly selected method in this explicit library may load its complete local playbook and applicable references; it is not blocked by donor assumptions that routers can only hint.

Shared reference needed by multiple explicit methods belongs in a plain local file with a clear reason-to-read pointer. Such a file is not another autonomous skill. Keep the canonical definitions once; provide valid relative links and load the complete relevant branch before acting.
