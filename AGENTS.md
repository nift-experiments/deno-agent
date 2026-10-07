<!-- nift:migration:start -->
## Nift migration

This project is being migrated to Nift.

Read MIGRATION.md before making migration changes.
Read HANDOVER.md for current state and next work.
Preserve the source baseline until parity verification is complete.
Follow migration checkpoints.
Maintain route/content/behaviour parity unless divergence is explicitly approved.
Record and classify known divergences.
Do not modify Nift core to solve source-project compatibility gaps without
stopping and reporting the requirement.
Prefer compatibility adapters/stages over rewriting source semantics solely for
cleanliness.
Run the required parity/build checks before checkpoint commits.
Update HANDOVER.md after meaningful checkpoints.
Do not declare completion without clean-checkout verification.
<!-- nift:migration:end -->
