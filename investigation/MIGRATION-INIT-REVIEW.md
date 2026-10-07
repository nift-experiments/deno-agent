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
