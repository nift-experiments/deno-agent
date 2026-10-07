# MIGRATION.md

A migration workbook for converting an existing site to Nift.

This project was created with `nift init --migration`: a normal Nift project
with an agent-ready migration playbook. It is **not** an automatic converter.
Nift provides the rails; the human or coding agent understands the source
framework. Parity comes before cleanup.

Read this file first. Read `HANDOVER.md` second and keep it current after
meaningful checkpoints. `AGENTS.md` (created or augmented by init) points
agents here.

## Operating contract

These rules are the migration contract. Do not violate them without explicit
authorization.

- Preserve route, content and behavioural parity unless divergence is
  explicitly approved.
- Do not modify Nift itself to solve source-project compatibility problems
  without stopping and reporting the requirement first.
- Commit at meaningful migration checkpoints.
- Maintain an explicit known-divergence list.
- Do not classify the migration as complete while unexplained differences
  remain.
- Prefer faithful compatibility stages over speculative rewrites.
- Do not optimize or redesign before the faithful baseline is established.
- Do not destroy the upstream/reference implementation while it is still
  needed for comparison.
- Record exact source and migration revisions.
- Keep `HANDOVER.md` current after meaningful checkpoints.

## Workflow

### Phase 1 - Understand the source project

Before changing anything, establish and record:

- source framework/generator and version;
- upstream repository and exact source revision/commit;
- source build command (and development command where relevant);
- deployment architecture;
- authored content inventory;
- templates/layouts inventory;
- components/shortcodes/render hooks inventory;
- static asset inventory;
- generated/index/listing pages;
- redirects;
- data files and schemas/taxonomies/frontmatter conventions;
- special rendering behaviour;
- the authoritative route set;
- upstream build time and peak memory.

Invariant: **DO NOT START MIGRATION UNTIL THE SOURCE BASELINE CAN BE
REPRODUCED.**

### Phase 2 - Establish parity fixtures

Build appropriate reference evidence before broad migration. Use proportional
fixtures; do not mandate browser testing where it is irrelevant. Candidate
fixtures:

- route inventory;
- generated-file inventory;
- representative browser captures;
- content checks;
- navigation checks;
- keyboard/runtime behaviour where relevant;
- mobile/desktop viewport coverage;
- a known-divergence ledger.

### Phase 3 - Establish the initial Nift structure

Set up:

- project initialization;
- tracking;
- source/output layout;
- templates;
- dependencies;
- schemas/taxonomies where appropriate;
- migration checkpoint structure.

Do not prematurely redesign the source architecture.

### Phase 4 - Migrate shared shells/templates first

Identify and recover the largest common structure first:

- common page shells;
- shared heads;
- headers/footers/navigation;
- layouts;
- repeated structural components.

### Phase 5 - Migrate authored content

Reconcile explicit corpus accounting:

- expected authored inputs;
- converted inputs;
- remaining inputs;
- generated/listing layouts;
- route counts.

Counts must be reconciled rather than guessed.

### Phase 6 - Source-specific compatibility

**MIGRATION SUPPORT DOES NOT MEAN NIFT MUST NATIVELY REIMPLEMENT EVERY SOURCE
GENERATOR'S SEMANTICS.** Faithful compatibility stages are legitimate. For
example, a Hugo source may require Goldmark or Chroma, MDX may use an
external/package rendering stage, and special shortcodes may need adapters.

Rule: **Prefer faithful compatibility over semantic rewrites unless the
migration goal explicitly permits behavioural changes.** And: **DO NOT MODIFY
NIFT CORE TO SOLVE A SOURCE-PROJECT COMPATIBILITY GAP WITHOUT STOPPING AND
REPORTING THE REQUIREMENT FIRST.**

### Phase 7 - Route/content/rendered parity

Require:

- an authoritative route-set comparison;
- missing and extra route detection;
- generated-file-set comparison where meaningful;
- content/render parity checks;
- explicit divergence classification.

No migration is complete while unexplained differences remain.

