# xAI Grok Imagine image

Evidence checked 9 October 2026. Generation/edit schema and examples were reviewed; no separate comprehensive creative handbook verified. Keep grok-imagine-image-2.0, image-quality, image-pro and image 1.0 identities distinct.

## Generation and iterative editing
Write the desired scene, layout and exact copy in natural language. On an edit, identify the supplied image and a specific change with a short preservation list. Reuse the selected actual result for the next edit rather than describing an imagined intermediate. xAI's edit JSON transport is not OpenAI SDK multipart merely because a client library is compatible.

Authored 2.0 edit example: “Replace the blue paper background with pale peach. Preserve the silver watch, dial markings, hand positions, camera angle and contact shadow.” This is an illustrative editing instruction, not a fidelity guarantee. Native output controls belong to the exact endpoint schema.

## Lifecycle must not change the requested model silently
The quality alias is scheduled to retire on 2 November 2026 and redirect to image-2.0 low; image-pro follows that redirect. On the audit date this is a future change. Image 1.0 is unaffected by that notice. Record requested alias and resolved target separately if execution occurs after the transition; seek a choice when the change alters the requested target.

## Sources
[Overview](https://docs.x.ai/developers/model-capabilities/imagine), [generation](https://docs.x.ai/developers/model-capabilities/images/generation), [editing](https://docs.x.ai/developers/model-capabilities/images/editing): overview/edit bodies and generation configuration reviewed; editing page updated 13 August 2026. [Retirement notice](https://docs.x.ai/developers/migration/imagine-image-quality-nov-2): notice body reviewed. No account access, generation or output quality was tested.
