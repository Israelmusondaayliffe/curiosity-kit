#!/usr/bin/env node
/*
 * transcribe.cjs — word-level transcription via hyperframes' native Whisper
 * (replaces the Python ElevenLabs Scribe path; no Python, no API key).
 *
 *   node transcribe.cjs <project-dir> [model] [language]
 * Reads:  <project>/source.mp4 (audio track)
 * Writes: <project>/transcript.json  — { text, language_code, words:[{text,start,end,type}] }
 */
const path = require("path");
const fs = require("fs");
const os = require("os");
const cp = require("child_process");
const guard = require("./contracts.cjs");

function hfRoot() {
  const roots = [
    process.env.HYPERFRAMES_ROOT,
    path.resolve(__dirname, "..", "..", ".."),
    path.join(os.homedir(), "Downloads", "hyperframes"),
  ].filter(Boolean);
  for (const r of roots)
    if (fs.existsSync(path.join(r, "packages", "cli", "dist", "cli.js"))) return r;
  console.error("[transcribe] hyperframes CLI not found — set HYPERFRAMES_ROOT");
  process.exit(3);
}
const ensureSource = guard.source;

function _usableWords(d) {
  return d && Array.isArray(d.words) && d.words.some((w) => w && "start" in w && "end" in w);
}
// Mean loudness of the audio, for the no-speech guard below. Silence → whisper
// hallucinates (famously "Thank you."), and the decision gate refuses "no speech".
function meanVolumeDb(audio) {
  try {
    // ffmpeg writes volumedetect stats to STDERR — capture it (spawnSync, no throw).
    const r = cp.spawnSync(
      "ffmpeg",
      ["-hide_banner", "-nostats", "-i", audio, "-af", "volumedetect", "-f", "null", "-"],
      { encoding: "utf8" },
    );
    const out = (r.stderr || "") + (r.stdout || "");
    const m = out.match(/mean_volume:\s*(-?(?:[\d.]+|inf)) dB/);
    return m ? (m[1]==="-inf" ? -Infinity : parseFloat(m[1])) : null;
  } catch {
    return null;
  }
}

// Where does AUDIBLE content end? Whisper hallucinates trailing words over a silent
// tail (observed: "I'm sorry." repeated over dead air at a clip's end). silencedetect
// finds a terminal silence running to EOF; words "spoken" inside it are fabricated.
// Conservative: applause/music read as non-silence, so this fires only on truly dead
// tails. Returns {speechEnd, total} or null.
function audibleEnd(audio) {
  try {
    const r = cp.spawnSync(
      "ffmpeg",
      [
        "-hide_banner",
        "-nostats",
        "-i",
        audio,
        "-af",
        "silencedetect=noise=-35dB:d=0.6",
        "-f",
        "null",
        "-",
      ],
      { encoding: "utf8" },
    );
    const out = (r.stderr || "") + (r.stdout || "");
    const durM = out.match(/Duration:\s*(\d+):(\d+):([\d.]+)/);
    const total = durM ? +durM[1] * 3600 + +durM[2] * 60 + +durM[3] : null;
    if (total == null) return null;
    const starts = [...out.matchAll(/silence_start:\s*([\d.]+)/g)].map((x) => +x[1]);
    const ends = [...out.matchAll(/silence_end:\s*([\d.]+)/g)].map((x) => +x[1]);
    if (!starts.length) return { speechEnd: total, total };
    const lastStart = starts[starts.length - 1];
    const closed = ends.some((e) => e > lastStart); // silence re-broken before EOF?
    return { speechEnd: closed ? total : lastStart, total };
  } catch {
    return null;
  }
}

