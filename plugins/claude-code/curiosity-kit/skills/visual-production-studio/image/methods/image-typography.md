# Make lettering and exact copy work in an image

Begin with a text inventory. Copy supplied spelling, capitalization, punctuation, diacritics, script and line breaks exactly. Mark proposed copy as proposed. Font names, color codes and layout labels are instructions unless the user wants them visible.

1. Assign each text string a role and reading priority. Set headline/supporting scale, location, alignment, spacing and relation to the picture. Reduce competing zones when density would make the intended size unreadable.
2. Describe letterforms through their construction: stroke weight, contrast, width, terminals, joins, counters and rhythm. Named fonts can guide the treatment but do not guarantee identical glyphs.
3. Specify how the letters exist. Printed ink, cut paper, painted signage, embroidered thread, carved stone, neon and drawn lettering each have different edges, thickness, light and contact. Let expressive display text carry character while protecting supporting readability.
4. For multilingual or mixed scripts, respect reading direction and the script's typographic conventions. Verify any requested translation before placing it in the prompt. Do not let the image model invent the translation or force a Latin lettering structure onto another script.
5. Use expressive prose for a simple word treatment or separate literal strings and placement in JSON for a dense inventory. Keep all exact strings in the delivered prompt.

Check the prompt against the inventory character by character. For a rendered image, read the actual lettering, punctuation and speaker/label association at useful size. If production-perfect copy is necessary, identify where separate typesetting may be needed rather than promising error-free generation.

[Typography recipes](../references/image-typography/gpt-typography.md) cover display words, mixed scripts, wordmarks, dense editorial and environmental lettering. Use [editorial](image-editorial.md) only when the page-level image/type composition is the main task.
