# Local Agent Presets

This directory contains auditable local agent preset definitions for recurring Ash Archive maintenance tasks. The canonical policy and rationale live in [`ash-archive/LOCAL-AGENT-PRESETS.md`](../../ash-archive/LOCAL-AGENT-PRESETS.md).

These files are intentionally descriptive and runner-neutral. Local tooling may translate them into a specific agent format, but translated presets must preserve the same guardrails, forbidden actions, checks, and human review gates.

## Presets

| File | Purpose |
|---|---|
| [`source-triage-agent.yaml`](source-triage-agent.yaml) | Evidence-first sourcing and provenance triage. |
| [`manifest-lint-agent.yaml`](manifest-lint-agent.yaml) | Mechanical fixes for manifest/schema convention failures. |
| [`modlist-regenerator.yaml`](modlist-regenerator.yaml) | Regenerate derived modlist markdown after manifest changes. |
| [`edition-drift-auditor.yaml`](edition-drift-auditor.yaml) | Audit OpenMW/MWSE divergence and duplicate risks. |
| [`documentation-sync-agent.yaml`](documentation-sync-agent.yaml) | Synchronize planning, policy, and workflow documentation. |
| [`release-readiness-agent.yaml`](release-readiness-agent.yaml) | Prepare advisory release-readiness and blocker summaries. |

## Runner expectations

- Run from the repository root unless a preset command specifies `ash-archive/` as the working directory.
- Treat `forbidden_actions` and `human_review_required_for` as hard stops.
- Record skipped checks with a reason.
- Do not use these presets to claim compatibility, installability, or release readiness without repository evidence.
