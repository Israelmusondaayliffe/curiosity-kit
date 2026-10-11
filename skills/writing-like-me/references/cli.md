# Local helper contract

Python 3.9+ standard library; no network, installs, model calls or sibling imports. Resolve SCRIPT to this package's absolute scripts/wlm.py path; never assume the working directory is the package root. `python3 SCRIPT --help` and `python3 SCRIPT COMMAND --help` are authoritative for flags. JSON goes to stdout. Exit 0 means a command completed, not that writing is good; 1 means a protect/claims check found a mismatch; 2 means invalid input, unavailable data, unsafe path or operational failure. Argparse usage errors use stderr. Preserve input copies and inspect actual outcomes.

## Read-only operations

- `python3 SCRIPT discover --host codex --workspace PATH [--home PATH]` (or claude-code): reports explicit-home or active-workspace VOICE/STYLE candidates and existence. Reads no guide contents; creates nothing; never guesses host-home locations or scans another host.
- `python3 SCRIPT count FILE`: Unicode character, UTF-8 byte and tokenized word counts. This is not a model-token counter; platform counting rules may differ.
- `python3 SCRIPT profile FILE`: mechanical rhythm, sentence-length, pronoun and contraction statistics. Infer voice from actual supplied passages, not these numbers alone.
- `python3 SCRIPT scan FILE [--profile blog|technical-blog|docs|casual|linkedin|investor-email]`: protected-span-aware lexical and limited structural candidates, with locations. Profile is a context label for the editorial reviewer, not a secret score adjustment. Semantic/source-aware checks remain manual. No authorship verdict, automatic score or ban list.
- `python3 SCRIPT protect BEFORE AFTER [--exact EXACT_BLOCK_FILE ...]`: compares ordered protected spans and any user-selected exact block. Ambiguous syntax yields a failed/manual-review result. Use original text files: line endings and exact bytes in protected spans matter. Conservative parsing may require manual review for unusual Markdown/quotes.
- `python3 SCRIPT claims LEDGER.json`: validates evidence_scope and claims array. Every claim has unique id, claim text, status supported/unsupported/uncertain/non-factual, evidence string and remedy keep/remove/qualify/verify/source. Supported requires a nonempty locator, not merely confidence. A valid schema does not prove that locator supports the claim.
- `python3 SCRIPT business FILE`: counts structural cues, with no passing threshold. A story or informative note may need none.

## Explicit output and confirmed writes

- `python3 SCRIPT punctuation FILE [--output NEW_FILE]`: preview diff by default. Optional new output replaces a dash and its surrounding spaces with a comma, or a period before a capital, only in unambiguous prose spans. Never overwrites input or existing output; check meaning after punctuation changes. Unknown formats or unmatched delimiters block automatic transformation.
- `python3 SCRIPT init --home PATH [--add-missing] [--confirmed]`: preview by default; confirmed creates VOICE.md, STYLE.md, examples/README.md and drafts/README.md from local templates. A nonempty home requires --add-missing; existing files survive. Interrupted partial setup is recovered by inspecting it and using --add-missing; never claim transactional all-or-nothing creation.
- `python3 SCRIPT guide --home PATH --guide VOICE.md|STYLE.md --proposed FILE`: previews the complete replacement and current expected_sha256. Re-read and merge user changes in the proposal; the helper never invents the merge.
- Same command plus `--confirmed --expected-sha256 HASH`: applies only after actual user confirmation of destination/content. Use literal `missing` for a new guide. Hash mismatch stops; reread and get renewed confirmation if the proposal materially changes. Existing target is backed up under home/.history; atomic replacement follows cooperative lock and repeated hash checks. No-op returns unchanged.

Paths are checked at their real location: a symlinked target is refused, and writes reject this skill tree, detected plugin/skill ancestors and cache/source-like directories wherever a symlink points. They do not establish authorization outside those guards: the caller must ensure the selected home is user-owned and outside all source/installed/cache roots. No synchronization or source/cache learning is allowed. A crashed .wlm-guide.lock requires inspection of active processes and target/backup state before authorized manual removal; do not bypass it automatically. Cooperative locking cannot guarantee protection against an unrelated writer ignoring the lock.

The CLI does not run editorial reviews, choose models, send content or publish it. A required failed or unavailable check stays unresolved.
