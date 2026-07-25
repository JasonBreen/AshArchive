---
name: ash-archive-changelog
description: Maintain evidence-backed Ash Archive project and edition changelog records. Use when adding, formatting, or normalizing changelog entries from repository evidence; never invent test results, claim compatibility, or declare release readiness.
---

# Maintain Ash Archive Changelog

## Canonical Policy

Read `.agents/presets/changelog-agent.yaml` completely before acting. Its `scope`,
`allowed_actions`, `forbidden_actions`, `required_checks`, `stop_conditions`, and
`human_review_required_for` are binding; this skill cannot broaden or relax them. Never invent
mod metadata, accept or reject a mod, promote a candidate, or claim compatibility without
documented evidence and human review.

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`, `.agents/presets/changelog-agent.yaml`, and
   `ash-archive/ROADMAP.md` completely.
2. Identify the set of repository changes to record. Derive entries only from committed
   diffs, merged pull request descriptions, or content already present in other repository
   documents. Do not infer or synthesize entries.
3. Add, format, or normalize changelog entries in `ash-archive/CHANGELOG.md` and the
   relevant edition changelog under `ash-archive/editions/*/CHANGELOG.md`. Keep Pilgrim and
   Sleeper entries independent and do not assert parity between them.
4. From `ash-archive/`, run `python tools/lint_repo.py`. Run
   `python tools/validate_manifests.py` when entries describe manifest or metadata changes.
5. Report every skipped check with a reason, and list each changed file with the entry added
   or normalized.

## Stop Conditions

Stop when an entry would claim compatibility, installability, or release readiness without
repository evidence, or when a version bump or first public release note requires human
authorization.
