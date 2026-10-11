# Build a source-grounded Sites artifact

Use this route for a Sites teaching resource, portfolio, report, workspace, dashboard, planner, gallery, catalog, prototype or small tool, including an artifact whose interface must follow a user-selected visual library. Sites supplies the available hosting and execution features. Web Product Studio owns the product, source decisions, implementation and acceptance. Use the user's chosen sources and visual preferences. A website that is not using Sites can use the other Web routes without this platform workflow.

Load [the host contract](../references/host-contract.md) for the current Sites capabilities. Read the host's building and hosting instructions before their respective actions. Use supported tools, available project conventions and the smallest sufficient implementation. An unavailable platform action remains a named gap; it does not justify a donor installation or a new account. Keep the requested local, preview, private or public scope throughout.

## 1. Name the artifact's job

Record the audience, the moment of use, what that person must understand or do, the smallest suitable format and observable first-version acceptance. Choose the format by the job:

| Job | Useful format | Content and controls |
| --- | --- | --- |
| Learn and apply a method | Teaching reference | Plain explanation, realistic examples, complete copyable material, search and navigation |
| Inspect selected work | Portfolio or gallery | Curated work, captions and provenance, filtering and full-size viewing |
| Understand evidence | Interactive report | Claims tied to data, uncertainty, comparison and relevant exports |
| Choose among alternatives | Review workspace | Comparable options, criteria, consequences and the actual choice control |
| Track or coordinate work | Board, tracker or launch calendar | Real records, owners and dates, filters and authorized updates |
| Revisit operational information | Dashboard or recurring review hub | Dated measures, latest snapshot, changes, exceptions, questions, decisions and actions, with period comparison or valid refresh behavior |
| Explore assumptions | Calculator or planner | Inputs, rules, units, outputs and reset or comparison |
| Find reusable knowledge | Registry, catalog or brief library | Identifiers, facets, source context, search and detail views |
| Start or join work | Onboarding or knowledge hub | Context, people, useful links and first steps, with search, a relevant checklist or copy controls |
| Demonstrate an idea | Prototype | Representative content, selected journey and explicit limits |
| Practice behavior or run a process | Simulation, game or workflow app | Real rules, state, feedback, roles and recovery appropriate to the job |

Combine formats only when one audience needs them together. A teaching portfolio may combine explanation, selected images, prompts and image inspection. Do not add a game, wizard or simulated dashboard merely to make a resource interactive.

## 2. Start the platform without choosing the design

For a new project, initialize the authorized project and preview through the current Sites route. Inspect what it creates. Do not start product edits or select a generic visual constitution before the source pass. Preserve the original human creation intent where the tool supports that field.

For an existing Site, inspect its actual source and rendered artifact. Record the approved structure, working controls and access level. Classify the requested changes as job, content, sources, curation, visual system, interaction or release. Freeze unrelated approved parts. Current tool availability is the source of truth for storage, authentication, access modes and integrations; do not assume a public website can read the owner's connected accounts.

## 3. Build the visual source field

Use the user's explicit source order when supplied. Otherwise start with this task-scoped order:

1. Explicit references supplied for this task.
2. A user-selected visual library or moodboards, if any.
3. Other relevant authorized assets, which may include Midjourney, Google Flow, FLORA or local files.
4. Public research that answers a named gap or broadens the comparison.
5. Generated exploration after the available source field is understood.

More sources do not settle a design. Record what you inspected, selected, rejected or could not access, and why. A specific approved task reference can control the direction without an unrelated library tour. Otherwise inspect relevant work in the selected library before choosing the UI style; if no library was selected, use the brief and authorized sources rather than assuming one. If missing access could materially change the result, pause that decision and ask for the smallest needed access or alternative. Continue independent work. Record when a selected source is not relevant, superseded by a supplied reference or unavailable; never mark it inspected from a remembered summary.

### Inspect the appropriate library

