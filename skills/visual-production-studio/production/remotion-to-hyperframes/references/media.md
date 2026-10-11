# Media translation: Audio, Video, Img, IFrame, staticFile

Source-derived mechanics retained from both pinned editions. Examples are recipes, not automatic permission to install, fetch, upload or execute source. Verify dependencies and adapters against the selected runtime; historical measurements are not current qualification. The owning METHOD.md controls semantic/loss handling.

## Asset paths

Remotion's `staticFile("x.png")` resolves to the project's `public/` directory.
HF uses relative paths from the composition's `index.html`, conventionally
`assets/`:

```tsx
<Img src={staticFile("logo.png")} />
```

```html
<img src="assets/logo.png" />
```

When translating, copy the asset from `remotion-src/public/x` to
`hf-src/assets/x`. Multiple files can be batched with a setup script;
see T2's `setup.sh` for an example pattern.

## `<Audio>`

```tsx
<Audio src={staticFile("music.wav")} volume={0.5} />
```

```html
<audio
  data-start="0"
  data-duration="6"
  data-track-index="2"
  data-volume="0.5"
  src="assets/music.wav"
></audio>
```

`data-start` and `data-duration` are required: the runtime needs them to
schedule the audio. Default to the composition's full duration if Remotion
didn't specify trim.

### Volume ramps

```tsx
<Audio src={staticFile("music.wav")} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
```

HF supports static `data-volume` only for now. Volume ramps need to be
applied to the audio file at translation time (with ffmpeg `afade`) or the migration is partial until the user accepts a documented audible difference. A visual-only SSIM pass cannot approve dropping it.

### Trim / playbackRate

```tsx
<Audio src={staticFile("music.wav")} startFrom={60} endAt={180} playbackRate={1.5} />
```

```html
<audio
  data-start="0"
  data-duration="<resolved from trim>"
  data-trim-start="2"
  data-trim-end="6"
  data-playback-rate="1.5"
  src="assets/music.wav"
></audio>
```

`startFrom` / `endAt` are frame indexes; convert to seconds.

## `<Video>` and `<OffthreadVideo>`

```tsx
<Video src={staticFile("intro.mp4")} muted playsInline />
<OffthreadVideo src={staticFile("intro.mp4")} muted />
```

```html
<video
  muted
  playsinline
  data-start="0"
  data-duration="5"
  data-track-index="0"
  src="assets/intro.mp4"
></video>
```

`<OffthreadVideo>` is a Remotion-specific optimization for headless
rendering. HF runs in headless Chrome already, so the off-thread variant
collapses to a regular `<video>`.

`playsinline` and muted decoding may be needed for the selected runtime/browser. Preserve any requested audible source track through the verified audio pipeline; never use the muted attribute as permission to discard sound.

## `<Img>`

```tsx
<Img src={staticFile("logo.png")} style={{ width: 200, height: 200 }} />
```

```html
<img src="assets/logo.png" style="width: 200px; height: 200px;" />
```

Width/height get rounded to integer px. If the original style has
animated dimensions, the GSAP tween animates them: see [timing.md](timing.md).

## `<IFrame>`

```tsx
<IFrame src="https://example.com" />
```

```html
<iframe src="https://example.com"></iframe>
```

The source describes a **screenshot mode** fallback for nested iframes. Verify that the selected renderer has it, can access the source and waits for a stable ready state. A fallback does not itself prove visibly correct output. See
[hyperframes-vs-remotion.mdx](https://github.com/heygen-com/hyperframes/blob/main/docs/guides/hyperframes-vs-remotion.mdx)
for details.

## `delayRender()` / `continueRender()`

```tsx
const handle = delayRender();
useEffect(() => {
  loadAsset().then(() => continueRender(handle));
}, []);
```

Inspect what the source barrier waits for. Map images to decode readiness, fonts to document.fonts.ready, video to metadata and completed seeks, Lottie to its ready signal, and custom loading to an explicit bounded readiness contract. The selected [Frame Adapter pattern](https://hyperframes.heygen.com/concepts/frame-adapters) may supply some of these. Remove delayRender/continueRender only after verifying each replacement, including errors/timeouts. A mount effect or queued microtask is not a substitute for completed loading.

## When the asset isn't a file

If Remotion's media source is a Buffer, dataURL, or URL.createObjectURL,
the asset doesn't exist on disk and can't be copied via setup.sh. Two
options:

1. Materialize the asset at translation time; write the buffer to a file
   in `hf-src/assets/`.
2. Embed as a data URL directly in the HTML (`src="data:image/png;base64,..."`)
   for small assets (< 100 KB).

For audio/video Buffers, option 1 is preferred: base64-encoded media
bloats the HTML and slows the renderer.
