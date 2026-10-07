# Optimized publication parity

All 2,573 publication files, including 834 HTML documents, reproduce the frozen publication bytes under serial, two-worker and four-worker human recomputation. Static assets, OG images, Markdown downloads, redirects, search/LLM artifacts and compiled frontend bytes remain covered by the same manifest.

The optimized HTTP rerun compares all 834 routes across the original and both migration servers: 2,502 responses match status, MIME and body SHA. The 27-state special contract also matches redirects, negotiation, Vary and Cache-Control.

All 104 responsive/theme states were recaptured, with full AX records and screenshots retained externally under `deno-baseline/browser-d8-final`. Three match the corresponding D6 screenshot pixels exactly; 101 differ within observed theme/search/copy-control regions. Every pixel outside those identified regions matches, and captured dimensions match the corresponding D6 screenshot. Live DOM checks establish the requested CSS viewport and theme; screenshot bitmap dimensions differ from CSS dimensions in the browser capture backend, so those quantities are recorded separately. D6's five tiny differences from upstream remain in the inherited evidence. This is browser/content parity with retained interaction-state differences, not a claim of 104 pixel-perfect screenshots.

Twenty interaction checks pass across both models: Windows tab, copy menu, code clipboard, mock search results, keyboard selection, empty/error search, mobile navigation, mobile contents and tablet API content. Local transport fixtures substitute only Orama search responses and forbid POST; live relevance, credentials, uploads, analytics and feedback are outside this local test.

Twenty prior source-maintenance cases, corruption/removal probes and explicit one-image OG updates pass. The full lifecycle suite will be repeated against the committed production worker configuration before final D8/D9 measurements. Nift core and upstream tracked source remain untouched. Labs remains on hold.
