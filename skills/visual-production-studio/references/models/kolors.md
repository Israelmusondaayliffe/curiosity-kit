# Kolors

Evidence checked 9 October 2026. Official repository/example guidance; no dedicated current creator handbook verified. English and Chinese text-to-image, image-to-image, IP-Adapter and ControlNet are different operations.

## Use the selected conditioning route
Write a coherent scene in the user's intended supported language. Text-to-image establishes appearance and composition in prose. Image-to-image starts from the supplied image and requested change; IP-Adapter binds an image-conditioning role, while ControlNet supplies structural conditioning. Do not pretend prose describing a pose supplies the actual control input, or assume one operation's settings apply to the others.

Authored text-only example: “A porcelain teapot on a bamboo tray beside an open window, gentle morning light, a small branch of plum blossoms in the background, calm ink-wash-inspired colors.” This is an illustrative general brief, not a native optimization claim. Preserve Chinese text when the user requests Chinese rather than automatically translating it.

## Source and limits
[Owner repository](https://github.com/Kwai-Kolors/Kolors): model description, usage and control sections reviewed 2026-10-09. April 2024 benchmarks are historical, not a current ranking. Per-runtime settings, account availability and quality were not tested.