- Midjourney: use an available authorized signed-in browser. Read the named or relevant populated boards and projects broadly before selecting. Record board/project, useful job URL, inspected scope, composition, crop, palette, density and material. Capture exact visible prompt text and parameters. Never reconstruct a private prompt from an image and label it exact.
- Google Flow: inspect relevant projects, alternate frames and outtakes. Keep original project/media identifiers in the private source record. Use selected available high-resolution media. A signed-in project URL cannot be a public source link.
- FLORA: prefer the connected tool for structured board state; inspect the rendered interface when needed for image or prompt evidence. Preserve meaningful board, group, model, prompt and output relationships. Process evidence and publishable work may have different eligibility.
- Local assets: inventory the authorized folder without moving, renaming or deleting originals. Filter by actual project, format, dates and dimensions. For a large set, use a contact sheet, then inspect finalists at full size. Copy only the selected assets into the controlled task source folder when that use is authorized. Record origin, filename, dimensions and rights.
- Public references: retain author, source URL, relevant qualities and known use terms. Research access does not grant permission to reproduce a whole identity, photograph or font.
- Generated work: use an available suitable model only when generation, sharing of its inputs and any spending are authorized. Preserve input-reference identities, exact prompt, model/settings, output and curation choice. A new image is a new source version. It cannot silently replace the approved reference.

Separate private research locators from public display fields. `public_eligibility: allowed` needs a supported rights and privacy decision; ownership or account access alone is insufficient. An allowed image can still have a private prompt, project ID or URL. Store only cleared fields in `public_projection` and keep disallowed fields out of the export.

## 4. Compare reference-derived directions

Compare directions only when a material visual choice remains unresolved or the user asks for alternatives. Use the smallest useful set at matched content, viewport and medium; three is an option, not a quota. For a straightforward authorized local preview, choose a reversible brief-led direction and record that assumption rather than inserting a design contest. Each cites inspected source IDs and defines layout/rhythm, color, typography, image treatment, material, motion or deliberate stillness, a useful signature tension and what it avoids. Differences must affect the reading hierarchy, composition or primary interaction, not only the palette. Use [the design method](design.md) for comparable renders and interpretation.

Use the current Sites design picker when a user selection is actually needed and the picker is available. Wait for the user's choice only when that consequential decision remains theirs; an authorized reversible implementation choice does not need another approval pause. An already approved direction needs no new contest. Reference-led work uses `design_constitution: null`; derive tokens from the selected evidence rather than applying a second generic style. If no option works, combine specific compatible qualities, explain the tradeoff and compare the revised direction before broad implementation.

## 5. Freeze the six grouped records

Copy [sites-records.json](../assets/sites-records.json) into the task's evidence folder and replace the synthetic example with the actual task. It is a planned record, not a release receipt. Its six groups preserve separate duties in one file:

| Group | Planned record | Final acceptance record |
| --- | --- | --- |
| `brief` | Job, audience, moment, content outline, required provenance and exact delivery intent | Same accepted scope, with actual source joins and current required content |
| `sources` | Available candidates, pending inspection and unresolved eligibility are honest states | Inspection evidence for used sources, exact prompt provenance where claimed, eligibility resolved for every public item |
| `curation` | Hold decisions may identify pending inspection | Every used source has a selected decision and reason; rejected, retired and held material stays outside the release |
| `authority` | Direction and tokens may remain unresolved before selection | Selected direction, inspected source joins, actual design rules, avoided qualities and rejected options |
| `profile` | Applicable profiles and every required check, initially unrun | Each applicable check passed with bound evidence for this source/build and intended audience |
| `release` | Requested delivery/access, prospective check plan, null build/deploy/retrospective values | Exact source/build/flow/review records, actual applicable access/deployment/health observations and a short retrospective |

Use the canonical [acceptance contract](../references/acceptance-contracts.md) for the detailed field meanings. All local evidence joins are `{ "path": "relative/path", "sha256": "actual lowercase SHA-256" }` under the selected evidence root. Use actual hashes, not the explanatory text shown here. Internal source joins use the declared source IDs. Keep the existing [acceptance flow](../assets/acceptance-flow.json) as the interaction contract; do not invent a parallel interaction schema.

Validate with the skill's own helper:

```bash
python3 scripts/check_web_evidence.py sites /absolute/task/sites-records.json --root /absolute/task
```

Run this from the installed skill root, or use the script's resolved absolute path. A passing planned record means its declarations are well formed. It does not approve a build, prove source inspection, grant release permission or establish quality. Final validation is an acceptance-success claim. Preserve failed and blocked observations in the task record and report incomplete work; do not move them to a final success record merely to finish the form.

### Teaching-library profile

Use `teaching-library` for teaching Sites, playbooks and searchable reference resources. Complete all six checks:

