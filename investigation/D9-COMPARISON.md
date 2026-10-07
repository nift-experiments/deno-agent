# Deno migration comparison

This experiment reconstructs the pinned Deno Docs production publication with two Nift projects, without modifying Nift. It preserves all 2,573 publication files, 834 HTML documents, 481 Markdown downloads, 834 OG images and 11,567 local search records. The source-model and external-service boundaries matter as much as build time.

```
deno:
maintained Markdown/MDX/frontmatter + prepared structured references
  → standalone corpus-bounded renderer
  → transient verified HTML/cache
  → Nift raw composition
  → publication + derived local search/LLM exports

deno-agent:
maintained HTML + coordinated metadata/download/search/LLM projections
  → Nift raw composition
  → publication
```

All OG images are maintained static assets. Normal publication copies them; an explicit selected-image maintenance command regenerates an image when an editor intentionally updates its page/title/template. Agent routine publication has no Markdown/MDX/JSX content renderer and launches no Deno runtime. Human source directories and actual plugins/components/generators remain authoritative; generated HTML is disposable derived state. The standalone adapter implements the actual pinned corpus, rather than constructing a Lume Site or rebuilding the framework generally. These are complete orchestrated Nift migrations, **not measurements of native Nift `@markup` performance**.

## Parity before performance

The complete publication manifest matches the frozen reference bytes. All 834 routes match original HTTP status, MIME and body hashes (2,502 responses), and the special contract covers redirects, health, content negotiation and cache headers. The D6 matrix retained five tiny upstream pixel differences. D8 recaptured all 104 model/theme/viewport states: three exactly match corresponding D6 screenshots, while 101 have differences within identified theme/search/copy control regions; every pixel outside those regions matches. Bitmap dimensions match D6, and separate live DOM observations confirm CSS viewport and theme. Twenty tab/copy/clipboard/search/mobile/tablet interactions pass. This is faithful browser/content behavior with recorded control interaction-state differences, not an assertion that every screenshot is pixel-identical.

Search UI fixtures supply deterministic local two-hit/empty/error responses. They do not prove live Orama relevance or backend indexing. Local search payload bytes are retained; no cloud upload, analytics or feedback was sent. Nondeterministic export build-clock/order fields are explicit frozen inputs in `data/search-clock.json`, while source content and metadata are regenerated. Clock refresh is a separate provenance decision; these frozen values must not be read as current production freshness timestamps. Inherited duplicate IDs and potential unresolved links/fragments remain visible in the original ledger, rather than silently being repaired.

## Improvement process

Initial migration warm medians were 134.86 seconds for `deno` and 144.07 seconds for `deno-agent`, dominated by routine OG regeneration. Those historical samples remain intact. The first static-asset observations were 23.35 and 1.54 seconds; they are individual observations, not medians. An intermediate source-cache campaign is also preserved separately. The first optimized five-sample campaign measured 16.51s forced / 16.70s application-cold for `deno`, and 1.28s / 1.45s for `deno-agent`. The final campaign on the layout-removal correctness checkpoint is faster (see below). That small correctness change does not justify attributing the timing difference to an optimization: the active host, OS cache and runtime variation remain uncontrolled. Both campaigns and the earlier human cold RSS outlier of 2,225.8 MiB remain in the evidence.

Profiling rejected the assumption that Markdown explained the 20-second gap. A diagnostic uncached renderer spent roughly one second in inclusive Markdown and a quarter-second of that in Prism, versus roughly ten seconds in DOM normalization and several seconds in JSX layouts. MDX applies to only three source pages. There was no per-page subprocess startup: one runtime owns the renderer and MDX engine, with process-cached imports; separate deterministic search/clock/LLM stages account for the other runtime invocations.

Production changes remove per-page component-directory inventory, memoize shared metadata, reuse verified deterministic pages/exports, and put the exact DOM parser/serializer plus table wrapping in four persistent DOM-only workers for large misses. Small edits avoid worker startup. Explicit frontmatter-field provenance ensures a removed field cannot resurrect its bootstrap value. Ancillary output hashes, malformed-cache recovery, literal template-like source syntax, source aliases and changed-versus-forced equality were tested. All serial/two/four-worker variants reproduce the same publication. Diagnostic forced times/RSS were 22.36s/887.1 MiB, 15.32s/1330.2 MiB and 13.51s/1485.8 MiB respectively. Four workers favor elapsed time while consuming more memory; that tradeoff remains in the evidence.

## Method and results

