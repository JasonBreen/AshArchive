---
name: ash-archive-triage-sources
description: Evidence-first sourcing and provenance triage for Ash Archive candidate mods. Use when investigating source identity, URLs, versions, archive names, redistribution constraints, package relationships, or uncertainty in shared source-triage control metadata; do not use it to accept mods or claim compatibility.
---

# Triage Ash Archive Sources

## Canonical Policy

Read `.agents/presets/source-triage-agent.yaml` completely before acting. Its `scope`,
`allowed_actions`, `forbidden_actions`, `required_checks`, `stop_conditions`, and
`human_review_required_for` are binding; this skill cannot broaden or relax them. Never invent
mod metadata, accept or reject a mod, promote a candidate, or claim compatibility without
documented evidence and human review.

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`, and
   `.agents/presets/source-triage-agent.yaml`, `ash-archive/shared/mod-meta-schema.md`, and
   `ash-archive/shared/sourced-mod-workflow.md` completely.
2. Identify the exact candidate record and unresolved sourcing question before researching.
3. Prefer current primary source pages. Record the exact page used and separate observed facts
   from inference. Never reconstruct missing versions, archive names, IDs, or URLs.
4. Update only the shared source-triage, sourced-mod, source-package, or workflow files allowed
   by the canonical preset. Preserve acceptance status and unresolved uncertainty.
5. From `ash-archive/`, run `python tools/validate_manifests.py` and
   `pytest tests/test_sourced_mods.py`.
6. Report candidates touched, verified facts, unresolved assumptions, citations, and skipped
   checks.

## Stop Conditions

Stop and request human review when source identity, licensing, redistribution, package mapping,
or compatibility remains ambiguous. Do not promote a candidate into either edition manifest.
