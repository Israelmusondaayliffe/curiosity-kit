# JSON-Formatted Seedance Prompt (Optional)

Selected recipe: use only relevant fields, supplied assets and the exact model profile. Descriptive tags and JSON are not universal native controls; preserve requested count/style/copy.


Some users prefer structured JSON for Seedance prompts. Offer this variant only when the user explicitly requests JSON format or API-style structure.

```json
{
  "references": [
    {"tag": "@Image 1", "role": "Chef husky identity", "exclude": "background"},
    {"tag": "@Audio 1", "role": "jazz score"}
  ],
  "style": "cinematic 3D render, warm golden hour kitchen",
  "stages": [
    {"time": "0-6s", "action": "stirs a copper pot", "end_state": "lifts spoon to taste"},
    {"time": "6-14s", "action": "tastes and barks a command", "end_state": "three plates on the counter"},
    {"time": "14-24s", "action": "waiter sweeps the plates to the pass", "end_state": "last plate lands"},
    {"time": "24-30s", "action": "chef nods into the lens", "end_state": "hold on face"}
  ],
  "constraints": "same face, same fur, same hat where visible unless the brief changes it; no subtitles",
  "audio": "(music: @Audio 1) <kitchen clatter, sizzling>",
  "duration": "30s",
  "aspect_ratio": "preserve"
}
```

The natural-language template remains the default. JSON is only for users who ask for it.
