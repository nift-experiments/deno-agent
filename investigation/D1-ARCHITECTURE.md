# D1 architecture inventory (baseline build in progress)

Upstream: https://github.com/denoland/docs at 9e5dd8d930c8734defe1c3172986e6312353ac1c. Full Git history and tracked source archive are retained externally. Local Deno 2.9.7 matches replacements.json and current official release; V8 15.0.245.2-rusty / TypeScript 6.0.3. Lume 3.1.2; JSX runtime SSX 0.1.14; main @deno/doc 0.187.0 versus reference generator 0.188.0. Both lockfiles preserved. Nift 4.8.0 remains frozen.

## Official production workflow

`deno install`, then `deno task build` with the local binary on PATH and external DENO_DIR. Build task runs reference type/doc generation, live JSR std-doc generation, then BUILD_TYPE=FULL Lume. Output `_site/`; emptyDest:false means stale-output hygiene must be explicit in later cold/lifecycle comparisons. CI uses an equivalent split reference/main build and cache-dependent SKIP_OG. We use unchanged complete production task first, not build:light or skipped reference/OG. The first build includes uncached nested downloads and is acquisition timing, not a five-run benchmark.

Reference type inputs derive from `deno types` and pinned @types/node 22.14.1; doc generation has content-hash caches, two lightweight tasks in parallel and Node generation separately with larger V8 allowance. Std package list/latest versions and rendered overviews come from live JSR API; freeze generated files plus URLs/version provenance before future baseline runs. Open Graph images use committed fonts. Full afterBuild copies source Markdown, lint-rule Markdown and produces LLM summary/full text. llms.json depends on separately generated Orama summary input; absence is logged and should not be silently called parity.

## Source accounting and families

SOURCE-INVENTORY.json is exact tracked-source inventory: 1,123 files / 53,278,161 bytes; 457 .md + 3 .mdx are candidates, not content pages. Runtime/deploy/sandbox/subhosting/examples/ai/lint tracked Markdown counts are 131/73/11/10/89/1/124. Generated std/API and TypeScript example pages add publication routes; README/AGENTS/ignored files prevent treating all Markdown as content.

Families: standard documentation with section sidebar/TOC; CLI command reference with structured command data; example tutorial/video/single-TypeScript scripts with JSDoc pragmas and listing/tag filters; lint-rule generation from Markdown; grouped Deno/Web/Node API landing/index/category/all-symbol/symbol/multi-symbol layouts; sandbox examples; styleguide; 404/raw/special pages; OG image layouts. Navigation comes from section `_data.ts`; authored frontmatter includes title/description/last_modified and version/canonical/redirect metadata. Corpus-driven Markdown plugins cover replacements, admonitions, code title/copy, relative paths, heading anchors and Prism syntax classes; MDX allows actual JSX within .md.

## Observable runtime contract

Preserve responsive header/section navigation, accordion state, TOC anchors, desktop/mobile layout, light/dark/system preferences, persisted grouped tabs, code-copy/page-copy/download menus, keyboard Ctrl/Cmd+K search, arrow selection/Escape, examples filters, API anchors/navigation and feedback UI. Inspect actual built families before final fixture selection; source inventory is not browser proof.

Redirects: generated `_redirects.json`, API old-symbol redirects, `oldurls.json`, `/go` entries and wildcard runtime rules; response status/Location belong to server parity, not just generated HTML. Production uses Lume server plus content negotiation for API/Markdown/LLM, health, feedback, GA and caching middleware. Analytics is disabled locally without environment configuration; feedback backend uses GitHub credentials and must not post during this experiment.

Search: Orama cloud client and separate local `deno task generate:search` full/summary payload. Production build does not itself upload search. Capture local corpus/index counts separately from remote index results. Never replace remote service with Pagefind for convenience or claim backend parity from mocked UI. No private cloud upload required for local build; classify remote boundary and fixture mode explicitly.

## Expected difficulties / current blockers

MDX components and Markdown hooks need real corpus fixtures before choosing a bounded renderer; normal Markdown is not enough. API generator/layout data can dominate route count and source transformation; maintained HTML avoids routine transformation but retains reference/metadata/download coherence duties. External JSR data and cache-dependent output require frozen provenance. Source Markdown downloads remain outputs in either source model. Backend handlers are a separate deployable layer. No demonstrated Nift core blocker: migration not started. Pending gate is successful complete upstream build and immutable publication inventory, then representative browser fixtures before D3.
