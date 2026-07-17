## Summary

Describe what changed, why, and what intentionally did not change.

## Area affected

- [ ] Shared sourcing or policy
- [ ] Pilgrim / OpenMW
- [ ] Sleeper / MWSE
- [ ] Tooling or schema
- [ ] Documentation
- [ ] Continuous integration
- [ ] Wabbajack planning

## Evidence and uncertainty

Separate repository/tooling results from source facts and in-game evidence. List unresolved
source identity, version, archive, plugin, licensing, compatibility, and testing questions.

## Validation

Run from `ash-archive/` or explain each skipped command:

```bash
python tools/lint_repo.py
python tools/validate_manifests.py
python tools/check_duplicate_mods.py
python tools/compare_editions.py
python tools/generate_modlist_markdown.py --check
pytest
```

- Commands run and exact results:
- Commands skipped and reasons:
- Generated modlists refreshed with `python tools/generate_modlist_markdown.py` when needed:
- Generated diffs reviewed:

## Human review gates

- [ ] No unverified mod was promoted to `testing` or `accepted`.
- [ ] Any `source_reference` added is provenance-only and was not treated as promotion, acceptance, or compatibility evidence.
- [ ] Candidate and edition status changes are explained separately.
- [ ] No final load order, installability, compatibility, or release-readiness claim was added without evidence.
- [ ] OpenMW and MWSE remain sibling editions; intentional engine-specific differences were preserved.
- [ ] Generated sections were not hand-edited.
- [ ] Rejected-mod reasoning and unresolved research questions were retained.
- [ ] Project-bible exceptions, source promotion, compatibility decisions, and release decisions received human review where required.
