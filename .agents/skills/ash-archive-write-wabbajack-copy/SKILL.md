---
name: ash-archive-write-wabbajack-copy
description: Draft evidence-backed, lore-native prose for Ash Archive Wabbajack descriptions, edition pages, installation guidance, known issues, and release notes. Use when writing or revising Pilgrim or Sleeper copy; never invent features or test results, hide constraints, hand-edit generated modlists, or claim readiness.
---

# Write Ash Archive Wabbajack Copy

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`,
   `.agents/presets/wabbajack-list-writer.yaml`, `ash-archive/ROADMAP.md`, and both
   edition README files.
2. Treat the project bible as the preference source. Translate its media lenses into
   Morrowind-native language instead of naming, copying, or crossing them over.
3. Trace every material feature, status, compatibility, installation, and support claim to
   repository evidence. Label unsupported language as a draft gap instead of polishing it
   into a claim.
4. Use restrained archival prose and evidence before explanation. Give Pilgrim the language
   of distance, weather, documents, tombs, and retrospective dread. Give Sleeper the
   language of dreams, doubles, identity fracture, intimate horror, and ritual repetition.
5. Keep installation steps, requirements, warnings, and known issues plain. Atmosphere must
   never obscure an action or constraint.
6. From `ash-archive/`, run `python tools/lint_repo.py`. Run
   `python tools/validate_manifests.py` when copy names included content, status, or
   compatibility, and run `pytest` when tooling-backed docs or tests change.
7. Report the factual source for material claims, draft claims needing review, exact command
   results, and skipped checks with reasons.

## Stop Conditions

Stop before inventing features, sources, versions, compatibility, or test results; claiming
installability or release readiness; hiding requirements or known issues; collapsing the
edition voices; changing support boundaries or design rules; or finalizing public copy
without human review.