function main() {
  const project = path.resolve(process.argv[2] || "");
  if (!process.argv[2]) {
    console.error("usage: transcribe.cjs <project-dir> [model] [language]");
    process.exit(1);
  }
  // Default = multilingual `small`, NOT `small.en`. Per hyperframes-media: ".en models
  // mistranslate non-English and mis-handle accented speech; default to small (auto-detects
  // language)." We hardcoded small.en before — it hallucinated a wrong transcript on an
  // accented speaker. Pass `small.en` only for known-clean-English; tough accents → a larger model.
  const model = process.argv[3] || process.env.WHISPER_MODEL || "small";
  const language = process.argv[4] || process.env.WHISPER_LANG || "";
  const out = path.join(project, "transcript.json");

  const src=ensureSource(project);const mediaDuration=guard.duration(project);
  const cache=guard.cache(project,'transcribe',{model,language,engine:process.env.TRANSCRIBE_ENGINE||'whisperx',model_revision:process.env.WHISPER_MODEL_REVISION||null},['audio.mp3','transcript.json','_wx_out']);
  if(cache.hit){const d=guard.transcript(JSON.parse(fs.readFileSync(out,'utf8')),mediaDuration);if(d.source_sha256!==guard.hash(src))throw Error('BLOCKED: transcript source mismatch');console.log('[transcribe] source-bound validated cache');return;}
  if(process.env.WHISPER_MODELS_READY!=='1'||!process.env.WHISPER_MODEL_REVISION)throw Error('BLOCKED: provision a pinned installed speech engine and models first; no automatic installation/download');
  const audio = path.join(project, "audio.mp3");
  if (!fs.existsSync(audio))
    cp.execFileSync(
      "ffmpeg",
      ["-y", "-i", src, "-vn", "-acodec", "libmp3lame", "-q:a", "2", audio],
      { stdio: "ignore" },
    );

  // ── engine: WhisperX (preferred — wav2vec2 forced alignment gives word timings far
  // tighter than whisper.cpp's segment-interpolated ones; our gates are 80ms-strict) →
  // fallback hyperframes whisper.cpp. Force with TRANSCRIBE_ENGINE=whisper|whisperx.
  let words = null,
    engine = null, detectedLanguage = null;
  const wantWx = (process.env.TRANSCRIBE_ENGINE || "whisperx") === "whisperx";
  if (wantWx) {
    try {
      const wav = path.join(project, "_wx_audio.wav");
      cp.execFileSync("ffmpeg", ["-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav], {
        stdio: "ignore",
      });
      const outDir = path.join(project, "_wx_out");
      fs.mkdirSync(outDir, { recursive: true });
      const wxModel = model.replace(/\.en$/, ""); // whisperx model names are multilingual ids
      const wxArgs = [
        wav,
        "--model",
        wxModel,
        "--device",
        "cpu",
        "--compute_type",
        "int8",
        "--output_dir",
        outDir,
        "--output_format",
        "json",
        "--no_align_deletes",
        "--print_progress",
        "False",
      ];
      if (language) wxArgs.push("--language", language);
      // strip our flag if this whisperx build doesn't know it
      let r = cp.spawnSync("whisperx", wxArgs, { encoding: "utf8", timeout: 600000 });
      if ((r.error || r.signal || r.status !== 0) && /no_align_deletes/.test(r.stderr || "")) {
        r = cp.spawnSync(
          "whisperx",
          wxArgs.filter((a) => a !== "--no_align_deletes"),
          { encoding: "utf8", timeout: 600000 },
        );
      }
      if ((r.error || r.signal || r.status !== 0))
        throw new Error(
          (r.stderr || "whisperx failed").split("\n").slice(-4).join(" ").slice(0, 300),
        );
      guard.requireSuccess(r,"WhisperX");
      const wxJson = JSON.parse(fs.readFileSync(path.join(outDir, "_wx_audio.json"), "utf8"));
      detectedLanguage = wxJson.language || null;
      const wx = [];
      for (const seg of wxJson.segments || [])
        for (const w of seg.words || []) {
          // alignment occasionally yields a word with no timing (OOV) — interpolate from neighbors later; mark null now
          wx.push({ text: String(w.word || "").trim(), start: w.start, end: w.end, type: "word" });
        }
      if(wx.some(w=>!Number.isFinite(w.start)||!Number.isFinite(w.end)))throw Error('BLOCKED: forced alignment has untimed tokens; review alignment or use an authorized fallback');
      if (wx.length) {
        words = wx.filter((w) => w.text);
        engine = `whisperx(${wxModel}+wav2vec2)`;
      }
      try {
        fs.unlinkSync(wav);
      } catch {}
    } catch (e) {
      console.error(
        `[transcribe] whisperx unavailable (${String(e.message || e).slice(0, 160)}) — falling back to whisper.cpp`,
      );
    }
  }

  if (!words) {
    // run hyperframes Whisper → writes a flat word array to <dir>/transcript.json
    const cli = path.join(hfRoot(), "packages", "cli", "dist", "cli.js");
    const args = ["transcribe", audio, "-d", project, "--json", "--model", model];
    if (language) args.push("--language", language);
    let info = {};
    try {
      const so = cp.execFileSync("node", [cli, ...args], { encoding: "utf8" });
      const line = so.trim().split("\n").filter(Boolean).pop();
      info = JSON.parse(line);
    } catch (e) {
      console.error("[transcribe] hyperframes whisper failed:", e.message);
      process.exit(1);
    }
    const flatPath = info.transcriptPath || out;
    const flat = JSON.parse(fs.readFileSync(flatPath, "utf8"));
    detectedLanguage = flat.language_code || flat.language || info.language || null;
    const arr = Array.isArray(flat) ? flat : flat.words || [];
    words = arr
      .filter((w) => (w.text ?? w.word) != null)
      .map((w) => ({
        text: w.text ?? w.word,
        start: w.start ?? w.t0,
        end: w.end ?? w.t1,
        type: "word",
      }));
    engine = `whisper.cpp(${model})`;
  }

  // Tail-hallucination guard: drop words whisper placed entirely inside a terminal
  // silence (it fabricates e.g. repeated "I'm sorry." over dead air). Word START past
  // the audible end (+0.4s slack) = fabricated; real final words start before it.
  const ae = audibleEnd(audio);
  let trimmedTail = 0;
  if (ae && ae.speechEnd < ae.total - 0.8) {
    const keep = words.filter((w) => w.start <= ae.speechEnd + 0.4);
    trimmedTail = words.length - keep.length;
    if (trimmedTail > 0) {
      console.error(
        `[transcribe] ⚠ trimmed ${trimmedTail} trailing word(s) starting after the audible end ` +
          `(${ae.speechEnd.toFixed(2)}s; clip ${ae.total.toFixed(2)}s) — whisper hallucinates over silent tails.`,
      );
      words = keep;
    }
  }

  guard.transcript({words},mediaDuration);
  const meanDb = meanVolumeDb(audio);
  if(meanDb!=null&&meanDb < -45)throw Error("BLOCKED: near-silent input; no trustworthy speech admission");
  const text = words
    .map((w) => w.text)
    .join(" ")
    .replace(/\s+([,.!?;:])/g, "$1")
    .trim();
  fs.writeFileSync(
    out,
    JSON.stringify(
      {
        text,
        language_code: language || detectedLanguage || "und",
        source_sha256: guard.hash(src),
        engine,
        words,
        ...(trimmedTail ? { trimmed_tail_words: trimmedTail } : {}),
      },
      null,
      2,
    ),
  );
  console.log(`[transcribe] ${engine} ${words.length} words → ${out}`);
  console.log(`[transcribe] text: ${text.slice(0, 160)}${text.length > 160 ? "…" : ""}`);

  // No-speech guard: whisper returns confident hallucinations over silence (e.g. the
  // whole clip as "Thank you."). The decision gate REFUSES "no speech" — operationalize
  // it so an agent trusting the transcript can't sail past the gate.
  cache.complete();
  if (meanDb != null && meanDb < -45) {
    console.error(
      `\n[transcribe] ⚠ NEAR-SILENT AUDIO — mean ${meanDb.toFixed(1)} dB (real speech ≈ -16..-26 dB).`,
    );
    console.error(
      `  This transcript is almost certainly a Whisper hallucination, NOT real speech.`,
    );
    console.error(
      `  Per the decision gate, REFUSE "no speech" — confirm with \`ffmpeg -i <src> -af silencedetect\`;`,
    );
    console.error(`  do NOT author captions from fabricated words.`);
  }
}
main();
