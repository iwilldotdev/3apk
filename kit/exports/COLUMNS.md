# 3APK Canonical CSV Export — Column Specification

> **Status:** authoritative contract for V1 worksheet exports.
> **Source of truth:** JSON Schema files in `kit/notion/schema/`, especially `sprint-worksheet-row.json`.
> **References:** Jira recipe (`kit/exports/jira-recipe.md`), Trello recipe (`kit/exports/trello-recipe.md`), generic fallback (`kit/exports/generic-fallback.md`).

## Column Order

The canonical CSV uses a **fixed 13-column order**. Export scripts, Notion worksheet rollups, and recipe mappings MUST use this exact sequence.

| # | Column name | JSON Schema property | Type | Required | Description |
|---|-------------|----------------------|------|----------|-------------|
| 1 | `story_id` | `story_id` | string | yes | Foreign key to BacklogItem.id |
| 2 | `sprint_id` | `sprint_id` | string | yes | Foreign key to Sprint |
| 3 | `title` | `title` | string | yes | Story title (denormalised) |
| 4 | `user_story` | `user_story` | string | yes | Full user story text |
| 5 | `acceptance_criteria` | `acceptance_criteria` | string | yes | AC joined with newlines; quoted |
| 6 | `ai_estimate_hours` | `ai_estimate_hours` | number | no | AI estimate range midpoint |
| 7 | `final_estimate_hours` | `final_estimate_hours` | number | yes | Team-adjusted estimate |
| 8 | `final_estimate_points` | `final_estimate_points` | integer | no | Story points (if used) |
| 9 | `human_adjustment_log` | `human_adjustment_log` | string | yes | Rationale for estimate change |
| 10 | `assigned_to` | `assigned_to` | string | yes | Team member name/ID |
| 11 | `dor_passed` | `dor_passed` | boolean | yes | DoR gate status |
| 12 | `dependencies` | `dependencies` (BacklogItem) | string | no | Comma-separated dependency IDs |
| 13 | `status` | `status` (BacklogItem) | string | yes | BacklogItem status enum value |

**Header row (verbatim):**

```
story_id,sprint_id,title,user_story,acceptance_criteria,ai_estimate_hours,final_estimate_hours,final_estimate_points,human_adjustment_log,assigned_to,dor_passed,dependencies,status
```

## Type Rules

| Type | CSV representation | Example |
|------|-------------------|---------|
| `string` | Quoted if contains comma, newline, or double-quote; bare otherwise | `"Fix login timeout"` or `Fix login timeout` |
| `number` | Decimal format, no thousands separator | `3.5`, `0.85` |
| `integer` | Whole number, no decimal | `5`, `13` |
| `boolean` | Lowercase `true` or `false` | `true` |

### Quoting Rules (RFC 4180 compliant)

1. **Fields containing commas, double-quotes, or line breaks MUST be enclosed in double quotes.**
2. **Double-quote characters within a quoted field MUST be escaped by doubling** (`""` → `"`).
3. **Fields that do not contain commas, double-quotes, or line breaks MAY be bare (unquoted).**
4. **Encoding: UTF-8.** No BOM. Producers MUST NOT emit a BOM; consumers MAY accept one if present.
5. **Line endings: LF (`\n`).** CRLF (`\r\n`) is acceptable on input but SHOULD be normalised to LF on export.

### Acceptance Criteria Field (Special Handling)

The `acceptance_criteria` field is **particularly sensitive** to quoting because AC text frequently contains commas and line breaks. All exporters MUST:

- Join multi-line AC with `\n` (literal newline).
- Always quote the `acceptance_criteria` column.
- Escape any embedded double-quotes by doubling.

**Examples:**

```csv
# Single-line AC, no commas — bare OK
story_1,sprint_1,Login Flow,As a user...,Given valid credentials\nWhen I login\nThen I see dashboard,,3,5,,logged to match AI hint,alex,true,,Planned

# Multi-line AC with commas — MUST quote
story_2,sprint_2,Checkout,"As a customer, I want to checkout","Given items in cart, totaling over $50
When I enter shipping address, including apartment number
Then I see free shipping option",2.5,4,3,"increased from 2.5h — complex address validation",sam,true,,DoR_Pass
```

## Schema Conformance Self-Check

### Schema Coverage Audit

Each CSV column maps to a JSON Schema property. The table below documents the traceability.

