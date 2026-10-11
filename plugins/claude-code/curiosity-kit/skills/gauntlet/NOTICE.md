# Sources and adaptations

This is a newly authored standalone implementation of functions studied in:

- Codex Gauntlet Loop, including the original Agent Ops packet-validator contract.
- Claude Gauntlet, including six role prompts and eight domain methods.

Both MIT grants from the Claude and Codex sources are retained in LICENSE. The owner-authored Codex copyright attribution uses the Curiosity Kit contributor name; third-party notices and license terms are unchanged. Donor code was studied rather than copied as a runtime dependency. The implementation preserves methods through local instructions, validation and tests, removes fixed-model rules and private sibling imports, and makes evidence/host limitations explicit.

Applicable design influences: cursor/plugins Pstack at e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a, and mattpocock/skills at 24fe0ef7737efae15c87225755e9f6f5965e4888. Verifiable units, actual driving/evidence, dependency-ready complete slices, fresh critique and evidence-led retrospectives inform the methods. Their model counts, external publication actions and host-specific defaults are not imported. No upstream scripts from those collections are shipped here.

Local deterministic tests are implementation checks. Independent matched-host qualification remains separate and must not be inferred from this notice. Source attribution and depersonalization do not establish fresh acceptance. Original contributions are licensed under the package-root MIT LICENSE; third-party material retains its stated terms.

Named model identifiers in tests/test_advisor_controls.py are synthetic test input records for the frozen arbitrary-model acceptance control. They are not runtime defaults or requirements.
