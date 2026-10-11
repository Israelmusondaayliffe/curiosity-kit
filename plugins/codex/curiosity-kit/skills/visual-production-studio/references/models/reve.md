# Reve 2.1

Evidence checked 9 October 2026. Official release/example coverage only; current endpoint schema and dedicated prompting guide remain unverified. Preserve Reve 2.1 as selected instead of treating the API announcement as a fully qualified adapter.

## Distinct operations
The 14 July 2026 API release describes generation, image editing, and experimental layout creation/edit/render. A layout representation is not necessarily an image prompt or the same operation as raster editing. Before producing native JSON, identify the requested operation and read its current schema. Do not reconstruct fields from a third-party SDK.

For prompt-only work, write the visible result and explicit edit delta. Authored generic edit example: “Move the red circle to the upper-right quarter of the poster. Keep its diameter, the cream background and the exact title ‘OPEN STUDIO’ unchanged.” This is useful intent, not verified Reve layout syntax or an execution recipe.

## Source and access gap
[Official API announcement](https://blog.reve.com/posts/the-reve-api/): full release body reviewed, published 14 July 2026. [Official API help section](https://help.reve.com/hc/en-us/sections/46837462958484-Reve-API) could not be retrieved; the linked console redirects to sign-in. Public HTML was retrieved, but that does not establish the authenticated schema. No login, generation or endpoint test was performed.