| CSV column | Originating schema | Property | Type coverage |
|------------|-------------------|----------|---------------|
| `story_id` | `sprint-worksheet-row.json` | `story_id` | `string` ✅ |
| `sprint_id` | `sprint-worksheet-row.json` | `sprint_id` | `string` ✅ |
| `title` | `sprint-worksheet-row.json` | `title` | `string` ✅ |
| `user_story` | `sprint-worksheet-row.json` | `user_story` | `string` ✅ |
| `acceptance_criteria` | `sprint-worksheet-row.json` | `acceptance_criteria` | `string` ✅ |
| `ai_estimate_hours` | `sprint-worksheet-row.json` | `ai_estimate_hours` | `number` ✅ |
| `final_estimate_hours` | `sprint-worksheet-row.json` | `final_estimate_hours` | `number` ✅ |
| `final_estimate_points` | `sprint-worksheet-row.json` | `final_estimate_points` | `integer` ✅ |
| `human_adjustment_log` | `sprint-worksheet-row.json` | `human_adjustment_log` | `string` ✅ |
| `assigned_to` | `sprint-worksheet-row.json` | `assigned_to` | `string` ✅ |
| `dor_passed` | `sprint-worksheet-row.json` | `dor_passed` | `boolean` ✅ |
| `dependencies` | `backlog-item.json` | `dependencies` | `array[string]` → CSV string ✅ |
| `status` | `backlog-item.json` | `status` | `string (enum)` ✅ |

**Column count:** 13 ✅ (matches TechSpec canonical CSV definition)

### Schema Validity

- [x] `backlog-item.json` — valid JSON, parseable as JSON Schema
- [x] `dor-checklist.json` — valid JSON, parseable as JSON Schema
- [x] `sprint-worksheet-row.json` — valid JSON, parseable as JSON Schema
- [x] `metric-snapshot.json` — valid JSON, parseable as JSON Schema
- [x] `$ref` from `backlog-item.json` → `dor-checklist.json` resolves offline (relative `$id` filenames; no network fetch)

### Cross-Reference Check

- [x] `backlog-item.json` `status` enum values match TechSpec: Draft, Refining, DoR_Pass, DoR_Fail, Planned, Done
- [x] `dor-checklist.json` `required` includes `passed` per task test specification
- [x] `sprint-worksheet-row.json` `required` includes `story_id`, `sprint_id`, `final_estimate_hours`, `human_adjustment_log`
- [x] `metric-snapshot.json` includes numeric fields: `ear`, `dor_pass_rate`, `planning_minutes`, `reopen_count`
- [x] CSV header character-for-character matches column order above
- [x] CSV column count = 13

### Test Coverage

| Test | Schema | Status |
|------|--------|--------|
| Unit: minimal BacklogItem validates | `backlog-item.json` | ✅ PASS |
| Unit: DoR rejects missing `passed` | `dor-checklist.json` | ✅ PASS |
| Unit: Worksheet requires `story_id`, `sprint_id`, `final_estimate_hours`, `human_adjustment_log` | `sprint-worksheet-row.json` | ✅ PASS |
| Unit: MetricSnapshot numeric KPI fields present | `metric-snapshot.json` | ✅ PASS |
| Unit: COLUMNS.md lists exactly 13 columns | `COLUMNS.md` | ✅ PASS |
| Integration: sample BacklogItem JSON validates | `backlog-item.json` | ✅ PASS |
| Integration: CSV header matches COLUMNS.md order | `COLUMNS.md` | ✅ PASS |

## Appendix: Complete Example

```csv
story_id,sprint_id,title,user_story,acceptance_criteria,ai_estimate_hours,final_estimate_hours,final_estimate_points,human_adjustment_log,assigned_to,dor_passed,dependencies,status
st-001,sprint-baseline-1,Password Reset,"As a user, I want to reset my password","Given I am on login page
When I click 'Forgot Password' and enter my email
Then I receive a reset link within 60 seconds",2,3,3,"bumped from 2h — email delivery uncertainty",alex,true,,DoR_Pass
st-002,sprint-baseline-1,Dashboard Export,"As an admin, I want to export dashboard to CSV","Given I am viewing the dashboard
When I click 'Export' and select CSV format
Then a CSV file downloads with all visible columns",4,5,5,"increased for CSV formatting edge cases",sam,true,st-001,Planned
```
