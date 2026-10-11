# HappyHorse (Alibaba hosted) — documented version and operation guidance

Checked 9 October 2026. Read only this selected family. No generation or native qualification is established by these documents. Exact versions and surfaces stay separate.


### Current verified versions and access
Alibaba's catalog lists **happyhorse-1.1-t2v**, **happyhorse-1.1-i2v**, **happyhorse-1.1-r2v** with native audio, 480p/720p/1080p and 3–15-second output. **happyhorse-1.0-video-edit** remains the named editing model; older 1.0 generation entries are also still listed. [Catalog](https://www.alibabacloud.com/help/en/model-studio/video-generate-edit-model/) (W1)

The T2V API accepts any language with a 5,000-non-Chinese-character or 2,500-Chinese-character ceiling and truncates excess. Model, endpoint, and key must be in the same region. Generation is asynchronous; task IDs expire after 24 hours. The English duration line still explicitly names 1.0 while the example uses 1.1, so the catalog and matching regional API must be checked together. [T2V reference](https://www.alibabacloud.com/help/en/model-studio/happyhorse-text-to-video-api-reference) (P1)

### Official prompt guidance available
The R2V reference documents **[Image 1]**, **[Image 2]** bindings matching media order, with explicit descriptions of the referenced object. It permits 1–9 reference images and specifies size/quality constraints. This is verified endpoint-specific guidance, not an inferred universal prompt style. [R2V reference](https://www.alibabacloud.com/help/en/model-studio/happyhorse-reference-to-video-api-reference) (P2)

The I2V API makes the text prompt optional and derives framing from the first frame. The editing API accepts source video plus optional reference images for directed changes, with original-audio preservation available. [I2V](https://help.aliyun.com/en/model-studio/happyhorse-image-to-video-api-reference) (P3), [Editing](https://help.aliyun.com/zh/model-studio/happyhorse-video-edit-api-reference) (P4)

### Remaining guide/authenticity gap
A standalone official HappyHorse 1.1 creative prompting guide was not successfully retrieved. An Alibaba marketing search result mentions a “Happy Horse Prompt Guide,” but the page redirects to a console and does not expose its target in this tool. Mark this unresolved rather than claiming none exists. Many similarly named third-party sites appeared; their alleged prompt-length rules and open-source claims were excluded. No official downloadable HappyHorse weights were verified. Alibaba's official social account links **happyhorse.com**, whose public page lists generation and editing, but provides little crawlable documentation. [Verified product site](https://www.happyhorse.com/) (P5)


## Verified reference syntax, bounded creative guidance

Authored HappyHorse 1.1 R2V: “The red toy car in [Image 1] rolls slowly across the wooden table shown in [Image 2]. Preserve the car's rounded shape and white roof; use the second image only for the setting.” These bindings are literal documented media-order labels, not arbitrary asset IDs. Check that actual uploads match them.

For I2V, the source sets framing and the prompt may be omitted; add text when a particular movement is required. For editing, use the named happyhorse-1.0-video-edit route and explicitly decide audio preservation rather than assuming the 1.1 generation model edits. Standalone creative-guide retrieval remains unresolved; do not import third-party prompt-length lore or claims of downloadable weights.
