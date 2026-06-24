# Mod Evaluation Rubric

Use this rubric during Phase 2 evaluation before any promotion into edition manifests.

## Scoring scale

- **3 (strong):** clear fit with low unresolved risk
- **2 (moderate):** workable but needs mitigation/testing depth
- **1 (weak):** high uncertainty or notable design/technical mismatch

## Rubric dimensions

1. **Atmosphere and thematic fit**
   - Aligns with Ash Archive pillars and target thematic bucket
   - Reinforces dread through Morrowind-native systems/lore
2. **Technical stability**
   - Installs cleanly in target edition(s)
   - No repeatable crashes, quest blockers, or severe regressions
3. **Conflict profile**
   - Known incompatibilities are documented
   - Conflict surface is manageable with current stack
4. **Mitigation viability**
   - Practical mitigation path exists (patch/load-order/configuration)
   - Mitigation does not create disproportionate maintenance burden
5. **Edition behavior clarity**
   - OpenMW/MWSE behavior differences are documented
   - Promotion target remains explicit (`openmw`, `mwse`, `both`, `neither`, `undecided`)

## Decision guardrails

- Hold candidate as `unverified` or `needs-testing` until evidence is complete.
- Do not promote to edition manifests without human review of evaluation notes.
- Preserve intentional OpenMW/MWSE differences; avoid forced parity.

## Evaluation note template (required fields)

- Candidate ID and tested version/package
- Test route(s) used
- Compatibility result by edition
- Conflict findings
- Mitigation plan and residual risk
- Recommendation (`hold`, `promote-openmw`, `promote-mwse`, `promote-both`, `reject`)