| Model | Publication mode | Median seconds | Range seconds | Median process/phase RSS MiB (range) |
|---|---|---:|---:|---:|
| deno | warm-normal-publication | 1.31 | 1.22–1.37 | 104.3 (104.0–105.0) |
| deno-agent | warm-normal-publication | 0.70 | 0.65–0.92 | 30.8 (30.3–31.0) |
| deno | warm-forced-full | 13.16 | 11.84–13.93 | 1486.5 (1441.7–2107.5) |
| deno-agent | warm-forced-full | 1.07 | 1.04–1.17 | 132.3 (131.8–141.2) |
| deno | application-cold | 11.16 | 10.85–13.67 | 1457.1 (1409.2–1513.5) |
| deno-agent | application-cold | 1.01 | 0.92–1.21 | 136.4 (132.0–140.1) |
| upstream | warm-full | 153.76 | 145.99–171.36 | 3186.7 (3090.3–3219.6) |
| upstream | application-cold | 314.69 | 305.30–364.76 | 3184.8 (3089.8–3277.1) |
| upstream | prepared-input-warm-publication | 25.57 | 24.38–27.47 | 3143.0 (3103.1–3224.1) |
| upstream | prepared-input-application-cold | 159.58 | 154.53–173.13 | 3137.7 (3058.4–3179.0) |

Forced-full component medians (nested subsets are not additive):

| Stage | deno seconds | deno-agent seconds |
|---|---:|---:|
| Renderer orchestration incl. source/cache preparation | 9.658 | — maintained / included above |
| Source discovery (subset) | 0.014 | — maintained / included above |
| Input hashing/output validation (subset) | 0.336 | — maintained / included above |
| Renderer process wall | 9.224 | — maintained / included above |
| Nift preparation + composition | 1.018 | 0.767 |
| Nift process (subset) | 0.443 | 0.425 |
| Local search generation + clock stage | 1.861 | — maintained / included above |
| LLM generation | 0.298 | — maintained / included above |
| Non-HTML publication | 0.242 | 0.264 |
| Asset/ancillary copy (subset) | 0.147 | 0.158 |
| Static OG copy (subset) | 0.060 | 0.064 |
| Markdown download copy (subset) | 0.023 | 0.024 |
| OG generation | 0.000 | 0.000 |
| Negotiation artifact generation | 0.000 | 0.000 |

Native component medians (frozen WASM delivery; full versus prepared-input boundary):

| Mode | Reference seconds | Search seconds | Lume publication seconds |
|---|---:|---:|---:|
| warm-full | 126.671 | 1.518 | 25.441 |
| application-cold | 138.738 | 1.546 | 174.542 |
| prepared-input-warm-publication | — prepared input | 1.485 | 24.074 |
| prepared-input-application-cold | — prepared input | 1.488 | 157.738 |

Human forced-full renderer counters (five-sample medians; overlapping work counters are not critical-path wall time):

| Counter | Seconds |
|---|---:|
| Initial metadata | 0.106 |
| YAML/frontmatter subset | 0.061 |
| Per-page metadata | 0.224 |
| Examples listing generator | 0.048 |
| Script examples generator | 0.017 |
| Lint generator | 0.107 |
| Grouped reference generator | 1.258 |
| Component binding | 0.067 |
| Bodies | 1.019 |
| MDX subset | 0.059 |
| Layouts | 4.157 |
| Inclusive Markdown (overlaps body/layout/generators) | 0.969 |
| Markdown parsing subset | 0.647 |
| Prism subset | 0.262 |
| JSX expansion (overlapping subset) | 4.087 |
| Redirect generation subset | 0.007 |
| DOM parallel job-work sum | 13.275 |
| Output I/O parallel job-work sum | 2.826 |
| Backpressure wait | 1.286 |
| Drain wait | 0.135 |

Changed-input observations (one serialized changed publication per case/model; coordinated source editing is outside build time; each equals forced recomputation):

| Change | deno seconds | deno-agent seconds |
|---|---:|---:|
| 1-bodies | 4.48 | 1.72 |
| 10-bodies | 4.91 | 2.29 |
| 100-bodies | 5.61 | 1.71 |
| shared-layout | 2.03 | 1.75 |
| navigation | 15.55 | 1.80 |
| title-metadata | 17.75 | 1.66 |
| generated-reference-data | 14.88 | 1.56 |
| route-add | 16.80 | 1.69 |
| route-rename | 19.05 | 1.61 |
| route-delete | 19.69 | 1.93 |

