---
name: ash-archive-audit-edition-drift
description: Audit and classify divergence between Ash Archive's Pilgrim OpenMW and Sleeper MWSE editions. Use for cross-edition status mismatches, duplicate risks, unexplained manifest differences, or parity questions; default to reporting and never force engine-specific content into parity.
---

# Audit Ash Archive Edition Drift

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`, `.agents/presets/edition-drift-auditor.yaml`,
   `ash-archive/shared/design-rules.md`, and both edition README files.
2. From `ash-archive/`, run `python tools/compare_editions.py` and
   `python tools/check_duplicate_mods.py`.
3. Trace each finding to the relevant manifest and edition rationale.
4. Classify every difference as `intentional`, `needs-review`, or
   `mechanical-fix-applied`. Default to report-only unless the user requested fixes.
5. After any mechanical edit, rerun both commands, `python tools/validate_manifests.py`, and
   `python tools/lint_repo.py`.
6. Report classifications separately for Pilgrim and Sleeper and preserve engine-specific
   rationale.

## Stop Conditions

Stop when the answer depends on engine testing, feature parity, load order, patch strategy, or
design judgment. A different mod count is not itself a defect.
