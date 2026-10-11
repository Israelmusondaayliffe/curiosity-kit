# Model lookup: load one selected family

Evidence snapshot: 9 October 2026. Resolve modality → exact family/version → operation → provider surface → reference roles. Open only the matching profile and needed operation; do not load this whole catalog's linked files. Bare or ambiguous names require clarification when they select different contracts. A newer release never overrides a named older version.

Evidence labels describe prompting documentation, not access, execution or quality: **G** = substantive official guide sections reviewed; **E** = schema/model-card/implementation/examples; **U** = unresolved guide, surface or lifecycle gap. Mixed labels apply per branch, not every version. Dates and actual read depth are in each profile; an access date is not a release date. Authored examples illustrate the cited guidance and have not been generated. Generic fallback examples are explicitly identified. No profile is natively qualified by static tests.

## Image

| Family / lookup aliases | Profile | Evidence / qualification |
|---|---|---|
| OpenAI Images; GPT Image 2; ChatGPT Images 2.5; Flare/Sunburst | [openai-image](openai-image.md) | G: Product/API and retained GPT Image 2 |
| Gemini image; Nano Banana 2 / 2 Lite / Pro / 2.1 | [google-image](google-image.md) | G: Shared guide; conflicting reference quotas |
| Seedream 5.0 Lite / Pro / Flash; 4.0 / 4.5 catalog | [seedream](seedream.md) | G/E: Pro/Flash coordinate guide; Lite schema/release |
| Recraft V4 / V4.1 / Flash; raster/vector | [recraft](recraft.md) | G/E: V4-family guide; Flash example/schema only |
| Luma Uni 1.1 / Max; historical Uni-1 | [luma-image](luma-image.md) | G: Historical snapshot mapping unverified |
| Ideogram 4 / 4.5; 3.0 / 2a / 2.0 catalog | [ideogram](ideogram.md) | G/E: Native caption schema; hosted conversion distinct |
| Midjourney V7 / V8.1 / V8.2; Edit; Draft; Void Style Hunter | [midjourney](midjourney.md) | G: Web/Discord only; Draft conflict retained |
| Google Imagen; Imagen 4 / Fast / Ultra | [imagen](imagen.md) | G/U: Original recipe retained; audited endpoints retired |
| FLUX 3 Image; FLUX.2 max/pro/flex/dev/klein; Kontext; older FLUX/tools catalog | [flux-image](flux-image.md) | G/E: 3 boxes differ from 2 structured prose |
| Qwen Image 3.0 / 2.1; PE-T2I / PE-I2I; older Qwen catalog | [qwen-image](qwen-image.md) | E: Hosted schema; PE-I2I instructions unqualified |
| HunyuanImage 3.0 / Instruct / Distil | [hunyuan-image](hunyuan-image.md) | E: Repository usage; no complete craft handbook |
| Wan 2.7 Image / Pro; older Wan/wanx image catalog | [wan-image](wan-image.md) | G/E: Usage guide; standalone prompt guide unread |
| Z-Image / Turbo; Omni-Base / Edit announced | [z-image](z-image.md) | E/U: Model-card examples; announced entries unavailable |
| Adobe Firefly Image 5 / 4 / 4 Ultra | [firefly-image](firefly-image.md) | G: Product guide; API parity unverified |
| Microsoft MAI Image 2.6 / Flash; 2.5 / Flash / Pro | [mai-image](mai-image.md) | E: Foundry preview schema/examples |
| Grok Imagine Image 2.0 / quality / pro / 1.0 | [grok-image](grok-image.md) | E: Quality/pro alias retirement scheduled 2 Nov 2026 |
| Runway Gen-4 Image / Turbo / References | [runway-image](runway-image.md) | G: Base and reference-mode guidance differ |
| Reve 2.1; generation/edit/layout | [reve](reve.md) | E/U: Official release; current API guide inaccessible |
| Amazon Nova Canvas | [amazon-canvas](amazon-canvas.md) | G: Inpaint/outpaint mask roles differ |
| Amazon Titan Image Generator G1 / v2 | [amazon-titan](amazon-titan.md) | G/U: HTML guide; PDF unavailable, lifecycle unverified |
| Amazon Nova 2 Omni | [amazon-omni](amazon-omni.md) | E/U: Multimodal schema; image operation details unqualified |
| SDXL; Stable Diffusion 3.5 Large/Medium/Large Turbo; Stable Image | [stable-diffusion](stable-diffusion.md) | U: SDXL recipes retained; current guide/schema gap |
| Leonardo Lucid Origin / Realism; Phoenix 1.0 / 0.9 | [leonardo](leonardo.md) | G/E: Product tips and Phoenix-specific references |
| Bria FIBO / FIBO Lite | [bria-image](bria-image.md) | G: Bridge and renderer are distinct processing stages |
| Kolors; IP-Adapter; ControlNet | [kolors](kolors.md) | E: Repository examples; no current craft guide verified |
| HiDream-O1-Image Full / Dev 8B / Dev-2604 | [hidream](hidream.md) | E: Owner usage; optional prompt agent distinct |
| Krea 2 | [krea](krea.md) | G: Product style references/moodboards |

