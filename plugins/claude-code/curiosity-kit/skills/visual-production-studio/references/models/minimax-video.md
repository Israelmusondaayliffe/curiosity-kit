# Hailuo / MiniMax — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## Hailuo unversioned original, H3, H3 Max

Surface: Hailuo app guide / MiniMax native API

### Status
H3 documented; do not auto-resolve bare Hailuo

### Source preservation
Hailuo original mention-only duration example; H3 current expansion

### Model ids
MiniMax-H3; MiniMax-H3-Max

### Modes
T2V; I2V first/last; H3 and H3 Max multimodal reference

### Prompt
Hailuo guide structures subject/action/setting/camera/lighting/style and bracketed camera moves. I2V should focus on action and camera. H3 requires text plus explicit typed reference roles.

### Controls
- Duration: H3 4–15s;H3 Max5–15s
- Resolution: H3 768P/2K;Max480P/768P
- References: Both variants: ≤9 reference images, 3 videos totaling ≤15s, 3 audio clips totaling ≤15s; mixed total 12 files
- Aspect: Adaptive plus 21:9, 16:9, 4:3, 1:1, 3:4, 9:16; T2V explicit ratio; I2V follows input
- Seed: Not found in inspected schema
- Negative: Not verified
- Prompt: ≤7000 characters; H3 Max extra.prompt_expansion_mode defaults balanced

### Cautions
Hard first/last I2V roles cannot mix with reference_image/video/audio roles. H3 Max is fal.ai-post-trained; distinguish provider-specific behavior. Hailuo2.3 launch is verified, but current version-specific API status and prompt controls not fully audited.

### Primary evidence
- [Hailuo prompt anatomy](https://hailuoai.video/pages/blog/ai-video-prompt-anatomy). primary article body opened Publication/update: 2026-07-21. Access: 2026-10-09.
- [MiniMax H3 video generation](https://platform.minimax.io/docs/api-reference/video-generation-v2-create). primary API body opened Publication/update: not established. Access: 2026-10-09.
- [MiniMax video generation guide](https://platform.minimax.io/docs/guides/video-generation). primary page body opened; relevant model/mode sections inspected Publication/update: not established. Access: 2026-10-09.
- [MiniMax Hailuo2.3 launch](https://www.minimax.io/news/minimax-hailuo-23). primary page body opened; relevant model/mode sections inspected Publication/update: 2025-10-28. Access: 2026-10-09.


## Reference role and motion examples

Authored H3 I2V: “The cat turns its head toward the opening door and steps down from the chair. The camera follows at floor height.” The initial frame establishes appearance. For H3 multimodal-reference creation, identify borrowed subject identity, motion and sound separately using actual typed inputs; do not mix first/last-frame roles with reference roles in one incompatible request.

The Hailuo camera vocabulary belongs to the guide and selected UI. Bracketed camera commands should use a verified supported term, not an invented phrase in brackets. A plain-language camera instruction is safer when the exact command vocabulary is unqualified.

For H3 Max, make prompt expansion visible when preserving exact dialogue or shot structure. The original unversioned Hailuo duration example stays historical and unresolved; it is not evidence that bare “Hailuo” means H3 or that Hailuo 2.3 has identical controls.
