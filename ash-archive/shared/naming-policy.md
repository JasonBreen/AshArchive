# Naming Policy

- Use lowercase kebab-case for candidate and manifest IDs: `the-dream-is-the-door`.
- Preserve the source's display name when it is known; do not normalize display names merely
  to make the editions look identical.
- Keep an ID stable after other records reference it. A rename must update every dependency,
  conflict, load-order, `source_reference`, and `related_manifest_ids` link.
- Use the same ID and display name across editions only for the same mod identity; edition
  comparison fails when a shared-ID name drifts. Different engine-native implementations may
  use different IDs with an explicit cross-edition rationale.
- Use lowercase edition directory names `openmw` and `mwse`; public names remain Pilgrim and Sleeper.
- Internal YAML control files use `.control.meta`. Do not confuse them with native MO2 `.meta` sidecars.

Run manifest validation, duplicate scanning, and edition comparison after identifier changes.
