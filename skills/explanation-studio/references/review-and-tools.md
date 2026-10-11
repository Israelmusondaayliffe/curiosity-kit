# Fidelity, inspection and delivery

Use these checks for artifacts and consequential rewrites. Scale them to the task. One sentence needs a careful read, not a formal report.

## Meaning review

Compare the final output with the source and request, not merely with an earlier draft.

- Main claim and scope: does it answer the actual question?
- Conditions and logic: are if/unless/only/not/and/or attached to the right action or claim?
- Confidence: did may/likely/unverified become certainty? Are recorded rationale and inference separate?
- Quantities: are number, unit, denominator, range and timing preserved?
- Identity: are function names, flags, versions, source subjects and error text exact where necessary?
- Effects: are completed, attempted, proposed, failed and unknown actions distinguished?
- Copy others will repeat: does every line of a suggested customer message, announcement or caption stay within the sources? It must not invent an ongoing investigation, a promised follow-up or service action, or what the end user saw. Keep counts exact in each line ("at most three attempts in total", not "tries again up to three times"). Leave anything the sender must supply or confirm as a visible placeholder.
- Prerequisites: does each step rely only on concepts introduced or actually known?
- Limitations: are essential warnings and analogy/model boundaries visible at the point of use?

Try a normal case and a contrasting or boundary case that could expose a misleading account. A convenient example is not proof of all cases. If the source itself is inconsistent, preserve or explain the conflict rather than silently fixing it in a summary.

For an analogy, check the real mechanism after removing the story. For a diagram, review every important relationship and direction. For an interactive model, compare displayed outputs with hand-derived expected values. For teaching, distinguish authored questions and reference answers from the learner's actual response.

## HTML checker

Resolve the skill directory using the host's actual installed path. Run the shipped file with an absolute artifact path:

```sh
python3 /resolved/skill/directory/scripts/check_html.py /absolute/path/explainer.html --json
```

Replace both example paths with actual resolved paths before running. Do not guess a personal installation location. The script works from any current directory and accepts one positional file plus optional `--json`. Its Python interface is `inspect_file(Path)`.

Requirements: Python 3.9+ and read access to the target file. Standard library only. No installation, network call, file rewrite or rendering occurs. It reads at most 1 MiB plus a sentinel byte and reports size, read and UTF-8 failures.

Output fields are `status`, `errors`, `warnings`, `limitation`.

- Exit 0: the documented static checks passed. Warnings can still require review.
- Exit 1: static findings or input/read failure.
- Exit 2: command-line argument error.

It checks HTML5 doctype, language, title, viewport, one h1/main, a visual structural marker and image-alt presence. It inspects common HTML/CSS/SVG resource attributes, imports and obvious JavaScript networking. Citation links differ from automatically loaded assets. Inline code, event handlers and motion require manual review. A visual marker or empty alt attribute can satisfy structure without satisfying the meaning.

The report is not factual verification, an accessibility audit, a JavaScript sandbox, an isolation guarantee, an offline certificate or evidence of learning. HTMLParser is tolerant, not a complete HTML conformance validator. CSS and JavaScript detection is deliberately incomplete; static pass must never be translated into a broader PASS. Do not make the checker silence a real issue by deleting evidence or changing the requested deliverable.

If a valid unsupported construction triggers a finding, inspect it and state the limitation. For example, only `data:image/` URLs count as inline, so an embedded `data:` font is reported as a resource dependency; system fonts avoid that. Prefer a simpler equivalent when it serves the request. Do not change the installed checker or waive a required runtime check during an ordinary explanation task without appropriate authority.

## Actual-medium review

A standalone HTML file needs actual opening and visual inspection if rendering is part of the request. Use the available browser's supported methods. Check a narrow and wide viewport, full content, labels, overlap, reading order and visible qualifications. Test keyboard focus and each promised control. Reduced-motion CSS presence is not proof its behavior is appropriate.

To claim no external-resource operation, inspect the actual artifact's resource behavior through supported browser/network capabilities, including the interactions exercised. If those observations are unavailable, say that only static dependency checks were completed. Even an observed no-request run covers only its conditions and actions.

An SVG or raster image needs pixel inspection at a useful size. An editable scene needs an actual editability check if promised. A video needs actual playback, duration, relevant frames, audio/caption and synchronization checks. An existing file extension proves none of those.

Keep the output inspectable without unnecessary tools. Native HTML disclosure and inline SVG are often sufficient. Do not install a rendering stack when an available tool meets the same requirement. Paid media, external publication and private-data transmission remain separately governed.

## Tool prerequisites and honest alternatives

| Work | Actual prerequisite | If unavailable |
|---|---|---|
| Explain supplied text | Readable complete relevant source | Ask for the missing passage or limit the source-specific claim |
| Explain current/code behavior | Appropriate authoritative lookup or source inspection | Give clearly bounded general explanation; no guessed implementation |
| Write standalone HTML | Authorized task output and file-writing capability | Return useful content/plan; requested file remains incomplete |
| Run checker | Python 3.9+, shipped script, readable file | Report checker unrun; do not substitute “looks valid” |
| Render/test HTML | Supported browser/inspection capabilities | Deliver authored file with rendering/interaction pending |
| Requested image/export | Compatible actual renderer or generation tool | Distinguish source/plan from rendered format |
| Playable narrated video | Actual renderer/composer plus requested audio capability | Complete plan, identify missing production portion |
| Delegate extension | Eligible available helper and task authority | Own local core still works; extension remains explicit |

Do not assume a missing tool in one view means the whole supported environment lacks it. Check the actual host's discovery/access route. A known access denial is not permission to bypass it. An equivalent alternative must meet the requested outcome, not silently reduce it.

## Return the useful result

Use the host's native attachment/artifact route. Check the returned identity and accessibility for the intended user. Preserve a useful local artifact if sending fails. A broken delivery link or inaccessible private path is not successful delivery.

Mention only material checks and limits in the ordinary response. Keep authored, structurally checked, rendered, exercised and learned as distinct claims. If a source or tool is missing, state the affected portion and smallest next step. No automatic publication, schedule or cleanup follows.
