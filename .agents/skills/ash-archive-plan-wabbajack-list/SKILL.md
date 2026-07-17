---
name: ash-archive-plan-wabbajack-list
description: Prepare taste-aligned, evidence-backed plans for the Ash Archive Pilgrim and Sleeper Wabbajack lists. Use for category coverage, evaluation batches, edition fit, evidence gaps, or nonbinding list direction; never accept mods, promote candidates, finalize load order, or invent compatibility.
---

# Plan Ash Archive Wabbajack Lists

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`,
   `.agents/presets/wabbajack-list-planner.yaml`, `ash-archive/ROADMAP.md`,
   `ash-archive/shared/sourced-mod-workflow.md`, and both edition README files.
2. Treat the project bible as the preference source. Translate its media lenses into
   Morrowind-native design; do not imitate or introduce crossover content. Surface any
   preference needed by the task that the project bible does not record.
3. Inventory repository evidence before recommending direction. Separate sourced facts,
   interpretations, recommendations, evidence gaps, and human decisions.
4. Plan Pilgrim around atmospheric long-play stability and retrospective dread. Plan
   Sleeper around reactive dream, ritual, and identity systems. Do not force parity.
5. From `ash-archive/`, run `python tools/lint_repo.py`. Run
   `python tools/validate_manifests.py` when using current inventory,
   `python tools/compare_editions.py` for cross-edition plans, and
   `python tools/check_duplicate_mods.py` when recommending candidate placement.
6. Report separate edition plans, exact command results, skipped checks with reasons, and
   the evidence or human decision needed for every unresolved point.

## Stop Conditions

Stop before accepting or rejecting mods, promoting candidates, finalizing edition
placement or load order, changing phase gates or taste rules, or resolving a plan that
depends on unrecorded provenance, compatibility evidence, or personal preference.
