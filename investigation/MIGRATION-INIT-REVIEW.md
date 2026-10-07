# Migration init review: D0 (running)

Nift 4.8.0, installed `/usr/local/bin/nift`; core is frozen. Read AGENTS first, then MIGRATION, then HANDOVER, then configuration/templates/content/assets and investigation README. Original generated guidance is retained in `investigation/generated-init/` before tailoring.

## Immediately useful

AGENTS explicitly points to the right files, forbids core fixes without reporting, requires parity/checkpoints/known divergences and handover updates. MIGRATION correctly gates implementation on reproducible upstream, separates route/content accounting, legitimizes bounded compatibility stages, requires incremental/full checks and clean-checkout reproduction. HANDOVER concretely explains configuration, frequent build/status, source/output ownership, literal sigils, JSON, paths and neighbouring tools. Initial build/status succeeds. These instructions should be retained.

## Concrete ambiguities and gaps

| Generated instruction | Interpretation / extra information needed | Suggested generated wording or file |
|---|---|---|
| “before changing anything” in Phase 1; initialization is Phase 3 | Init necessarily creates a placeholder before upstream discovery. No source translation starts here. | “Init scaffolding may exist; do not translate upstream pages before a reproducible baseline.” |
| “Preserve the source baseline” | Source checkout, production reference and output need distinct sibling paths. Chose `../deno-upstream`, `../deno-baseline`, local `public/`. | Generate a baseline manifest with source URL/SHA, source directory, immutable reference directory, migration output directory, tool hashes and commands. |
| “Record exact source and migration revisions” | Need external generated API inputs and registry data pinned too. Deno generates API docs from the binary and std docs from live JSR. | Add external-input inventory: version/URL/body hash/capture date/cache boundary, and flag unresolved moving inputs. |
| “known-divergence list” | No actual ledger/checkpoint files are created, only an investigation README. | Generate `investigation/KNOWN-DIVERGENCES.md` with ID, route, observed behavior, inherited/intentional/blocking classification, evidence, approval and resolution. |
| “checkpoint structure” / workflow phases | Eleven phases are useful dependencies, not a commit checklist; compatibility proof is needed before broad authored migration. | Generate a status table with acceptance gates, commands/evidence paths, and current/next checkpoint. Keep phases rather than auto-replacing with Docker stages. |
| “faithful compatibility”; “do not prematurely redesign” | User explicitly authorizes two source models: maintained MDX/structured inputs versus maintained HTML. Same rendered parity does not require same maintained semantics. | Ask/store `source-model: authored` or `rendered`, preserving source/reference independently in either mode. |
| static assets live in output tree | Default init creates generic assets and an empty index that are not Deno output. No evidence says those are migration results. | Mark scaffold as placeholder; suggest preserve/replace at architecture proof, forbid inclusion in parity/benchmark counts. |
| “peak RSS” and “benchmark proportionally” | No aggregation boundary, sample policy or production-versus-dev distinction. | Add elapsed pipeline/process RSS fields, five serialized samples, prepared dependencies exclusion and explicit remote/search/frontend stages. |
| “Read README” | Init does not generate a project README. | Generate short commands/current-status README or qualify “if present”. |

## Rerun behavior

Disposable rerun probe exited 1: “this directory is already a Nift project”. All file hashes unchanged, including custom AGENTS and content sentinels. Safe refusal, not idempotent regeneration. First-init augmentation probe passed: existing AGENTS prefix retained exactly and one managed block appended. Recommend document refusal and offer explicit non-destructive guidance-refresh mode rather than rebuilding a project.

## Documentation consultation / inferred choices

No nift.dev consultation was needed for D0; generated build/status/configuration instructions were actionable. No raw composition API is assumed from Docker: consult current docs and prove it at D3. External upstream README, tasks and CI are necessary to identify production stages. Their build:light command is not a complete production baseline. Remote Orama upload needs private service credentials; do not upload to upstream's service. Preserve local search payload and classify remote behavior separately.

## Status

D0 initialization and first review complete; D1 baseline acquisition in progress. No migrated content, no performance claim and no Nift modification. Revisit all categories after actual campaign work; this is an initial assessment, not the final init review.

Generated public/index.html contains a whitespace-only content line, so default git diff --check flags trailing whitespace on initial import. Preserve the generated scaffold for dogfooding; use a one-time blank-at-eol exemption for D0, not a Nift core edit.

D1 finding: upstream full build succeeds without custom patches, but separate local search generation is needed for llms.json, live external std inputs need freezing, and generated std custom-section whitespace changes on rerun. Suggested baseline scaffolding must distinguish complete CLI success from complete deployment/search payload coverage and account for nondeterministic outputs.

## D2 findings

Add generated guidance: "Derive source-to-route accounting from the pinned executable configuration and generated outputs; do not treat source extension counts or upstream README prose as authoritative page counts." Ordinary .md is MarkdownIt despite upstream prose suggesting MDX. Add separate inventory templates for authored sources, generated inputs, downloads, redirects, search records and HTML routes. A parity ledger should retain inherited duplicate IDs and unresolved links instead of silently repairing them. Documentation discovery should point to the docs index: guessed template/incremental/tracked URLs returned 404; actual tracked-file documentation is https://nift.dev/docs/tracked-json.html and the index links incremental-builds.html. The external afterRender probe is investigation only, not maintained source or a routine build stage.

## D3 findings

Proposed generated wording: "For pre-rendered HTML, use an explicitly raw composition path and register every renderer input and transient fragment as a dependency. Include a real-source literal-syntax fixture; rendered content must not become template code." Add a tracked-file example naming template explicitly. Add: "Generated-input ownership must be explicit: distinguish upstream refresh/acquisition from publication and state which prepared inputs are committed. Compare both complete pipeline costs and comparable rendering components." Initialized public output and page build metadata should be disposable; removing the initial placeholder must be included in the ownership ledger. Fresh-checkout guidance should warn that nested upstream ignore rules may omit prepared inputs unless deliberately included.

## D4 findings

Proposed wording: "Keep filesystem inventory paths distinct from renderer runtime source paths; normalization can alter relative links, Markdown alternatives, edit links and feedback bindings." The one Vento expression demonstrates why source compatibility should be corpus driven: an exact source-function expansion suffices without implementing a general template engine. Add real-source whole-family parity before calling a compatibility adapter complete.

## D5 findings

Proposed generated external-input inventory fields: owner, refresh command, maintained/generated status, content hash, network boundary, clock/order normalization, and normal-build inclusion. Include compiled frontend assets and WASM alongside content/API inputs. Proposed wording: "A complete publication may include Markdown downloads, source examples, search indexes, llms files, sitemap, redirects and generated social images; verify their ownership and lifecycle, not just HTML routes." Add a standalone HTTP contract template recording status, Location, MIME, Vary, Cache-Control and body hashes. No-credentials local testing can retain real middleware while using deterministic browser transport mocks. Do not conflate avoiding Markdown/MDX rendering with removing all runtime/tool dependencies. Preserve inherited code-block whitespace when byte fidelity requires it; keep checks on migration-authored code.

## D6: verification evidence must name its boundaries

Proposed MIGRATION.md wording: "Record clean-checkout revisions, complete output manifests and post-build Git status. Distinguish byte equality, semantic/browser behavior, pixel differences, remote service mocks and inherited source defects. Verification runs that overlap other work must not become benchmark samples." A source-generated server can own negotiation/redirect semantics outside Nift; the generated playbook should require these HTTP contracts explicitly.
