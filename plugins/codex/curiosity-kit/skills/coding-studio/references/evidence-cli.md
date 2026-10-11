# Selected-input evidence helper

Use `scripts/evidence.py` when you need to compare the bytes of an explicit file list before reusing earlier evidence. It uses Python 3.9 or newer and the standard library. There is no installation step.

The helper reads selected files and optional context. `snapshot` creates one new JSON file. `check` only reads. It never runs the command named in context or changes Git state.

## Interface

Resolve the installed skill directory from the loaded entry. The commands below use paths relative to that directory; from another working directory invoke the script by its resolved absolute path. Do not assume the project root contains the installed skill.

```text
python3 scripts/evidence.py snapshot --root ROOT --file REL [--file REL ...] --out NEW_JSON [--context JSONFILE]
python3 scripts/evidence.py check SNAPSHOT [--root ROOT] [--context JSONFILE]
```

Paths passed to `--file` are literal, slash-separated paths relative to the selected root. Select each file explicitly. The helper never expands globs. Literal bracket or wildcard characters are accepted where the filesystem allows them, including Next.js paths such as `pages/[id].tsx`. Quote these paths and paths containing spaces so your shell does not expand them. Absolute paths, backslashes, empty components, `.` and `..` components, control characters and duplicate paths are rejected. Directories are not expanded.

`--out`, `--context` and `SNAPSHOT` resolve from the command's current working directory. The output's parent must already exist. Existing outputs are never overwritten, including symlinks and hard links. Single-value options may appear only once.

By default, `check` uses the absolute root recorded in the snapshot. An explicit `--root` compares the same selected relative paths in another directory. The result prints the root actually checked. This override does not establish that two repositories, branches or execution environments are equivalent.

Only check a snapshot whose root and selected paths you intend to read. Inspect unfamiliar snapshots before using them. There is no signature or provenance verification.

## Context

Context is an optional UTF-8 JSON object with string values. For example:

```json
{
  "comparison_base": "the independently verified base revision",
  "operation": "review",
  "cwd": ".",
  "requested_command": "python -m unittest"
}
```

Choose the fields that matter for your task. The helper compares the supplied string values exactly, ignoring JSON object order. It rejects duplicate keys, nested values and non-standard values such as `NaN`.

If the snapshot recorded context, `check` requires `--context` with your current context. Obtain current values through the project or host tools before checking. Reusing stale context only proves that the stale strings match. The helper does not query Git, verify the supplied revision, inspect the environment or execute the requested command. Use a full verified revision when base identity matters.

Omitted context is distinct from an explicitly supplied empty object. Adding context to a snapshot that recorded none is drift. Without context, successful output says `not_recorded`.

Do not put credentials or other secrets in context. The snapshot stores its full contents.

## Disposable example

Set the shell variable SKILL_DIR to the actual installed coding-studio directory identified from the loaded entry. The example works from any current directory and creates only temporary sample files and one new snapshot. Keep that temporary directory for inspection.

```sh
EVIDENCE="${SKILL_DIR:?Set SKILL_DIR to the resolved installed coding-studio directory}/scripts/evidence.py"
WORK="$(mktemp -d)"
WORK="$(cd "$WORK" && pwd -P)"
mkdir -p "$WORK/project/src"
printf 'def answer():\n    return 42\n' > "$WORK/project/src/answer.py"
printf '{"operation":"review","cwd":".","requested_command":"python -m unittest","comparison_base":"abc123"}\n' > "$WORK/context.json"

python3 "$EVIDENCE" snapshot --root "$WORK/project" \
  --file src/answer.py --out "$WORK/snapshot.json" \
  --context "$WORK/context.json"

python3 "$EVIDENCE" check "$WORK/snapshot.json" --context "$WORK/context.json"
# Exit 0, status match.

printf 'def answer():\n    return 99\n' > "$WORK/project/src/answer.py"
python3 "$EVIDENCE" check "$WORK/snapshot.json" --context "$WORK/context.json"
# Exit 1, status drift, changed path src/answer.py.
```

The sample base string is a fixture, not evidence of any repository revision. The command string is recorded and compared, never executed.

## Results and errors

- Exit `0`: the snapshot was written, or all selected file bytes and supplied context matched.
- Exit `1`: a selected file changed or went missing, or supplied context differed.
- Exit `2`: arguments or JSON are invalid, an input is unsafe or unavailable, a root is missing, a read changed during collection, a size limit was exceeded, or an output cannot be created.

Successful operations print one JSON object to stdout. Comparison output lists changed or missing paths, changed context keys, and unavailable files. Unavailable verification takes precedence over known drift and retains the known differences. Invalid requests and fatal read errors print a short error to stderr. Do not treat missing output or exit `2` as a match.

Each snapshot records its format, absolute root, selected relative paths, measured byte counts, computed SHA-256 digests and context. `check` hashes the actual current files. It does not accept caller-provided hashes as evidence that current files match.

The JSON format rejects unknown fields, duplicate keys, invalid digests and duplicate file paths. Preserve snapshots if you rely on them. Editing both a snapshot and its inputs can manufacture a match because snapshots are not authenticated.

## Bounds and limitations

- At most 512 selected files, 64 MiB per file, and 256 MiB of selected file content per operation. Context and snapshot JSON each have a 1 MiB limit.
- Only regular files are read. Observed symlinks, Windows reparse points, special files and symlinked ancestors are rejected. This applies to the root, selected inputs, context, snapshot and output parents. On macOS, `/tmp` commonly aliases `/private/tmp`. Explicitly resolve your chosen root and other input/output paths to their real locations before invoking the helper. The example uses `pwd -P` for this purpose.
- The helper compares file identity, size and change timestamps before and after reading, and rechecks successful reads before creating output or returning comparison results. It detects ordinary concurrent changes. Collection is not atomic across files and is not an OS security boundary against hostile path replacement. Stop concurrent writers when stable evidence matters.
- Validation finishes before output creation. Output uses exclusive creation. A write or storage failure can leave a partial new output; inspect it before retrying with a new output path. The helper never deletes or replaces it.
- Unlisted files, dependencies, the Git index, command results, browser state, reviewer coverage and remote state remain unknown. A match does not establish scope completeness, test success, acceptance, authority, freshness after the check, or production safety.

File modes and timestamps help detect changes during a read. They are not part of the saved byte comparison. A permission-only change between separate invocations may still match if the file remains readable.

