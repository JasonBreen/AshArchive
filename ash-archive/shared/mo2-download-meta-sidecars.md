# MO2 Download `.meta` Sidecars vs Internal Control Metadata

## Separate artifact classes

- Native MO2/Wabbajack download `.meta` sidecars belong to downloaded archives and use the
  format expected by Mod Organizer 2.
- Repository `.control.meta` files are YAML internal control data used by Ash Archive tools;
  they are not MO2 download sidecars.
- Renaming or serializing internal YAML as `.meta` does not make it a native MO2 sidecar.

## Native sidecar evidence

Import native sidecars from a real MO2 downloads directory only when the exact artifact and
fields are available. Do not synthesize Nexus file IDs, hashes, file sizes, archive names, or
other download metadata.

The repository-root [`modlist.txt`](../../modlist.txt) is an imported inventory snapshot. It
is not a complete source of native sidecar data, and disabled rows remain evidence rather
than deletion candidates. Local paths recorded in imported metadata describe the snapshot;
they are not portable acquisition instructions or verified archive identities.

See [`mod-meta-schema.md`](mod-meta-schema.md) for internal field ownership.
