# MO2 Download `.meta` Sidecars vs Internal Control Metadata

## Separation of artifact types

- MO2/Wabbajack download `.meta` sidecars are a **separate artifact class** from internal project metadata.
- Internal `.control.meta` files are YAML-formatted **internal control metadata** used by repository tooling and are **not MO2 download sidecars**.

## Source of native sidecars

- Native MO2 download sidecar `.meta` files should be imported from a real Mod Organizer 2 downloads directory when available.
- Do **not** synthesize native MO2 `.meta` files unless the exact required fields are known and verified.

## Data integrity guardrails

- Do **not** invent Nexus file IDs, archive hashes, file sizes, or other download metadata.
- `modlist.txt` is a source inventory, **not** a complete source of MO2 download sidecar metadata.
- Disabled rows in `modlist.txt` are evidence and must remain preserved.
