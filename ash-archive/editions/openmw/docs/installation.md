# Installation status — Pilgrim Edition

> Pilgrim Edition does not yet have a public Wabbajack installer or a supported manual installation procedure.

The repository currently contains planning metadata and a generated modlist preview. Those files are inputs to sourcing and evaluation; they are not a complete install recipe and should not be treated as one.

## Not yet defined

- Supported Morrowind distribution and clean-game baseline
- Pinned OpenMW version and configuration
- Verified archive identities and acquisition rules
- Final mod selection and load order
- Patch and conflict-resolution plan
- Wabbajack build and clean-machine installation evidence
- Hardware, storage, and support requirements

## Current developer workflow

Repository contributors can validate the planning data from `ash-archive/`:

```bash
python tools/validate_manifests.py
python tools/generate_modlist_markdown.py
python tools/compare_editions.py
python tools/check_duplicate_mods.py
```

These commands validate repository structure only. They do not install or launch Morrowind.

## Publication gate

Installation instructions should be written only after Phase 3 produces a reproducible Pilgrim configuration and Phase 4 records successful clean-environment Wabbajack installs. Until then, use the [generated modlist](../MODLIST.md) only as a planning preview and consult the [release checklist](../wabbajack/release-checklist.md) for blockers.
