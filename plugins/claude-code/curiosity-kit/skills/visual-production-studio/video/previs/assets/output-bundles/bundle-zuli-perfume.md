# Bundle: ZuLi Perfume Ad (UISDC Commercial Pair)

Preserved worked example, not a current model capability claim or a user-approved recipe. Check actual upload roles and selected-surface controls before use. Final artistic acceptance belongs to the user or the creative reviewer explicitly designated for the current task.
Reference for the commercial table format and terse Chinese Stage 2 form. Luxury product ad, 15s.

## Brief

- Subject: a luxury perfume bottle, brand name "ZuLi"
- Motion register: slow atmospheric product reveals (rotation, mist, light play)
- Environment: high-key white studio with gold accents, marble surface
- Duration: 15 seconds
- Aspect: 16:9
- Palette: high-key white, gold, soft amber, deep ebony bottle
- Panels: 6 storyboard rows in table format (each row = duration + visual + narration + SFX + transition)
- Target image model: GPT Image 2
- Target video model: Seedance 2.0 (Chinese terse syntax)

## Stage 1 prompt (GPT Image 2)

```
生成一张短视频分镜设计全图。

主题：15秒高端香水广告分镜脚本
香水品牌："ZuLi"
整体排版工整规范，表格与对应参考画面一一对应，画面风格全程统一，无任何多余元素、无水印、无乱码。

脚本结构需包含 6 个分镜行，每行包含以下列：
- 分镜号
- 时长（秒）
- 画面描述
- 旁白台词
- 音效
- 转场方式

分镜 1（0 to 2.5s）：宏观特写镜头，金色光线穿过水雾，香水瓶在白色大理石台面上缓缓显现。旁白："ZuLi。" 音效：低频氛围声 + 轻微水雾声。转场：淡入。
分镜 2（2.5 to 5s）：俯视镜头，香水瓶静置中心，金色光晕从顶部洒下。旁白："每一滴，都是时间的痕迹。" 音效：玻璃轻响。转场：硬切。
分镜 3（5 to 7.5s）：低角度推近，喷雾从瓶口扩散成金色雾霭。旁白：（静默） 音效：精致喷雾声。转场：硬切。
分镜 4（7.5 to 10s）：中景，女模特半身侧影，金色雾霭萦绕脖颈。旁白："你的存在，已被记住。" 音效：心跳一次。转场：交叉淡化。
分镜 5（10 to 12.5s）：宏观特写，光线穿过香水瓶折射出琥珀色光斑。旁白：（静默） 音效：玻璃水晶轻撞。转场：硬切。
分镜 6（12.5 to 15s）：广角静止，香水瓶在白色背景中央，品牌字"ZuLi"缓缓浮现。旁白："ZuLi。专属于你。" 音效：尾音淡出。转场：淡出。

风格：16:9 写实风格，电影感，高级质感，超清，8K。
画面风格：高调白色 + 金色光晕 + 深乌木瓶身。
负面：水印、乱码、多余文字、廉价质感。
```

## Stage 1 expected output description

A landscape 16:9 sheet formatted as a commercial pitch table. 6 storyboard rows, each row showing a small visual thumbnail on the left and metadata columns on the right (duration, visual description, voiceover, SFX, transition). High-end commercial aesthetic with white and gold dominant. Product (perfume bottle) is the recurring visual anchor.

## Stage 2 prompt (Seedance 2.0, Chinese terse form)

```
仅需根据故事板分镜生成 15 秒香水广告视频。

参考图：@Image1（分镜脚本全图）。
保持品牌一致性，保持香水瓶外观一致性。

[0 to 2.5s] 镜 1：宏观特写，金色光线穿过水雾，香水瓶缓缓显现于白色大理石台面。旁白："ZuLi。" 音效：低频氛围 + 轻微水雾。
[2.5 to 5s] 镜 2：俯视镜头，香水瓶静置中心，金色光晕从顶部洒下。旁白："每一滴，都是时间的痕迹。" 音效：玻璃轻响。
[5 to 7.5s] 镜 3：低角度推近，喷雾从瓶口扩散成金色雾霭。旁白：（静默） 音效：精致喷雾声。
[7.5 to 10s] 镜 4：中景，女模特半身侧影，金色雾霭萦绕脖颈。旁白："你的存在，已被记住。" 音效：心跳一次。
[10 to 12.5s] 镜 5：宏观特写，光线穿过瓶身折射出琥珀色光斑。旁白：（静默） 音效：玻璃水晶轻撞。
[12.5 to 15s] 镜 6：广角静止，香水瓶在白色背景中央，"ZuLi" 字幕缓缓浮现。旁白："ZuLi。专属于你。" 音效：尾音淡出。

镜头：50mm 等效，浅景深，电影质感。
色彩：高调白、金色、暖琥珀、深乌木。全片色调一致。
风格：写实电影感，超清，8K。
画面比例：16:9。
保留结尾要求的“ZuLi”品牌字；无多余文字、无对白字幕、无水印。
```

## Notes on expected output

- Chinese terse form (根据故事板分镜生成...) is the documented Seedance 2.0 idiom that ships in UISDC tutorials. Its compactness is useful; no language-quality or training-data claim is established here.
- For Western markets, swap to English literal translation (see the Stage 2 English variant below) and keep the structural beats identical.
- Product macro fidelity is the failure point. Seedance 2.0 occasionally morphs the bottle silhouette across shots. Mitigation: upload a clean product reference photo as @Image2 alongside the storyboard and add "保持瓶身一致" (maintain bottle consistency).

## English literal translation (optional drop-in)

```
Generate a 15-second perfume ad video from the storyboard. Reference: @Image1 (full storyboard).
Maintain brand and bottle identity throughout.

[0 to 2.5s] Shot 1: macro close-up, gold light pierces water mist, perfume bottle slowly appears on white marble. Voiceover: "ZuLi." SFX: low ambient + faint mist.
[2.5 to 5s] Shot 2: overhead, bottle centered, gold halo from above. Voiceover: "Every drop, a trace of time." SFX: glass chime.
[5 to 7.5s] Shot 3: low angle push-in, atomized spray expands into gold mist. Voiceover: (silence) SFX: refined spray.
[7.5 to 10s] Shot 4: medium, female model in profile, gold mist around her neck. Voiceover: "Your presence is remembered." SFX: single heartbeat.
[10 to 12.5s] Shot 5: macro close-up, light refracts through the bottle into amber highlights. Voiceover: (silence) SFX: crystal glass tap.
[12.5 to 15s] Shot 6: wide static, bottle centered on white, "ZuLi" wordmark slowly resolves. Voiceover: "ZuLi. Yours alone." SFX: tail-out.

Lens: 50mm equivalent, shallow DoF.
Palette: high-key white, gold, warm amber, deep ebony. Consistent throughout.
Style: cinematic photoreal, 8K.
Aspect: 16:9. Preserve the requested final “ZuLi” wordmark. No unrelated text overlays, dialogue subtitles or watermarks.
```

## Variant family

Commercial Ad Table (Stage 1 Skeleton 3) plus Seedance Chinese Terse (Stage 2 Skeleton 2). Product subject, table layout, dual-language Stage 2 are the structural deltas from canonical.
