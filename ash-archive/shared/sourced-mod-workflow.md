# Sourced Mod Workflow (Candidate Intake Desk)

`shared/sourced-mods.meta` is an **intake desk** for candidates, not a list of accepted mods.


## Canonical YAML schema

`shared/sourced-mods.meta` must use a **top-level `sourced_candidates:` list**.

```yaml
sourced_candidates:
  - id: example-mod-id
    thematic_bucket: dream-sixth-house
    # ...remaining required candidate fields
```

Do not use bucket-grouped shapes like `buckets: -> candidates:` in this file.

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

## Source triage gate for unmanaged/unknown-origin entries

- `shared/source-triage.meta` tracks active `modlist.txt` entries with `Nexus_ID` of `0` or `-1`.
- While `source_triage.triage_status` is `open`, listed entries are blocked from `.meta` promotion.
- Keep listed entries in an `unverified` state until triage is closed and package identity + license/source questions are resolved.
- Only after triage closure may entries move to normal `planned`/`candidate`/`rejected` flows for manifest promotion.

## Multi-package `.meta` convention

Use `shared/source-package-meta.meta` when a single source page (for example one Nexus ID) distributes multiple installable packages.

- Parent-level `.meta` records shared source metadata once:
  - `nexus_id`
  - `nexus_url`
  - `base_version`
  - `provenance`
- Child/package-level `.meta` records package-specific metadata:
  - `variant_name`
  - `install_artifact`
  - `edition_notes`
  - `plugin_list`
  - optional `package_version` when it differs from `base_version`

### Version override rules

1. Treat parent `.meta.base_version` as the default version for all packages under that source.
2. If a package has a different version than the parent, set child `.meta.package_version` explicitly.
3. When both are present, child `.meta.package_version` is authoritative for that package.
4. Do not mutate parent `base_version` to match a one-off child package; keep parent version as the shared default for the source page.
5. If many packages diverge and no stable default exists, set parent `base_version` to the most current shared baseline and keep explicit child overrides for all divergences.
