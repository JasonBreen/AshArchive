---
name: ash-archive-update-changelog
description: Generate and update Ash Archive changelog entries from recent commits using clear user-facing language grouped by features, bug fixes, chores, and breaking changes. Use for `/changelog` requests and release-note drafting from git history; do not invent behavior changes, compatibility claims, or test results.
---

# Update Ash Archive Changelog

## Canonical Policy

Read `.agents/presets/documentation-sync-agent.yaml` completely before acting. Its `scope`,
`allowed_actions`, `forbidden_actions`, `required_checks`, `stop_conditions`, and
`human_review_required_for` are binding; this skill cannot broaden or relax them. Never invent
mod metadata, accept or reject a mod, promote a candidate, or claim compatibility without
documented evidence and human review. Do not invent release readiness or test outcomes.

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`, and
   `.agents/presets/documentation-sync-agent.yaml` completely.
2. Identify the target changelog file (`ash-archive/CHANGELOG.md` unless explicitly directed
   elsewhere) and collect the requested commit window from git history.
3. Translate commit subjects into user-facing entries grouped under `Features`, `Bug fixes`,
   `Chores`, and `Breaking changes`.
4. Keep claims bounded to what the commit history supports. If a category has no entries, write
   `- None.` rather than inferring changes.
5. Preserve existing changelog style and ordering while adding the new dated entry.
6. Run `pytest` from `ash-archive/` when tooling docs or tests change.
7. Run `python tools/validate_manifests.py` from `ash-archive/` when changelog text references
   manifest policy or metadata examples.
8. Run `python tools/lint_repo.py` from `ash-archive/` when skill files or related agent config
   change, and report skipped checks with reasons.

## Stop Conditions

Stop when requested wording would claim compatibility, installability, release readiness, or
behavior changes that are not supported by repository evidence.
