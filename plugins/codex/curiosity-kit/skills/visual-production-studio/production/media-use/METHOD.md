# Media preparation and reuse

Resolve a composition's media need into an inspectable frozen local asset plus provenance. This is a stateful asset-preparation method: it adopts local files, probes metadata, tracks project identity, supports explicitly scoped cross-project reuse, then uses an explicitly selected provider only when necessary and authorized. A provider catalog result is not permission to transmit private content, spend credits or acquire rights.

## Select the source lane

1. Read the project inventory and actual brief: type, subject/entity, role, aspect, duration, language, transparency, rights and source constraints.
2. Search exact project prompt/type identity, then the specified entity. Verify the current path exists and is still the intended asset.
3. Adopt existing assets/ without network. Inspect dimensions, duration/codec, visible/audible suitability and rights. Filenames are retrieval hints, not proof of subject identity.
4. Only with explicit cross-project permission, read a selected cache directory. Match exact prompt/type or entity, verify content hash and complete marker, import a project-local copy and preserve provenance. Sensitive/private/licensed-restricted assets must not be promoted by default.
5. On a local miss, select the actual approved acquisition adapter. Search/generate/capture are distinct operations. Candidate review is required where visual identity matters: do not confuse the bundled resolver's top-result choice with multi-candidate curation.
6. Freeze accepted media, inspect it, register it, regenerate .media/index.md and reference its local path downstream. No render-time remote retrieval.

## Concrete bundled CLI

```bash
node <METHOD_DIR>/scripts/resolve.mjs --adopt --project <project>
node <METHOD_DIR>/scripts/resolve.mjs --type image --intent 'supplied product hero' --project <project> --json
node <METHOD_DIR>/scripts/resolve.mjs --type bgm --intent 'approved search query' --provider heygen --project <project>
node <METHOD_DIR>/scripts/resolve.mjs --promote <record-id> --cache-dir <approved-cache> --project <project>
node <METHOD_DIR>/scripts/resolve.mjs --type image --intent 'exact approved query' --reuse-cache --cache-dir <approved-cache> --project <project>
```

Flags include --type/-t, --intent/-i, --entity/-e, --project/-p, --adopt, --json, --provider, --promote, --cache-dir and --reuse-cache. Default operation is project/local-only. Cache use is opt-in, not automatic; there is no hidden organize command. Serialize each project's resolver calls; the CLI lock prevents concurrent manifest ID allocation. After a crashed process, inspect the lock and ownership before removing a stale lock.

The concrete external adapter implements selected HeyGen audio catalog BGM/SFX search and asset image/icon search. Its historical CLI contract expects the X-HeyGen-Client-Source attribution header, introduced in >=0.1.6; verify actual installed version and command availability before use. The generic provider registry also retains local brand extraction from frame.md → design.md → DESIGN.md, and a voice stub. Voice generation is unimplemented here. No bundled 19-file SFX fallback exists in this owner; do not claim it does. The resolver does not implement news/web/tweet retrieval, image generation, background removal or vectorization. Use a real authorized specialized adapter for those operations or report unavailable, preserving the requested need.

An API key or installed binary establishes capability only. Select account/provider and get any needed transmission/payment/access approval. Never request keys in chat, silently install a CLI, configure persistent credentials or fall back across providers. Local assets remain usable when a provider is unavailable.

## Storage, provenance and quality

Project .media/manifest.jsonl is the machine ledger; .media/index.md is the readable inventory. Records carry id, type, path, source, description, actual duration/dimensions/transparency where known, entity and provenance. Type directories distinguish audio/bgm, audio/sfx, audio/voice, images and video. Local brand data is a design document, not a logo image. Keep source URL/provider ID, license/attribution, acquisition date, original requested prompt, modifications and reuse scope alongside accepted media. A missing probe value stays unknown; successful adoption does not certify quality.

Explicit cache promotion writes content-addressed SHA-256 data and a completion marker under the user-selected cache. Imports verify bytes rather than trusting names. Do not store private media in a global default HOME. No automatic promotion or hidden cross-project reading. Both original project and new imported reference keep their identity; do not replace user files.

Remote freeze requires HTTPS, bounded streaming bytes, timeout, allowed media content types and redirect validation. It writes a temporary partial and promotes only a complete nonempty file. Sensitive URLs/content require the same authorization as other transmission. A nominal content type still needs media decoding and actual viewing/listening. Broken/incomplete downloads do not become registered assets. Use argument-array subprocess calls for metadata and provider queries, never shell-interpolated filenames.

Return the path/id, type and observed metadata, source/rights caveats and any unfilled need. Keep noisy search results on disk with enough provenance to audit. Final assembly must fail on missing requested media; an intentional no-audio/no-image choice is different and must come from the accepted plan.
