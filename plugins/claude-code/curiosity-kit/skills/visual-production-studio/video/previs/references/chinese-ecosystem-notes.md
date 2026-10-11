# Chinese Ecosystem Notes

Current use: follow [previs method](../../methods/previs.md) and `validation-contract.md` for mode-specific timing, actual upload roles, autonomy and evidence. Version names and provider behavior in imported examples are historical, unverified here; reuse their craft without treating them as current native controls or rankings.
The Chinese-language AI filmmaking ecosystem (UISDC tutorials, Jimeng / Dreamina platform, Bilibili / Xiaohongshu communities) leads in observed Previs-to-Sequence variants. Load this when the user requests Chinese-language prompts or works within Jimeng / Dreamina.

## Language choice

The imported examples include Chinese-language filmmaking prompts. Keep their useful idioms and terse forms. These examples do not establish model training composition, language superiority or platform feature parity. Use the user's language; translation is optional.

## Terse Stage 2 form

The Chinese variant of Stage 2 is dramatically shorter than the English beat-by-beat version. The terse form leans on the storyboard reference doing the heavy lifting. Seedance reads the composite as keyframes without needing English to spell out every beat.

Canonical terse form:

```
根据故事板分镜生成[N]秒视频。参考图：@Image1（分镜脚本）。保持角色一致性，无文字、无字幕。
```

Literal English translation: "Generate a [N]-second video according to the storyboard panels. Reference image: @Image1 (storyboard script). Maintain character consistency. No text, no subtitles."

Expanded form (still terse compared to English):

```
根据故事板分镜生成[N]秒视频，主题：[topic]。
参考图：@Image1（分镜脚本）。[character refs as @Image2, @Image3 if multi-character].
风格：[style]，[palette description]，写实电影感，4K，超清。
保持角色一致性，按照分镜顺序逐帧生成，无文字、无字幕、无水印。
```

## Chinese Stage 1 idioms

Recurring phrases in UISDC and Jimeng tutorials. Use these in Chinese-language Stage 1 prompts when the user works in that ecosystem.

| Chinese | Literal English | Use |
|---|---|---|
| 导演示意图 | director's diagram | Stage 1 board format |
| 分镜设计板 | storyboard design board | composite layout |
| 分镜脚本 | storyboard script | the composite as a structural document |
| 镜号 | shot number | per-panel label |
| 写实 | photorealistic | style modifier |
| 电影感 | cinematic feel | style modifier |
| 高级感 | high-end aesthetic | luxury or premium register |
| 超清 | ultra-clear | resolution modifier (often paired with 4K or 8K) |
| 4K / 8K | 4K / 8K | resolution declaration |
| 比例 | aspect ratio | aspect declaration |
| 整体排版工整规范 | overall layout neat and standardized | layout quality directive |
| 表格 | table | tabular layout (commercial board format) |
| 画面风格全程统一 | visual style unified throughout | consistency directive |
| 无任何多余元素 | no extraneous elements | cleanliness directive |
| 无水印、无乱码 | no watermarks, no garbled text | safety belt |

## Subtitle conventions

Chinese Stage 2 examples often close with 无文字、无字幕 ("no text, no subtitles"). This is the safety belt against the model rendering Chinese characters into the video frame, which is a possible annotation-bleed failure. Keep intentional brand text or subtitles when requested.

Extended subtitle safety belt:

```
无文字、无字幕、无水印、无乱码。
```

Literal English: "No text, no subtitles, no watermarks, no garbled text."

## Three-model pipeline pattern

Atlas Cloud's Ranx tutorial and similar variants use a three-model pipeline rather than two-model:

1. **GPT Image 2** for character sheet plus storyboard composite.
2. **Nano Banana 2 (Gemini 3 Pro Image)** for environment concept separately.
3. **Seedance 2.0** for video, consuming all three references.

The example separates environment development from the structural board. No comparative fidelity claim is established here. The storyboard's environment panels stay schematic; the actual environment reference comes from Nano Banana 2.

Stage 2 prompt for three-model pipeline:

```
根据故事板分镜生成15秒视频。
参考图：@Image1（分镜脚本）、@Image2（角色参考）、@Image3（环境参考）。
风格：[environment style description]，写实电影感，4K，超清。
保持角色一致性和环境一致性，按照分镜顺序逐帧生成，无文字、无字幕、无水印。
```

## Jimeng / Dreamina platform notes

Jimeng (PRC market) and Dreamina (international market) are ByteDance's Seedance front-ends. Model versions and controls may differ by account and surface; inspect them before execution.

**Jimeng:** Chinese-first interface. Reference image upload labeled 参考图. Inspect actual reference and audio controls; do not assume a nine-image limit.

**Dreamina:** English-first interface. Use the actual attachment labels exposed by the selected surface; historical tag examples below are not a current API contract.

Keep the requested language. No cross-platform quality equivalence has been verified in this repair.

## Audio handling conventions

In the Chinese ecosystem, audio is often referenced separately rather than described inline:

```
音频参考：@audio_file_1（背景音乐），@audio_file_2（音效合集）。
```

Literal English: "Audio reference: @audio_file_1 (background music), @audio_file_2 (sound effects collection)."

For pure SFX (no music), inline natural-language descriptions work:

```
音效：第1镜重低音冲击，第3镜陶瓷碎裂声，第5镜瀑布水流声。
```

Literal English: "Sound effects: shot 1 deep bass impact, shot 3 ceramic shatter, shot 5 waterfall sound."

## Mixed-language user guidance

If the user is bilingual or works across both ecosystems:

- Use English Stage 1 prompts for international image models (GPT Image 2 in ChatGPT, Gemini in AI Studio).
- Use Chinese Stage 2 prompts for Jimeng / Dreamina. Switch to English Stage 2 for Veo Flow, Kling international, or other non-ByteDance platforms.
- The Chinese terse Stage 2 form is compact and board-led; effectiveness requires actual output inspection. Suggest it when the user works primarily in Jimeng / Dreamina.

When the user writes their brief in Chinese, mirror their language. When they write in English, default to English with Chinese as an alternate option ("Want the terse Chinese version instead?").

## UISDC tutorial structure

UISDC tutorials follow a consistent format:

1. Brief description in Chinese (topic, duration, aesthetic).
2. Stage 1 prompt in Chinese (one paragraph, dense, with all parameters inline).
3. Generated storyboard image embedded.
4. Stage 2 prompt in Chinese (terse, often one or two sentences).
5. Generated video embedded.

When deconstructing a UISDC variant, expect the Stage 1 prompt to be one long paragraph rather than a structured template. Translate to a structured skeleton for clarity, but keep Chinese tokens when the user wants the terse form back.

## Common Chinese-ecosystem failure modes

- **Mixed-script glyph errors:** When the prompt is in Chinese but contains English brand names or character names, the model sometimes renders them as Chinese characters or stylized glyphs. Mitigation: quote the exact requested spelling and inspect the result; do not invent a translation of a brand name.
- **Aspect ratio assumed 16:9:** Chinese-ecosystem tutorials default to 16:9 even when the user wants 9:16. Always declare aspect explicitly.
- **Style drift toward Chinese aesthetic defaults:** Seedance 2.0 has a slight bias toward CG-stylized Chinese commercial aesthetics. Mitigation: state target style explicitly in both Chinese and English ("写实电影感, cinematic photoreal") to anchor against the bias.
