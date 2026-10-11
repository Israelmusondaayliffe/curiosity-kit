# Deck

## Unit and bar

Separate the slide-order argument, individually consequential slides, and the visual system. An outline or speaker-note document is a prose artifact. The deck itself must be rendered.

Use real reference decks from the same communication category, stored as PDFs or slide images. Freeze comparison sizes and the intended audience. Assess the narrative in order; assess the visual system across representative layouts and check every slide for defects. Every factual figure needs source tracing, including chart labels and footnotes.

## Inspection recipe

Render the current deck each round and inspect its PDF or slide images. Capture the authorized renderer's outputs and exit status with `python3 scripts/inspection.py check --input payload.json`. A failed render or missing slide blocks judgment.

A fresh reader sees the rendered slides alone, in order, and answers these frozen questions: What is the ask? What is the evidence? What is the next step? What would make you say no? Record guesses, answerability, and slide locations. Use `python3 scripts/inspection.py reader --input payload.json` to validate the saved record and question identity. Do not soften these questions after a failure.

Use `python3 scripts/inspection.py claims --input payload.json` for figures and factual claims. An integrity judge checks semantics, denominators, dates, units, and whether chart encodings exaggerate the evidence.

## Comparison and worked check

Blind-pair rendered decks or matched slide sets at comparable sizes. Seal identity mappings and omit source filenames and builder commentary. For a board-update metrics section, trace every displayed number to its source and verify the plotted values independently. For a teaching deck, check whether the audience can reconstruct the lesson and required action from the slides.

Quality preference cannot excuse fabricated figures, unreadable labels, clipped content, or unverified reference files. Research owns collection of the underlying evidence; strategy owns the decision logic the deck presents.
