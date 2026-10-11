# HunyuanVideo — documented version and operation guidance

Checked 9 October 2026. Read only this selected family. No generation or native qualification is established by these documents. Exact versions and surfaces stay separate.


### Current verified core
**HunyuanVideo-1.5**, official weights **tencent/HunyuanVideo-1.5**. Its repository lists 480p and 720p T2V/I2V, CFG-distilled and sparse variants, a 480p I2V step-distilled model, and separate super-resolution stages to 720p/1080p. The reference implementation requires NVIDIA CUDA and lists 14 GB minimum GPU memory with offloading. Its examples are visual-generation workflows; do not promise synchronized native audio from the core model. [Repository](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5) (H1)

### Official prompting coverage
A dedicated versioned English handbook is available and was read. T2V guidance combines an identifiable subject, motion, and setting, then adds framing, camera movement, lighting, style, and atmosphere. I2V focuses on subject motion, environmental motion, and optional camera direction. It also documents stylistic, lighting, and camera vocabulary with examples. The material is more specific than a generic cinematic prompt checklist. [HunyuanVideo 1.5 Prompt Handbook](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/assets/HunyuanVideo_1_5_Prompt_Handbook_EN.md) (H2)

### Access and lifecycle
The official community license excludes the EU, UK, and South Korea from its defined territory, and has additional large-service commercial conditions. Preserve this as an eligibility gate rather than describing unrestricted open source. [License](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/LICENSE) (H3)

Retain the older HunyuanVideo and HunyuanVideo-I2V identities where already present. Separate family adjuncts include **HunyuanVideo-Avatar** for audio-driven human animation and **HunyuanVideo-Foley / Foley-XL** for generated sound accompanying video. The latter repository dates XL's release to 2025-09-29. These are separate capabilities, not evidence that 1.5 itself produces audio. [Avatar](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar) (H4), [Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley) (H5)

**HunyuanCustom** is another distinct released route for identity-preserving image/text, audio-driven, and video-driven customization. Its repository documents subject replacement and multiple conditioning paths; do not collapse these into basic first-frame I2V. [Official repository](https://github.com/Tencent-Hunyuan/HunyuanCustom) (H6)


## Guide-backed T2V/I2V example

Authored HunyuanVideo-1.5 T2V: “A red paper lantern hangs above a narrow stone lane at dusk. The lantern swings slowly in the breeze as warm light reveals its paper ribs. Medium close shot, gentle forward camera movement, cool blue shadows.” For I2V, reduce repeated appearance description: “The lantern swings slowly and settles; a light breeze moves the leaves in the background. Gentle forward camera movement.”

The handbook supports these distinct visual/motion constructions. Avatar, Foley/Foley-XL and HunyuanCustom require their own audio, video or identity conditioning; they are not flags that turn core 1.5 into a universal audiovisual model. Keep license eligibility separate from the quality of an authored prompt.
