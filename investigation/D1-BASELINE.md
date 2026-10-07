# D1: pinned production baseline

Upstream https://github.com/denoland/docs, commit `9e5dd8d930c8734defe1c3172986e6312353ac1c`. Source/history untouched. Complete source archive, full Git bundle, logs, local binary/cache, generated inputs, acquisition tree and prepared immutable `site/`/archive/manifests are preserved in sibling `../deno-baseline`. Full source checkout stays in `../deno-upstream`. No migrated pages yet; scaffold is not a parity result.

## Reproduction and measurement

Official Deno 2.9.7 Linux x86_64 binary from GitHub release; version matches pinned replacements.json. Lume 3.1.2 / SSX 0.1.14; exact task/import manifests and lockfiles retained in upstream archive. Put `../deno-baseline/tools` on PATH and set DENO_DIR to its cache. Run from upstream: `deno install`, `deno task build`. The task generates reference types/docs and std docs before full Lume/OG images; output is `_site/`. Local search workflow is `deno task generate:search`, no cloud upload. Run it before another full build so summary-derived llms.json and local search assets are copied into output. Production preview: `deno task prod` (PORT can select a local port).

Dependency installation and first nested downloads were outside the prepared observation. Acquisition full task: 434.19 s / 2,842.5 MiB GNU-time peak process RSS, exit 0. Separate local search generation: 1.60 s / 562.5 MiB, exit 0. Prepared complete `deno task build`: 171.56 s / 3,117.1 MiB, exit 0; Lume reports 28.93 s, which is not the whole task. Reference type work remains in the full task; content caches are upstream behavior. These are single baseline observations, not five-run medians or Nift comparisons; OS caches uncontrolled and active desktop host. GNU time records individual process high-water usage, not aggregate concurrent memory. Later D7 will define and instrument serial component/full/search pipelines and warm/fresh boundaries fairly.

## Publication inventory

Prepared reference: **2,573 files**, **213,555,032 bytes**, **834 HTML documents**, **481 Markdown downloads**, **239 published TypeScript files**, **834 per-route OG images**, **1,005 asset files** under the stated extension definition. API HTML family has 101 documents including landing/special pages; generator reports 94 grouped API pages. Generated global redirect file has 338 unique keys (Lume logs 346 entries before duplicate-key consolidation); API redirects have 11,295 keys. Runtime middleware additionally merges go/oldurls and wildcard rules. Do not add these counts without reconciling duplicates/behavior.

HTML families: runtime 172; examples 326; lint 125; API 101; deploy 73; styleguide 12; sandbox 11; subhosting 10; 404/AGENTS/ai/orama one each. Exact routes/assets/file hashes are retained. Source inventory has 460 Markdown/MDX candidates; conventional path mapping matches 365 built routes, not a final authored-content count. LLM collector counts 479 documents; Orama counts 467 Markdown documents plus 11,100 API records = **11,567 search documents**. Counts describe different models and must remain separately labelled. D2 must finish custom-path/generated-source reconciliation before calling any count “authored content pages”.

## Reference behavior and boundaries

Pinned production server preview confirms root 301 to /runtime/, HTML 200, Markdown download/content negotiation 200, old Deno.serve symbol 301 to grouped HTTP-server anchor, llms/health 200 and nonexistent route 404. Initial desktop light/dark and mobile/menu screenshots frozen externally. Runtime HTML unchanged between acquisition/prepared builds; comprehensive browser/search/API matrix is D2, before substantial migration. Browser operations changed theme and menu only; no feedback submitted or cloud indexing upload. Local analytics disabled without GA configuration, feedback needs backend credentials, Orama results come from remote service. Local search corpus is frozen; it is not proof of remote index equivalence.

Inherited reference-generation warnings: 330 dead source links; retained reference-warnings.log. Do not silently fix then claim parity. First acquisition lacked llms.json because no summary index existed; prepared reference includes it after official search generation. Upstream emptyDest:false and live std registry latest-version fetch are reproducibility concerns, not Nift blockers; freeze inputs and use isolated fresh output in later comparisons.

## Architecture and next gate

Read D1-ARCHITECTURE.md for families/components/plugins and two maintained-source models. Preserve Markdown/MDX/frontmatter/structured API source in deno; maintain rendered HTML and explicit models in deno-agent. D2 first: finalize route/source accounting, remote service/HTTP parity contract and representative fixtures. D3: prove bounded MDX/plugin compatibility and shared-shell/raw-composition/dependencies on real content before scaling. No Nift core blocker demonstrated. Generated phases retained with D0–D9 concrete checkpoints; no broad translation authorized by this baseline completion claim.

## Init assessment

Generated AGENTS→MIGRATION→HANDOVER sequence and baseline gate guided work well. Safe rerun refusal and existing-AGENTS augmentation verified. Missing concrete manifests/checkpoint/divergence/fixture files and source-model selection required additions, all recorded with example wording in MIGRATION-INIT-REVIEW.md. Generated scaffold contains blank-at-eol whitespace and no README; preserved for honest dogfooding. No Nift changes, no quiet source rewrites. Final init review remains due at D9.

Prepared-reference input manifest refreshed to the final successful run. Acquisition generated inputs are retained separately. Observed 41 generated std Markdown files lose a blank line inside the preserved custom section on regeneration (e.g. fs.md), so publication Markdown/LLM bytes change while rendered HTML may remain equal. Do not infer a registry-version change from this; freeze exact inputs and classify nondeterminism in D2.