- `first-time-reader-explanation`: every core concept explains what it is, why it helps and how to use it in language the intended newcomer understands.
- `practical-examples`: representative examples demonstrate the actual method, including the choice or result that makes the example useful.
- `copyable-material`: prompts, commands or templates are complete. Drive the copy control and compare the clipboard result with the exact visible text, including line breaks, punctuation and parameters. Keep provenance separate from the copy payload. Truncated visual previews must expose the full text before copying; label any intentional transformation.
- `search`: test a relevant query, a changed query, no results, clearing/reset and keyboard use against known result IDs. If filters combine with search, verify their combined rules and counts.
- `working-controls`: exercise every visible filter, copy, download, navigation and disclosure control. Confirm the destination or effect, not only a success toast.
- `mobile`: read, search, inspect an example, copy and navigate at the required narrow viewport. Record hardware-specific gaps separately from desktop emulation.

### Public-source-privacy profile

Also use `public-source-privacy` for public artifacts whose research includes private or mixed-access sources. Complete all five checks before public acceptance:

- `public-source-whitelist`: an explicit allowlist covers every public source name, URL, attribution, identifier and prompt. `release.public_source_ids` joins selected, inspected sources with allowed eligibility and cleared `public_projection` fields.
- `private-source-redaction`: prohibited names, URLs, account/project IDs, paths, prompts and attribution are absent from rendered text and packaged data. Removing a visible source button alone is insufficient.
- `export-scan`: inspect the actual built assets, downloads, inline data, metadata, source maps and public API responses. Check both forbidden private markers and completeness against the allowlist. Do not copy private ledger files into the build.
- `anonymous-route-test`: exercise each intended public route, asset and download in a clean unauthenticated context. An owner's signed-in browser is insufficient. Also confirm private-only routes and data remain inaccessible when relevant.
- `source-release-parity`: bind the scanned source, built package, saved Sites version, deployment receipt and live result. A scan of yesterday's source does not clear today's export.

Both profiles apply to a public teaching library built from mixed private and public sources. One profile's pass cannot replace the other's evidence.

## 6. Build with real content

Use [the local build method](build.md), representative final content and selected real assets. Write the plain teaching explanation first. Add examples that demonstrate it, then controls that help readers find, compare, inspect or reuse the material. Remove repetition that adds no decision or understanding.

Keep exact prompt text as one canonical value used for display and copying. Escape it as content, not executable markup. Test long prompts, line breaks, parameters, quotation marks and unicode. Preserve source-specific distinctions: an exact visible prompt, a workflow description and a prompt that is private or unavailable are different things. Do not fill missing provenance with plausible text.

Provide real loading, empty, error and partial-data behavior where the artifact needs it. Use actual counts derived from displayed data, or omit counts. A link or download must work for the intended audience. Never substitute a generated stand-in for available approved material merely because retrieval takes effort.

## 7. Verify every promise

Use [verification](verify.md) for separate functional and visual verdicts. The Sites acceptance flow includes all visible controls and required reading, retrieval and state-changing journeys. In particular:

- Open full-size images; test close button, backdrop close, Escape, focus entry, background inertness and logical focus return. Test previous/next order and endpoints where shown.
- Check exact copy results, downloads and source destinations. Observe clipboard-denied or download-failure behavior when applicable.
- Exercise keyboard, supported touch interactions and desktop/mobile layouts. Inspect image loading, missing media, overflow, long text, zoom and meaningful console errors or warnings.
- Check all displayed counts against the actual content and all access promises from the intended viewer's perspective.
- For updates that persist, read the durable effect back through a second request or consumer. A click animation is not a saved change.

Give an independent evaluator the frozen brief, selected direction, exact build and fresh rendered artifact. Do not supply a desired verdict. Record their identity and evidence, including remaining disagreement. A builder's self-review or an `independent: true` field cannot establish independence. If independent review is unavailable, disclose the gap and do not claim this route's final acceptance.

## 8. Revise the named failure

Classify the failed observation before changing anything. A weak explanation needs a content correction; inaccessible source links need an access correction; a visual mismatch needs a bounded visual change. Do not redesign approved navigation to repair prompt copying.

