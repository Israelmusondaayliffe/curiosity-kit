# Amazon Titan Image Generator

Evidence checked 9 October 2026. G1 and v2 are retained separately. HTML model guidance reviewed; dedicated prompt-engineering PDF unavailable. Current lifecycle and every mask-schema detail remain unverified.

## Prompt construction and operation choice
Use a caption-like scene description and the selected endpoint's separate exclusions. For an edit, specify the desired full composition and target change; bind mask/conditioning inputs according to that version. v2-specific conditioning, palette and background-removal capabilities must not be applied to G1 by family name.

Authored caption: “A yellow ceramic vase with three white tulips on a round oak table, centered composition, pale blue wall, soft diffused daylight and natural petal texture.” A v2 palette request can be represented as creative intent, but the actual palette control must come from the v2 API schema. A generic caption does not imply a new native grammar.

## Evidence and unresolved conflict
[Model guide](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-image-models.html): subsequently opened and complete body reviewed. [Service card](https://docs.aws.amazon.com/ai/responsible-ai/titan-image-generator/overview.html): indexed primary body reviewed, not independently opened in this audit. Their mask-format descriptions conflict; use the exact API before submission. [Linked prompting PDF](https://d2eo22ngex1n9g.cloudfront.net/Documentation/User%2BGuides/Titan/Amazon%2BTitan%2BImage%2BGenerator%2BPrompt%2BEngineering%2BGuidelines.pdf) returned 404. Dates not established. No lifecycle or execution assurance follows from a surviving documentation page.
