# Follow-up Tasks

This checklist tracks the immediate work needed to finish **Phase 1 — Sourcing** and prepare Ash Archive for **Phase 2 — Evaluation**.

## Repository maintenance foundation

The control-repository work needed to support the sourcing milestone is complete:

- [x] Standardize internal YAML control metadata on the `.control.meta` filename convention.
- [x] Add schema, naming, generation, duplicate, drift, and repository-lint checks.
- [x] Add runner-neutral maintenance presets with matching Codex agents and reusable repository skills.
- [x] Add pull-request workflows for repository checks and archive integrity.
- [x] Make editable dependency installation work for the metadata-only control project.

These checks protect repository consistency; they are not substitutes for mod compatibility testing or end-to-end game installation.

## Milestone target: Phase 1 sourcing exit

Phase 1 is complete when candidate pools cover the major needs of both editions, validation passes cleanly, and every active candidate has provenance, confidence, and decision notes.

### Source triage gate

- [ ] Resolve every open blocking question in `shared/source-triage.control.meta`.
- [ ] Decide whether official plugins and DLC entries are baseline requirements, manual-only prerequisites, or source-tracked candidates.
- [ ] Identify canonical sources, package identities, and distribution constraints for `source unknown` and Nexus ID `0` entries.
- [ ] Keep blocked entries `unverified` until package identity, source, and licensing questions are resolved.
- [ ] Close `source_triage.triage_status` only after all promotion-gate blockers are resolved.

### Candidate intake expansion

- [ ] Expand `shared/sourced-mods.control.meta` beyond the current dream, blight, and survival buckets.
- [ ] Add candidates for underrepresented categories, especially foundation, preservation, architecture, soundscape, UI/journal, and faith/Temple themes.
- [ ] Record a stable kebab-case ID, source URL, evidence notes, source confidence, compatibility status, thematic bucket, promotion target, risk level, and engine notes for every new candidate.
- [ ] Leave compatibility as `unverified` or `needs-testing` unless repository evidence supports a stronger state.
- [ ] Retain rejected candidates with explicit reasoning instead of deleting them.

### Multi-package source metadata

- [ ] Audit `shared/source-package-meta.control.meta` for sources that require child package records.
- [ ] Confirm each package has a reproducible install artifact, variant name, edition notes, and plugin list.
- [ ] Add child `package_version` values when a package differs from its parent `base_version`.
- [ ] Remove local absolute paths from install-artifact records only after a verified portable archive identity is available.
- [ ] Keep parent source metadata stable when only one child package version diverges.

### Phase 2 evaluation preparation

- [ ] Define the first evaluation batches by category and test route.
- [ ] Start with high-impact horror candidates: Sixth House/dream, blight/ambience, and MWSE survival/body-pressure candidates.
- [ ] Create a repeatable evidence format for compatibility, conflicts, mitigation, performance, and edition-specific behavior.
- [ ] Do not promote candidates into edition manifests until human review confirms the evaluation evidence.
- [ ] Preserve intentional OpenMW/MWSE differences rather than forcing feature parity.

### Placeholder manifest cleanup

- [ ] Replace `source: "tbd"` and empty source, version, archive, or requirement fields only when verified provenance exists.
- [ ] Update patch, testing, requirement, conflict, and load-order notes as evaluation evidence becomes available.
- [ ] Keep placeholder entries marked `planned` until they have enough evidence to advance.
- [ ] Regenerate modlist markdown after manifest updates.

### Milestone validation

Run from `ash-archive/` before proposing Phase 1 completion:

- [ ] `python tools/lint_repo.py`
- [ ] `python tools/validate_manifests.py`
- [ ] `python tools/generate_modlist_markdown.py`
- [ ] Confirm generated modlists have no unexplained diff.
- [ ] `python tools/compare_editions.py`
- [ ] `python tools/check_duplicate_mods.py`
- [ ] `python tools/summarize_sourced_mods.py`
- [ ] `pytest`

Record the exact results and any skipped check in the milestone pull request.