After a correction, replay the failed flow and affected neighboring behavior using fresh artifacts. Keep the first failure and superseded receipt. Unchanged checks may carry forward only when their actual inputs and dependencies remain unchanged. Stop broad revision once the user calls the artifact satisfactory; remaining sign-off changes are surgical. Use an explicit time/iteration or no-progress boundary when the task needs one, and report the next discriminating step rather than repeatedly generating alternatives.

## 9. Deliver, and retain the useful lesson

Follow [delivery](deliver.md) at the requested scope. For an authorized Sites deployment, the ordered chain is:

1. Validate the exact candidate and applicable profiles.
2. Freeze the source. Commit only if authorized; otherwise use a content identity and report the uncommitted boundary.
3. Package that source and bind the output to it.
4. Save the Sites version through the current platform tools.
5. Deploy that version to the approved audience.
6. Poll the actual deployment to its terminal result within the task's authorized observation period.
7. Test the live artifact and access as the intended viewer. Keep deployment success separate from live health.
8. Save what worked, what failed, the cause of the correction and the next useful change. Record "none observed" only when true.

A local-only request ends with the tested local artifact and its evidence. Its deployment fields remain `not-requested` and live health `not-required`; this can be complete within that scope. A requested public release with blocked anonymous access or unresolved source eligibility is incomplete. Deliver useful permitted work with the exact blocker instead of widening access or hiding the gap.

## Source-derived method case: a visual teaching portfolio

Read this case when a teaching artifact keeps accumulating revisions or when the builder needs to distinguish content, interaction, source and sign-off failures. This depersonalized case preserves eight lessons from private historical work. Its private release records are not bundled; the case is not installation, acceptance or new execution proof for this package.

The artifact's job was to teach a visual framework and prove it with a portfolio of actual work. Readers needed to understand the framework, inspect full images and reuse complete prompts. They did not need a game to make the framework feel interactive.

| Release | Interpretation and failure | Corrective decision |
| --- | --- | --- |
| 1 | A scripted teaching experience used scenes and lesson mechanics that competed with the framework. | Put the framework, plain explanation and visual evidence first. Remove the forced lesson rather than polish its mechanics. |
| 2 | Simplification left a stage-based interface. The framework and portfolio needed continuous reading rather than a staged progression. | Change the information architecture to match reading and browsing. Keep a visible content outline and let readers move directly between explanation and work. |
| 3 | A game-like process simulator treated "interactive" as a request for game mechanics. | Define interactivity as working, useful controls. Test navigation, image inspection, prompt copying and downloads against actual reader tasks. |
| 4 | The editorial teaching portfolio looked more appropriate, but generated stand-ins outweighed the owner's real work. | Inspect the task-selected source libraries, such as Midjourney, Flow, FLORA or local assets, before generating. Select authentic examples that demonstrate the taught method. |
| 5 | A larger owned-source portfolio fixed the source mix but substituted quantity for curation. | Compare candidates by teaching role, composition and fit. Reject weaker or repetitive examples, and record why each retained image earns its place. |
| 6 | Taste-led feedback arrived after a satisfactory structure existed; a broad redesign would risk approved work. | Freeze structure and behavior. Limit this pass to curation, copy and the distinctive visual qualities that the feedback actually concerned. |
| 7 | The portfolio-completeness pass exposed inaccurate or incomplete prompt and source detail. | Preserve exact visible prompt text, parameters and tool-specific provenance. Compare copied text with the displayed complete prompt, and distinguish private source records from public destinations. |
| 8 | Sign-off found small public-source and attribution gaps. | Make only the named corrections. Scan the final export, check source eligibility and test the actual live public artifact before declaring release complete. |

For a similar task, define the continuous reading structure in the brief, inspect owned sources before direction selection, and place exact-copy and public-access checks in the acceptance flow before implementation. During review, classify each finding using its actual cause. A private source URL in an otherwise approved gallery needs a source/access correction, not another layout direction.

Keep the useful feedback at its proper level. ELI5 context belongs where a first-time reader needs it. Images need full-detail viewing and reliable closing behavior. More examples earn their cost only if they add understanding. Independent review should inspect the final artifact. Once the user says the artifact is satisfactory, preserve the structure and accept only bounded sign-off changes.

The case's historical repository paths are omitted because they are private provenance, not portable runtime dependencies. Its private source identity remains outside the distribution; source-family attribution and rights limits are preserved in [NOTICE](../NOTICE).
