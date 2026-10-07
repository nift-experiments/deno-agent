# Final corrected-source measurements

Five serialized samples per mode, after the source-layout removal fix. All migration samples retain every reference byte; native HTML stays exact with clock/dependency-path differences classified separately. Native measurements use frozen exact WASM delivery with original compile/startup/worker lifecycle inside timing. Live std acquisition is excluded; full native includes reference regeneration, prepared-input native excludes it. The original direct CLI samples remain separate.

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


Earlier optimized human forced/fresh medians16.51/16.70s remain in D8-FINAL-MEASUREMENTS.md. The final campaign is faster, but the small correctness fix is not evidence of a performance improvement. OS caches and active host workload are uncontrolled. Keep both campaigns and all RSS ranges. The maximum measured process/phase RSS is not aggregate process-tree memory. The full stage comparison and maintenance judgment are in D9-COMPARISON.md.
