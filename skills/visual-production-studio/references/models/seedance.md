# Seedance — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## 2.5

The original “Seedance 2.5 Pro” spelling is retained as a source label, not a verified separate BytePlus API alias. Resolve that selected surface before execution; do not silently erase “Pro” or assume it denotes another model.

Surface: BytePlus ModelArk native API

### Status
Public API documented; account/model activation not tested

### Source preservation
Dedicated prompt-builder branch and distinct sd25-pe optimizer

### Model ids
dreamina-seedance-2-5-260628

### Modes
text-to-video; first-frame I2V; first+last I2V; multimodal reference generation; visual/audio video editing; forward/backward extension

### Prompt
Assign each numbered asset an explicit role and borrowed dimension. Use coherent integer-second shot intervals, camera actions, exact dialogue/speakers and deliberate audio. Preserve ordered keyframes, storyboard/blockout roles and boundary continuity. Prompt reference frames are approximate; hard boundary roles are separate.

### Controls
- Duration: 4–30 seconds or -1; edit must -1
- Aspect: 16:9,4:3,1:1,3:4,9:16,21:9,adaptive; hard I2V/edit/extend must adaptive
- Resolution: 480p/720p/1080p; 1080p 10-bit HEVC
- References: Up to 30 images + 10 videos + 10 audio; videos combined <=30s; audio combined <=30s
- Task: omni_reference_task_type auto/reference/edit/extend, still checked against prompt intent
- Audio: generate_audio; native API says mono
- Seed: Not listed for this model in BAPI supported-model list
- Negative: Selective exclusions in prose; no dedicated negative field verified
- Camera: Natural-language camera; camera_fixed not listed for 2.5
- Frames: frames field is restricted to 1.0 in BAPI

### Cautions
Edit duration tolerance differs across guide/API (~0.3/0.33 vs ~0.4s). Guide says mismatched last frame stretches; API says crops. API allows legacy --parameter syntax; clean prompt separation remains a studio policy. Real-person reference eligibility is provider-specific; verify authorized portrait workflow.

