---
name: ash-archive-sync-docs
description: Synchronize Ash Archive documentation, links, commands, status language, and maintenance workflows without changing project policy. Use for stale README, roadmap, checklist, agent, or edition-doc references; do not use to alter design pillars, phase gates, edition identity, or unsupported readiness claims.
---

# Synchronize Ash Archive Documentation

## Canonical Policy

Read `.agents/presets/documentation-sync-agent.yaml` completely before acting. Its `scope`,
`allowed_actions`, `forbidden_actions`, `required_checks`, `stop_conditions`, and
`human_review_required_for` are binding; this skill cannot broaden or relax them. Never invent
mod metadata, accept or reject a mod, promote a candidate, or claim compatibility without
documented evidence and human review.

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`, and
   `.agents/presets/documentation-sync-agent.yaml` completely.
2. Identify the authoritative document for each disputed command, status, or policy statement.
3. Make the smallest set of prose and link changes that restores consistency. Preserve the
   two-edition model and evidence-before-explanation principle.
4. Run `python tools/lint_repo.py` from `ash-archive/`. Run `pytest` when tooling docs or tests
   change, and run `python tools/validate_manifests.py` when examples describe manifest policy.
5. Check changed links and report every skipped automated check with a reason.
6. List each changed document and the inconsistency resolved.

## Stop Conditions

Stop when wording would change project scope, roadmap phase gates, edition identity, design
rules, installability, compatibility, or release-readiness claims without existing evidence.
