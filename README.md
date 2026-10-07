# Deno Docs — maintained HTML migration

This agent-primary project maintains rendered page bodies under `html/`, shared shell fragments under `templates/`, and minimal route/title/download metadata under `data/`. Nift composes raw HTML without Markdown, MDX or JSX content rendering during normal publication.

Run `python3 scripts/build.py` for the complete publication. `--force` forces Nift composition. Routine builds require Python and the frozen Nift binary; Deno is used for the standalone preview server and explicit image maintenance, not ordinary publication.

Markdown downloads, search payloads, LLM projections and redirects are maintained publication inputs. Content edits must coordinate these representations and update the corresponding `projection_body_sha256` acknowledgement. That guard detects unacknowledged body changes; it does not prove semantic projection consistency. See `investigation/D7-MAINTENANCE-CONTRACT.md`. Route additions/renames also require download ownership and static OG mappings; the owned publication ledger retires obsolete outputs.

OG images are maintained source under `assets/og/`, mapped to original published URLs by `data/og-assets.json`. Normal builds never regenerate them. Use `python3 scripts/update-og.py --route /runtime/run/` for an explicit update, with pinned `DENO_BIN`/`DENO_DIR` configured. New image routes need an entry in `data/og.json`; `--all` is only for intentional whole-corpus maintenance.

Read AGENTS.md → MIGRATION.md → HANDOVER.md before work. Parity contracts and ownership boundaries are recorded in investigation/D5-COMPLETE-PUBLICATION.md and D6-WHOLE-SITE-PARITY.md. Profiling and final benchmarks remain in progress; the Deno Labs page is on hold.
