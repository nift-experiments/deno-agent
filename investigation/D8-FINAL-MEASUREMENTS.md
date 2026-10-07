# Final optimized migration measurements

Five serialized samples per mode on the active i7-12700H desktop (Linux 7.0.0-29,64 GiB). Model order alternates by sample. Dependencies/maintained prepared inputs are outside timing; OS/user workload is uncontrolled. All 30 complete publications reproduce all 2,573 reference bytes/files. Nift core is frozen.

| Model | Mode | Median seconds | Range seconds | Median process/phase RSS MiB (range) |
|---|---|---:|---:|---:|
| deno | warm-normal-publication | 1.83 | 1.79–2.17 | 104.9 (104.6–105.1) |
| deno | warm-forced-full | 16.51 | 14.83–22.45 | 1474.1 (1425.0–1579.5) |
| deno | application-cold | 16.70 | 14.64–24.05 | 1452.5 (1405.8–2225.8) |
| deno-agent | warm-normal-publication | 1.03 | 0.97–1.61 | 31.1 (30.4–31.3) |
| deno-agent | warm-forced-full | 1.28 | 1.19–1.35 | 136.4 (128.7–141.6) |
| deno-agent | application-cold | 1.45 | 1.34–1.63 | 129.4 (127.1–138.1) |

Normal publication reuses input/output-verified derived pages and exports; it is not full source recomputation. Forced-full bypasses caches and forces Nift composition. Application-cold removes `.generated`, `public` and `.nift/public`, retaining committed inputs and external installed dependencies. RSS is the maximum measured process/phase quantity, not aggregate concurrent process-tree memory. Four DOM worker threads contribute to the renderer process peak.

Initial OG-regenerating warm medians 134.86s/144.07s, first static-asset observations 23.35s/1.54s and intermediate cache samples remain separate. Serial/two/four-worker profiles are diagnostics, not headline medians. Forced/fresh human memory is higher than the serial diagnostic in exchange for lower wall time. All 834 OG images remain static in normal publication.

All 20 maintenance/lifecycle cases were repeated against committed production defaults, without carrying forward previous cases. Each changed publication equals forced recomputation, with ancillary and owned-output retirement assertions. Coordinated source editing is outside timed publication in both models. These changed-input timings are individual observations, not five-sample medians.

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

Raw samples contain hierarchical renderer/orchestration/copy/process counters with nested/parallel boundaries. Search/LLM preparation remains a changed-input fixed cost; shared-source/frontmatter/reference invalidation is conservative. Agent ancillary projections avoid derivation but require coordinated authoring. Native full/prepared-input comparison and D9/init/fresh-checkout closeout follow separately. Labs remains unpublished.
