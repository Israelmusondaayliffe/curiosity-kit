# Emotion, Cinematography, and Sound

Selected Seedance 2.5 optimizer reference, retained from the pinned source and scoped by [the rebuilt method](../methods/seedance.md). Current selected-surface controls and conflicts are in [the model profile](../../references/models/seedance.md). This is an authoring recipe, not native execution proof. User-requested format and explicit model version take precedence.

### Emotion and Observable Performance

When only a direction such as tense, warm, or oppressive is given, allow the model to determine the specific performance. When the user needs control over the acting, use:

```text
emotional or atmospheric direction + triggering event + the character's observable performance + observable changes in camera work, lighting, or sound
```

Choose a small number of the clearest cues from the eyes, brows, mouth, breathing, gaze, hand movements, and body posture. Do not pile on every possible microexpression. Divide the performance into stages by triggering event only when the emotion changes multiple times.

```text
The overall emotion shifts from <starting emotion> to <ending emotion>.
After <triggering event>, <the subject> first shows <an immediate observable reaction>.
Then, <the eyes, brows, mouth, breathing, gaze, or hand movements> gradually <change>.
Finally, <the subject> expresses <the target emotion> through <an outwardly observable performance>.
```

Completed example:

```text
The overall emotion shifts from restrained anticipation to trying to stay composed after disappointment.
After seeing the waiter place a returned letter on the table, the woman's fingers tracing the rim of her cup suddenly stop, and her gaze falls on the return mark on the envelope.
Her brows tighten slightly, her faint smile gradually disappears, and after a slow breath in, she turns the envelope face down on the table.
Finally, she looks up at the empty chair across from her, keeps her shoulders straight, and says in a calm but slightly strained voice: {I understand.}
```

### Professional Cinematography

Basic shot language and popular camera movements can be written directly into the Prompt. When the frame contains multiple subjects, still specify which subject the camera centers on, where the move begins, and where it ends. Do not use only a term detached from its subject.

```text
popular camera movement + target subject + starting position or state + direction of movement + arrival position or state
```

Popular camera movements include a continuous one-take shot, dolly zoom, aerial perspective, FPV, bullet time, handheld camera work, and rebound speed ramping. For a continuous one-take shot, specify the sequence of subjects, spaces, and events the camera passes through. For handheld camera work, specify the tracked subject and the degree of shake. For rebound speed ramping, specify the action beat at which the movement accelerates, decelerates, or rebounds, as well as the final hold state.

For highly specialized cinematography terms, terms whose industry meanings are inconsistent, or terms that require precise control over visual changes, retain the term and expand it into observable results:

```text
cinematography term + target subject + visual change + foreground/background relationship + direction or speed
```

For example, shallow depth of field should specify that the subject remains sharp and how the background blurs. A tracking shot should specify that the camera matches the subject's speed and the direction of the background motion blur. A rack focus should specify which object the focus moves from and which object it moves to, and how each object's sharpness changes. A vignette should specify that the four corners gradually darken while the center retains normal brightness. Focal-length, aperture, and shutter values may only supplement these instructions; they cannot replace the final visible result.

### Sound, Dialogue, and Text

Use the following when content types need to be distinguished:

| Content | Symbols | Example |
|---|---|---|
| Music | `()` | `(Soft piano music plays in the background)` |
| Sound effect | `<>` | `<A bell rings in the distance>` |
| Dialogue | `{}` | `{Hello, welcome back}` |
| Subtitle | `【】` | `【Chapter 1: Departure】` |

For dialogue language, use: `language + optional regional variety or accent + delivery + speaker + {dialogue}`. Label each speaker separately; do not make a single blanket declaration at the beginning. If English dialogue is likely to be spoken in Chinese, explicitly write at least "Use English." When the user explicitly specifies a regional variety or accent, or explicitly asks for stronger reinforcement, use a complete instruction such as "natural, conversational American English" or "authentic Los Angeles English." If the user provides only English dialogue, do not add an American, British, or regional accent without instruction. If the user does not specify the dialogue language, do not infer Mandarin, a dialect, or a regional accent from the writing system. When subtitles are unnecessary, also state that no subtitles appear on screen.

For multi-speaker dialogue, bind the speaker and audio at each stage, and state that the other characters keep their mouths naturally closed while listening. Identify the sources of ambience, sound effects, and music separately so unrelated audio is not mistaken for background music.

If the final Prompt uses `<>` to mark sound effects, do not also enclose subject names in angle brackets. Use ordinary character names so the same symbols do not serve two roles.

For tasks without dialogue, constrain speech, lip movement, sound sources, and visible text carriers at the same time. For example, characters keep their mouths naturally closed, there is no narration, only the specified ambience remains, and no subtitles or signs appear on screen.

### Products and Physical Processes

Convert abstract selling points such as efficient, intelligent, or reliable into "initial state -> specific operation -> observable result." Show only one operation or functional result in each stage, and continuously preserve product appearance, component positions, the operator, and scene relationships.

```text
Stage 1: At the start, <the initial state of the product and its components>; <the operator completes one specific operation>; at the end, <a directly visible state>.
Stage 2: Continue from <the previous stage's state>; <the product performs one function>; at the end, <a directly visible result>.
Stage 3: <The operator completes the concluding operation>; at the end, <the final state of the product, its components, and the finished output>.
```

Completed example:

```text
Stage 1: At the start, the desktop humidifier is off, its water tank is empty, and the top cover is placed to the right of the unit. The operator removes the water tank and fills it with clean water. At the end, the water level is below the maximum fill line.
Stage 2: The operator reinstalls the water tank, closes the top cover, and presses the power button once. At the end, the operator's hand has moved away from the button, and the humidifier remains in a fixed position.
Stage 3: A continuous stream of fine white mist emerges from the outlet and rises vertically, with no water accumulating on the desktop. At the end, the unit, water tank, and top cover remain visually intact.
```

Do not write only "show the complete process of installing, operating, and completing the product workflow." Exact on-screen text, formulas, and product parameters remain subject to the capability boundaries in the Output Contract.
