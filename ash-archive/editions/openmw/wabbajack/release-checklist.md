# Pilgrim Edition release checklist

Pilgrim Edition remains in Phase 1 sourcing. Checked repository-foundation items do not imply that the edition is installable or release-ready.

## Repository foundation

- [x] Edition directory, manifest schema, and generated modlist pipeline exist.
- [x] Manifest, generated-output, drift, duplicate, lint, and test checks are available in pull-request automation.
- [x] Planning-stage installation, post-install, and known-limitations documents exist.

## Phase 1 — sourcing gate

- [ ] Major category candidate coverage is sufficient for Pilgrim Edition.
- [ ] Active candidates have verified or explicitly qualified provenance.
- [ ] Source-triage blockers affecting Pilgrim are resolved or deliberately deferred.
- [ ] Multi-package sources have reproducible child-package identities.
- [ ] Placeholder source, version, archive, and requirement fields are resolved where evidence permits.

## Phase 2 — evaluation gate

- [ ] Initial Pilgrim evaluation batches and routes are defined.
- [ ] Candidate compatibility, conflicts, performance, and mitigation are recorded.
- [ ] Accepted, rejected, and deferred decisions retain evidence and human review.
- [ ] Intentional differences from Sleeper Edition are documented.

## Phase 3 — hardening gate

- [ ] OpenMW version and configuration are pinned.
- [ ] Final mod selection, load order, and patch plan are reproducible.
- [ ] Installation and post-install instructions are tested.
- [ ] Startup, travel, weather, interior, combat, save/reload, and long-play routes pass.
- [ ] Known issues, performance expectations, and support data are documented.

## Phase 4 — release gate

- [ ] A release-candidate manifest freeze is recorded.
- [ ] Wabbajack artifact builds from the frozen inputs.
- [ ] Clean-environment installation succeeds using the public instructions.
- [ ] Generated artifacts match verified source metadata and the frozen manifest.
- [ ] Release notes, prerequisites, known issues, and support boundaries are complete.
- [ ] Human maintainer approves distribution.

Record exact evidence for every completed item. A passing repository check cannot replace an install or playtest result.
