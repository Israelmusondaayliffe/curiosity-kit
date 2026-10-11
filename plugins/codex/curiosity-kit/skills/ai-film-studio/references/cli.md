# Compile and check the actual film work

Use Python 3.9 or newer; the script uses only the standard library. No installation, network, provider execution, subprocess generation, or account access is involved. These operations prepare text locally. An input JSON file is production data, **not permission** to generate, pay, upload, publish, or approve its own content. Keep the user's actual settled decisions and approval in the host conversation.

## Ordinary invocation

From the skill directory, copy `assets/project.example.json` into a user-approved temporary/project workspace and replace its original example story with the actual settled work. Do not write project outputs into the installed skill.

```sh
python3 scripts/film.py compile --project /path/to/project.json --out /path/to/project-output
python3 scripts/film.py check --project /path/to/project.json --out /path/to/project-output
python3 scripts/film.py status --project /path/to/project.json --out /path/to/project-output
```

For generic and dated Seedance 2.5 formatting together:

```sh
python3 scripts/film.py compile --project /path/to/project.json --out /path/to/project-output --targets assets/targets.json --target generic --target seedance-2.5
python3 scripts/film.py check --project /path/to/project.json --out /path/to/project-output --targets assets/targets.json --target generic --target seedance-2.5
```

Use the same target selection for compile, check and status. Profiles are dated format data, not verified current capabilities. The implemented dated reference binding is image-only: attach images in the listed order if later authorized and supported on the actual surface. Mixed image/video/audio references need a separately reviewed prompt; this compiler does not pretend to support them. `generic` works without a target file.

Operator provenance stays in the existing manifest: full dated target profiles (including source links, capture date, capability warnings and operator `technical_suffix`) plus asset identity/state/parent/version bindings. None of this bookkeeping is pasted into model prompts. Prompt references contain target image-slot bindings where applicable, project tags, reference roles in words, exact descriptors and the approved inheritance clause. Project-authored technical tags remain last; target operator instructions do not become technical prompt text. Dependency hashes still detect source/binding revisions even when prompt bytes would be unchanged.

Outputs are readable `scenes/<scene>.md`, `shotlists/<scene>.md`, and `prompts/<target>/<scene>--<shot>.txt`, plus one private-to-the-project ownership/hash manifest. The scene and individual shot choices are authored by the agent/user first. The script compiles that work; it does not invent a screenplay from a blank form. Review and deliver the actual scene, shotlist and prompts, not just the command's JSON report.

## Compact input contract

The complete original four-shot example is the definitive runnable shape. Fields:

- Project: `title`, `brief`, `formula`, `assets`, `scenes`.
- Formula: by default, `blocks` is an exact permutation of the 16 supported block names shown in the example, with `technical` last. Supplied order is honored. `descriptor_policy` is `verbatim`; `style_constant` is exact text. Other descriptor policies are rejected rather than guessed.
- Custom headed formula: optionally supply `formula.layout` as ordered groups, each `{ "heading": "EXACT HEADING:", "blocks": ["semantic_block"] }`. This takes precedence over `formula.blocks`. All 16 semantic blocks must still appear exactly once across the groups, and `technical` must be last. For example, a final group can be `{ "heading": "CONSTRAINTS:", "blocks": ["constraints", "quality", "technical"] }`. Headings are emitted verbatim as unique single lines, with each group's semantic contents concatenated in the declared order. Both generic and dated targets preserve this layout. This is data-only grouping, not executable templating.
- Exact project clauses: optional `formula.silence_rule` is appended verbatim as the final text in the audio semantic block, after SFX. Optional `inheritance_clause` on each location asset replaces the default location-reference ban with that project's exact clause. Negative wording is permitted in these safety/continuity clauses. Keep the approved ban and silence meaning; the host reviews their substance. Canonical output checking detects any alteration. Cast context always contains the exact active character count and `no duplicates`.
- Asset: safe `id`, persistent `identity`, named `state`, `parent` (`null` or another state asset ID of the same identity), `kind` (`character`, `prop`, `location`), unique `@tag`, exact `descriptor`, positive integer `version`. Every character also has locked `voice` and source `behavior` text. State parents cannot cycle.
- Scene: `id`, `title`, `dramatic_question`, complete `prose`, location asset ID, `geography`, ordered `shots`. Geography contains exact shared `text`, a `landmarks` list whose names appear in that text, `camera_side` and `reverse_rule`.
- Shot: safe `id`, story `purpose`, positive `duration` in seconds, `active` references, `first_frame` positions, `format`, `optics`, `camera`, `beats`, `physics`, `light`, `dialogue`, `acting`, `quality`, positive `constraints`, and final `technical` tags. Optional `sfx` overrides the neutral diegetic room/action sound default.
- Active reference: `asset`, exact current `version`, and `role`: `identity` for character, `prop-state` for prop, `geography` for location. Only one state of each identity can be active. The scene location must be active. Every active descriptor is reproduced exactly; inactive descriptors are excluded.
- First frame: exactly one entry for each active character and prop: `asset`, named `landmark`, nonnegative `distance_m`, `frame_side` (`left`/`right`) and `gaze`. For a prop, `gaze` describes its orientation. Opening occupancy is restated after every cut.
- Beat: numeric `start`, `end`, and positive present-tense `action`. Beats cover the duration contiguously, with at most three sentences each. Quoted dialogue belongs in audio only. The camera should participate in the action text.
- Light: exactly `source` and `motivation`. One motivated source is permitted. Obvious compound-source wording is rejected; this is not a general natural-language lighting solver.
- Dialogue: `speaker` (an active character asset ID), exact `line` without enclosing quotes, positive `action`, positive `reaction`. The compiler emits locked voice, quoted line, action, reaction in that order, plus silence for other characters during each line and a whole-shot silence list. Empty dialogue produces a silent cast. Music goes to post; permitted generated audio is dialogue and diegetic SFX.
- Acting: mapping of every active character asset ID to an observable, scene-specific performance. The locked behavior paragraph is a source for rewriting this performance, not a paragraph pasted into every shot.
- State change: when an identity switches asset between shots, that shot must explicitly declare `state_changes: {"identity": "new-asset-id"}`. First encounter establishes its state. State persists across scene boundaries. Every later shot uses the new asset until another declared change. This declaration records a filmmaker decision; it cannot grant approval.