### Phase 8 - Incremental correctness

Verify, as appropriate for the project:

- single-page edits;
- shared-template edits;
- asset changes;
- data changes;
- dependencies;
- targeted builds;
- incremental-vs-full equivalence.

A migration that only passes a full clean build is insufficient evidence.

### Phase 9 - Benchmark

Record proportionally:

- source baseline build time;
- Nift clean/full build time;
- warm/full and targeted/single-page builds where useful;
- peak RSS;
- environment/hardware;
- measurement methodology.

Do not cherry-pick. Do not hide compatibility-stage cost. If an external
renderer exists, measure and report its cost separately where useful.

### Phase 10 - Clean-checkout verification

Before completion verify on a fresh checkout:

- fresh clone;
- dependency acquisition;
- build from scratch;
- route/content checks;
- no reliance on untracked local state;
- no absolute developer-machine paths.

### Phase 11 - Handover / final report

Produce a final report containing at least:

- source revision;
- migration revision;
- route counts;
- content counts;
- known divergences;
- compatibility stages;
- build measurements;
- memory measurements;
- clean-checkout result;
- remaining work;
- maintenance recommendation.

## Document roles

- `MIGRATION.md` - methodology, baseline, migration plan, parity
  requirements, checkpoints, migration-specific evidence/state.
- `HANDOVER.md` - current operational state, completed work, current blocker,
  exact commands, important decisions, exact next action.
- `AGENTS.md` - project instructions (Nift's migration block is managed and
  safe to augment).
- `investigation/` - baseline evidence, reproductions, audit notes, route
  inventories, browser-matrix metadata, benchmark data, compatibility findings.

## What comes after migration

A faithful migration achieves source parity first. Once the constraints are
understood, a subsequent native-Nift evolution may simplify the architecture -
but do not strip away a compatibility stage until parity is proven and the
simplification is explicitly authorized.

## Deno campaign checkpoints (project-specific)

The generated eleven phases remain the methodology. Concrete gates: D0 init/review (complete); D1 upstream production baseline and inventories (in progress); D2 observable parity fixtures/remote-service contract; D3 shared-shell and representative-family architecture proofs, bounded rendering and dependency/full equality; D4 ordinary corpus; D5 generated/reference/special families and ancillary/search; D6 whole-site/browser parity; D7 full/fresh/changed/lifecycle measurements; D8 production-worthy profiling with before/after evidence and unchanged parity; D9 comparison and final init review/clean-checkout verification. D3 may prototype compatibility before broad Phase 5 work; this makes the generated dependency order actionable without replacing its parity-first contract.

Source is `../deno-upstream` pinned in investigation/BASELINE.json. Reference artifacts/logs/tools live in `../deno-baseline`, separate from this project's `public/`. Never treat the init placeholder as migrated output. Do not modify Nift or tracked upstream files. No remote Orama upload to upstream services. All external generated inputs and service boundaries must be frozen/classified before parity claims. Record five serialized benchmark samples after parity, complete publication/search work, and individual-process versus aggregate RSS boundaries.

Maintained-source model: Maintain rendered HTML bodies, explicit metadata/navigation and shared templates. No routine Markdown or generated-reference transformation unless proven necessary; downloaded Markdown remains publication output.

## D9 final comparison checkpoint

D0–D9 architecture, corpus, HTTP/browser, lifecycle and five-sample benchmark gates are complete; the preceding checkpoint history is retained. Read investigation/D9-COMPARISON.md and MIGRATION-INIT-FINAL-REVIEW.md. Native full and prepared-input boundaries, frozen WASM delivery, measured process/phase RSS and prior timings remain explicit. The final report checkpoint is followed by fresh committed-checkout verification. No Nift core change, Docker experiment change or Labs publication.

## Final clean-checkout gate

D0–D9 complete. Both fresh committed report-checkpoint clones pass complete reference-byte equality and clean Git status. See investigation/D9-CLOSEOUT.md. Labs remains on hold; further improvement candidates are separate future work.
