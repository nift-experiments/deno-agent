# D5 complete publication

Both source models publish exactly **2,573 files / 213,555,032 bytes**, matching every frozen file byte for byte: 834 HTML routes, 834 OG images, 481 Markdown files, compiled/static assets, source script downloads, redirects, sitemap, llms outputs and local Orama payloads. The 27 read-only HTTP states (nine per server) match original statuses, selected headers and body hashes. Browser revalidation and benchmark/lifecycle work remain D6–D9.

## Source and runtime ownership

Human authored Markdown/MDX, directory data, original JSX layouts/components, scripts, typed/reference sources and prepared structured deno-doc JSON remain source. Standard-library generated Markdown is pinned and committed. Routine publication uses standalone engines and actual bounded generators, then raw Nift composition; no Lume Site is instantiated. Search uses the original local generator and llms functions. Generated redirects are consumed from the original reference generator's JSON yield.

Agent maintained main HTML, surrounding HTML fragments, explicit route metadata, downloads and ancillary search/LLM projections remain source. It does not run Markdown/MDX renderers. OG authoring templates were converted once to maintained JavaScript; image builds use Satori, resvg and Sharp, not a routine JSX source transform. Deno remains a dependency for OG rasterization and the production server. Do not describe the agent project as having no Deno dependency, or either project as removing every Lume library.

Both retain the pinned standalone Lume HTTP Server and original middleware through a bounded root-path adapter. Redirects, go/old links, Markdown negotiation and downloads, llms MIME/cache behavior, health and 404 are preserved. Remote feedback/analytics credentials were not configured or exercised. Production integrations remain explicit external-service boundaries. No feedback, telemetry or search upload was sent.

Compiled frontend artifacts are pinned maintained publication assets, with original TypeScript/Tailwind source retained in the human project. Updating frontend authoring inputs requires refreshing those artifacts, rather than assuming an unchanged compiled asset follows a source edit. Examples' published TypeScript downloads are copied from human authored scripts. Agent ancillary exports/search projections are explicit maintained source and must remain consistent when editing the HTML; D7 adds complete lifecycle validation beyond the representative HTML proof.

## Clocks, order and inherited behavior

Search acquisition timestamps and occurrence order, llms generatedAt, and sitemap source dates are frozen explicitly in data/search-clock.json and sitemap-dates.json. Upstream search contains duplicate IDs: occurrences are retained, not deduplicated. New/changed content remains indexable; freezing clocks does not freeze the human generator's content. The original sitemap excludes 404 and contains 833 entries. Inherited Markdown alternate-link quirks, duplicate controls/IDs and unresolved links are preserved.

The standalone upstream OG dependency bootstraps WASM through a network URL. These migrations use the identical pinned registry WASM bytes locally, making acquisition a setup concern. All 834 regenerated PNGs match the original bytes. No core change or generic framework implementation was needed.

Initial diagnostic complete builds observed human ~178.90s and agent ~158.51s, dominated by uncached OG rasterization (~154.73s/~157.88s). These runs overlapped development/verification and are **not benchmark headline samples**. The earlier standalone first OG pass was ~189.61s. Keep these observations; caching/invalidation is an obvious profiling target for D8. The original upstream Lume pipeline already has an OG cache. D7 must serialize formal samples and disclose cache/source ownership boundaries.

All initialized placeholder output (index plus CSS/JS demo assets) is retired through explicit ownership; build outputs and metadata are ignored, not committed. Imported source/rendered code-block whitespace is intentionally preserved for byte parity; whitespace checks apply to migration-authored code/docs, with pinned source/HTML/assets/exports exempted. Continue directly through D6–D9.
