# Local Agent Presets

This document explains the reusable local agent presets for routine Ash Archive maintenance.
The machine-auditable YAML files in `../.agents/presets/` are canonical; the Codex TOML
agents and repo-scoped skills bind to those presets. All layers are intentionally conservative:
agents may prepare evidence, apply authorized mechanical updates, and run validation, but
they must not invent provenance, compatibility evidence, or release readiness.

## Shared operating rules

Every preset must follow these baseline constraints before doing specialized work:

- Read `../AGENT-RULES.md`, `PROJECT-BIBLE.md`, and the relevant edition or shared documentation before editing.
- Keep changes small, branch-scoped, and reviewable.
- Treat all `.control.meta` files as internal YAML control metadata, not Mod Organizer 2 download sidecars.
- Never synthesize source URLs, archive names, version numbers, Nexus IDs, compatibility claims, or test results.
- Leave uncertain entries marked `unverified`, `needs-testing`, `planned`, or `blocked` as appropriate.
- Preserve rejected records and their reasoning.
- Run only the validation commands relevant to the files touched, then report commands that were skipped and why.

## Preset matrix

| Preset | Main purpose | Primary files | Safe automation level | Required checks |
|---|---|---|---|---|
| `source-triage-agent` | Turn open sourcing questions into evidence-backed triage notes. | `shared/source-triage.control.meta`, `shared/sourced-mods.control.meta`, `shared/source-package-meta.control.meta` | Draft and annotate only; do not promote candidates. | `python tools/validate_manifests.py`, `pytest tests/test_sourced_mods.py` |
| `manifest-lint-agent` | Repair schema, naming, ordering, and convention issues reported by tooling. | `shared/*.control.meta`, `editions/*/manifests/*.control.meta` | May apply mechanical fixes that are directly implied by validation output. | `python tools/validate_manifests.py`, `pytest tests/test_validation.py tests/test_control_meta_conventions.py` |
| `modlist-regenerator` | Regenerate derived modlist markdown after manifest edits. | `editions/*/MODLIST.md`, manifest files when needed for context | Generated output only; do not hand-edit generated sections. | `python tools/generate_modlist_markdown.py`, diff review, `python tools/generate_modlist_markdown.py --check`, `python tools/validate_manifests.py` |
| `edition-drift-auditor` | Identify unintended divergence between OpenMW and MWSE editions. | `editions/openmw/**`, `editions/mwse/**`, `tools/compare_editions.py` | Report or annotate; do not force parity when divergence is intentional. | `python tools/compare_editions.py`, `python tools/check_duplicate_mods.py` |
| `documentation-sync-agent` | Keep README, roadmap, checklist, and policy references synchronized. | `README.md`, `ROADMAP.md`, `FOLLOW-UP-TASKS.md`, `editions/*/docs/*.md` | May edit prose and links; must not change project scope without explicit request. | `pytest` when tooling docs change; otherwise markdown review only. |
| `release-readiness-agent` | Prepare Wabbajack release checklist status summaries. | `editions/*/wabbajack/*.md`, `editions/*/docs/*.md`, manifests | Checklist and gap reporting only until human release review. | `python tools/validate_manifests.py`, `python tools/generate_modlist_markdown.py --check`, `pytest` |
| `wabbajack-list-planner` | Prepare evidence-backed direction for the Pilgrim and Sleeper lists. | `PROJECT-BIBLE.md`, shared and edition manifests, edition Wabbajack docs | Advisory planning only; do not accept, promote, place, or order mods. | `python tools/validate_manifests.py`, `python tools/compare_editions.py`, `python tools/check_duplicate_mods.py` when relevant |
| `wabbajack-list-writer` | Draft restrained, edition-specific Wabbajack prose. | Root and edition README files, changelogs, Wabbajack and installation docs | Draft copy only; material claims and final public wording require evidence and human review. | `python tools/validate_manifests.py` for inventory claims, `pytest` for tooling-backed docs or tests |

## Preset definitions

### `source-triage-agent`

Use this preset for sourcing backlog cleanup and provenance review.

**Inputs**
- Open blockers in `shared/source-triage.control.meta`.
- Candidate records in `shared/sourced-mods.control.meta`.
- Multi-package source details in `shared/source-package-meta.control.meta`.

**Allowed actions**
- Add evidence notes from verified, cited sources.
- Normalize candidate IDs, source confidence labels, thematic buckets, and promotion targets when the evidence is already present.
- Cross-reference multi-package sources without changing acceptance status.

**Stop conditions**
- The agent cannot verify a source identity.
- A source has unclear redistribution or package constraints.
- A candidate would need human compatibility judgment.

**Completion report**
- List each candidate touched.
- Separate verified facts from unresolved assumptions.
- State why any blocked item remains blocked.