Native changed-input production observation (one sample, not a median): 135.08s total; reference_types_and_doc 111.73s, search 1.36s, lume_publication 22.00s. This repeats reference/search/full Lume production publication rather than development-server hot reload. Source editing is outside timing and the authored file was restored.


Normal unchanged publication may reuse verified derived output. Forced-full publication recomputes every human page/export and forces Nift composition. Application-cold removes local generated/output/build metadata while retaining committed prepared inputs and installed dependencies. Native upstream full phases include reference type/doc regeneration, local search and full Lume publication, including its native OG stage; native prepared-input publication omits reference regeneration to match the migration's maintained prepared-input boundary. Live std registry acquisition is frozen/excluded from repeated measurements. Native warm Lume publication already caches unchanged OG images by JSX; clearing application state regenerates them. The repeated native campaign locally delivers the exact two pinned resvg/esbuild WASM byte streams, preserving compilation count, worker lifetime and initialization inside timing. Two direct CLI dependency-fetch failures and three successful direct CLI observations are retained separately and are not pooled with this frozen-delivery campaign. This is qualified native production-phase timing, not an unchanged official full-task measurement.

The original official full `deno task build` observation (171.56s, 3117.1 MiB) remains separately labelled as one baseline observation.

Five serialized samples per mode run on the same active desktop host with model ordering alternated where practical. OS caches and other user workload are uncontrolled. Dependency installation, external acquisition, source editing and repository cloning are outside timed publication; local search preparation/publication remains inside where the source model derives it. Compiled browser assets are maintained publication inputs in both migrations; ordinary publication does not rebuild the original frontend bundle. Prepared structured references, std content and frozen publication clocks are explicit input/refresh boundaries rather than hidden application caches. The native generated HTML matches every original document; seven non-HTML path/hash differences are classified: dependency-symlink realpaths change the SDK chunk name/import while normalized code is identical, and search/LLM/sitemap publication clocks differ. Migration output retains all original bytes.

Peak figures are maximum measured process/phase RSS, **not aggregate concurrent process-tree memory**. DOM worker threads contribute to the renderer process's RSS.

Component counters are hierarchical. Prism/parsing are subsets of inclusive Markdown; MDX is a body subset; generator families are generation subsets; JSX calls also occur in layouts. Parallel DOM/output job-work counters overlap main-thread production. Do not add nested/overlapping numbers to infer whole-pipeline time.

## Why the human model remains slower

The initial gap was largely avoidable implementation work: shared preparation and full DOM normalization were repeated even when source was unchanged. The final cached gap is small because those deterministic outputs are reused. Fresh/forced human builds still derive rendered bodies, grouped references, shared shells, DOM normalization and search/LLM exports; the agent project maintains those representations directly. This is a different authoring contract, not an equal amount of transformation work executed by different engines.

The final forced median gap is 12.09s (13.16s versus 1.07s). Human renderer orchestration accounts for about 9.66s, derived search for 1.86s and LLM generation for 0.30s; preparation/publication also differ. Inclusive Markdown is about 0.97s, with Prism about 0.26s inside that figure. These are independently computed component medians and nested counters, so they explain the scale rather than form an exact additive accounting of the median gap.

There is no defensible numerical claim that all 12.09s is irreducible authoring-model cost. The source model requires deriving the maintained publication representations; it does not require this particular renderer implementation or DOM pipeline. The campaign demonstrated avoidable repeated discovery/shared work, redundant OG generation and serial normalization, then removed those costs within the faithful architecture. Further narrowing of global invalidation or replacing the normalization/layout strategy would need additional dependency and semantic work, rather than a safe obvious deletion from the accepted pipeline.

It would be inaccurate to classify all remaining forced/fresh time as an inherent Markdown tax. Actual parsing/highlighting remains a small subset. The need to derive outputs from authoritative source is intrinsic to this human model; the chosen DOM/layout/reference/export implementation, runtime startup and conservative invalidation are tooling choices that could improve further. Source frontmatter/shared-code/structured-data changes conservatively invalidate all pages, and changed search inputs trigger whole-index preparation. These are transparent remaining profiling targets, not proof of a Nift core limit. Nift composition itself is only one measured part of publication.

## Maintenance judgment

For **agents implementing under human direction**, I prefer `deno` for this particular corpus and its complete publication contract. The agent-primary model is faster and has a simpler build, but one documentation edit can require coordinated HTML, downloadable Markdown, search statistics/content, LLM projections and metadata changes. Its acknowledgement hash catches an unreviewed body change, not semantic disagreement between those representations. The human model derives those projections from one maintained source and keeps structured references editable. With the profiled renderer and verified caches, its build cost is a reasonable price for that consistency. If the product deliberately dropped or redesigned those projection requirements, the agent choice could change; that is outside this parity experiment.

