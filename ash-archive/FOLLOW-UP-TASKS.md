# Follow-up Tasks

This list tracks remaining work for **Phase 1 - Sourcing** and preparation for
**Phase 2 - Evaluation**. Repository hardening does not clear source, compatibility, or
in-game testing blockers.

## Source triage gate

- [ ] Resolve every blocking question in `shared/source-triage.control.meta`.
- [ ] Decide whether official plugins and DLC are baseline requirements, manual-only
  prerequisites, or source-tracked candidates.
- [ ] Identify canonical sources, package identities, and distribution constraints for
  `source unknown`, Nexus ID `0`, and unmanaged entries.
- [ ] Keep blocked entries unverified until identity, source, and licensing questions are resolved.
- [ ] Close `source_triage.triage_status` only after every promotion-gate blocker is resolved.

## Candidate intake expansion

- [ ] Expand `shared/sourced-mods.control.meta` beyond the current dream, blight, and survival groups.
- [ ] Add candidates for foundation, preservation, architecture, soundscape, UI/journal,
  faith/Temple, and other underrepresented categories.
- [ ] Record stable IDs, primary source URLs, evidence notes, source confidence,
  compatibility status, thematic bucket, promotion target, risk, and engine uncertainty.
- [ ] Keep compatibility `unverified` or `needs-testing` unless reliable documentation or
  recorded test evidence supports a stronger value.
- [ ] Retain rejected and superseded candidates with explicit reasoning.

## Source-to-manifest links

- [ ] Add `source_reference` only where an edition entry and canonical candidate represent
  the same mod identity and intended edition.
- [ ] Keep `related_manifest_ids` synchronized with manifest links.
- [ ] Do not interpret a source link as candidate promotion, edition acceptance, or testing.
- [ ] Leave edition-specific version, archive, plugin, patch, conflict, and load-order facts
  blank or explicitly unknown until evidence exists.
- [ ] Resolve any remaining manifest candidates that have trustworthy repository-recorded
  provenance but no canonical source record.

## Multi-package source metadata

- [ ] Audit `shared/source-package-meta.control.meta` for source pages with multiple installable packages.
- [ ] Confirm each package's identity, variant, artifact evidence, edition notes, and plugin list.
- [ ] Use child `package_version` only when it differs from the verified parent `base_version`.
- [ ] Distinguish imported local-path evidence from a portable, verified archive identity.

## Phase 2 evaluation preparation

- [ ] Define the first evaluation batches by category and route.
- [ ] Start with high-impact Sixth House/dream, blight/ambience, and MWSE body-pressure candidates.
- [ ] Expand `shared/mod-evaluation-rubric.md` with maintainer-approved weighting or decision thresholds if needed.
- [ ] Record compatibility, conflicts, mitigations, performance, and edition-specific behavior.
- [ ] Keep candidate promotion and edition status advancement as separate human-review decisions.
- [ ] Preserve intentional OpenMW/MWSE differences rather than forcing feature parity.

## Edition evidence and documentation

- [ ] Build the first reproducible Pilgrim installation before replacing its blocked installation/post-install pages.
- [ ] Build the first reproducible Sleeper installation before replacing its blocked installation/post-install pages.
- [ ] Define and execute edition-specific load-order, performance, and test-route evidence.
- [ ] Populate known issues from observed builds; an empty issue list is not evidence of zero issues.
- [ ] Record compiler inputs and clean-install results before checking any release-readiness item.

## Maintainer decisions

- [ ] Resolve the conflict between the root CC0 `LICENSE` and the incomplete nested MIT `LICENSE.md`.
- [ ] Confirm a private security-reporting channel and update `SECURITY.md` with it.
- [ ] Approve any candidate promotion, compatibility conclusion, edition acceptance, final
  load order, design-bible exception, or release-readiness decision.

## Validation checklist

Run from `ash-archive/` after each applicable batch:

- [ ] `python tools/lint_repo.py`
- [ ] `python tools/validate_manifests.py`
- [ ] `python tools/check_duplicate_mods.py` after adding or renaming manifest entries
- [ ] `python tools/compare_editions.py` after cross-edition changes
- [ ] `python tools/generate_modlist_markdown.py` after manifest changes, followed by diff review
- [ ] `python tools/generate_modlist_markdown.py --check`
- [ ] `pytest` before opening or updating a pull request

Use `python tools/summarize_sourced_mods.py` as a read-only intake report when reviewing
candidate coverage; it is not a compatibility check.