### Primary evidence
- [BytePlus Seedance 2.5 prompt guide](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide). embedded primary HTML body; sections 1–477 and 908–979 inspected Publication/update: 2026-09-28T08:51:12Z. Access: 2026-10-09.
- [BytePlus Seedance 2.5 tutorial](https://docs.byteplus.com/en/docs/modelark/seedance-2-5). embedded primary HTML body; compatibility, model IDs, output settings and duration inspected Publication/update: 2026-09-28T06:48:10Z. Access: 2026-10-09.
- [BytePlus Create video generation task](https://docs.byteplus.com/en/docs/modelark/create-video-generation-task-api). embedded primary HTML body; request fields and per-model supported lists inspected Publication/update: 2026-10-08T13:25:47Z. Access: 2026-10-09.
- [ByteDance Seedance 2.5 launch](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5). primary page body opened Publication/update: 2026-07-31. Access: 2026-10-09.

## 2.0, 2.0 Fast, 2.0 Mini, source label 2.0 Pro

Surface: BytePlus native API; Dreamina app separate

### Status
2.0 family documented; exact requested Pro alias must be clarified

### Source preservation
Explicit Stage-2 target; Pro spelling remains unresolved

### Model ids
dreamina-seedance-2-0-260128; dreamina-seedance-2-0-fast-260128; dreamina-seedance-2-0-mini-260615

### Modes
text-to-video; I2V; first/last; multimodal reference; edit/extend via references

### Prompt
Use ordered shots; precise per-shot timing is unstable. Label subjects consistently by media type and ordinal, not asset IDs. Edit/extend wording directly names the master video; 'reference' may route differently. One camera movement per shot; concrete action transitions. Audio notation distinguishes music/SFX/dialogue/subtitles.

### Controls
- Duration: 4–15 seconds or -1
- References: 9 images,3 videos,3 audio; video/audio totals <=15s
- Resolution: 2.0 480p/720p/1080p/4k; Fast/Mini 480p/720p
- Seed: Not listed in current BAPI supported-model list
- Draft: Not supported by2.0/Fast/Mini; return_last_frame supported

### Cautions
Launch-level stereo claim versus current BytePlus API mono restriction is surface/version-specific. Do not replace requested 2.0 with 2.5. Guide advises consistent dialogue language and possible pronunciation substitutions: never silently change user-authored dialogue; flag feasibility instead. Multi-view character references discouraged in FAQ despite illustrative appendix; keep identity roles explicit. Tutorial examples contain timestamps although dedicated prompt guide warns exact timing is unstable.

### Primary evidence
- [ByteDance Seedance 2.0 launch](https://seed.bytedance.com/en/blog/seedance-2-0-official-launch). primary page body opened Publication/update: 2026-02-12. Access: 2026-10-09.
- [BytePlus Seedance 2.5 prompt guide](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide). embedded primary HTML body; sections 1–477 and 908–979 inspected Publication/update: 2026-09-28T08:51:12Z. Access: 2026-10-09.
- [BytePlus Create video generation task](https://docs.byteplus.com/en/docs/modelark/create-video-generation-task-api). embedded primary HTML body; request fields and per-model supported lists inspected Publication/update: 2026-10-08T13:25:47Z. Access: 2026-10-09.
- [BytePlus Seedance2.0 series tutorial](https://docs.byteplus.com/en/docs/modelark/seedance-2-0). Primary embedded HTML body extracted; model table and prompt-engineering sections inspected Publication/update: 2026-09-29T09:37:39Z. Access: 2026-10-09.
- [BytePlus Seedance2.0 prompt guide](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide). Primary embedded HTML body extracted; basic/advanced formulas, other tips and all FAQ read; appendices not fully inspected Publication/update: 2026-09-28T05:31:06Z. Access: 2026-10-09.


## Construct by operation, retaining the full original branch

For 2.5 BUILD, give a coherent physical action with its causal result; use integer-second intervals only when the requested shot structure needs them. Authored timed brief: “0–4s: tracking beside the courier as she runs to the closed gate. 4–8s: she stops, lifts the latch and pushes the gate open; camera settles behind her, revealing the garden.” A continuous take should describe a traversable camera route; a beat-cut music video should state actual cuts and sound continuity. Neither needs a forced four-beat template.

Bind each actual asset once by media type/ordinal and purpose. Character sheets A/B/C/D, storyboard grids, coarse/fine blockouts, intermediate poses and hard boundary frames are different roles. Preserve positive borrowed content plus explicit non-transfer constraints. An ordered storyboard is not an array of hard keyframes.

For 2.0, preserve English beat-by-beat or Chinese terse board-reference form. Authored 2.0 I2V: “The woman lifts the cup, pauses with it near her lips, then sets it down. Camera holds the source framing.” Ordered actions fit this guide better than promising exact sub-second shot timing. Keep 2.0 controls and aliases; source ‘Pro’ still needs clarification.

For visual/audio/camera editing, name the master video, target interval, change and protections. Authored audio-only intent: “In the supplied master video, replace only the room ambience with gentle rainfall outside; retain all visual frames and approved dialogue.” For extension, describe only the new segment and boundary position/motion; distinguish forward from backward extension. Do not satisfy edit-plus-extend by pretending one operation supports both.

Retain controlled reveals, action relays, conditional long-duration planning, green-screen plates, compositing, two-clip joins, exact multilingual speaker/dialogue ledgers, DECONSTRUCT, REMIX and the distinct sd25-pe optimization path. Use [selected Seedance method](../../video/methods/seedance.md) and its operation-specific resources. These authoring capabilities are not blanket native support claims; ultra-long output, hard timings and uncommon audio/control routes still need the exact selected surface.

Reference accounting is part of this branch: preserve the exact subject/asset cardinality, original labels, and unused-asset ledger. Do not invent additional characters or infer an attachment from a prose description. Reconcile every requested borrowed dimension with the selected version's actual role syntax.
