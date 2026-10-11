# Hunyuan Image — selected model guidance

Documentation checked 9 October 2026. Use only the requested version, operation and surface below. Documentation is not account access, a native run or an output-quality guarantee. Historical versions remain valid requested targets; unavailable features require an explicit limitation, never silent substitution.

## HunyuanImage-3.0, HunyuanImage-3.0-Instruct, HunyuanImage-3.0-Instruct-Distil

Surface: Tencent official open-weight repository

### Status
new_current_discovery

### Prompting
Base is text-to-image; Instruct/Distil add text+image editing and prompt self-rewrite. README bot_task separates direct image, auto, recaption and think_recaption; do not make enhancer instructions mandatory user syntax.

### Controls
image_size auto/widthxheight/ratio; seed; system-prompt selection. Recommended example steps50 or Distil8. No native negative/count/output-format contract established; PNG shown as example.

### Guide gap
Official README usage and prompting controls qualified; no standalone comprehensive creative prompting guide found. Hosted Tencent API not audited.

### Primary evidence
- [HunyuanImage 3.0 owner repository](https://github.com/Tencent-Hunyuan/HunyuanImage-3.0). README model release/usage, lines 330–410, 418–502, 536–580 of 663; not every visual example or source file. Publication/update: not established. Access: 2026-10-09.


## Base generation versus instruction editing

Authored base T2I brief: “A small red lacquered box centered on pale stone, lid open to reveal a cream silk interior, soft top light, three-quarter product view.” For Instruct editing with a supplied result: “Close the lid; preserve the box's size, red finish, position and lighting.” These follow the repository's documented operation split, not an independently verified special prose formula.

Choose bot_task deliberately: direct image generation, automatic handling, recaptioning and think_recaption are different processing choices. Do not silently rewrite a user's literal copy or expand a concise edit into unrelated scene changes. Distil's example step count belongs to Distil; base settings and hosted Tencent controls are not interchangeable.
