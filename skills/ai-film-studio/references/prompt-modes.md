# Prompt modes and preservation

Use the mode the user requested. The scene compiler handles structured shot-generation text. The following modes are complete local prose methods, not claims that every provider exposes these operations.

## Image asset preparation

Read the [asset playbook](../playbooks/assets.md). Write natural prose naming the subject, identity/state, reference role, composition needed for its use, materials and controllable lighting. Keep model settings in the real UI when known. Separate a neutral identity sheet from the scene look.

Original output form:

    Purpose and subject: [the reusable asset and approved state].
    Identity/material: [exact approved descriptor].
    View: [the view needed to prove or reuse it].
    Environment/light: [only the conditions needed for this asset].
    Reference influence: [what each reference controls and excludes].
    Proof: [what must be inspected before the asset is approved].

Check that each clause serves the requested asset. A character sheet needs its distinct views; a location needs playable geometry; a prop needs scale and contact. Do not apply mandatory palette percentages or a vendor's default style. Repair the earliest failing asset property and preserve the approved master.

## Surgical visual or audio edit

Identify the sole source/master and actual requested change. Inspect it where possible; label inaccessible content instead of inventing observations. Specify replacement/removal, the exact region/time/subject affected, and all protected elements. A moving-subject replacement inherits the original path, timing and occlusion while protected people remain unchanged. An audio-only edit preserves visual frames and changes only the approved audio property.

    Master: [source ID and inspected range].
    Change: [one precise visual or audio correction].
    Preserve: [identity, position, motion, timing, camera, light, sound or other protected facts].
    Boundary: [where the change begins/ends and how it joins unchanged material].
    Check: [visible/audible comparison proving the correction and preservation].

Do not derive exact motion or timestamps from sparse previews. Missing precision requires an honest range or a requested inspection step. Review both the change and preserved elements; if they drift, return to the master rather than accumulating full-frame rerenders.

## Extension

For forward extension, inspect the source's ending and carry its subjects, count, positions, movement, light, sound and unresolved action into the new beginning. For backward extension, end at the existing opening state and avoid introducing later props or events early. Keep one instance of each entity and preserve spatial connections.

    Source boundary: [observed terminal/opening state].
    Direction and length: [requested forward/backward interval].
    Continuing facts: [identity, topology, ownership, motion, sound].
    New action: [bounded events ending in a specified state].
    Join check: [what must agree at the boundary].

If the user asks for an edit and an extension, first repair and approve the source boundary, then extend that revised source. Do not merge two operations into an ambiguous request. A provider that cannot extend remains an unavailable execution route; a text plan can still be delivered as a plan.

## Key states, storyboards and blockouts

List supplied first, last and intermediate states in their given order. Preserve shot numbering and causal relationships. For a storyboard, map each panel to the intended shot/beat and the elements it controls. For a coarse blockout, map each geometric object to exactly one final entity. For a fine blockout, distinguish pose/trajectory/camera guidance from final material/style. Exclude guides, labels and production annotations from the intended film image.

    Ordered source states: [IDs and inspected observations].
    Mapping: [source element -> final entity and permitted influence].
    Action between states: [causal, feasible transitions].
    Preserve: [counts, ownership, topology and story outcome].
    Check: [each required state, correspondence and absence of guide artifacts].

Asset understanding must respect explicit user labels. Report a conflicting visual observation instead of silently remapping characters. Account for unused references. No profile promises pixel-perfect matching or frame-accurate control merely because the prompt asks for it.

## Final pass

Give one best complete prompt unless variants were requested. Compare it to the story/dialogue contract, active references, declared mode and preservation scope. Honor the requested language. Name target syntax or live-control uncertainty separately; never fabricate an attachment, upload or generated result.
