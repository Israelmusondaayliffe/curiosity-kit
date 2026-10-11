# Migrate a prompt without losing its job

Migration changes a selected model, version or interface while preserving the task and its stable requirements. It is not a general permission to rewrite product policy, change models again, install a harness or weaken tests. If the user asked only for an audit, use [audit](audit.md).

## Freeze the source and intended target

Read the full source prompt and the configuration, examples, relevant tool schemas and output parser that affect its behavior. Inspect other authorized instruction files only when they influence this task. Keep source bytes and a rollback reference. Record exact source/target labels, interface, tool availability, output requirements, evaluation cases and any observed failures. Resolve aliases against the actual selected interface; do not silently choose the newest model.

Read the relevant [provider branch](../references/provider-guide.md). Separate mandatory request-compatibility changes from behavioral suggestions. An API model ID, a chat-product model label and a self-hosted checkpoint have different contracts. A current guide's claim that an old prompt should work is a starting hypothesis. An unavailable target permits provisional prompt preparation, not an invented runtime result.

## Classify before editing

Inventory each consequential instruction, example and tool description:

- Stable product requirement, factual source constraint, authority/safety rule, output contract or task-specific acceptance test. Preserve it unless the user approves a product change.
- Model compensation or a workaround for an observed failure. Keep the evidence, then test whether the target still needs it.
- Duplicate or conflicting wording: compare obligations by meaning, including within the same sentence, bullet or section, keep one owning statement per obligation, and replace other restatements with references while preserving every distinct requirement and its specificity; examples may demonstrate rules. For example, "Give every step a number. Use numbered steps." becomes "Use numbered steps."
- Obsolete interface setting, model reference or unavailable tool. Replace from applicable current evidence or mark blocked.
- Unclear instruction. Name the ambiguity and its impact; do not optimize away meaning you have not established.

Retain deliberate demonstrations and required formatting. Do not adopt blanket bans on XML, verification, citations, examples or specific words. A source-before example may properly contain a parameter rejected by the target; label it rather than treating every quoted configuration as active.

## Change one attributable group

Where execution is available and authorized, establish an unchanged-source baseline first. If the source already fails, preserve that result and do not claim subtraction preserved working behavior. Then separate experiments:

1. Model/interface change plus only mandatory compatibility edits.
2. Effort or execution-mode calibration at the selected target.
3. Prompt subtraction or a targeted instruction repair.
4. Tool-set or orchestration changes when actually needed.

Match case inputs, parser, tools, grader and intended conditions. Effort labels are not equal work across models. Keep stable requirements while comparing task completion, quality, resource use and side effects. Reduce one coherent compensation group at a time, such as repeated scope reminders or an old workaround. Restore or repair a change that causes a critical failure or harms a required category. Do not optimize a mean by sacrificing a rare important boundary.

For cross-provider or fallback migration, translate the requirements into the target's actual interface instead of renaming fields mechanically. Opaque state, forced tools, output budgets, progress blocks, compaction and prefill require particular attention. A fallback transition needs [its own method](fallback.md). Persistent harness application belongs to HE; return a proposed compatible change and evidence without applying unowned global state.

## Verify and deliver

Review the complete migrated prompt, native configuration and examples together. Check null/error schemas, allowed actions, tool/result identity, output completion, citation behavior, relevant source preservation and explicit stopping. Use promptcheck for its narrow local checks and [benchmark](benchmark.md) for the frozen comparison. Reuse unchanged passing evidence with its exact source revision; rerun affected cases after repair rather than silently relabeling old results.

Return a complete target prompt and a keep/remove/change/add ledger. Each consequential entry names the source instruction, reason, current source or observed evidence, and affected check. Report actual measured results separately from proposed checks and unresolved runtime compatibility. Include exact target/interface, old/new configuration, risks and a rollback order: restore prompt and matching tool/parser configuration, restore supported target selection, then run the preserved baseline checks. Do not claim an account or installed configuration was changed unless it actually was authorized and verified.
