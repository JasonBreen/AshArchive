# Changelog

Repository-level changes are recorded here. Edition-specific planning changes are also summarized in each edition's changelog.

## [Unreleased]

### Added

- Shared sourced-mod candidate intake, validation, summary tooling, and promotion guidance.
- Initial evidence-backed candidate set for dream/Sixth House, blight/ash/weather, and MWSE survival themes.
- Source-triage and multi-package provenance records, including explicit promotion blockers and child-package metadata.
- Mod Organizer 2 planning records for Sleeper Edition.
- Expanded roadmap and Phase 1 follow-up checklist.
- Six baseline maintenance presets for source triage, manifest linting, modlist generation, edition drift, documentation sync, and release-readiness assessment.
- Matching project-scoped Codex agents and reusable repository skills for every canonical preset.
- Wabbajack list-planning and evidence-backed copywriting presets, agents, and skills, bringing the synchronized automation set to eight workflows.
- Pull-request workflows for repository lint/tests and archive-integrity checks.

### Changed

- Migrated internal YAML control records to the `.control.meta` filename convention and clarified that they are not MO2 download sidecars.
- Hardened manifest validation, category and engine rules, duplicate detection, generated-markdown sanitization, and error reporting.
- Added repository linting for Python, YAML control metadata, agent TOML, skill metadata, and preset/translation consistency.
- Made generated modlist freshness, edition drift, and duplicate checks part of pre-merge automation.
- Configured the metadata-only Python project so editable installs work in development and CI.
- Expanded contributor, agent, status, edition, installation, known-limitations, post-install, and release-gate documentation.

### Fixed

- Reconciled the sourced-candidate schema with its validator and summary tool after parallel changes.
- Corrected metadata loader terminology and legacy filename-convention tests after the `.control.meta` migration.
- Fixed editable-install package discovery for the control repository.
- Strengthened tests so every canonical preset must have a matching Codex agent and repository skill.

## [0.1.0] — 2026-04-25

- Initial Ash Archive dual-edition control repository scaffold.
