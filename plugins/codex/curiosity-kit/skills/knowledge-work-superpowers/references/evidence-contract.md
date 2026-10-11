# Evidence record and checker

Use this record and helper whenever a substantial file deliverable requires a traceable evidence record, for example because the user asks for one or the governing completion gate requires a checkable record. Run it on the final artifact before claiming completion, without a parallel bespoke verifier or duplicate Markdown record. Chat answers, small tasks and ordinary file drafts without that requirement do not need JSON. The former seven-file Markdown bundle checker is replaced by this single record, not supported as a second interface. Preserve the useful source IDs, claim status and traceability checks without parsing arbitrary Markdown tables.

## Run it

Prerequisites are Python 3.9 or later, its standard library, and authorized read access to the explicitly selected files. No installation, network, API key, source retrieval or runtime framework is needed. Resolve the script and example relative to the actual installed skill directory. These commands assume that directory is your current directory.

```sh
python3 scripts/check_evidence.py --help
python3 scripts/check_evidence.py assets/evidence-example.json
python3 scripts/check_evidence.py /authorized/work/evidence.json --artifact /authorized/work/report.md
```

The filled synthetic example deliberately records an unreviewed artifact. It returns exit 1 with two `REVIEW_INCOMPLETE` findings. Supplying an artifact without a recorded review hash adds `ARTIFACT_UNREVIEWED`. Do not change these fields to pass just to clear the command. Review the actual artifact first.

Exit 0 means the declared structure is consistent under these checks. Exit 1 reports consistency findings, including unresolved review blockers. Exit 2 means bad input, schema, I/O or command usage. Help exits 0. Findings print to stdout as `LABEL location: detail`; invalid input prints `INVALID_INPUT` to stderr, while argparse prints usage errors. Neither path emits a Python traceback. The checker stops at the first malformed schema or input error; repair it and rerun to obtain relational findings.

The program reads only the command-line record and optional artifact. It never follows recorded locations, origin references, URLs or dependencies to files. It writes no files and does not recurse through directories. Record input is limited to 1 MiB, artifact input to 32 MiB. Inputs must be regular files. The record and Markdown artifact must be valid UTF-8. Binary non-Markdown artifacts receive byte presence and SHA256 identity checks only. For larger artifacts use a suitable separate identity check and state that this checker did not inspect them.

## Version 1 fields

All listed keys are required; extra keys are rejected so misspellings do not silently disappear. Objects, lists and strings must have their stated types. `version` is the integer `1`, never a Boolean. IDs are `S1`, `S2`, ... for sources and `C1`, `C2`, ... for claims. No leading zero or whitespace is allowed. IDs must be unique within their group. Every list of strings has nonempty, unique entries. Empty lists are allowed unless a rule below says otherwise. All prose fields must contain non-whitespace text. This checks presence, not the honesty or quality of that text.

Top-level fields are `version`, `sources`, `claims`, `review`. Sources and claims are lists. An empty list is useful for a record that genuinely has no sources or factual claims; it is no proof of complete coverage.

Each source has:

- `id`, `title`, `location`: identity, useful title and exact user-authorized URL, file locator or supplied-text location. Locations are prose and are never opened by the checker.
- `type`: `primary`, `secondary` or `discovery`. Search snippets, search results and uninspected leads remain discovery evidence.
- `access`: `full`, `partial`, `supplied`, `unread` or `inaccessible`. Supplied means the actual supplied excerpt was read, not that the unseen underlying document was read. Full means the claimed whole source was actually inspected.
- `read_extent`: what was actually read, including section, page or line boundaries for partial reading. Use exactly `none` for unread or inaccessible sources. Do not describe retrieval alone as a read.
- `publication_date`, `accessed_date`: actual calendar dates in `YYYY-MM-DD`, or exactly `unknown`. Accessed date is the actual read or access-attempt date. Publication date can describe the relevant version date. Never invent a date to satisfy the checker. Unknown dates are valid.
- `origin_ids`: source IDs for known originating evidence. Empty means no identified upstream source in this record, not proven independence. Self-origin and unknown IDs are findings. The helper does not resolve provenance or establish independence.
- `passages`: exact useful passage locators, with brief excerpts when permitted. Read sources need at least one. Unread and inaccessible sources require an empty list. A supplied excerpt's location must distinguish it from the unseen full source.

Each claim has:

- `id`, `text`: one material factual claim and its identity. Recommendations can remain in the human artifact with their factual premises recorded here.
- `status`: `supported`, `inferred`, `disputed` or `unresolved`.
- `source_ids`: known source IDs. Supported, inferred and disputed claims require a source. Supported and inferred claims require at least one read, non-discovery source with a passage locator. This is only a necessary structural condition for support.
- `depends_on`: known claim IDs for material dependencies. Self-dependency and longer cycles are findings. An empty list means no recorded dependency; it does not prove none exists. Assess propagation to dependent conclusions manually when evidence changes.
- `rationale`: why this status fits the actual evidence, including uncertainty, inference steps and scope limits. It is delivered text: keep it within the same population and denominator limits as the artifact. No compulsory confidence score is used.
- `counterevidence`: relevant contradictory passages or evidence and their locators. Empty means none recorded, not that exhaustive disconfirmation succeeded. A disputed claim needs at least one entry. Contradictions within one source are valid; two different source IDs are not required.
- `artifact_locations`: human-readable locations of affected text, such as a named section, paragraph, caption or slide. An empty list is valid before drafting. These locators support navigation, not automatic coverage or actual-location verification.

`review` has:

- `reviewed_sha256`: lowercase 64-character SHA256 of the exact artifact bytes reviewed, or `unknown`. Record it after reviewing those bytes. A recorded hash alone does not establish that a review happened.
- `requirements_verdict`, `evidence_verdict`: each `pass`, `fail` or `unreviewed`. Record requirement compliance separately from evidence, reasoning and reader quality. Anything except `pass` produces `REVIEW_INCOMPLETE`.
- `findings`: a list of objects with exactly `severity`, `state`, `location`, `detail`, `resolution`. Severity is `critical`, `important` or `minor`; state is `open` or `resolved`. The remaining fields are nonempty prose. Detail names the defect and evidence, location identifies affected text, and resolution explains the actual repair or what remains needed. An open Critical or Important defect produces `REVIEW_BLOCKER`, even if both verdicts say pass. Minor open findings do not block structural exit 0. Resolution prose cannot prove a defect was fixed.

## Artifact checks and finding labels

With `--artifact`, the helper checks a nonempty file and compares its SHA256 to the recorded reviewed version. An unknown hash means unreviewed; a mismatch means the artifact changed. Without the option it prints `ARTIFACT_NOT_CHECKED`; exit 0 can still occur, and does not certify artifact identity.

For filenames ending in `.md` or `.markdown`, canonical markers are `[[source:S1]]` and `[[claim:C1]]`. Put them at useful locations only if this convention suits the artifact. Unknown IDs inside exact markers are findings. Scanning is literal across the whole file, including code fences and quotations, so quoted examples need known IDs or should avoid this optional convention. Ordinary links, bare IDs, malformed markers and unmarked prose are not a coverage check. No marker minimum is imposed. Non-Markdown files print `ARTIFACT_IDENTITY_ONLY` and receive no content parsing.

Stable finding labels are `DUPLICATE_ID`, `UNKNOWN_ORIGIN`, `SELF_ORIGIN`, `READ_EVIDENCE_MISSING`, `UNREAD_EVIDENCE_CONFLICT`, `UNKNOWN_SOURCE`, `UNKNOWN_DEPENDENCY`, `CLAIM_SOURCES_MISSING`, `NO_READ_SUPPORT`, `COUNTEREVIDENCE_MISSING`, `DEPENDENCY_CYCLE`, `REVIEW_INCOMPLETE`, `REVIEW_BLOCKER`, `EMPTY_ARTIFACT`, `ARTIFACT_UNREVIEWED`, `ARTIFACT_CHANGED` and `UNKNOWN_ARTIFACT_REFERENCE`.

Duplicate JSON keys, nonstandard NaN/Infinity constants, unexpected fields, invalid types, dates or enums, malformed IDs, repeated string-list entries, invalid UTF-8 and oversized files are invalid inputs, exit 2. A structurally valid list that repeats a source or claim ID produces `DUPLICATE_ID`, exit 1. If both malformed input and consistency findings exist, exit 2 takes precedence.

## Synthetic example and checks

The entire fictional primary source is: "Eight people attended the workshop. Ten people registered." The example records its first sentence without inventing a publication date, causal explanation or review. These are invented sample facts, not a claim about a real event.

Development self-checks live outside runtime in `evals/knowledge-work-superpowers/test_check_evidence.py`. From the repository root run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s evals/knowledge-work-superpowers -p test_check_evidence.py -v
```

They use temporary sample files and cover both correct and deliberately wrong records, CLI exits, bounded input, review identity, references and the no-implicit-read boundary. The shipped helper has no fixture-writing or self-test mode.

A consistent schema cannot establish truth, inferential validity, arithmetic, source independence, current freshness, complete factual coverage, review approval, user consent, authority, rendering, acceptance or delivery. Inspect actual passages and the complete current artifact, compute quantities independently, and use the appropriate format parser or viewer. An unavailable check remains unperformed. A tool result cannot authorize a send, publication or other action.
