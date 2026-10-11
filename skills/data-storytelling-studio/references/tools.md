# Tools and execution contracts

The runtime method has no compulsory personal sibling, model, online service or package install. Use supported host tools already available. Respect explicit model/provider choices; otherwise select suitable available capabilities by task, tool access and cost. Exact benchmark model names are development evidence only.

## Host and format prerequisites

Load the installed entry through the host's actual supported skill mechanism. A namespace varies between standalone and combined packages; inspect it rather than assuming a slash command exists. Root owns Codex/Claude packaging metadata. This source does not install or register itself.

Plain readouts/reports can be complete Markdown files with local SVG exhibits and source references. Python 3.9+ on a POSIX host is needed only for the bundled chart helper. Native .docx/.pdf/.pptx/.xlsx/notebook exports, browser interactions and hosted sites require actual format capabilities. Prefer supported document, slide, spreadsheet, plotting and browser tools; read their current instructions before using them. Do not infer availability from a plugin name or run another host's catalog CLI. Inspect only the capabilities the selected output needs.

A missing optional reviewer does not prevent substantive writing. A missing required renderer prevents a claim of rendered quality. A missing hosting tool or authority prevents publication. Deliver a complete useful fallback when appropriate and label the unmet requested format exactly. Do not install dependencies, start a service, add credentials or invoke a provider as a presence probe.

## Local dot plot

`scripts/chart.py` produces one self-contained SVG with no network resources, from an explicit checked UTF-8 CSV. All rows are plotted in file order. Column selection and title/caption/source/alternative text are explicit. No filtering, aggregation, estimates, sorting or metric calculation occurs. Choose a purpose-built checked summary upstream; do not hide inconvenient rows to make the plot look better.

From the skill directory, with an existing authorized output directory:

```sh
python3 scripts/chart.py assets/example.csv \
  --label label --value rate --unit 'Percent completed within target' \
  --title 'Overall completion fell while both case types improved' \
  --caption 'Fictional checked summary. Case mix changed; these observations do not establish a policy effect.' \
  --source 'example.csv, all six rows; definitions in example-method.md' \
  --alt 'Overall completion fell from 82.7 to 33.6 percent. Routine and complex case rates both increased.' \
  --out /actual/authorized/output/completion.svg
```

Replace the output path with the actual authorized location. The SVG file must not already exist, even as a symlink; use a new version for a revision. Parents are not created. An existing input/output is never overwritten. Under a frozen/resume contract, pass `--expect-sha256 ACTUAL_INPUT_HASH`; mismatch stops before output. The normal output includes the exact source hash for later comparison.

For supplied uncertainty intervals, add `--lower lower_column --upper upper_column` together. Each pair must contain its value. The caption must explain the actual interval meaning and method from the source; the script cannot infer those. Use another real plotting capability when the requested encoding is not a categorical dot plot.

Input limits: 1 MiB, 1–30 rows, unique nonempty headers, distinct selected columns, unique displayed labels, complete rows and finite decimal values. Blank/missing/ragged rows are rejected, never treated as zero or dropped. Comma-grouped or localized numeric strings require an explicitly checked conversion outside this helper. The value labels preserve supplied numeric strings; the axis uses approximate tick formatting. The domain includes zero. Descriptive text is escaped as XML and embedded source metadata records only the CSV basename/hash and selected columns, not the full input path.

Exit 0 means rendered; exit 2 means invalid/unavailable input, stale identity, unsupported bounds or write failure. Argparse help exits 0. The report explicitly leaves source truth, statistics, caption support, visual inspection and publication authority unverified. It is not an OS sandbox: parent paths resolve through the host filesystem, and an output write interrupted by OS failure can be partial. Inspect the actual named output before retrying; do not erase unrelated files.

## Actual inspection and delivery

Open/render the emitted SVG through an available image/browser tool. Confirm text, values, intervals, order and scale against the CSV, and inspect clipping and legibility at the intended size. Read its accessible description and retain an adjacent table when the audience needs exact values. An XML parse is not visual proof. Preserve privacy rules for both visible values and embedded metadata.

For a requested native artifact, verify the actual export opens and inspect its final pages/slides/interactions. Tie the review to the exact artifact version. Keep generated file, render result, uploaded file, hosted deployment and recipient access distinct. None of these grants permission for the next external action. A local delivery does not authorize sharing raw evidence or activating refresh/monitoring.
