# 3APK Golden Fixtures

Golden reference files for manual conformance testing of JSON Schema contracts, canonical CSV exports, and export recipes (Jira/Trello). Example data supports the **RODRIGO HERPICH MULLER LTDA** pilot narrative (baseline → intervention sprints); replace with live project data in the PEX report when available.

> **Partner company:** RODRIGO HERPICH MULLER LTDA — see [`../playbook/empresa-parceira.md`](../playbook/empresa-parceira.md). Story IDs (`nova-*`) are technical fixture prefixes, not client names.

## Files

| File | Purpose | Validates against |
|------|---------|-------------------|
| [`sample-backlog-items.json`](sample-backlog-items.json) | Three backlog stories demonstrating `Draft`, `DoR_Pass`, and `DoR_Fail` statuses | [`backlog-item.json`](../notion/schema/backlog-item.json) |
| [`sample-worksheet-export.csv`](sample-worksheet-export.csv) | Golden canonical worksheet export (5 rows, multi-line AC quoting) | [`COLUMNS.md`](../exports/COLUMNS.md) + [`sprint-worksheet-row.json`](../notion/schema/sprint-worksheet-row.json) |
| [`sample-metric-snapshot.json`](sample-metric-snapshot.json) | Baseline + intervention sprint KPI snapshots | [`metric-snapshot.json`](../notion/schema/metric-snapshot.json) |

## Usage

1. **Schema validation** — validate JSON fixtures against schemas in `kit/notion/schema/` using any Draft-07 JSON Schema validator (see [Validation Record](#validation-record) below).
2. **CSV conformance** — compare `sample-worksheet-export.csv` header character-for-character with [`COLUMNS.md`](../exports/COLUMNS.md); confirm ≥5 data rows and RFC 4180 quoting on `acceptance_criteria`.
3. **Export recipe smoke tests** — import `sample-worksheet-export.csv` per [`jira-recipe.md`](../exports/jira-recipe.md) and [`trello-recipe.md`](../exports/trello-recipe.md) (task_09).
4. **Playbook checklist** — dry-run validation checklist items 3–7 in [`validation-checklist.md`](../playbook/validation-checklist.md) (task_10).

### Quick validation (requires Python `jsonschema`)

From the repository root:

```bash
python3 kit/fixtures/validate_fixtures.py
```

The script is a **developer convenience** for local verification; V1 has no CI gate (see ADR-003).

## Fixture Narrative

| ID | Status | Role in pilot |
|----|--------|---------------|
| `nova-001` | Draft | Unrefined OAuth request — blocked from worksheet |
| `nova-002` | DoR_Fail | Partial refinement — fails `testable_ac` and `nfr_flags_set` gates |
| `nova-003` | DoR_Pass | Fully refined export story — appears across baseline/intervention/evidence sprints in CSV |

The worksheet CSV includes **5 rows**: three `nova-003` commitments across pilot phases plus two negative rows (`nova-001`, `nova-002`) demonstrating DoR-filter violations for checklist exercises.

Metric snapshots capture **baseline** (high EAR, low DoR rate, 180 planning minutes) vs **intervention** (EAR 0.96, DoR 80%, 120 minutes, confidence 4.2).

## Validation Record

Last validated: **2026-05-31** (task_03)

### JSON Schema validation

| Fixture | Schema | Result | Notes |
|---------|--------|--------|-------|
| `sample-backlog-items.json` (3 items) | `backlog-item.json` | ✅ PASS | Each array element validates individually |
| `sample-metric-snapshot.json` (2 records) | `metric-snapshot.json` | ✅ PASS | Baseline + intervention phases populated |

### CSV header conformance

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| Column count | 13 | 13 | ✅ PASS |
| Header order | `story_id,sprint_id,title,user_story,acceptance_criteria,ai_estimate_hours,final_estimate_hours,final_estimate_points,human_adjustment_log,assigned_to,dor_passed,dependencies,status` | Matches [`COLUMNS.md`](../exports/COLUMNS.md) verbatim | ✅ PASS |

### Test checklist (task_03)

| Test | Result |
|------|--------|
| Exactly one `Draft`, one `DoR_Pass`, one `DoR_Fail` in backlog | ✅ PASS |
| Each backlog item validates against schema | ✅ PASS |
| CSV header matches COLUMNS.md order | ✅ PASS |
| CSV ≥5 data rows with non-empty `story_id` and `final_estimate_hours` | ✅ PASS (5 rows) |
| At least one row: quoted `acceptance_criteria` containing a comma | ✅ PASS (row 1) |
| Metric snapshot: two sprint records validate | ✅ PASS |
| CSV `story_id` values ⊆ backlog fixture IDs | ✅ PASS |
| Required-field population ≥80% | ✅ PASS (see coverage table below) |

### Required-field coverage (≥80% target)

| Schema | Required fields | Populated in fixture | Coverage |
|--------|-----------------|----------------------|----------|
| `backlog-item.json` | 4 (`id`, `title`, `status`, `dor`) | 4/4 per item; optional fields populated on DoR_Pass/Fail items | 100% |
| `dor-checklist.json` | 1 (`passed`) | 1/1 per item; all 4 gates set on refined items | 100% |
| `metric-snapshot.json` | 4 per record | 4/4 required + 6/6 optional KPI fields | 100% |
| `sprint-worksheet-row.json` (via CSV) | 4 per row | 4/4 required on all 5 rows | 100% |

## Related

- TechSpec: Integration / Conformance Tests (Manual)
- ADR-003: Artifact-first layout; fixtures + manual checklist (no validation binary in V1)
- [`kit/notion/SPEC.md`](../notion/SPEC.md) — Notion field names mirrored in fixtures
