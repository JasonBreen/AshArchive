# `.control.meta` File Schema for `modlist.txt` Conversion

This document defines the canonical schema for per-mod metadata files in this repository.

## Purpose

Internal control metadata `.control.meta` files provide deterministic, machine-readable metadata converted from `modlist.txt` rows and augmented with project triage fields. These internal control records are **not MO2 download sidecars** and must not be treated as native MO2/Wabbajack download metadata.

## File format and naming

- Content format: YAML-structured metadata documents.
- File-extension convention in this repository: `.meta` (this schema specifically uses `.control.meta`).
- Naming pattern: `<slug>-<source_id>.control.meta`
  - For Nexus-backed rows, `source_id` is the numeric `nexus_id`.
  - For non-Nexus rows (`Unmanaged:*`, `DLC:*`, and rows without a Nexus ID), use `local`.

Examples:

- `the-dream-is-the-door-47423.control.meta`
- `beware-the-sixth-house-46036.control.meta`
- `unmanaged-siege-at-firemoth-local.control.meta`
- `dlc-tribunal-local.control.meta`

## Slug normalization rules

Build `<slug>` from `mod_name` using the following deterministic normalization:

1. Trim leading/trailing whitespace.
2. Convert to lowercase.
3. Convert apostrophes (`'`, `’`) to nothing.
4. Convert underscores (`_`) and all whitespace runs to a single hyphen (`-`).
5. Convert any punctuation other than hyphen to a separator, then collapse repeated separators to one hyphen.
6. Remove leading/trailing hyphens.

### Normalization examples

- `Skies .IV` -> `skies-iv`
- `Starfire's npc Additions - Danae's Edits and Fixes` -> `starfires-npc-additions-danaes-edits-and-fixes`
- `Better_Clothes` -> `better-clothes`

## Canonical schema

Each file must contain the following top-level keys:

```yaml
schema_version: 1
slug: string
kind: nexus | unmanaged | dlc | local
source:
  mod_name: string
  nexus_id: integer | null
  nexus_url: string
  archive_filename: string
  version: string
  install_date: string   # ISO-8601 UTC preferred, e.g. 2025-03-25T19:19:53Z
  status: enabled | disabled
project:
  edition_target: openmw | mwse | both | undecided
  category: string
  confidence: low | medium | high
  notes: string
```

## `kind` semantics and unmanaged representation

Use `kind` to distinguish rows with different source guarantees:

- `nexus`: Standard Nexus-backed row (`nexus_id > 0` and non-empty Nexus URL).
- `unmanaged`: Row where `mod_name` starts with `Unmanaged:`.
- `dlc`: Row where `mod_name` starts with `DLC:`.
- `local`: Any non-Nexus row that is neither `Unmanaged:` nor `DLC:`.

### Differences from Nexus-backed entries

For `unmanaged`, `dlc`, and `local` rows:

- `source.nexus_id` must be `null`.
- `source.nexus_url` is `""`.
- `source.archive_filename` may be empty when not available.
- `source.version` should preserve `modlist.txt` value; if absent, use `""`.

For `nexus` rows:

- `source.nexus_id` must be the numeric ID from `modlist.txt`.
- `source.nexus_url` should be the direct Nexus mod URL from `modlist.txt`.

## Field mapping table (`modlist.txt` -> `.control.meta`)

| `modlist.txt` column | `.control.meta` target | Mapping rule |
|---|---|---|
| `#Mod_Name` | `source.mod_name` | Copy as-is. |
| `#Nexus_ID` | `source.nexus_id` | If value > 0, copy integer; otherwise `null`. |
| `#Mod_Nexus_URL` | `source.nexus_url` | Copy as-is; empty for non-Nexus rows. |
| `#Download_File_Name` | `source.archive_filename` | Copy as-is (full path allowed). |
| `#Mod_Version` | `source.version` | Copy as-is. |
| `#Install_Date` | `source.install_date` | Convert `YYYY/MM/DD HH:MM:SS` to ISO-8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`) when possible. |
| `#Mod_Status` | `source.status` | `+` -> `enabled`; `-` -> `disabled`. |
| `#Primary_Category` | `project.category` | Copy category text; if empty, use `uncategorized`. |
| *(derived)* | `slug` | Normalize from `source.mod_name` using slug rules above. |
| *(derived)* | `kind` | `Unmanaged:*` -> `unmanaged`; `DLC:*` -> `dlc`; Nexus-backed -> `nexus`; else `local`. |
| *(project input)* | `project.edition_target` | Required manual/project classification. |
| *(project input)* | `project.confidence` | Required manual/project confidence (`low|medium|high`). |
| *(project input)* | `project.notes` | Required manual/project notes. |

## Minimal examples

### Nexus-backed entry

```yaml
schema_version: 1
slug: the-dream-is-the-door
kind: nexus
source:
  mod_name: The Dream is the Door
  nexus_id: 47423
  nexus_url: https://www.nexusmods.com/morrowind/mods/47423
  archive_filename: The Dream is the Door-47423-1-3-1655842474.7z
  version: 1.3.0.0
  install_date: 2025-03-29T12:59:31Z
  status: enabled
project:
  edition_target: both
  category: Immersion
  confidence: medium
  notes: Candidate aligns with dream pillar; pending in-engine verification.
```

### Unmanaged entry

```yaml
schema_version: 1
slug: unmanaged-siege-at-firemoth
kind: unmanaged
source:
  mod_name: "Unmanaged: Siege at Firemoth"
  nexus_id: null
  nexus_url: ""
  archive_filename: ""
  version: ""
  install_date: 2026-01-13T23:38:37Z
  status: enabled
project:
  edition_target: undecided
  category: uncategorized
  confidence: low
  notes: Base content not sourced from Nexus row metadata.
```
