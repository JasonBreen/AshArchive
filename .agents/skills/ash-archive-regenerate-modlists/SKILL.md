---
name: ash-archive-regenerate-modlists
description: Safely regenerate Ash Archive OpenMW and MWSE `MODLIST.md` files from edition manifests. Use after manifest changes affect generated public lists or when checking generated-output drift; never use it to hand-edit generated sections or alter manifest status to shape output.
---

# Regenerate Ash Archive Modlists

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`, and
   `.agents/presets/modlist-regenerator.yaml`.
2. Inspect the current diff and identify the source manifest change that should affect generated
   output.
3. From `ash-archive/`, run `python tools/generate_modlist_markdown.py`.
4. Review both generated diffs. Stop on unexpected deletions, scope expansion, or output that
   contradicts manifest status.
5. Run `python tools/validate_manifests.py` and `python tools/lint_repo.py`.
6. Report generated files changed and whether the change is generated-only or accompanies
   manifest edits.

## Guardrails

Never hand-edit a generated section, suppress generator failures, or change a manifest status
solely to make generated output appear clean. Escalate generator logic changes for human review.
