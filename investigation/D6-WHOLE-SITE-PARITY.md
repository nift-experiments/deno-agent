# D6 — whole publication and browser parity

Both committed D5 checkouts build from source with only the disclosed prepared dependency cache/toolchain reused. Their complete 2,573-file SHA-256 manifests equal the immutable reference (213,555,032 bytes); builds leave Git clean. Exact revisions and manifests are in D6-clean-checkouts.json.

All 834 HTML routes were fetched from the original production server and each migration: 2,502 responses match status, content type and body hash. D6-all-route-http.json records every route. D5-http-parity.json additionally covers redirects, Markdown negotiation, health and 404 headers and bodies.

Exact HTML bytes preserve content, headings/IDs, links, canonical/meta fields and structured data. Exact non-HTML bytes preserve downloads, search records/metadata, redirects, llms, frontend/static assets and all 834 OG images. The inherited D2 contract ledger (47 duplicate-ID routes and potential unresolved paths/fragments, some affected by runtime redirects) remains unchanged; no upstream defect was repaired and called parity.

## Browser evidence

13 representative routes × desktop/mobile × light/dark × two maintained-source models = 104 captured states. All screenshot dimensions match the corresponding frozen original capture. 99 are pixel-identical. Five have small control/navigation differences, with the largest mean absolute RGB difference 0.03181 on the 0–255 channel scale. D6-browser-matrix.json retains hashes, dimensions, difference bounding boxes and magnitude for every capture. These are not described as 104 pixel-identical screenshots. The HTML, CSS and JS bytes are identical; the remaining differences are localized to theme controls and CLI navigation indicators. A mismatched compositor frame was rejected and recaptured; it is not a publication defect.

D6-interactions.json records 20 passing checks: installation tabs, copy options, actual code clipboard content, deterministic search results/empty/error responses, ArrowDown selection, mobile menu/TOC and tablet API content in both models. Original D2 behavior remains the reference. Screenshots and full accessibility trees are preserved externally under deno-baseline/browser-d6. Search SDK transport is mocked locally; POST forwarding is disabled. No feedback, telemetry or search uploads were sent upstream.

## Boundaries

Local UI/server parity does not prove operation of remote Orama, Claude, feedback storage or deployment credentials. Those remain explicit original service boundaries. Clean-checkout verification runs and browser work were allowed to overlap: their durations are verification diagnostics, not serialized benchmark samples. D7 will measure whole pipelines and complete changed-input/ancillary lifecycle before D8 optimization.
