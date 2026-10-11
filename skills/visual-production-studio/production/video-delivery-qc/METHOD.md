# Video delivery quality control

Inspect a requested video against its actual brief. Separate objective file checks, visual/motion review, audio listening, caption/source fidelity and delivery/access. The helper only verifies metadata and basic bounds; it cannot certify artistic quality or semantic truth.

## Bind the inspection

Identify the exact current file, source/project revision, render time, requested destination/format, dimensions/aspect/fps, duration tolerance, audio/captions/alpha requirements and platform-safe regions. Hash or otherwise bind evidence to this file. Existing output from an older input is stale. Preserve the source brief and state assumptions. If a file is absent/corrupt/unreadable, mark blocked instead of reusing prior reports.

## Technical check

```bash
python <METHOD_DIR>/scripts/inspect_delivery.py <video> --min-width 1080 --min-height 1080 --min-duration 5 --max-duration 7 --require-audio --output <report.json>
```

Use only requirements actually requested. ffprobe is primary; macOS mdls is a weaker metadata fallback when available. A missing duration or unknown audio state cannot satisfy a requested constraint. Explicit silence is valid when requested. Check exact dimensions/aspect/fps, codec, frame count, container, color/alpha and sample rates with ffprobe as relevant; the bundled minimum-bound checker does not implement every platform spec. Reject nonfinite/inconsistent requested bounds. Metadata presence of an audio stream does not prove audible speech or correct sync.

## Watch, listen and compare

Review beginning/end, scene changes, representative middle frames, dense/peak overlap and short text. Check blank/black frames, missing assets/fonts/glyphs, flicker, jumps, incorrect crops, collisions, safe-area clipping, line breaks, enough reading time, deliberate holds, continuity and final frame. Test forward/backward/random seeks for procedural/HTML compositions. A contact sheet is insufficient for motion/sync.

Listen for missing requested voice/music/SFX, clipping, abrupt cuts/clicks, inappropriate ducking, silence and intelligibility. Compare caption words, names/numbers/punctuation and timestamps against approved transcript/source; no caption source means accuracy is untested. Verify exact product/PR/source claims and geographic/chart labels. Inspect transparency on contrasting backgrounds when alpha is requested. Check accessibility constraints requested by the user and platform-specific regions; don't invent compliance from a basic metadata pass.

## Repair and report

Fix the smallest owned source affecting the defect, rerun related checks, re-render and inspect the new exact output. Keep failures and their dispositions. Use [inspection checklist](references/inspection.md) and [report template](assets/qc-report-template.md) as compact starting aids. Record requested versus observed, tools/versions, evidence paths, pass/fail/untested/blocked by check, and known limitations. Do not let an overall label hide untested visual/audio review.

Deliver only the verified current artifact through the requested channel, with access checked. Publishing/sharing externally is a separate action. Give a short result: file, duration/dimensions/fps, significant failures and exact unverified boundaries. Avoid claiming “fully checked” when only ffprobe ran.