### `manifest-lint-agent`

Use this preset when validation fails or metadata conventions drift.

**Inputs**
- Tool output from `python tools/validate_manifests.py`.
- Relevant tests under `tests/`.
- Manifest schema guidance in `shared/mod-meta-schema.md` and naming rules in `shared/naming-policy.md`.

**Allowed actions**
- Fix YAML structure, missing required fields, duplicate IDs, filename convention issues, and sort/order issues when the intended value is unambiguous.
- Add placeholder-safe values only when existing policy explicitly permits them.

**Stop conditions**
- A fix requires inventing source metadata, compatibility status, or review evidence.
- Validation output points to a design decision rather than a structural issue.

**Completion report**
- Quote the failing validation category in summary form.
- List mechanical fixes applied.
- Include before/after check results.

### `modlist-regenerator`

Use this preset after manifest changes that affect public modlist markdown.

**Inputs**
- Current manifests under `editions/*/manifests/`.
- Generator implementation in `tools/generate_modlist_markdown.py`.

**Allowed actions**
- Run the generator.
- Commit regenerated markdown when it is the expected result of manifest changes.

**Stop conditions**
- Generated output includes unexpected deletions or scope changes.
- The generator fails or emits content that contradicts manifest status.

**Completion report**
- Identify generated files changed.
- State whether changes are purely generated or accompanied by manifest edits.

### `edition-drift-auditor`

Use this preset to check whether Pilgrim and Sleeper diverged intentionally.

**Inputs**
- `tools/compare_editions.py` output.
- Edition README files and load-order policies.
- Shared design rules and the project bible.

**Allowed actions**
- Open issues or add notes for unexplained drift.
- Flag duplicate candidates, mismatched status, or cross-edition notes that lack rationale.

**Stop conditions**
- The correct fix would require deciding feature parity.
- Differences are clearly engine-specific or lore/design-specific.

**Completion report**
- Classify drift as `intentional`, `needs-review`, or `mechanical-fix-applied`.
- Preserve edition-specific rationale.

### `documentation-sync-agent`

Use this preset for keeping planning documents consistent.

**Inputs**
- Root README and contributing docs.
- `ROADMAP.md`, `FOLLOW-UP-TASKS.md`, `PROJECT-BIBLE.md`.
- Edition documentation under `editions/*/docs/`.

**Allowed actions**
- Update links, command lists, status references, and checklist wording.
- Add planning documents for new maintenance workflows.

**Stop conditions**
- A change would alter design pillars, edition identity, roadmap phase gates, or release claims.

**Completion report**
- List changed docs and the consistency issue each change resolves.
- Confirm no installability, compatibility, or release-readiness claim was added unless already evidenced.

### `release-readiness-agent`

Use this preset only for pre-release evidence gathering and checklist preparation.

**Inputs**
- Edition release checklists.
- Install, post-install, known-issues, and testing docs.
- Current validation and generation output.

**Allowed actions**
- Mark checklist items as blocked, pending, or evidence-needed.
- Prepare release-gap summaries.
- Confirm that required commands still pass.

**Stop conditions**
- Any checklist item requires a completed end-to-end install test not present in repository evidence.
- Any release note would imply an installable build before Phase 4 criteria are met.

**Completion report**
- Summarize readiness by edition.
- List blockers by severity.
- Include exact validation commands and results.

### `wabbajack-list-planner`

Use this preset for nonbinding, evidence-backed planning across the Pilgrim and Sleeper lists.

**Inputs**
- The project bible, roadmap, follow-up tasks, and shared sourcing records.
- Both edition manifests, README files, and Wabbajack planning documents.

**Allowed actions**
- Analyze category coverage and propose evaluation batches.
- Recommend edition-specific direction while preserving engine-specific differences.
- Identify sourcing, compatibility, and decision gaps without promoting candidates.

**Stop conditions**
- Candidate fit depends on unrecorded provenance or compatibility evidence.
- Edition placement, final load order, or a design preference requires human judgment.

**Completion report**
- Separate recorded facts, interpretations, recommendations, and evidence gaps.
- Report Pilgrim and Sleeper plans independently, with exact checks and skipped-check reasons.

### `wabbajack-list-writer`

Use this preset to draft Wabbajack, installation, known-issue, and release prose from recorded evidence.

**Inputs**
- Root and edition README files, changelogs, and Wabbajack documents.
- Edition installation, post-install, and known-issues documentation.

**Allowed actions**
- Draft edition descriptions, verified feature copy, installer guidance, and release notes.
- Preserve distinct Pilgrim and Sleeper voices while keeping instructions and warnings plain.
- Label unsupported language as a draft gap instead of presenting it as fact.

