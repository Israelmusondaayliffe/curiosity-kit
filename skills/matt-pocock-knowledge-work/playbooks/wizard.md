# Wizard

Read the [host contract](../references/host-contract.md) before first repository access or action. This playbook runs only inside an explicitly selected Matt family workflow; source commands are not permission.

A **wizard** is a bash script that walks a human, step by step, through a manual procedure that's tedious to do by hand and tedious to re-explain to an AI every time. It opens each URL, says exactly what to click and copy, captures the values, writes them where they belong (`.env`, GitHub secrets), confirms at every stage, and shows how many stages are left. It might configure third-party services, run a one-off migration, or move the project from one state to another.

The staged interaction library is provided by [template.sh](../resources/wizard/template.sh): stage-by-stage progress, confirmation gates, cross-platform URL opening (including WSL), hidden secret entry, bounded literal `.env` upserts, `gh secret`/`gh variable` writes, and a closing summary. **Your job is only to scope the procedure and author its stages.** Reuse this adapted library above the `STAGES` marker unchanged when authoring a procedure. The migration repair changes are documented below; do not reintroduce the donor’s shell-quoted dotenv encoding.

A wizard is ephemeral by default: built for one run, saved to a scratch or `scripts/` path, retained until the user authorizes deletion after the job is done. Commit it only when the user wants a repeatable setup path that should live in the repo.

## Process

### 1. Scope the procedure

Work out every manual step the human must take and every value that gets captured along the way. Read the repo first, don't ask cold:

- For setup: nonsecret variable **names** from `.env.example`, documentation, compose/framework configuration and `.github/workflows/*`. Inspect names through a safe redacted mechanism; never read real `.env` secret values into model context. Every `secrets.*` / `vars.*` reference needs an explicit produce/reuse/out-of-scope decision. Existing secrets are handled only by the human’s secure tools.
- For a migration or transition: the current state, the target state, and the irreversible actions between them.

Then show the user the ordered list of stages and the values each produces, and confirm: they may add, drop, or reorder.

**Done when:** every stage is named in order, and for each captured value you know (a) where the human gets it, (b) where it's written (`.env`, a GitHub secret, both, or nowhere; some stages are pure actions), and (c) whether it's secret (hidden entry) or public.

### 2. Map each stage's journey

For each stage, write the precise path a human follows: which URL to open, what to do there, where a value is shown, which variable it fills: e.g. "Dashboard → Developers → API keys → Reveal test key → copy". Where you don't actually know the current UI or the exact command, say so and ask the user or check the docs: never invent steps that may not exist.

**Done when:** every stage traces to concrete instructions a stranger could follow.

### 3. Author the wizard

Copy the full [template.sh](../resources/wizard/template.sh) to the authorized collision-free target path. Replace the example stage with one `stage` per step, in dependency order. Use the library helpers: `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, `pause`/`confirm`. Set `TOTAL_STAGES` to the number of stages you wrote. Pin `WIZARD_GITHUB_REPO` to the exact verified owner/repository for approved CI writes; never let the CLI silently infer a different destination.

Hold the bar the template sets: open the URL before asking for its value, use `ask_secret` for anything secret, `write_env` each compatible local value; use a verified human-native parser-aware tool for unsupported local values, `set_secret` only the values CI actually needs, and `confirm` before any irreversible action. Each `stage` clears the screen so only the current step is visible: keep a stage to one focused task so nothing the human needs scrolls away. Don't touch the library above the marker.

### 4. Verify and hand off

- `bash -n <script>`; run `shellcheck` if available.
- `chmod +x <script>`.
- Never run a live wizard yourself: it opens browsers and captures real credentials. The human enters, confirms and submits secrets only in their private terminal or an approved secure handoff, not chat or an agent-observed terminal. Trace the live procedure statically: every value from step 1 is captured and lands where step 1 said, and every `set_secret` name exactly matches a `secrets.*` reference in CI.
- Tell the user how to run it. If repeatability and the scoped repository changes are authorized, retain it, commit only its owned files when permitted and link it from the README. Otherwise deliver the prepared script without claiming it ran or configured anything.

## Library behavior, limits and isolated verification

The adapted library retains banner, stage progress, screen clearing, `say`/`step`/`note`/`warn`, WSL/Linux/macOS URL fallbacks, visible `ask`, hidden `ask_secret`, rerun defaults, local env writes, GitHub secret/variable writes, confirmation gates and closing summaries. All stages remain inside `run_wizard`; keep the final invocation so Bash parses the procedure before prompts. The source’s Stripe stage is an **example**, not an approved operation or a claim that its dashboard path is current.

- `pause`, `ask`, `ask_secret` and `confirm` fail closed on EOF, including partial unterminated input. Ctrl-C/TERM stop with an incomplete message and clean the owned temp file. Completed writes are not rolled back; rerun reconciles the current values. Never describe the wizard as transactional across services.
- `confirm` accepts exactly y/yes, case-insensitively; other answers decline. A declined required action must be recorded in `SKIPPED`, not silently treated as complete. Author irreversible stages as explicit confirmed operations and retain their own safety/approval requirements.
- `write_env` emits literal single-quoted **single-line** values. Spaces, `$`, `#`, backslashes and double quotes are preserved in that bounded dialect. Apostrophe, CR and LF are rejected **before any mutation**. Existing ambiguous/multiline quoting is also rejected. Dotenv parsers differ; this is not arbitrary-value or universal-parser support. Never `source` or `eval` dotenv. The human keeps the original private input and uses their verified target-parser-aware editor/tool for unsupported values, including multiline secrets, then reruns or verifies the remaining stages. Test the actual application's parser before describing compatibility.
- Local updates validate names, reject symlinks/nonregular targets, create new files at 0600, preserve an existing file’s mode, write via a same-directory owned temp and atomically rename after a conflict check. They do not tighten an existing permissive mode silently; tell the human if their intended secrets file needs a privacy correction. No claim of an adversarial filesystem lock or permission-preserving ACL migration is made.
- CI helpers require the pinned repository destination and human confirmation for each submission; only name/status are printed. Unknown destination, missing/unauthenticated CLI, failed write or declined submission enters `SKIPPED`. Secret values are not printed; disable tracing. A successful CLI response means the submission succeeded, not that a deployment was tested.
- `finish` reports planned stages completed only if the count matches and nothing was skipped. Any skip/count mismatch reports incomplete and returns exit 2; runtime/input failure is nonzero. Finish logs names and remaining actions, never values. The author must record declined required non-CI stages in `SKIPPED` as well.

When the user authorizes end-to-end skill tests, make a separate isolated fake-value copy: replace browser and `gh` commands with stubs, redirect `ENV_FILE` to owned temporary storage and use a synthetic repository name. Exercise exact yes/no, EOF/Ctrl-C, reruns, supported-value roundtrips through the actual parser, before-write rejection of unsupported values, existing-content/mode preservation, symlink refusal, temp cleanup, and skipped-versus-complete summaries. Never test with real accounts, credential files or live endpoints. Report those isolated results separately from live onboarding, which remains human-run and unverified until observed through safe nonsecret evidence.
