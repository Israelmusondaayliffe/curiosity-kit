# Provenance and adaptation

The source baseline comprises earlier Writing Quality editions for Codex and Claude.

Both have 35 methods: 33 cw-* methods, Business Writing Intent and Claim Boundary Checker. Their method bodies largely agree; host differences include invocation metadata, declared guide paths, packaging and reviewer model pins. The new runtime is reauthored around those functions, with one entry and local playbooks/lenses. No old native command, agent type or path is claimed to exist in this package.

The original [NOTICE](../NOTICE) is retained unchanged, including full MIT permission text and attribution to Katie Parrott / EveryInc Compound Writing, commit 18702f0ece9f2b852e305807e0271b2d550d9b4b. Its referenced declarations are actually included under [upstream/original](../upstream/original/README.txt). No standalone source LICENSE was found or invented.

## Cleanup sources

The source records credit humanizer (Siqi Chen, MIT), stop-slop (Hardik Pandya, MIT), no-ai-slop (Peter Yang, MIT, commit 61c21c351da4dcb40946a11fead978f2078a2c65), avoid-ai-writing (Conor Bronsdon, MIT), and an Unslop source supplied during the original adaptation. These are historical source attributions, not claims of a new live audit or installed dependency. The matching copyright notices and MIT terms are bundled in [third-party notices](licenses/THIRD_PARTY_NOTICES.md), together with the taxonomy’s separate CC BY-SA attribution.

Pattern families 1–24 adapt Wikipedia's Signs of AI writing taxonomy; the adapted taxonomy in [pattern-catalog.md](pattern-catalog.md) retains [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) terms. The original source title and link are [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Families 25–36 trace to avoid-ai-writing; 37–41 to the source Unslop additions; 42–47 to no-ai-slop/stop-slop. The catalog is rephrased, context-sensitive and removes unsupported authorship and model-mechanism inferences.

[lexicon.csv](lexicon.csv) preserves the source's lexical dataset verbatim for completeness. Historical column names and rationales are source data, not runtime claims that a word proves AI authorship. The active playbook overrides blanket bans and gives source/voice/context priority. [word-options.csv](word-options.csv) extracts the source's replacement pairs as optional suggestions, not automatic substitutions or evidence for claims.

Historical prebuilt personal voice profiles, hardcoded writing-home paths and permanent reviewer model names are intentionally not packaged as active instructions. Guides remain user-selected host-local inputs. Full methods are rebuilt locally; another plugin, compiler or writing skill is not required.

Original contributions are licensed under the package-root MIT LICENSE; third-party material retains its stated terms. This grant does not relicense unattributed third-party source material.

Archived README and ARCHITECTURE declarations retain their upstream bytes as `.txt` evidence, not active runtime instructions. ARCHITECTURE.txt was retrieved from the same pinned Compound Writing commit to accompany the README reference. Historical relative paths describe the upstream tree.
