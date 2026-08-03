# Changelog

## [Unreleased]
- Add Python 3.11 continuous integration for repository lint, validation, comparison,
  deterministic generated-file checks, and tests.
- Add provenance-only links between canonical sourced candidates and edition planning entries.
- Strengthen validation and document the separation between automated consistency checks and
  human compatibility, acceptance, and release decisions.
- Replace misleading documentation placeholders with explicit blocked-state guidance.

## [2026-07-26] - 2026-07-26

### Features
- Validation and edition-comparison workflows now run faster by removing redundant processing in
  duplicate checks and cross-edition comparison steps.

### Bug fixes
- Repository validation now avoids follow-on `validate_manifest` noise when `load_mods` fails, so
  error output stays focused on the root failure.
- Manifest test coverage now includes explicit `load_mods` error propagation paths and reliable
  missing-file handling.

### Chores
- Expanded automated test coverage for shared path helpers, manifest metadata error handling, and
  mod-section rendering.
- Refactored repository-configuration validation into helper methods to improve maintainability.

### Breaking changes
- None.

## [0.1.0] - 2026-04-25
- Initial scaffold and tooling for Ash Archive control repository.