## Video

| Family / lookup aliases | Profile | Evidence / qualification |
|---|---|---|
| Seedance 2.5; 2.0 / Fast / Mini; sd25-pe | [seedance](seedance.md) | G: Native BytePlus; source Pro aliases unresolved |
| Kling 3 / 3.0 / Omni; 4.0 / Flash | [kling](kling.md) | G/U: App guides; API shell; 4.0 staged access |
| Veo 2 / 3.0 / Fast; 3.1 / Fast / Lite; GA vs preview | [veo](veo.md) | G/U: Historical authoring and per-surface lifecycle |
| Gemini Omni 1.1 Flash / Flash Preview | [gemini-omni](gemini-omni.md) | G/E: Separate family from Veo |
| Runway Gen-4 / Turbo / 4.5; Aleph2; Act-Two; Characters | [runway-video](runway-video.md) | G/E: Characters catalog-only detailed prompting |
| Luma Ray3 / Modify; Ray3.2 | [luma-video](luma-video.md) | G/E: Ray3 product versus Ray3.2 API |
| Pika V2.2; Pikaframes; 2.5 / Keyframe | [pika](pika.md) | G/E: Old FAQ conflicts; version-specific endpoint schemas |
| Hailuo; MiniMax H3 / H3 Max; Hailuo 2.3 | [minimax-video](minimax-video.md) | G/E: Unversioned Hailuo unresolved; role exclusivity |
| Vidu Q4 Preview; Q3 variants; Q2 / Q1 / 2.0 | [vidu](vidu.md) | G/E: Older catalog shallow; Q4 schema conflicts |
| Midjourney Video; source V1 | [midjourney-video](midjourney-video.md) | G: Image V7 is not Video V1 |
| Adobe Firefly Video; Video2 Preview | [firefly-video](firefly-video.md) | G/E: Native and partner surfaces distinct |
| Grok Imagine Video 1.5 / Lite / classic | [grok-video](grok-video.md) | G/E: Classic-only edit/extend; 1.5 reference/keyframes |
| FLUX 3 Video; FLUX Video Edit | [flux-video](flux-video.md) | G: Generation/continuation/edit separate; Omni Reference announced |
| Amazon Nova Reel | [amazon-reel](amazon-reel.md) | G: Storyboard interval vs long-prompt modes |
| Bria video editing; removal/replacement/masks/upscale | [bria-video](bria-video.md) | E/U: Overview; exact per-endpoint prompting gap |
| HunyuanVideo 1.5 / I2V; Avatar; Foley / XL; HunyuanCustom | [hunyuan-video](hunyuan-video.md) | G/E: Core handbook; adjunct repository routes |
| LTX-2.5 Fast / Pro; LTX-2.3 Pro / Fast; open weights | [ltx](ltx.md) | G/E: 2.3 Pro retake/extend retained |
| Wan 3.0 / Prime; 2.7 / 2.6 / 2.5 / 2.2 / 2.1; Wan-Animate-2 | [wan-video](wan-video.md) | G/E/U: Hosted 3 guide; 2.2 linked guide unread |
| CogVideo / CogVideoX; X1.5; older 2B/5B/I2V/continuation | [cogvideo](cogvideo.md) | E/U: Owner converter; linked broader guide inaccessible |
| Mochi 1; genmo/mochi-1-preview | [mochi](mochi.md) | E: Preview card examples; no newer release verified |
| HappyHorse 1.1 T2V/I2V/R2V; 1.0 edit/generation | [happyhorse](happyhorse.md) | E/U: Native R2V binding; dedicated guide retrieval unresolved |

## Discovery and retained provenance

The selected FLUX image, Qwen image, Wan image, Z-Image, Seedream and Ideogram files include the 45 supplemental catalog entries from the bounded image survey. They remain discoverable names with their own missing/shared-guide status; catalog presence does not qualify an adapter. Unknown names require exact source verification, not nearest-family substitution. This is not an exhaustive current model catalog.

Sora video active routes are retired by the approved scope; original Sora source provenance remains in audit fixtures. This exception does not retire OpenAI images, older versions in other families, or any non-Sora authoring method. Model-neutral image/video work uses the selected method and common contract without borrowing another family's unsupported controls.
