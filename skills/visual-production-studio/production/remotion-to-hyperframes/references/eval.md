# Validate an actual migration

Use this reference after the source and target have been authored. Runtime tools
are `../scripts/lint_source.py`, `../scripts/render_diff.sh` and
`../scripts/frame_strip.sh`. Original T1–T4 corpus, old runner and calibration
records live in the development eval tree. They are not runtime dependencies.

## Ordered evidence

1. Lint and inspect the actual source. Zero files is a setup error; a clean regex
   scan does not prove compatibility. Preserve source identity and chosen props.
2. Prepare a separate authorized project copy and locally frozen assets. Check
   actual installed Remotion/HyperFrames, browser, GSAP and font versions. Never
   run the archived automatic-install runner to fill a missing dependency.
3. Render the selected composition on each actual engine. Record exact commands,
   duration/fps/dimensions/frame count, font set, pixel/color settings and any
   warnings. Missing tools or skipped render tiers are UNRUN, never PASS.
4. Run `bash <METHOD_DIR>/scripts/render_diff.sh baseline.mp4 target.mp4 diff`.
   Set `R2HF_SSIM_THRESHOLD` to the frozen source-specific gate. Default .85 is a
   retained diagnostic threshold, not permission to accept poor fidelity.
5. Open `summary.json`, `metadata.json`, ordered `ssim.log`, stderr and worst
   frame locations. Preflight rejects width/height, frame-rate, frame-count,
   duration, pixel format or declared color metadata differences before SSIM.
   Identical unknown color fields are recorded as unknown, not confirmed BT.709.
   Variable timing is rejected by the helper's decoded timestamp-spacing check.
6. Run `bash <METHOD_DIR>/scripts/frame_strip.sh baseline.mp4 target.mp4 strip 8`.
   Each row is a distinct selected frame, baseline left and target right, with
   indices/times in `samples.json` and `timestamps.txt`. Requests for more samples
   than available frames fail. First/last frames are included; additionally
   inspect just-before/at/after every source boundary, loop seam and Freeze edge.
7. Assert important localized text/number values and geometry. Cold seek, reverse
   seek and sequential playback must agree. Inspect fonts, small labels, missing
   objects and readable evidence crops. A global mean can conceal these errors.
8. Check requested audio presence, non-silent cues, trim/rate/envelope and sync,
   and listen. SSIM contains no audio evidence. The historical T2 silent WAV does
   not establish meaningful audio fidelity.

## Compare like with like

Both renders need matching pixel and color configuration. The historical
Remotion fixtures used `Config.setVideoImageFormat("png")` and
`Config.setColorSpace("bt709")` to reduce encoder differences. Apply an equivalent
configuration only in the authorized test copy and check the installed CLI/API.
Do not silently rescale, retime, truncate, substitute fonts or normalize away a
real requirement. Metadata match alone cannot prove a correct color pipeline.

The source corpus's April 2026 means (T1 .974, T2 .985, T3 .953) and gates
(.95/.95/.90) remain historical measurements. Hardware/browser/font drift and
T3 counter-clock/easing discrepancies prevent treating those scores as current
proof. Freeze an appropriate source-specific gate and semantic checks before
repair; do not tune thresholds to hide observed errors or infer an absolute
noise floor from one old fixture.

## Failure diagnosis and delivery

Use per-frame score order and `worst_frames` to localize failures before changing
code. Boundary-only errors suggest interval/clock mismatch; animation clusters
suggest easing or Freeze/Loop semantics; text-only differences suggest fonts or
counter values. Read [timing](timing.md), [sequencing](sequencing.md),
[media](media.md) or [fonts](fonts.md) for the affected mapping.

The helper's pass means only that eligible paired video frames meet a numeric
SSIM gate. Report technical, semantic, audio and perceptual outcomes separately.
A comparison setup failure exits 2 and writes status ERROR; a valid below-gate
comparison exits 1; a valid above-gate comparison exits 0. Preserve earlier
failed evidence and output hashes with the final translation notes.
