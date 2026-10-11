# Example Storyboards

This folder is a pointer set, not a media library. The skill cannot host or redistribute the source storyboard images. Each entry below is an anchor case used by the DECONSTRUCT mode to test recognition rules in `../../references/in-the-wild-variants.md`.

When a user uploads an existing storyboard, the agent matches it against these anchor cases to identify the variant family.

## Canonical anchors

### 1. Kōda Forest Rebirth
- Creator: Kōda (@aimikoda)
- Source: X post
- Model pair: GPT Image 2 + Seedance 2.0
- Subject: aggressive contemporary dance, forest spirit transformation
- Duration: 15s
- Panels: 12 (3 by 4 grid)
- Why canonical: The four-color arrow legend (Red = camera, Blue = subject, Yellow = light, Green = environment) originated here. This is the reference for arrow convention defaults across the skill.

### 2. Hiphop Ink-Brush Dancer
- Creator: Abdul Shakoor (@abxxai)
- Source: X post
- Model pair: GPT Image 2 + Seedance 2.0
- Subject: ink-wash hip-hop dance in white space
- Duration: ~15s
- Panels: 8
- Why canonical: Established the per-panel timeline format (0:00 to 0:15 with SFX per beat). Style is monochrome ink-brush, infinite white environment, beat-synced motion.

### 3. Teppanyaki Cooking Sequence
- Creator: Abdul Shakoor (@abxxai)
- Source: X post
- Model pair: GPT Image 2 (Seedance 2.0 implied)
- Subject: anime-style chef performance
- Panels: 12
- Why canonical: Anime production board aesthetic with character study sidebar plus sound notes. Demonstrates the pattern outside dance and combat.

## Commercial and narrative anchors

### 4. UISDC ZuLi Perfume Ad
- Creator: UISDC tutorial
- Source: UISDC article
- Model pair: GPT Image 2 + Seedance 2.0
- Subject: 15-second luxury perfume commercial
- Panels: storyboard table (not strict panel grid)
- Why canonical: Commercial table format with storyboard + duration + visual + narration + SFX + transition. Chinese-language Stage 1, terse Chinese Stage 2.

### 5. UISDC Wuxia 英雄救美·反转
- Creator: UISDC tutorial
- Source: UISDC article
- Model pair: GPT Image 2 + Seedance 2.0
- Subject: 15-second martial arts short with reversal
- Panels: 9 (镜)
- Why canonical: Multi-character narrative with separate character reference sheets (front, side, costume) uploaded as @Image2, @Image3 alongside the storyboard. Demonstrates the character-locking pattern.

### 6. UISDC Nordic Warrior vs Dragon
- Creator: UISDC tutorial
- Source: UISDC article
- Model pair: GPT Image 2 + Seedance 2.0
- Subject: epic fantasy, female warrior versus dragon
- Panels: 8 beats
- Why canonical: Densest single-image previs artifact observed. Contains character design (front, side, back, close-up), environment concept (overhead camera map), 8-shot storyboard grid, lighting transitions, audio reference, color palette swatches in one composite.

## High-density anchors

### 7. Atlas Cloud Ranx Cyberpunk Fight
- Creator: Atlas Cloud tutorial
- Source: Atlas Cloud article
- Model pair: GPT Image 2 (character + storyboard) + Nano Banana 2 (environment) + Seedance 2.0
- Subject: 15-second dual cyber combat
- Panels: 16-grid
- Why canonical: Highest panel density observed (16 panels for 15s, ~0.94s per beat). Three-model pipeline. Demonstrates the "style locking is a losing battle, let each model do what it does best" principle.

### 8. Qiita 3x3 Trailer Template
- Creator: xiji2646 (Qiita)
- Source: Qiita article
- Model pair: GPT Image 2 + Seedance 2.0
- Subject: generic 15-second trailer
- Panels: 9 (3 by 3)
- Why canonical: Japanese-language template that codifies the "each panel = one shot" rule. Most reusable bare-bones skeleton.

## Use in DECONSTRUCT mode

When a user uploads a storyboard with intent to reverse-engineer it:

1. Vision-extract: panel count, grid shape, arrow conventions, timing structure, camera grammar, SFX notation, subject archetype, palette, motion register.
2. Match against the eight anchors above using the recognition rules in `../../references/in-the-wild-variants.md`.
3. Identify the closest variant family.
4. Reconstruct Stage 1 prompt using the closest Stage 1 skeleton.
5. Reconstruct matching Stage 2 prompt using the model-routed Stage 2 skeleton.
6. Output both prompts plus structural delta notes (which variant family, how it differs from canonical).
