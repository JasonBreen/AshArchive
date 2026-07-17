# Ash Archive Codex Agents

These TOML files make the runner-neutral presets in `.agents/presets/` available as
project-scoped Codex agents. Codex discovers them when this repository is trusted.

The YAML preset with the same stem is the canonical policy source. Keep the TOML agent
instructions synchronized with its scope, required reading, forbidden actions, checks,
stop conditions, handoff requirements, and human review gates.

Available agents:

- `source-triage-agent`
- `manifest-lint-agent`
- `modlist-regenerator`
- `edition-drift-auditor`
- `documentation-sync-agent`
- `wabbajack-list-planner`
- `wabbajack-list-writer`
- `release-readiness-agent`

Use these agents for focused delegation. They do not replace the repository-wide rules in
`AGENTS.md`, `AGENT-RULES.md`, or `ash-archive/PROJECT-BIBLE.md`.
