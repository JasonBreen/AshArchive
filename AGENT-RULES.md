# Agent rules

These rules apply to Codex, Copilot, Claude, and other AI assistants contributing to Ash Archive.

## Required workflow

1. Follow the repository guidance in `AGENTS.md` and read `ash-archive/PROJECT-BIBLE.md` plus the affected edition or shared documentation.
2. Work on a dedicated branch and submit changes through a pull request.
3. Keep the task small, focused, and limited to the requested scope.
4. Select the narrowest applicable preset in `ash-archive/LOCAL-AGENT-PRESETS.md` and matching workflow under `.agents/skills/`.
5. Treat `.agents/presets/` as canonical policy; `.codex/agents/` and `.agents/skills/` may not relax preset stop conditions or review gates.
6. Document uncertainty instead of guessing.
7. Run relevant validation before opening or updating a pull request and report skipped checks with reasons.
8. Update affected changelogs and status documentation when the repository's capabilities or milestone state changes.

## Human decisions

AI assistants may gather evidence, prepare drafts, and apply mechanical changes within documented policy. Human review remains required for:

- accepting or rejecting mods;
- promoting candidates into edition manifests;
- compatibility and playtesting claims;
- final load order, patch strategy, and edition-parity decisions;
- public wording that changes support boundaries;
- Wabbajack release readiness; and
- exceptions to the project bible.

Do not use delegation, a different preset, or a different tool to bypass a stop condition.

## Repository direction

1. Preserve the two-edition model:
   - **Pilgrim Edition** — OpenMW
   - **Sleeper Edition** — classic Morrowind with MCP, MGE XE, and MWSE
2. Do not collapse both editions into one shared load order or one undifferentiated voice.
3. Preserve Morrowind-native psychological horror and the evidence-before-explanation principle.
4. Do not remove or weaken constraints in `ash-archive/PROJECT-BIBLE.md` without explicit human approval.
5. Do not imply that the planning repository is an installable or playable release.

## Data integrity

1. Do not invent URLs, Nexus IDs, archive names, versions, file sizes, hashes, requirements, licenses, test results, or compatibility evidence.
2. Do not mark mods as accepted or tested without the review and evidence required by repository policy.
3. Preserve rejected records and their reasoning.
4. Treat YAML-formatted `.control.meta` files as internal control metadata, not MO2 download sidecars.
5. Import native MO2 `.meta` data only from verified source artifacts; do not synthesize it from incomplete inventory data.
6. Do not hand-edit generated `MODLIST.md` sections; run the generator and inspect its diff.

## Content boundaries

1. No direct horror-franchise crossover content.
2. No Skyrimification, anime face replacers, or generic jump-scare design.
3. Do not add convenience fast travel without explicit design review.
4. Do not add survival systems without configuration, compatibility, and testing plans.
5. Do not obscure requirements, warnings, or known limitations for atmosphere.

## Validation

From `ash-archive/`, run the checks relevant to the change:

```bash
python tools/lint_repo.py
python tools/validate_manifests.py
python tools/generate_modlist_markdown.py
python tools/compare_editions.py
python tools/check_duplicate_mods.py
python tools/summarize_sourced_mods.py
pytest
```

Pull requests to `main` also run repository and archive-integrity workflows. Passing automation proves structural consistency only; it does not prove in-game compatibility, installability, or release readiness.