Scene prose is the dramatic source. Shot dialogue must already be reconciled with it by the author; the script cannot infer screenplay dialogue semantics from arbitrary prose. For crowded scenes, design the crowd as an asset with a stated count and use the playbook's human review; the compiler's character count counts active character assets, not independently detected people.

## What checks mean

`check` rereads the source, validates its structural continuity and formula constraints, independently recompiles expected text, then compares **each real emitted file** with that result. It does not trust a fixture saying it passed, nor trust the manifest's output hashes as content validation. A planted descriptor paraphrase, missing silence instruction, second light, stale state, wrong location inheritance, changed duration, or any other byte-level alteration of an emitted prompt fails. Reordered blocks are checked against the supplied order, not merely counted.

Source validation additionally rejects stale asset versions, undeclared state switches, duplicate identities/tags, wrong roles, missing first-frame occupants, unknown landmarks, invalid time ranges, overt negative-action phrasing, quoted dialogue in action, and obvious compound light declarations. Location references always include the explicit composition, camera angle and colour inheritance ban. Geography and style are shared exact constants.

These checks establish deterministic fidelity, **not creative or pixel quality**. They cannot establish that a prose descriptor contradicts another, detect every second light described indirectly, judge motion feasibility from duration alone, identify emotion-only acting, prove a scene's dramatic effectiveness, inspect media, or prove current target-service support. Review those separately. The roughly one-second opening wide, available shot budget, behavior transfer, physically feasible action speed, age handling, project-specific ban-word substitutions and no lens look unless requested remain author/reviewer checks. Do not claim a native host or media-generation pass from these CLI tests.

## Revision, repair and resume

`status` and `check` are read-only. `compile` never changes the source JSON. The manifest stores output content hashes and source-dependency hashes, not approval. A changed source marks only dependent outputs stale. A changed locked behavior also invalidates prompts that use that asset, even when the rendered text has not yet changed: rewrite the acting before recompiling when that change calls for it. Unaffected files retain their bytes and modification times. An unchanged repeat writes nothing, including the manifest.

If a real emitted file was edited outside the compiler, `compile` stops before overwriting anything. Reconcile intentional changes back into the source. After an authorized repair, use `compile ... --repair` to replace only changed manifest-owned files. This flag is a local overwrite instruction, not external-action permission. Files unknown to the manifest are never overwritten on a collision, even with `--repair`; unrelated paths are untouched. Unsafe IDs and output symlinks are refused.

Removed/renamed scenes, shots or targets appear as `obsolete`; the compiler keeps them and their ownership history, never silently deletes them. `check` continues to report `needs-work` until the user resolves that old output set, for example by approving a fresh output directory for the revised scope. Do not delete files or reset the manifest merely to manufacture a pass.

Exit 0: compilation completed, or check/status is current. Exit 1: actual outputs need attention. Exit 2: invalid input, unsafe/colliding output, or other blocked operation. Read the JSON report's per-file reason: `missing`, `stale-source`, `modified-output`, `unowned-conflict`, or `current`.

## Public CLI regression tests

From the library root:

```sh
python3 evals/ai-film-studio/test_cli.py
```

The tests run the public commands in temporary directories with original sample data, inspect actual scene/shotlist/prompt text, plant prompt and source defects, prove selective source revision, check data-driven target bindings, preserve unrelated files, and verify repeated compilation performs no writes. They run no model, network, host-installation or paid-provider operations.
