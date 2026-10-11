# Bria FIBO and FIBO Lite

Evidence checked 9 October 2026. Guide-backed structured-brief workflow. Input-to-structured-prompt bridge and image renderer are separate stages; a blueprint is not the same thing as its transport request.

## Construct and refine the shot specification
Start with an explicit creative brief: subject, camera/framing, action, environment, light, material, text and composition. Inspect the generated structured prompt before rendering when fidelity matters. Refine the relevant structured property instead of adding contradictory free text. Preserve the accepted blueprint plus seed when comparing renderer iterations; bridge rewriting can introduce variation before the renderer sees that seed.

Authored creative brief: “Tabletop photograph of a folded cream scarf beside a dark-green ceramic cup. Three-quarter overhead view; the scarf forms a diagonal from lower left to upper right. Broad soft window light, visible woven fibers, no requested lettering.” This is the bridge input, not a guessed FIBO schema. A later request to change the cup color should modify that accepted property while retaining camera and layout.

## Processing-surface distinction
The standard bridge uses Gemini 2.5 Flash; Lite uses FIBO-VLM. A FIBO renderer/model name does not prove the whole workflow is local. Verify the actual processing route and permission before transmitting assets or installing a local component. No deterministic result or privacy guarantee was tested.

## Sources
[Generation overview](https://docs.bria.ai/image-generation-overview), [generation architecture](https://docs.bria.ai/image-generation), [best practices](https://docs.bria.ai/image-generation-best-practices): actual catalog, architecture and creative-brief guidance reviewed 2026-10-09; publication dates not established.
