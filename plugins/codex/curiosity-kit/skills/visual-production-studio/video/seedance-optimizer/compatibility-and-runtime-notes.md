# Compatibility And Runtime Notes

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

- **Text-only Agent**: Handles text and explicit reference labels; it must not claim to have viewed attachments or the contents of file paths.
- **Multimodal Agent**: Reads images, videos, and audio within the permissions available at runtime, then performs two-pass asset understanding and automatic mapping.
- **No filesystem access**: Retain the user's existing labels; for inaccessible paths, apply the `Current Agent Cannot Read the Assets` fallback without claiming to have inspected them.
- **No network access**: Do not attempt to inspect the content of remote URLs or infer asset content from URL names.
- **Output only**: This Skill outputs text and does not require file writes, network access, tool calls, or binary-output capabilities.
