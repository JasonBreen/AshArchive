# Sourced Mod Workflow (Candidate Intake Desk)

`shared/sourced-mods.yaml` is an **intake desk** for candidates, not a list of accepted mods.

## Candidate intake

For each sourced candidate:

1. Record the source candidate with a stable kebab-case `id` and `name`.
2. Capture `evidence_notes` and `source_url` (or leave URL empty when unknown).
3. Set `source_confidence` (`verified`, `likely`, or `unverified`).
4. Set `compatibility_status` conservatively:
   - keep `unverified` until tested or backed by reliable documentation
   - use `needs-testing` or `conflicting-reports` when appropriate
5. Assign one `thematic_bucket` matching project pillars.
6. Assign `promotion_target` (`openmw`, `mwse`, `both`, `neither`, or `undecided`).
7. Document `risk_level` and relevant engine-specific uncertainty in `engine_notes`.

## Promotion paths

Allowed status transitions:

- `candidate` → `under-review` → `promoted`
- `candidate` → `rejected`
- `candidate` → `superseded`

## Promotion into edition manifests

- `promoted` candidates should only be added to edition manifests after human review.
- Promotion can differ between OpenMW and MWSE.
- Preserve edition-specific implementation logic during promotion.
- Do not force feature parity between editions.

## Rejection and evidence retention

- Keep rejected entries with reasoning in `promotion_notes`/`evidence_notes`.
- Do not delete rejection evidence lightly; historical context is valuable for future triage.

## Testing and compatibility claims

- Compatibility remains `unverified` until tested or backed by reliable documentation.
- If compatibility is marked as tested-compatible (`openmw-compatible`, `mwse-compatible`, or `both-compatible`), include notes describing what was tested and how.
