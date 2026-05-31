# Export Recipe Validation Log

> **Task:** task_09 — Export recipes (Jira + Trello + generic fallback)  
> **Last validated:** 2026-05-31  
> **Fixture:** [`sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv)

## Automated Checks

Run from repository root:

```bash
python3 kit/exports/test_export_recipes.py
python3 kit/fixtures/validate_fixtures.py
```

| Check | Command | Result | Notes |
|-------|---------|--------|-------|
| Recipe unit tests | `test_export_recipes.py` | ✅ PASS | 13/13 column mappings in Jira + Trello; generic Markdown template present |
| Fixture CSV integrity | `validate_fixtures.py` | ✅ PASS | 5 rows; multiline quoted AC; header matches COLUMNS.md |
| Column shift (multiline AC) | `test_export_recipes.py` | ✅ PASS | All rows parse to exactly 13 columns |
| No API integration in recipes | `test_export_recipes.py` | ✅ PASS | Manual import/copy-paste only (ADR-001) |

## Column Mapping Coverage

| Recipe | Columns mapped | Coverage |
|--------|----------------|----------|
| [`jira-recipe.md`](jira-recipe.md) | 13/13 | 100% |
| [`trello-recipe.md`](trello-recipe.md) | 13/13 | 100% |
| [`generic-fallback.md`](generic-fallback.md) | 13/13 | 100% |

### Core column mapping verification

| CSV column | Jira target | Trello target | Generic fallback |
|------------|-------------|---------------|------------------|
| `title` | Summary | Card name | Title / name |
| `acceptance_criteria` | Description / AC field | Description / Checklist | Description AC section |
| `final_estimate_hours` | Original Estimate | Custom Field (Hours) | Estimate field |
| `assigned_to` | Assignee | Members | Assignee |

## Manual Import Smoke Tests

These steps require facilitator access to Jira/Trello test workspaces. Record pass/fail when executed.

### Jira smoke test (checklist item 4)

| Step | Expected | Result | Executed by | Date |
|------|----------|--------|-------------|------|
| Import fixture CSV (DoR-pass rows 1–3) | ≥3 issues created | ☐ Pending manual run | | |
| Row 1 Summary | `Sprint worksheet CSV export` | ☐ | | |
| Row 1 multiline AC with comma preserved | 4 AC lines visible | ☐ | | |
| Row 1 Original Estimate | 5 hours | ☐ | | |
| Row 1 Assignee | Alex Chen (or mapped) | ☐ | | |
| Rows 4–5 filtered (DoR fail) | Not imported | ☐ | | |

**Procedure:** [`jira-recipe.md`](jira-recipe.md) § Smoke Test Procedure

### Trello smoke test (checklist item 5)

| Step | Expected | Result | Executed by | Date |
|------|----------|--------|-------------|------|
| Create cards from rows 1–3 | ≥3 cards | ☐ Pending manual run | | |
| Card 1 name | `Sprint worksheet CSV export` | ☐ | | |
| Card 1 multiline AC | Comma + newlines preserved | ☐ | | |
| Card 1 member | Alex Chen | ☐ | | |
| Card 1 estimate | 5h | ☐ | | |

**Procedure:** [`trello-recipe.md`](trello-recipe.md) § Smoke Test Procedure

### Generic fallback smoke test

| Step | Expected | Result | Executed by | Date |
|------|----------|--------|-------------|------|
| Render row 1 Markdown template | All sections populated | ☐ Pending manual run | | |
| Paste into issue tracker | Title + AC + estimates render | ☐ | | |

**Procedure:** [`generic-fallback.md`](generic-fallback.md) § Smoke Test

## Worked Example Traceability

Fixture rows used in all three recipes:

| Row | story_id | sprint_id | Used in |
|-----|----------|-----------|---------|
| 1 | nova-003 | sprint-baseline-01 | Jira, Trello, Generic (primary multiline AC example) |
| 2 | nova-003 | sprint-intervention-02 | Jira, Trello worked example table |
| 3 | nova-003 | sprint-evidence-03 | Jira, Trello, Generic row 3 example |
| 4 | nova-001 | sprint-baseline-01 | DoR skip example (Draft) |
| 5 | nova-002 | sprint-baseline-01 | DoR skip example (DoR_Fail) |

## Failure Mode Documentation

| Failure mode | Documented in |
|--------------|---------------|
| UTF-8 / encoding | All three recipes + COLUMNS.md |
| Multiline AC column shift | jira-recipe, trello-recipe, generic-fallback |
| Missing columns / wrong mapping | jira-recipe, trello-recipe |
| DoR filter violations | All three recipes |

## Sign-off

| Role | Name | Date | Notes |
|------|------|------|-------|
| Automated validation | `test_export_recipes.py` | 2026-05-31 | PASS |
| Manual Jira import | Facilitator | | Pending pilot workspace |
| Manual Trello import | Facilitator | | Pending pilot workspace |
