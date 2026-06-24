# Follow-up Tasks

This task list tracks the immediate work needed to finish **Phase 1 - Sourcing** and prepare the project for **Phase 2 - Evaluation**.

## Milestone target: Phase 1 sourcing exit

Phase 1 is complete when candidate pools are sufficiently populated across major categories for both editions, validation passes cleanly, and all active candidates have provenance plus decision notes.

### Source triage gate

- [ ] Resolve every open blocking question in `shared/source-triage.control.meta`.
- [ ] Decide whether official plugins and DLC entries are baseline requirements, manual-only prerequisites, or source-tracked candidates.
- [ ] Identify canonical sources, package identities, and distribution constraints for `source unknown` and Nexus ID `0` entries.
- [ ] Keep blocked entries `unverified` until package identity, source, and licensing questions are resolved.
- [ ] Close `source_triage.triage_status` only after all promotion-gate blockers are resolved.

### Candidate intake expansion

- [ ] Expand `shared/sourced-mods.control.meta` beyond the current dream, blight, and survival buckets.
- [ ] Add candidates for underrepresented major categories in both editions, especially foundation, preservation, architecture, soundscape, UI/journal, and faith/Temple themes.
- [ ] Record stable kebab-case IDs, source URLs, evidence notes, source confidence, compatibility status, thematic bucket, promotion target, risk level, and engine notes for each new candidate.
- [ ] Leave compatibility as `unverified` or `needs-testing` unless there is documented test evidence or reliable upstream documentation.
- [ ] Retain rejected candidates with explicit rejection reasoning instead of deleting them.

### Multi-package source metadata

- [ ] Audit `shared/source-package-meta.control.meta` for multi-package sources that need child package records.
- [ ] Confirm each package has an install artifact, variant name, edition notes, and plugin list.
- [ ] Add child `package_version` values when a package differs from the parent `base_version`.
- [ ] Keep parent source metadata stable when only one child package version diverges.

### Phase 2 evaluation preparation

- [ ] Define the first evaluation batches by category and test route.
- [ ] Start with high-impact horror candidates: Sixth House/dream, blight/ambience, and MWSE survival/body-pressure candidates.
- [ ] Prepare evaluation notes for compatibility, conflicts, mitigation paths, and edition-specific behavior.
- [ ] Do not promote candidates into edition manifests until human review confirms the evaluation evidence.
- [ ] Preserve intentional OpenMW/MWSE differences rather than forcing feature parity.

### Placeholder manifest cleanup

- [ ] Replace `source: "tbd"` and empty source/version/archive fields only when verified provenance exists.
- [ ] Update patch notes, testing notes, requirements, conflicts, and load-order notes as evaluation evidence becomes available.
- [ ] Keep placeholder entries marked `planned` until they have enough evidence to advance.
- [ ] Regenerate modlist markdown after manifest updates.

### Validation checklist

- [ ] Run `python tools/validate_manifests.py` after each metadata batch.
- [ ] Run `python tools/generate_modlist_markdown.py` after manifest changes.
- [ ] Run `python tools/compare_editions.py` after cross-edition status changes.
- [ ] Run `python tools/check_duplicate_mods.py` after adding or renaming candidates.
- [ ] Run `pytest` before opening milestone-completion PRs.

