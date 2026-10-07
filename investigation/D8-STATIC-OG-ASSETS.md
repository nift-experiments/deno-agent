# Maintained OG publication assets

The 834 accepted OG images are maintained source under `assets/og/`. `data/og-assets.json` maps each image to its original published route. Normal builds copy these assets; they never run Satori, resvg, or Sharp. Original public URLs and the 2,573-file publication contract are preserved.

A changed page/title/template does not implicitly regenerate images. Update selected images explicitly with `python3 scripts/update-og.py --route /runtime/run/`; use `--all` only for an intentional whole-corpus maintenance update. Set `DENO_BIN` and `DENO_DIR` for the pinned prepared toolchain. Human updates prepare metadata through the compatibility renderer; agent updates use maintained OG metadata and route titles. New agent routes require a corresponding `data/og.json` entry before generation. New published routes require an asset manifest entry; removed routes cease publication through the ownership ledger.

The explicit command updates maintained PNG bytes and their manifest hashes. Review and commit those changes as source maintenance. Its elapsed cost is recorded separately in `.generated/og-maintenance-metrics.json`. Routine build metrics report zero OG generation, with static copying included in publication.

The earlier five-sample warm medians remain evidence of the initial architecture: deno 134.86s and deno-agent 144.07s. That architecture regenerated all images. Optimized publication results must identify this intentional asset-ownership change; upstream Lume generation remains included in upstream measurements. These are different production architectures, not identical image-generation workflows.

Both corrected publications were checked against the immutable baseline: every file path and SHA-256 matched. This checkpoint does not complete the remaining D7 benchmark/lifecycle campaign.
