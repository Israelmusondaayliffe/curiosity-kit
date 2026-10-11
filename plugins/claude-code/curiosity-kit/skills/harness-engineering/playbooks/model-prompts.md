# Model prompts

Create, migrate or test prompts a harness uses, adapted to the selected model without freezing the harness to one generation. Anthropic models serve Claude Code and Cowork harnesses; OpenAI models serve Codex harnesses.

Honor requests for a short test plan without running tests when only a plan is requested, while preserving authority boundaries and substantive verification requirements.

## Steps

1. Classify the surface: thread prompt, instruction file, skill, autonomous run (Goal, scheduled task, headless run), API system prompt, or builder surface.
2. Keep an explicitly named target model. For the model the environment is configured to run, use `model_settings` from `hectl audit`, not a raw read of the config file. If the user says latest, current or default, read the vendor's current official documentation for that platform's model family before choosing or rewriting. Never invent a model name, parameter, price or availability claim.
3. Use an installed model-specific prompting skill when one is visible; prefer the namespaced plugin copy.
4. State the outcome, needed context, constraints, authority, output contract and completion evidence once each.
5. Separate stable user policy from temporary model compensation. Remove duplicate reminders and obsolete workarounds. For instruction files and skills, apply [context doctrine](../references/context-doctrine.md) and never carry a request to expose reasoning into any surface.
6. Write test cases for success, ambiguity, approval, tool routing, formatting and stopping.
7. Run each case more than once at fixed model, effort, tools and scorer.
8. Subtract one coherent group at a time. Restore any change that causes a critical failure, lowers a category, or lowers the overall pass rate.
9. Mark model-specific blocks as provisional with the date and source they came from.

## After a major model change

Freeze the prompt, model, effort, tool inventory, scorer, routing state, hashes and a representative behavior suite, then follow [subtraction protocol](../references/subtraction-protocol.md). Recheck approval behavior, tool routing, response length, stop conditions, task-start capability context and completion evidence after installation. Compare only runs with matching conditions; rescore frozen raw outputs when the scorer changes.
