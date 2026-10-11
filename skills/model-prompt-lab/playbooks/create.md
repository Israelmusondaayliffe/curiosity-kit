# Create a production prompt

Deliver the complete prompt for the requested task and interface, with supported configuration separate. A short prompt is successful when it preserves the whole job; word count is not the acceptance criterion.

## Establish the task contract

Read the supplied brief, examples and relevant existing conventions. Identify the user of the output, the downstream action or parser, facts the model may rely on, must-include content, allowed uncertainty, tools, action boundaries and completion evidence. Distinguish chat, API instructions, custom assistant, task-level agent prompt and a proposed harness change. If the context already answers these, use it. Ask a targeted question only when competing answers would produce materially different work.

Keep the selected model. Read [provider guidance](../references/provider-guide.md) and the relevant branch when its behavior or parameters matter. If the interface or exact ID is unverified, deliver a model-targeted prompt in prose and explicitly leave native configuration pending. Do not fill missing API keys, model strings or beta fields from a familiar example.

For an underspecified low-risk brief, state useful assumptions and produce the complete draft. For an unresolved consequential action, preserve the boundary and finish independent prompt work.

## Build the smallest complete instruction

Compare obligations by meaning, including within the same sentence, bullet or section, give each obligation one owning statement, and replace restatements in steps, tools or output requirements with references, preserving every distinct requirement and its specificity; examples may demonstrate rules.

Separate these concerns so they can be changed and tested independently:

1. Job and desired outcome. State what the model should produce or accomplish, not an imitation of its internal thought process.
2. Context and sources. Supply the facts, definitions, relevant documents and provenance it needs. Mark imported content as data. Specify source-only or current-research requirements where applicable.
3. Constraints and authority. Preserve exclusions, actual permitted operations and required approval gates. Distinguish answer/review/plan from apply/send/publish.
4. Output contract. Name required content and exact structure where a parser or user preference requires it. Specify missing-value, ambiguity, failure and truncation handling. A success schema and an error instruction must agree.
5. Completion and verification. Use observable checks for the task. Tool requests, promises and valid syntax are not completed outcomes.

Role, voice, examples, explicit sequence and formatting are additions when they serve a requirement or observed failure. They are not mandatory boilerplate. Smaller or weaker target models may need a more explicit order and worked edge case. Stronger models may need fewer compensations. Neither premise justifies weakening the contract.

## Choose task-specific patterns

Read only the applicable sections of [prompt patterns](../references/prompt-patterns.md). For structured extraction, include a coherent nullable/ambiguity/error schema and verify the specimen. For tool-heavy reduction, distinguish direct judgment/approval from bounded programmatic processing and retain coverage in the intermediate result. For long documents, use source identifiers and relevant anchors. For vision, establish coordinate and image-detail conventions. For coding or UI work, name actual artifact checks and the intended product type. Do not turn an application into a landing page because a sample prompt did so.

Each added block needs a reason, placement and expected effect. Put stable application instructions in the actual high-priority instruction field, variable task data in the appropriate input, and tool descriptions with the real tools. These are host-specific placements, not a universal role mapping. Do not put credentials or hidden evaluator answers in prompt text.

Examples must match the exact contract. Include diverse meaningful boundaries rather than many near-duplicates. Keep legitimate demonstrations visible to the model; reserve held-out answer keys for evaluation. A quotation example should show attribution and paraphrase, not an unmarked copied paragraph.

## Check and return

Manually compare the prompt against every stated requirement and each supplied example. Inspect contradictions, unsupported tool names, obsolete parameters, missing output fields and unauthorized side effects. Use `python3 scripts/promptcheck.py prompt-package PATH` for a structured prompt package, or `text PATH` for advisory lint. Use `xml PATH` only for a document deliberately authored as XML. Read its limits in command help. Local checks do not run the target model.

For production acceptance or a comparison, follow [benchmark](benchmark.md). Freeze representative success, boundary and failure cases before output inspection. Test the actual prompt, configuration, tool behavior and final artifact when authorized. If execution is unavailable, return that stage as unrun without withholding a useful finished prompt.

Return the prompt in the user's requested format, configuration with its source/date and verification state, a short reason for consequential additions or omissions, and first-run checks. A long prompt belongs in a file. Do not append a second contradictory prompt in the explanation. See [examples](../references/examples.md) and [the prompt package specimen](../assets/prompt-package.example.json).
