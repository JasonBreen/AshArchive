# Ash Archive

Ash Archive is a control repository for a dual-edition Morrowind Wabbajack project built around Morrowind-native psychological horror design.

## Editions
- **Ash Archive: Pilgrim Edition** (OpenMW) — *The island remembers.*
- **Ash Archive: Sleeper Edition** (classic Morrowind + MCP + MGE XE + MWSE) — *The dream notices you.*

## Current status
This repository is **planning and scaffold only**. It is not yet a final Wabbajack installer, not yet playable, and does not define a final load order.

## Tooling quick start
From `ash-archive/`:

- Validate manifests:
  - `python tools/validate_manifests.py`
- Generate modlist markdown:
  - `python tools/generate_modlist_markdown.py`
- Compare editions:
  - `python tools/compare_editions.py`
