## Summary

Describe what changed and why.

## Edition affected
- [ ] Shared
- [ ] Pilgrim / OpenMW
- [ ] Sleeper / MWSE
- [ ] Tooling
- [ ] Documentation only

## Type of change
- [ ] Documentation
- [ ] Manifest/schema
- [ ] Tooling
- [ ] Mod sourcing
- [ ] Wabbajack planning
- [ ] Testing
- [ ] CI
- [ ] Other

## Validation

```bash
cd ash-archive
python tools/validate_manifests.py
python tools/generate_modlist_markdown.py
python tools/compare_editions.py
python tools/check_duplicate_mods.py
pytest
```

## Notes on uncertainty / evidence

Document unknowns, assumptions, and missing evidence explicitly.

## Design constraints check

- [ ] I did not collapse OpenMW and MWSE into one load order.
- [ ] I did not invent mod URLs, versions, archive names, or test results.
- [ ] I did not claim compatibility testing without documented evidence.
- [ ] I preserved project design constraints and did not weaken `ash-archive/PROJECT-BIBLE.md`.
- [ ] I did not manually overwrite generated sections.
