# Installation status — Sleeper Edition

> Sleeper Edition does not yet have a public Wabbajack installer or a supported manual installation procedure.

The repository currently contains planning metadata, a generated modlist preview, and preliminary Mod Organizer 2 notes. These are not a complete install recipe or production profile.

## Planned engine and tool stack

- Classic Morrowind
- Morrowind Code Patch
- MGE XE
- MWSE
- Mod Organizer 2

The exact versions, acquisition paths, configuration, and compatibility constraints remain to be verified and pinned.

## Mod Organizer 2 planning

MO2 is recorded as a planned external tool in [`manifests/external-tools.control.meta`](../manifests/external-tools.control.meta). The current [setup notes](../mod-organizer-2/setup-notes.md) and [profile notes](../mod-organizer-2/profile-notes.md) deliberately avoid claiming a production configuration.

Internal repository `.control.meta` files are not native MO2 download sidecars. Native sidecar data must be imported from verified MO2 artifacts; see the [metadata distinction](../../../shared/mo2-download-meta-sidecars.md).

## Not yet defined

- Supported Morrowind distribution and clean-game baseline
- Pinned MCP, MGE XE, MWSE, and MO2 versions
- Verified archive identities and acquisition rules
- Production MO2 profile and executable configuration
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

Installation instructions should be finalized only after Phase 3 produces a reproducible Sleeper configuration and Phase 4 records successful clean-environment Wabbajack installs. Until then, use the [generated modlist](../MODLIST.md) only as a planning preview and consult the [release checklist](../wabbajack/release-checklist.md) for blockers.
