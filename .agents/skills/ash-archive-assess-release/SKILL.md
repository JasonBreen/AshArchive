---
name: ash-archive-assess-release
description: Prepare advisory, evidence-backed Ash Archive Wabbajack release gap assessments. Use when reviewing Pilgrim or Sleeper checklists, blockers, validation evidence, install-test gaps, or pre-release status; never declare an edition release-ready or invent end-to-end test results.
---

# Assess Ash Archive Release Evidence

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`, `.agents/presets/release-readiness-agent.yaml`,
   `ash-archive/ROADMAP.md`, and both edition release checklists.
2. Separate repository-recorded evidence from pending, blocked, or absent evidence. Keep Pilgrim
   and Sleeper assessments independent.
3. From `ash-archive/`, run `python tools/lint_repo.py`,
   `python tools/validate_manifests.py`, `python tools/generate_modlist_markdown.py`, and
   `pytest`.
4. Inspect generated diffs and treat missing end-to-end install evidence as a blocker, not an
   inference target.
5. Classify blockers by severity and identify the human decision or evidence needed to clear
   each one.
6. Report exact commands and results. Explain skipped checks.

## Stop Conditions

Stop before marking a release ready, claiming installability, finalizing Wabbajack packaging,
or resolving blocker severity that needs maintainer judgment.
