# CogVideo / CogVideoX — documented version and operation guidance

Checked 9 October 2026. Read only this selected family. No generation or native qualification is established by these documents. Exact versions and surfaces stay separate.


### Current verified open family
The official repository still identifies **CogVideoX1.5-5B** and **CogVideoX1.5-5B-I2V** as latest. Current official namespace is **zai-org**; older examples retain **THUDM** aliases. Preserve the prior 2B, 5B, I2V, continuation, and original CogVideo identities where already supported. Version 1.5 lists 5/10-second output at 16 fps, English prompting, and 224-token prompt limits. Its higher-resolution requirements should not be confused with the older 480p models. [Repository](https://github.com/zai-org/CogVideo) (C1), [1.5 model card](https://huggingface.co/zai-org/CogVideoX1.5-5B) (C2)

### Official prompting coverage and gaps
The repository's official prompt-conversion implementation is readable. It expands short requests into a coherent descriptive video caption. Its I2V prompt explicitly starts motion from the source frame, uses English complete sentences, and avoids camera transitions, scene switching, and perspective shifts. This is official implementation guidance, not a newly dated prose guide for a new generation. [Prompt conversion source](https://github.com/zai-org/CogVideo/blob/main/inference/convert_demo.py) (C3)

The broader Feishu user guide is officially linked but retrieval failed. [Linked guide](https://zhipu-ai.feishu.cn/wiki/DHCjw1TrJiTyeukfc9RceoSRnCh) (C4)

### License
The repository code's Apache badge is not the weight license for every checkpoint. The CogVideoX model license calls for commercial registration and additional licensing beyond its usage threshold; 2B is separately documented as Apache-2.0. [Model license](https://github.com/zai-org/CogVideo/blob/main/MODEL_LICENSE) (C5)


## Caption expansion grounded in the starting frame

Authored CogVideoX1.5 I2V caption: “The woman in the source frame gently raises the umbrella and takes two slow steps forward. Rain continues to fall onto the pavement. Her coat and the surrounding street remain consistent as the motion unfolds from the starting image.” This follows the owner's conversion implementation: coherent English complete sentences and continuous motion without scene switching, new camera perspective or transitions.

For T2V, include the missing visible subject, setting and action in one coherent caption within the selected token budget. Preserve a requested older 2B/5B/I2V or continuation route rather than treating 1.5 examples as its contract. The linked general guide remains unreadable; runtime continuation controls and weight licensing need exact-checkpoint verification.
