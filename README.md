# The Dream Is The Door

**The Dream Is The Door** is a dual-edition Morrowind Wabbajack modlist built around psychological horror native to Vvardenfell. The project is contained in the [`ash-archive`](ash-archive/) sub-directory and ships as two sibling editions that share aesthetic pillars and narrative logic while using engine-specific techniques.

---

## Editions

| Edition | Engine | Tagline |
|---|---|---|
| **Ash Archive: Pilgrim Edition** | OpenMW | *The island remembers.* |
| **Ash Archive: Sleeper Edition** | Classic Morrowind + MCP + MGE XE + MWSE | *The dream notices you.* |

**Pilgrim Edition** is stable, atmospheric, and long-play-focused. It emphasises weather, distance, documents, tomb architecture, and retrospective dread through environmental pressure.

**Sleeper Edition** is script-heavy and reactive. It uses MWSE to deliver dream contamination, identity fracture, and sleep-state horror through event timing and ritual repetition.

---

## Design pillars

- **The Island Remembers** — Vvardenfell is already haunted by prophecy, reincarnation, and suppressed history.
- **The Dream is Geological** — dread accumulates in strata, not moments.
- **Reincarnation is Body Horror** — the Nerevarine arc treated as violation, not triumph.
- **Dagoth Ur is Intimate, Not Loud** — the antagonist as contamination, not spectacle.
- **The Tribunal Are the Beautiful Crime Scene** — divinity as cover-up.
- **Evidence Before Explanation** — logs, notes, shrines, and rumours foreshadow; nothing is explained twice.

Horror emerges from Morrowind's own systems and lore. No horror-franchise crossover content, no generic jump scares, no Skyrimification.

---

## Current status

> **Planning and scaffold only.** The list is not yet installable, not yet playable, and does not define a final load order.

See [ROADMAP.md](ash-archive/ROADMAP.md) for the phased plan and [CHANGELOG.md](ash-archive/CHANGELOG.md) for version history.

---

## Repository structure

```
TheDreamIsTheDoor/
└── ash-archive/              # Main project root
    ├── editions/
    │   ├── openmw/           # Pilgrim Edition manifests and docs
    │   └── mwse/             # Sleeper Edition manifests and docs
    ├── shared/               # Categories, design rules, evaluation rubric
    ├── tools/                # Python validation and generation scripts
    ├── PROJECT-BIBLE.md      # Full design philosophy and horror translation notes
    ├── ROADMAP.md
    └── CHANGELOG.md
```

---

## Tooling quick start

All commands are run from inside `ash-archive/`.

```bash
# Validate manifests
python tools/validate_manifests.py

# Generate modlist markdown
python tools/generate_modlist_markdown.py

# Compare editions
python tools/compare_editions.py
```

---

## Documentation

- [Project Bible](ash-archive/PROJECT-BIBLE.md) — thesis, dual-edition philosophy, horror translation notes, and core atmosphere rules
- [Roadmap](ash-archive/ROADMAP.md) — development phases from scaffold to Wabbajack release
- [Pilgrim Edition](ash-archive/editions/openmw/README.md) — OpenMW edition identity and scope
- [Sleeper Edition](ash-archive/editions/mwse/README.md) — MWSE edition identity and scope
- [Changelog](ash-archive/CHANGELOG.md)

---

## License

See [LICENSE.md](ash-archive/LICENSE.md).
