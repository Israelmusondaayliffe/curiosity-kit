# Attribution

The `graphic-overlays` skill (its card-based design system: styles, layouts, frames,
fonts, and the GSAP-driven composition workflow) is **adapted from** the open-source
**vtake-skills** project (`vtake-cut`):

> https://github.com/notedit/vtake-skills

Adaptations for this repo: renamed to `graphic-overlays`; transcription repointed to
local Whisper via `hyperframes transcribe` (dropping the third-party `@notedit/vtake`
CLI and the `vtake.app` proxy); audio/metadata extraction inlined with `ffmpeg`/`ffprobe`;
the fixed third-party brand outro removed in favour of an optional, neutral outro;
artifacts aligned to the `videos/<project>/` convention.

The original is MIT-licensed; its notice is retained below as required.

```
MIT License

Copyright (c) 2026 leeoxiang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Separate font notices

Inter and Caveat retain their original SIL OFL notices. In the skill, the canonical copies are the inter.txt and caveat.txt files under ../embedded-captions/licenses/third-party-licenses/fontsource/. Independent overlay bundles must include those notices with the reused font files; the documented export layout places them in licenses/. Separate assets do not inherit the MIT license above. GSAP retains its own header and vendor terms. LXGW WenKai TC and Virgil payloads are excluded from this copy. The former embeds copyright 2024 The LXGW WenKai Project Authors and an OFL URL, but matching complete redistribution records were not supplied. The latter embeds copyright 2011 Your Own Font Foundry and a personal-use-only restriction. Retain those source credits; neither excluded asset is relicensed here. Use a supplied licensed font when its specific appearance is required.
