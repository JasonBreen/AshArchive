# `.meta` Creation Wave Checklist

This checklist tracks staged `.meta` creation across sourced candidates.

## Global completion definition

A row can be marked complete for a wave only when all acceptance criteria below are met:

- [ ] Required fields complete
- [ ] Edition target assigned
- [ ] Source confidence assigned
- [ ] Status set (`planned`, `candidate`, or other approved workflow status)

---

## Wave 1 — Fast / High-Certainty

**Scope:** active Nexus-backed mods with a clear category and unique source.

### Intake filter

- [ ] Mod appears active on Nexus (or is represented by a currently valid Nexus page)
- [ ] Category mapping is unambiguous
- [ ] Source record is unique (no duplicate source identity across intake)

### Acceptance criteria (Wave 1)

- [ ] Required fields complete
- [ ] Edition target assigned
- [ ] Source confidence assigned
- [ ] Status set (`planned`, `candidate`, or other approved workflow status)

### Progress checklist

- [ ] Build Wave 1 candidate list
- [ ] Create `.meta` files for all Wave 1 rows
- [ ] Run QA pass for schema/field completeness
- [ ] Mark Wave 1 complete

---

## Wave 2 — Structured Families

**Scope:** repeated Nexus-ID groups (multi-package parents/children).

### Intake filter

- [ ] Grouped by shared Nexus identifier or explicit parent/child relationship
- [ ] Parent package identified
- [ ] Child packages mapped with relationship notes

### Acceptance criteria (Wave 2)

- [ ] Required fields complete
- [ ] Edition target assigned
- [ ] Source confidence assigned
- [ ] Status set (`planned`, `candidate`, or other approved workflow status)

### Progress checklist

- [ ] Build Wave 2 family map
- [ ] Resolve parent/child naming and linkage conventions
- [ ] Create `.meta` files for all Wave 2 rows
- [ ] Run QA pass for family consistency and schema/field completeness
- [ ] Mark Wave 2 complete

---

## Wave 3 — Manual Triage

**Scope:** unmanaged/local/blank-category items and ambiguous naming rows.

### Intake filter

- [ ] Marked unmanaged/local OR missing category
- [ ] Ambiguous naming requires manual resolution
- [ ] Missing/low-confidence source details captured for review

### Acceptance criteria (Wave 3)

- [ ] Required fields complete
- [ ] Edition target assigned
- [ ] Source confidence assigned
- [ ] Status set (`planned`, `candidate`, or other approved workflow status)

### Progress checklist

- [ ] Build Wave 3 triage queue
- [ ] Resolve ambiguous names and normalize IDs
- [ ] Research and annotate source evidence for low-confidence rows
- [ ] Create `.meta` files for all Wave 3 rows
- [ ] Run QA pass for schema/field completeness and triage-note quality
- [ ] Mark Wave 3 complete

---

## Overall program tracker

- [ ] Wave 1 complete
- [ ] Wave 2 complete
- [ ] Wave 3 complete
- [ ] `.meta` creation program complete
