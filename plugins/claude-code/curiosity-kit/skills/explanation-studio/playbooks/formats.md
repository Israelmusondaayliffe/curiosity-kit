# Carry meaning into the requested form

Choose representation by the user's request and what makes the relationship understandable. Do not automatically start with writing, climb every format or claim each format costs more. A simple diagram can be cheaper than elaborate prose; a video request can begin with a scene plan.

## Keep one source of meaning

Before changing form, identify the claim, mechanism, key conditions, unknowns, quantities, units and exact terms that must survive. For a short answer, a mental check is enough. For a larger artifact, a few source-linked notes prevent drift; do not introduce a required ledger framework.

Re-read the original source when the existing explanation may be wrong. A polished prior answer is not independent evidence. Mark newly introduced background as such. Do not let a diagram, caption or narration strengthen an uncertain statement.

Generate the requested form directly from this meaning. Reuse useful existing content, but do not make intermediate files just to satisfy a ladder. Compare the final artifact back to the source and the reader's actual question.

## Prose and reference

Use [explain](explain.md) for a clear direct account. If the user asks to look up an exact flag or limit, give that fact without an unnecessary lesson. Keep a procedure's actions and conditions distinct from the explanation of why. A requested rewrite should preserve meaning rather than create a new opinion or diagnosis.

## Diagrams, images and HTML

Use [visual](visual.md). Choose precise diagrams when relationships and labels carry the meaning. An illustration can help with a spatial idea, but inspect its pixels and factual labels. If a requested renderer is unavailable, say which format remains unproduced; do not label source text a rendered image.

An interactive HTML explanation needs a useful control, not merely clickable decoration. Show the important consequence of the input and keep a noninteractive explanation visible. A standalone artifact embeds its required assets. A shareable web deployment is a separate action with its own destination, privacy and authorization checks.

## Plan a short explainer video

A video plan is local explanatory work and does not require an installed video sibling. Ground the content, establish audience, duration and desired takeaway, then write a usable scene sequence. For each scene provide:

- The exact point and source or illustrative assumption.
- The narration or on-screen text the audience will receive.
- The visible elements and their labels.
- The motion or transition that explains a relationship.
- Approximate duration and what must stay visible.

Keep stable terms and visual identities across scenes. Put the important condition beside the relevant action in narration and image. Do not show certainty in the animation while narrating uncertainty. Use subtitles or a transcript when required. Avoid a fast visual change that removes a caveat before it can be read.

### Small plan example

Topic: a timeout does not establish whether a write succeeded. Illustrative timings, not a trace.

1. About 8 seconds. Show a client sending a write to a service. Narration: “The client asks the service to save the change.”
2. About 12 seconds. Show two possible paths: the service did not finish, or it saved the change but the response was delayed. Narration: “No response arrived in time. Either path is still possible.” Keep both branches labeled possible.
3. About 10 seconds. Show the `retry_safe` check before a retry arrow. Narration: “Under this rule, retry only when `retry_safe` is true.” Show false leading to no retry, with the first effect still unknown.

This plan teaches a bounded rule. It does not certify a real application's retry safety, and it is not a playable video.

## Produce only with real tools and authority

When the request includes a playable video, inspect the actual available production capability. Prefer a suitable native tool, then an already installed local renderer/composer. Possible tools have different requirements; naming a renderer, TTS service or ffmpeg in prose does not make it available.

Before rendering, establish the selected tool, accepted input, output path, required assets, narration/caption support, cost and permissions. Use only authorized content and services. Do not invent an API key, install software, clone a voice or start paid generation as a side effect of explanation. Follow applicable approvals. An explicit supplied voice/format choice takes precedence over convenience.

Execute the scene plan through the selected supported tool. Keep the plan's claims and timing aligned with production. Inspect intermediate frames where layout, text or motion can fail. Check the final file actually plays, has the intended duration, and contains the required audio/captions. Listen to narration or use an appropriate supported inspection, not merely an audio-file existence check. Check synchronization and readable labels at playback speed.

If a render fails, inspect the error and repair the concrete cause within the task's bounds. Do not retry indefinitely. If a static slide or silent version is a materially weaker deliverable, label it and obtain agreement where needed rather than quietly replacing the request. A missing renderer can leave a complete scene/narration plan and incomplete production. Say exactly that.

## Delivery and recovery

Check the actual delivered file, not only an editor preview. Use the host's supported attachment or artifact route and verify the returned reference. Do not publish a private explanation to obtain a convenient link. Keep useful authored material if delivery fails and identify the exact delivery limit.

When adapting for another audience, remove inappropriate private context and add the orientation that reader needs without thinning essential caveats. Sharing authority must cover that artifact and destination. A change of format is not permission to send it.

Report the narrow achieved state: explanation delivered; diagram rendered but editability unverified; HTML authored with rendering pending; video plan complete and production blocked; or playable video inspected. Claims follow observed evidence, not the name of the output file.
