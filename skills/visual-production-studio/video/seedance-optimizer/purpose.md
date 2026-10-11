# Purpose

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

Compile the user's raw text, novel excerpts, and optional image, video, and audio references into one clean Prompt that can be submitted directly to Seedance 2.5. Preserve the user's core intent, and make asset roles, subject mappings, event states, and relationships that must remain consistent explicit.

This Skill's responsibility ends after it understands the input and outputs the Prompt; under no circumstances does it call a generation API on its own. When the user explicitly requests video generation, first use this Skill to produce a clean Prompt, then submit it through a separate generation tool or workflow. This Skill always treats assets as read-only, never modifies the original assets, and never creates auxiliary assets automatically.
