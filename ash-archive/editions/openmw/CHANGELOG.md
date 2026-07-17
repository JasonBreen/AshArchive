# Changelog

## [Unreleased]

### Added

- Edition status, artifact index, installation-state, known-limitations, post-install, and release-gate documentation.
- Pilgrim-aware planning, writing, drift-audit, documentation-sync, and release-readiness automation under the shared preset policy.

### Changed

- Migrated edition manifests from legacy YAML filenames to YAML-formatted `.control.meta` records.
- Kept the generated Pilgrim modlist under pre-merge freshness, manifest, drift, and duplicate checks.
- Clarified that manifest states and generated previews do not imply an installable or playtested release.

### Current development note

- Pilgrim Edition remains in Phase 1 sourcing with no public installer, final load order, patch plan, or end-to-end compatibility record.

## [0.1.0] — 2026-04-25

- Initial Pilgrim Edition scaffold.
