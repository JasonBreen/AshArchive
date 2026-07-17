# Repository Agent Guidance

Read and follow [`AGENT-RULES.md`](AGENT-RULES.md) before making changes in this
repository. For work under `ash-archive/`, also read
[`ash-archive/PROJECT-BIBLE.md`](ash-archive/PROJECT-BIBLE.md) and the documentation
for the affected edition or shared subsystem.

Repo-scoped Codex agents live in `.codex/agents/`. Their canonical scopes, guardrails,
checks, stop conditions, and human review gates are the runner-neutral YAML presets in
`.agents/presets/` and the policy in `ash-archive/LOCAL-AGENT-PRESETS.md`.

When delegating work:

- Choose the narrowest agent whose documented scope covers the task.
- Keep acceptance, compatibility, release-readiness, edition-parity, and design decisions
  with a human reviewer.
- Do not use an agent to bypass a preset stop condition or forbidden action.
- Require each agent to report validation it ran and explain any skipped check.
