# LTX — documented version and operation guidance

Checked 9 October 2026. Read only this selected family. No generation or native qualification is established by these documents. Exact versions and surfaces stay separate.


### Current verified models
Hosted IDs: **ltx-2-5-fast**, **ltx-2-5-pro**. Both list T2V, I2V, A2V, portrait/landscape, and output tiers through 4K. Fast allows up to 20 seconds at the lower-resolution/lower-frame-rate combinations; Pro lists 6/8/10 seconds. Both support camera-motion controls, silent output, and automatic duration. Last-frame conditioning and automatic duration have compatibility restrictions. Neither 2.5 variant currently lists retake or extend. [LTX-2.5 API matrix](https://docs.ltx.io/models/ltx-2-5) (L1)

**ltx-2-3-pro** still supports audio-to-video, retake, and extend; **ltx-2-3-fast** supports T2V/I2V. Keep this explicit compatibility route rather than treating “latest” as a full functional replacement. [LTX-2.3 matrix](https://docs.ltx.io/models/ltx-2-3) (L2)

Open-weight identity: **Lightricks/LTX-2.5**, with official Diffusers and pre-trained collections. The model card identifies a 22B distilled transformer package and the LTX-2.x Community License. Its commercial summary distinguishes entities below/above $10M annual revenue and notes special conditions for transferring fine-tunes; the binding license must be checked. [Model card](https://huggingface.co/Lightricks/LTX-2.5) (L3)

### Official prompting coverage
The current open-source guide explicitly covers 2.5. Use chronological prose, concrete actions, visible performance cues, camera directions relative to the subject, and explicit audio/dialogue. For multi-shot output, name cuts in prose, re-identify recurring subjects, and state audio continuity at cuts. First-frame I2V generally favors one continuous take unless a cut is intentional. Optional local enhancement uses a separate rewrite pass; it is not an API CLI flag. The guide includes Dub-It-specific instructions and cautions that text accuracy and complex physics still need review. [Current 2.5-aware guide](https://docs.ltx.io/open-source-model/usage-guides/prompting-guide) (L4), [API guide](https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide) (L5)

### Preserve more than basic generation
Official open-source documentation also exposes LoRA/IC-LoRA, video input, EXR/HDR, foley, dubbing, motion/structural controls, relighting, in/outpainting, and restoration workflows. Availability must be checked per asset/runtime, rather than inferred for every hosted endpoint. [Open-source overview](https://docs.ltx.io/open-source-model/getting-started/overview) (L6)


## Chronological performance and retained retake

Authored LTX-2.5 shot: “A woman at a café table turns toward the arriving server. She smiles, lifts one hand and says, ‘Just a coffee, please.’ The camera gently moves closer to her face; cups clink softly in the background.” Observable gestures, ordered action and exact dialogue make the performance concrete. When cutting, re-identify the subject and state whether ambience continues.

For a requested LTX-2.3 Pro retake, identify the source clip, exact target interval, revised action/audio and unchanged context. Do not call the 2.5 generation endpoint merely because it is newer. Retake, extend, audio-to-video, dubbing, foley, relighting and structural-control workflows each require their documented model/runtime. An open-weight IC-LoRA or HDR workflow does not establish an equivalent hosted API operation.