**Stop conditions**
- A material claim lacks repository evidence or would imply unsupported readiness.
- Final public voice, support boundaries, or project direction require human judgment.

**Completion report**
- Identify the repository source for material claims and flag claims needing review.
- Distinguish edition-specific copy and report exact checks and skipped-check reasons.

## Recommended local preset format

Local agent runners can encode each preset as YAML, JSON, or TOML. Keep the structure simple and auditable:

```yaml
name: source-triage-agent
scope:
  - ash-archive/shared/source-triage.control.meta
  - ash-archive/shared/sourced-mods.control.meta
mode: evidence-first
allowed_actions:
  - annotate_verified_sources
  - normalize_existing_metadata
forbidden_actions:
  - invent_provenance
  - promote_candidates_without_review
required_checks:
  - python tools/validate_manifests.py
  - pytest tests/test_sourced_mods.py
handoff:
  require_summary: true
  require_uncertainty_log: true
```

Preset files live outside generated content in `.agents/presets/`, with one runner-neutral YAML file per preset and a README that points back to this plan. Runnable project-scoped Codex translations live in `.codex/agents/`, with one TOML file per preset. Keep both layers synchronized whenever this policy changes.

## Committed preset files

The repository currently includes runner-neutral YAML presets under `.agents/presets/`:

- `.agents/presets/source-triage-agent.yaml`
- `.agents/presets/manifest-lint-agent.yaml`
- `.agents/presets/modlist-regenerator.yaml`
- `.agents/presets/edition-drift-auditor.yaml`
- `.agents/presets/documentation-sync-agent.yaml`
- `.agents/presets/release-readiness-agent.yaml`
- `.agents/presets/wabbajack-list-planner.yaml`
- `.agents/presets/wabbajack-list-writer.yaml`

Use `.agents/presets/README.md` as the local index for maintenance presets and this document as the policy source for guardrails and review gates.

## Runnable Codex agents

The repository includes project-scoped Codex agents under `.codex/agents/`. Codex loads
these agents when the repository is trusted, and the root `AGENTS.md` directs sessions to
the repository-wide rules. The TOML files are runner-specific translations; the YAML
presets above remain canonical.

`tests/test_repo_agents.py` verifies that every canonical preset has a matching Codex
agent and that required reading, forbidden action identifiers, and validation commands are
preserved in its instructions.

## Repo-scoped skills

Reusable workflows live under `.agents/skills/` and are available throughout the repository:

| Skill | Canonical preset |
|---|---|
| `ash-archive-triage-sources` | `source-triage-agent.yaml` |
| `ash-archive-lint-manifests` | `manifest-lint-agent.yaml` |
| `ash-archive-regenerate-modlists` | `modlist-regenerator.yaml` |
| `ash-archive-audit-edition-drift` | `edition-drift-auditor.yaml` |
| `ash-archive-sync-docs` | `documentation-sync-agent.yaml` |
| `ash-archive-assess-release` | `release-readiness-agent.yaml` |
| `ash-archive-plan-wabbajack-list` | `wabbajack-list-planner.yaml` |
| `ash-archive-write-wabbajack-copy` | `wabbajack-list-writer.yaml` |

Each skill contains concise procedural guidance and generated UI metadata. The preset remains
the policy source; a skill cannot relax its stop conditions or human review gates.

Run `python tools/lint_repo.py` to lint Python, YAML control metadata, agent TOML, and skill
metadata. `tests/test_repo_skills.py` also keeps the checked-in skill set under test.

## Automation rollout plan

1. **Document-first pass** - keep this document as the human-readable policy and preset index. **Complete.**
2. **Repo-agent configuration** - maintain runner-neutral YAML presets and project-scoped Codex TOML translations with automated consistency checks. **Complete.**
3. **Repo-skill configuration** - maintain discoverable repo workflows and lint them against their canonical presets. **Complete.**
4. **Guardrail enforcement** - keep exact preset-to-agent and preset-to-skill bindings, forbidden actions, stop conditions, and human gates under test. **Complete.**
5. **Mechanical maintenance** - permit only the file-scoped edits authorized by each canonical preset; generated output and validator-implied repairs remain reviewable. **Enabled with validation.**
6. **Evidence workflows** - permit source annotations only when evidence and uncertainty are retained; promotion and compatibility decisions remain human-gated. **Enabled with human gates.**
7. **Release workflows** - keep `release-readiness-agent` advisory-only until a human authorizes release work. **Advisory only.**

## Human review gates

Human review remains required for:

- Accepting or rejecting mods.
- Promoting candidates into edition manifests.
- Compatibility claims based on playtesting.
- Wabbajack release readiness.
- Any change that weakens the project bible, evidence standards, or edition distinction.