For **mixed human and agent editing**, I also prefer `deno`: Markdown/frontmatter/source organization are easier to review, and editors do not have to synchronize the same fact across several publication representations manually. Removing migration effort and incumbency does not change either preference. This differs from the earlier Docker assessment because the maintained ancillary contract and actual editing burden differ; the result is an independent judgment, not a predetermined preference for HTML.

The demonstrated publication performance and ability to preserve a production-scale site without core modifications justify a serious Deno/Nift engineering evaluation. They do not establish that Deno definitely should migrate. An official decision must weigh long-term adapter ownership, structured-input refresh tooling, deployment/services, editor ergonomics and integration with Deno's existing ecosystem. Native upstream behavior and search/acquisition boundaries remain part of that evaluation.

## Remaining improvement candidates

Keep source-family/metadata invalidation narrower where correctness can be proved; consider per-record search/LLM updates; reduce shell/DOM work and layout duplication; amortize remaining runtime startup; profile large prepared-reference memory and hashing; improve selected-image metadata preparation; optimize common filesystem publication without weakening owned-output retirement. Agent projection-maintenance tooling could reduce coordinated-edit risk, but would be a separate source-maintenance feature, not a hidden renderer in normal builds. These candidates are separate from the accepted migration and do not authorize Nift changes.

The final init assessment gives concrete generated-file and wording recommendations in `MIGRATION-INIT-FINAL-REVIEW.md`. No Labs page is published as part of this closeout; the user's publication hold remains in effect.

## Evidence and reproduction

Pinned upstream source: `9e5dd8d930c8734defe1c3172986e6312353ac1c`. Final measured migration source: `deno` `380baeb`, `deno-agent` `4a81df5`; later closeout commits contain documentation/evidence only. Deno 2.9.7 and Nift 4.8.0 are recorded in [BASELINE.json](BASELINE.json). Nift binary SHA-256 remains `eae6fee767e2c21d0100b4c96ab660c685f12b80202e2d4eae563316ca62bf08`.

Run `python3 scripts/build.py` for complete normal publication; `--force` recomputes all derived human content/exports and forces Nift composition. With committed maintained inputs and prepared dependency cache, remove `.generated`, `public` and `.nift/public` to reproduce application-cold state. Dependency acquisition is separate. `nift build` / `nift status` cover composition only. Explicit selected-image maintenance is `python3 scripts/update-og.py --route /runtime/run/`; image changes are intentional maintained-source updates.

- [Archived external runners](benchmark-runners/README.md).
- [Final migration samples](d9-final-profile-benchmark.json), [qualified native samples](d9-final-upstream-benchmark.json), [native changed-input observation](d9-final-upstream-changed-input.json).
- [Initial OG-heavy campaign](d7-initial-benchmark.json), [first static-asset observations](d8-static-og-verification.json), [intermediate cache campaign](d8-page-cache-benchmark.json).
- [Earlier optimized campaign](d8-profile-benchmark.json), [production lifecycle](d8-production-lifecycle.json), [worker/cache correctness](d8-worker-cache-correctness.json), [source field removal](d8-frontmatter-removal.json), [layout-removal native control](d9-layout-removal.json).
- [Whole-route HTTP](d8-all-route-http.json), [special HTTP states](d8-http-parity.json), [browser matrix](d8-browser-parity.json), [interactions](d8-browser-interactions.json), [explicit OG maintenance](d8-og-maintenance-check.json).
- [Native dependency delivery](d9-native-dependency-delivery.json), [pinned WASM inputs](d9-native-wasm-inputs.json), [archived external runner bootstrap](native-benchmark-bootstrap.ts), [native clock/dependency-path classification](d8-native-nondeterminism-details.json), [direct CLI observations](d7-upstream-network-bound-observations.json).
- [Final clean-checkout ledger](d9-final-fresh-checkouts.json) records successful fresh clones of this report checkpoint: builds began without application state, matched the complete reference manifest and left Git clean.

The external native bootstrap is benchmark-runner tooling, not migration source. To reproduce its dependency delivery, place it at the external runner root as `native-bootstrap.ts`, acquire the exact two assets listed in the WASM ledger under `tools/native-wasm/`, then run the pinned original CLI/config through the documented `deno task --eval` command. It intercepts only those two URLs; original compilation and worker lifecycle stay inside publication timing. Preserve the original direct CLI observations separately.
