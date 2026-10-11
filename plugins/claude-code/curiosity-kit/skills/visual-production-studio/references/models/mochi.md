# Mochi — documented version and operation guidance

Checked 9 October 2026. Read only this selected family. No generation or native qualification is established by these documents. Exact versions and surfaces stay separate.


### Verified identity and lifecycle
The official current downloadable model remains **genmo/mochi-1-preview**, marketed as **Mochi 1**. It is an Apache-2.0 text-to-video research preview. The official repository and current Genmo home page did not establish a newer Mochi release, an official HD checkpoint, or retirement. Retain it as a supported legacy/research route rather than silently upgrading or deleting it. [Repository](https://github.com/genmoai/mochi) (M1), [Current Genmo site](https://www.genmo.ai/) (M2)

### Prompting and capability limits
An official model card provides examples and implementation controls, but a dedicated creator prompting handbook was not located. The model card says the preview targets 480p, can distort under extreme motion, and favors photorealistic output over animation. The reference implementation needs about 60 GB VRAM on one GPU; optimized external runtimes have different requirements. Do not promise native audio or first-frame I2V merely because a host offers adjacent tools. Maximum duration should be validated per runtime; example frame counts do not establish a universal limit. [Model card](https://huggingface.co/genmo/mochi-1-preview) (M3)


## Honest preview-oriented authoring

Authored Mochi 1 preview T2V brief: “A close view of a brown horse standing in a sunlit field. Its mane moves gently in the breeze and it slowly turns its head toward the camera. Warm natural light, detailed coat texture, steady framing.” This uses the card's photorealistic emphasis and avoids overloading the preview with extreme motion; it is a general studio example, not a dedicated handbook or measured improvement.

Keep the selected preview identity. A host's I2V or audio tool is not evidence that the owner checkpoint accepts those inputs. Resolve runtime frame count and output limits before execution, and inspect motion distortion in any later authorized run.
