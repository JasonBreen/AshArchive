# Sleeper Edition release checklist

Sleeper Edition remains in Phase 1 sourcing. Checked repository-foundation items do not imply that the edition is installable or release-ready.

## Repository foundation

- [x] Edition directory, manifest schema, and generated modlist pipeline exist.
- [x] Mod Organizer 2 is recorded as planned external tooling with preliminary setup and profile notes.
- [x] Manifest, generated-output, drift, duplicate, lint, and test checks are available in pull-request automation.
- [x] Planning-stage installation, post-install, and known-limitations documents exist.

## Phase 1 — sourcing gate

- [ ] Major category candidate coverage is sufficient for Sleeper Edition.
- [ ] Active candidates have verified or explicitly qualified provenance.
- [ ] Source-triage blockers affecting Sleeper are resolved or deliberately deferred.
- [ ] Multi-package sources have reproducible child-package identities.
- [ ] Placeholder source, version, archive, and requirement fields are resolved where evidence permits.

## Phase 2 — evaluation gate

- [ ] Initial Sleeper evaluation batches and routes are defined.
- [ ] Candidate compatibility, script conflicts, performance, balance, and mitigation are recorded.
- [ ] Dream, sleep, survival, and body-pressure systems have explicit configuration and interaction tests.
- [ ] Accepted, rejected, and deferred decisions retain evidence and human review.
- [ ] Intentional differences from Pilgrim Edition are documented.

## Phase 3 — hardening gate

- [ ] MCP, MGE XE, MWSE, and MO2 versions and configuration are pinned.
- [ ] A production MO2 profile, executable set, final load order, and patch plan are reproducible.
- [ ] Installation and post-install instructions are tested.
- [ ] Startup, dream/sleep, travel, scripted-event, combat, save/reload, performance, and long-play routes pass.
- [ ] Known issues, performance expectations, and support data are documented.

## Phase 4 — release gate

- [ ] A release-candidate manifest and MO2 profile freeze are recorded.
- [ ] Wabbajack artifact builds from the frozen inputs.
- [ ] Clean-environment installation succeeds using the public instructions.
- [ ] Generated artifacts match verified source metadata and the frozen manifest.
- [ ] Release notes, prerequisites, known issues, and support boundaries are complete.
- [ ] Human maintainer approves distribution.

Record exact evidence for every completed item. A passing repository check cannot replace an install or playtest result.
