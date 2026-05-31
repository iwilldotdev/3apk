# 3APK Notion Hub — Setup Specification

> **Status:** authoritative facilitator guide for V1 manual Notion setup.
> **Source of truth for field names:** JSON Schema files in [`schema/`](schema/).
> **Architecture reference:** TechSpec "Notion databases"; PRD F3 (DoR gate), F6 (metrics KPIs).

This document enables facilitators to create the four Notion databases (**Backlog**, **Sprints**, **Planning Worksheet**, **Metrics**) on the **free tier** without Notion API integration. Property names MUST match JSON Schema property names exactly so skills, fixtures, and CSV exports stay aligned.

---

## Prerequisites

1. Notion account (free tier is sufficient).
2. A team workspace page titled **3APK Planning Hub** (or equivalent).
3. Local copies of schemas in `kit/notion/schema/` for cross-check during setup.

---

## Hub Layout (Recommended)

Create four **full-page databases** as siblings under the hub page:

```
3APK Planning Hub (page)
├── Backlog          (database)
├── Sprints          (database)
├── Planning Worksheet (database)
└── Metrics          (database)
```

Link each database from the hub page with a short description and deep link to the **DoR-filtered** worksheet view (created in [§3 Planning Worksheet](#3-planning-worksheet-database)).

---

## Global Property Mapping Rules

| JSON Schema type | Notion property type | Notes |
|------------------|---------------------|-------|
| `string` | **Text** | Use **Title** only for the human-facing story title (`title` in Backlog). |
| `string` (enum) | **Select** | Add every enum value from schema; do not rename options. |
| `number` | **Number** | Format: number (not percent) unless noted. |
| `integer` | **Number** | Whole numbers only. |
| `boolean` | **Checkbox** | Unchecked = `false`. |
| `array` of `string` | **Text** | Store one item per line, or comma-separated IDs for `dependencies`. |
| `string` (`format: date`) | **Date** | ISO 8601 in exports; Notion date picker in UI. |
| nested `dor` object | **Checkbox** fields | Flatten to top-level properties on Backlog (see [§1](#1-backlog-database)). |

**Naming rule:** Notion property names = JSON property names (snake_case). Do not translate to Portuguese or camelCase in V1.

---

## 1. Backlog Database

**Purpose:** Single source for refinement outputs, DoR evaluation, and story lifecycle before sprint commitment.

**Schema:** [`schema/backlog-item.json`](schema/backlog-item.json) (embeds [`schema/dor-checklist.json`](schema/dor-checklist.json) via `dor`).

### 1.1 Create the database

1. On the hub page, type `/database` → **Table – Full page**.
2. Name the database **Backlog**.
3. Rename the default **Name** column to **`title`** (property type stays **Title**).

### 1.2 Properties

Add properties in this order. The mapping table is the contract for task_10 validation.

| # | Notion property name | Notion type | JSON Schema | Required | Description |
|---|---------------------|-------------|-------------|----------|-------------|
| 1 | `title` | Title | `backlog-item.title` | yes | Short story title |
| 2 | `id` | Text | `backlog-item.id` | yes | Stable ID (UUID or `st-001`); used as `story_id` in worksheet/CSV |
| 3 | `raw_request` | Text | `backlog-item.raw_request` | no | Original request before refinement |
| 4 | `user_story` | Text | `backlog-item.user_story` | no | Refined user story |
| 5 | `acceptance_criteria` | Text | `backlog-item.acceptance_criteria` | no | One AC per line (maps to `array[string]`) |
| 6 | `estimate_hours` | Number | `backlog-item.estimate_hours` | no | Hours estimate (nullable) |
| 7 | `estimate_points` | Number | `backlog-item.estimate_points` | no | Story points (nullable) |
| 8 | `dependencies` | Text | `backlog-item.dependencies` | no | Dependency IDs/titles, comma-separated |
| 9 | `risks` | Text | `backlog-item.risks` | no | One risk per line |
| 10 | `problem_clear` | Checkbox | `dor-checklist.problem_clear` | no | DoR gate 1 |
| 11 | `testable_ac` | Checkbox | `dor-checklist.testable_ac` | no | DoR gate 2 |
| 12 | `dependencies_surfaced` | Checkbox | `dor-checklist.dependencies_surfaced` | no | DoR gate 3 |
| 13 | `nfr_flags_set` | Checkbox | `dor-checklist.nfr_flags_set` | no | DoR gate 4 |
| 14 | `passed` | Checkbox | `dor-checklist.passed` | yes | Aggregate DoR pass; drives worksheet filter |
| 15 | `status` | Select | `backlog-item.status` | yes | Lifecycle status |

**`status` select options (exact strings):**

- `Draft`
- `Refining`
- `DoR_Pass`
- `DoR_Fail`
- `Planned`
- `Done`

### 1.3 DoR gate implementation (PRD F3)

Notion has no API-driven gate in V1. Implement DoR with **checkbox fields** plus **manual discipline**:

1. **Four gates** map 1:1 to `dor-checklist.json`: `problem_clear`, `testable_ac`, `dependencies_surfaced`, `nfr_flags_set`.
2. **`passed`** is the aggregate gate used by the Planning Worksheet filter.
3. **Facilitator rule:** After each refinement paste, verify all four gate checkboxes. Set `passed` = checked only when all four are checked.
4. **Status sync (manual):**
   - All gates true → set `status` to `DoR_Pass` and check `passed`.
   - Any gate false → set `status` to `DoR_Fail` and uncheck `passed`.
5. **Optional formula assist:** If your Notion plan supports formulas on the same database, add a read-only formula property `dor_auto` (display only) such as:

   ```
   and(problem_clear, testable_ac, dependencies_surfaced, nfr_flags_set)
   ```

   Use it as a visual hint only; **`passed` remains the filter source** because free-tier formula rollups into other DBs are limited.

6. **Block non-ready stories:** Stories with `status` = `DoR_Fail` or `passed` unchecked MUST NOT appear in the Planning Worksheet **Sprint Candidates** view (see [§3.3](#33-dor-filtered-view-mandatory)).

### 1.4 Optional: relation to Sprints + rollup

**Should (recommended for pilot narrative):**

1. Add relation property **`Sprint`** → relate to **Sprints** database (allow single or multiple per your process; single is enough for V1).
2. On **Sprints**, add reverse relation **Backlog items** (auto-created).
3. Optional rollup on **Sprints**: `DoR passed count` = rollup of Backlog.`passed` where **Calculate** = `Checked` count.

This does not replace worksheet filtering; it helps facilitators report DoR % per sprint.

### 1.5 Backlog views

| View name | Type | Filter / sort |
|-----------|------|----------------|
| All stories | Table | Sort: `status` ascending |
| Refinement queue | Table | `status` is `Draft` or `Refining` |
| DoR passed | Table | `passed` is checked AND `status` is `DoR_Pass` |
| DoR failed | Table | `status` is `DoR_Fail` OR `passed` is unchecked |

---

## 2. Sprints Database

**Purpose:** Team capacity and sprint window for planning skill input and metrics linkage.

**Schema note:** There is no separate `sprint.json` in V1. Fields below are defined by TechSpec ("capacity hours, dates, status") and foreign keys `sprint_id` in `sprint-worksheet-row.json` and `metric-snapshot.json`.

### 2.1 Create the database

1. Add **Table – Full page** database named **Sprints**.
2. Rename default **Name** column to **`sprint_name`** (Title type) — aligns with `metric-snapshot.sprint_name` label.

### 2.2 Properties

| # | Notion property name | Notion type | JSON / contract | Required | Description |
|---|---------------------|-------------|-----------------|----------|-------------|
| 1 | `sprint_name` | Title | `metric-snapshot.sprint_name` | yes | Human label (e.g. `Sprint 1 — Baseline`) |
| 2 | `sprint_id` | Text | `sprint-worksheet-row.sprint_id`, `metric-snapshot.sprint_id` | yes | Stable ID referenced by worksheet and metrics |
| 3 | `capacity_hours` | Number | TechSpec Sprints | yes | Declared team capacity for planning skill |
| 4 | `start_date` | Date | TechSpec Sprints | yes | Sprint start |
| 5 | `end_date` | Date | TechSpec Sprints | yes | Sprint end |
| 6 | `status` | Select | TechSpec Sprints | yes | Planning lifecycle |

**`status` select options:**

- `Planned`
- `Active`
- `Closed`

### 2.3 Sprints views

| View name | Filter |
|-----------|--------|
| Active sprint | `status` is `Active` |
| Closed sprints | `status` is `Closed` |

---

## 3. Planning Worksheet Database

**Purpose:** Sprint commitment rows for DoR-passed stories with human-adjusted estimates and export to canonical CSV.

**Schema:** [`schema/sprint-worksheet-row.json`](schema/sprint-worksheet-row.json)

### 3.1 Create the database

1. Add **Table – Full page** database named **Planning Worksheet**.
2. Add relation **`Backlog item`** → **Backlog** (one story per row).
3. Add relation **`Sprint`** → **Sprints** (one sprint per row).

### 3.2 Properties

| # | Notion property name | Notion type | JSON Schema | Required | Description |
|---|---------------------|-------------|-------------|----------|-------------|
| 1 | `story_id` | Text | `story_id` | yes | Copy from linked Backlog `id` |
| 2 | `sprint_id` | Text | `sprint_id` | yes | Copy from linked Sprints `sprint_id` |
| 3 | `title` | Text | `title` | no | Denormalised from Backlog |
| 4 | `user_story` | Text | `user_story` | no | Denormalised |
| 5 | `acceptance_criteria` | Text | `acceptance_criteria` | no | Single text field (newline-separated AC) |
| 6 | `ai_estimate_hours` | Number | `ai_estimate_hours` | no | AI hint only |
| 7 | `final_estimate_hours` | Number | `final_estimate_hours` | yes | Team commitment |
| 8 | `final_estimate_points` | Number | `final_estimate_points` | no | Optional points |
| 9 | `human_adjustment_log` | Text | `human_adjustment_log` | yes | Mandatory rationale (PRD F4) |
| 10 | `assigned_to` | Text | `assigned_to` | no | Owner name |
| 11 | `dor_passed` | Checkbox | `dor_passed` | yes | Must be checked for sprint export |
| — | `Backlog item` | Relation | — | yes | Link to Backlog row |
| — | `Sprint` | Relation | — | yes | Link to Sprints row |

**Denormalisation workflow:** When adding a worksheet row, link Backlog + Sprint, then copy `id` → `story_id`, Backlog `title` → `title`, etc. Rollups can mirror `passed` → `dor_passed` if available:

- Rollup `dor_passed` from **Backlog item** → property `passed` → **Calculate:** `Show original` (checkbox).

If rollup is unavailable on free tier, set `dor_passed` manually from Backlog `passed`.

### 3.3 DoR-filtered view (mandatory)

Create view **Sprint Candidates**:

| Setting | Value |
|---------|-------|
| View type | Table |
| Filter 1 | `dor_passed` **is checked** |
| Filter 2 | `final_estimate_hours` **is not empty** (optional, for lock readiness) |
| Sort | `sprint_id` ascending, then `story_id` |

**Explicit block rule:** Rows where linked Backlog has `status` = `DoR_Fail` or `passed` unchecked MUST NOT be added to this view. If a `DoR_Fail` story appears, delete the worksheet row or fix Backlog gates first.

**Integration guarantee:** Facilitators run sprint planning only inside **Sprint Candidates** so `DoR_Fail` stories never enter commitment or CSV export.

### 3.4 Export note

Canonical CSV column order is defined in [`../exports/COLUMNS.md`](../exports/COLUMNS.md). Export manually from Notion (CSV) or copy via recipe in task_09; property names above match CSV headers.

---

## 4. Metrics Database

**Purpose:** One row per sprint capturing PEX KPIs (PRD Success Metrics / F6).

**Schema:** [`schema/metric-snapshot.json`](schema/metric-snapshot.json)

### 4.1 Create the database

1. Add **Table – Full page** database named **Metrics**.
2. Add relation **`Sprint`** → **Sprints**.
3. Use **`sprint_name`** as Title (or Text) — map to schema `sprint_name`.

### 4.2 Properties

| # | Notion property name | Notion type | JSON Schema | Required | Description |
|---|---------------------|-------------|-------------|----------|-------------|
| 1 | `sprint_name` | Title | `sprint_name` | yes | Display label |
| 2 | `sprint_id` | Text | `sprint_id` | yes | FK to Sprints |
| 3 | `captured_at` | Date | `captured_at` | yes | Snapshot date (ISO 8601 in exports) |
| 4 | `story_count` | Number | `story_count` | yes | Committed stories (≥5 for KPI validity) |
| 5 | `ear` | Number | `ear` | no | Estimation Accuracy Ratio (see [§4.3](#43-ear-and-kpi-formulas)) |
| 6 | `dor_pass_rate` | Number | `dor_pass_rate` | no | Fraction 0.0–1.0 (display as % in views) |
| 7 | `planning_minutes` | Number | `planning_minutes` | no | Participant-minutes |
| 8 | `reopen_count` | Number | `reopen_count` | no | Stories reopened mid-sprint |
| 9 | `confidence_score` | Number | `confidence_score` | no | Survey mean 1.0–5.0 |
| 10 | `notes` | Text | `notes` | no | Facilitator qualitative notes |
| 11 | `phase` | Select | `phase` | no | Pilot phase grouping |
| — | `Sprint` | Relation | — | recommended | Link to Sprints row |

**`phase` select options:**

- `baseline`
- `intervention`
- `evidence`

### 4.3 EAR and KPI formulas

V1 uses **documented formulas**; facilitators compute values manually or via Notion formula/rollup where the plan allows.

#### Estimation Accuracy Ratio (`ear`)

**PRD definition:** `EAR = Sum(actual hours) / Sum(estimated hours)` per sprint, target range **0.85–1.15**, minimum **≥5 stories**.

**Inputs (capture outside Metrics or in `notes` if needed):**

- `actual_hours_total` — sum of hours logged at sprint end
- `estimated_hours_total` — sum of `final_estimate_hours` from Planning Worksheet for that `sprint_id`

**Formula:**

```
ear = actual_hours_total / estimated_hours_total
```

**Interpretation:**

| EAR | Meaning |
|-----|---------|
| &lt; 0.85 | Team over-estimated |
| 0.85 – 1.15 | On target (±20%) |
| &gt; 1.15 | Team under-estimated |

Store the result in the **`ear`** number property at sprint close.

**Optional Notion formula property** `ear_calc` on Metrics (if you track totals as helper number fields `actual_hours_total` and `estimated_hours_total` on the same row):

```
if(estimated_hours_total > 0, actual_hours_total / estimated_hours_total, empty)
```

#### DoR pass rate (`dor_pass_rate`)

```
dor_pass_rate = dor_passed_count / story_count
```

Where `dor_passed_count` = Backlog items planned this sprint with `passed` checked. Target: **≥ 0.80**.

#### Planning minutes (`planning_minutes`)

Record: `(refinement_minutes + planning_ceremony_minutes) × participants`. Target: **−30% vs baseline** sprint.

#### Reopen count (`reopen_count`)

Count Backlog items moved from `Planned` back to `Refining` or `DoR_Fail` during the sprint. Target: **−25% vs baseline**.

#### Confidence score (`confidence_score`)

Post-sprint anonymous survey (5 questions, 1–5 scale). Store the **mean** in `confidence_score`. Target: **≥ 4.0**.

### 4.4 Metrics views

| View name | Filter / group |
|-----------|----------------|
| By phase | Group by `phase` |
| Baseline vs intervention | Filter `phase` is `baseline` or `intervention` |
| KPI dashboard | Show `ear`, `dor_pass_rate`, `planning_minutes`, `reopen_count`, `confidence_score` |

---

## 5. Master Property Mapping Table

Quick reference: every JSON Schema property in task_01 schemas → Notion.

| JSON Schema file | Property | Notion database | Notion property |
|------------------|----------|-----------------|-----------------|
| `backlog-item.json` | `id` | Backlog | `id` |
| `backlog-item.json` | `title` | Backlog | `title` |
| `backlog-item.json` | `raw_request` | Backlog | `raw_request` |
| `backlog-item.json` | `user_story` | Backlog | `user_story` |
| `backlog-item.json` | `acceptance_criteria` | Backlog | `acceptance_criteria` |
| `backlog-item.json` | `estimate_hours` | Backlog | `estimate_hours` |
| `backlog-item.json` | `estimate_points` | Backlog | `estimate_points` |
| `backlog-item.json` | `dependencies` | Backlog | `dependencies` |
| `backlog-item.json` | `risks` | Backlog | `risks` |
| `backlog-item.json` | `status` | Backlog | `status` |
| `dor-checklist.json` | `problem_clear` | Backlog | `problem_clear` |
| `dor-checklist.json` | `testable_ac` | Backlog | `testable_ac` |
| `dor-checklist.json` | `dependencies_surfaced` | Backlog | `dependencies_surfaced` |
| `dor-checklist.json` | `nfr_flags_set` | Backlog | `nfr_flags_set` |
| `dor-checklist.json` | `passed` | Backlog | `passed` |
| `sprint-worksheet-row.json` | `story_id` | Planning Worksheet | `story_id` |
| `sprint-worksheet-row.json` | `sprint_id` | Planning Worksheet | `sprint_id` |
| `sprint-worksheet-row.json` | `title` | Planning Worksheet | `title` |
| `sprint-worksheet-row.json` | `user_story` | Planning Worksheet | `user_story` |
| `sprint-worksheet-row.json` | `acceptance_criteria` | Planning Worksheet | `acceptance_criteria` |
| `sprint-worksheet-row.json` | `ai_estimate_hours` | Planning Worksheet | `ai_estimate_hours` |
| `sprint-worksheet-row.json` | `final_estimate_hours` | Planning Worksheet | `final_estimate_hours` |
| `sprint-worksheet-row.json` | `final_estimate_points` | Planning Worksheet | `final_estimate_points` |
| `sprint-worksheet-row.json` | `human_adjustment_log` | Planning Worksheet | `human_adjustment_log` |
| `sprint-worksheet-row.json` | `assigned_to` | Planning Worksheet | `assigned_to` |
| `sprint-worksheet-row.json` | `dor_passed` | Planning Worksheet | `dor_passed` |
| `metric-snapshot.json` | `sprint_id` | Metrics | `sprint_id` |
| `metric-snapshot.json` | `sprint_name` | Metrics | `sprint_name` |
| `metric-snapshot.json` | `captured_at` | Metrics | `captured_at` |
| `metric-snapshot.json` | `story_count` | Metrics | `story_count` |
| `metric-snapshot.json` | `ear` | Metrics | `ear` |
| `metric-snapshot.json` | `dor_pass_rate` | Metrics | `dor_pass_rate` |
| `metric-snapshot.json` | `planning_minutes` | Metrics | `planning_minutes` |
| `metric-snapshot.json` | `reopen_count` | Metrics | `reopen_count` |
| `metric-snapshot.json` | `confidence_score` | Metrics | `confidence_score` |
| `metric-snapshot.json` | `notes` | Metrics | `notes` |
| `metric-snapshot.json` | `phase` | Metrics | `phase` |
| TechSpec | `capacity_hours` | Sprints | `capacity_hours` |
| TechSpec | `start_date` / `end_date` | Sprints | `start_date`, `end_date` |
| TechSpec | sprint `status` | Sprints | `status` |
| FK contract | `sprint_id` | Sprints | `sprint_id` |

**Coverage:** 37 mapped properties / 37 schema + contract properties = **100%** (target ≥80%).

---

## 6. Facilitator Setup Checklist (Free Tier)

Use this checklist once per pilot environment.

### 6.1 Before you start

- [ ] Confirm Notion **free tier** limits: unlimited pages for individuals; team trial may apply — use a single facilitator workspace if member limits block guests.
- [ ] Disable property name auto-translate; keep **English snake_case** names.
- [ ] Open `kit/notion/schema/*.json` side-by-side while creating properties.

### 6.2 Database creation order

1. [ ] **Sprints** (worksheet and metrics depend on `sprint_id`)
2. [ ] **Backlog** (DoR checkboxes + `status`)
3. [ ] **Planning Worksheet** (relations + **Sprint Candidates** view)
4. [ ] **Metrics** (link to Sprints; enter baseline row after week 1)

### 6.3 Free-tier constraints

| Constraint | Mitigation |
|------------|------------|
| Limited formula complexity | Keep `passed` manual; use optional `dor_auto` hint only |
| Rollup across relations may be gated | Copy `passed` → `dor_passed` manually on worksheet rows |
| CSV export column names | Re-export may use display names — verify against [COLUMNS.md](../exports/COLUMNS.md) before Jira/Trello import |
| Guest access | Invite team as members to hub page; avoid embedding private DBs |
| File upload size | Store PEX photos in LMS; link URLs in `notes` only |

### 6.4 Post-setup smoke test

- [ ] Create one Sprint with `sprint_id` = `sprint-baseline-1`
- [ ] Create Backlog item `st-001` with all DoR gates checked, `passed` checked, `status` = `DoR_Pass`
- [ ] Create Backlog item `st-002` with `status` = `DoR_Fail`, `passed` unchecked
- [ ] Add worksheet row only for `st-001`; confirm `st-002` is **not** visible in **Sprint Candidates**
- [ ] Add Metrics row with `phase` = `baseline` and `story_count` ≥ 5

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| DoR-fail story in worksheet | Filter missing or `dor_passed` not synced | Enforce **Sprint Candidates** filters; fix Backlog `passed` |
| CSV import column mismatch | Notion renamed export headers | Map export columns per COLUMNS.md; rename properties to snake_case |
| `ear` empty | Totals not recorded | Add helper fields or compute in spreadsheet; paste into `ear` |
| Duplicate `story_id` | Manual ID entry | Enforce unique `id` on Backlog before linking worksheet |
| Status out of sync | Manual gate bypass | Re-run DoR checklist; set `DoR_Fail` until gates pass |

---

## Appendix A — Manual Field-Mapping Verification Checklist

Sign off after setup (peer or self-review). Mark **PASS** only if property name and type match this spec.

### A.1 Backlog (`backlog-item.json` + `dor-checklist.json`)

| Property | Type in Notion | PASS |
|----------|----------------|------|
| `title` | Title | [ ] |
| `id` | Text | [ ] |
| `raw_request` | Text | [ ] |
| `user_story` | Text | [ ] |
| `acceptance_criteria` | Text | [ ] |
| `estimate_hours` | Number | [ ] |
| `estimate_points` | Number | [ ] |
| `dependencies` | Text | [ ] |
| `risks` | Text | [ ] |
| `problem_clear` | Checkbox | [ ] |
| `testable_ac` | Checkbox | [ ] |
| `dependencies_surfaced` | Checkbox | [ ] |
| `nfr_flags_set` | Checkbox | [ ] |
| `passed` | Checkbox | [ ] |
| `status` | Select (6 options) | [ ] |

### A.2 Sprints (TechSpec contract)

| Property | Type in Notion | PASS |
|----------|----------------|------|
| `sprint_name` | Title | [ ] |
| `sprint_id` | Text | [ ] |
| `capacity_hours` | Number | [ ] |
| `start_date` | Date | [ ] |
| `end_date` | Date | [ ] |
| `status` | Select | [ ] |

### A.3 Planning Worksheet (`sprint-worksheet-row.json`)

| Property | Type in Notion | PASS |
|----------|----------------|------|
| `story_id` | Text | [ ] |
| `sprint_id` | Text | [ ] |
| `title` | Text | [ ] |
| `user_story` | Text | [ ] |
| `acceptance_criteria` | Text | [ ] |
| `ai_estimate_hours` | Number | [ ] |
| `final_estimate_hours` | Number | [ ] |
| `final_estimate_points` | Number | [ ] |
| `human_adjustment_log` | Text | [ ] |
| `assigned_to` | Text | [ ] |
| `dor_passed` | Checkbox | [ ] |
| Relation to Backlog | Relation | [ ] |
| Relation to Sprints | Relation | [ ] |
| View **Sprint Candidates** filters `dor_passed` checked | View | [ ] |

### A.4 Metrics (`metric-snapshot.json`)

| Property | Type in Notion | PASS |
|----------|----------------|------|
| `sprint_name` | Title | [ ] |
| `sprint_id` | Text | [ ] |
| `captured_at` | Date | [ ] |
| `story_count` | Number | [ ] |
| `ear` | Number | [ ] |
| `dor_pass_rate` | Number | [ ] |
| `planning_minutes` | Number | [ ] |
| `reopen_count` | Number | [ ] |
| `confidence_score` | Number | [ ] |
| `notes` | Text | [ ] |
| `phase` | Select (3 options) | [ ] |

**Reviewer:** _______________ **Date:** _______________

---

## Appendix B — Integration Test Script (Manual)

Run after hub setup. Expected duration: 30–45 minutes.

1. **Create Sprints row** with `sprint_id` = `test-sprint-1`, `capacity_hours` = 40, `status` = `Planned`, dates spanning current week.
2. **Create Backlog row A** with `id` = `test-st-pass`, `title` = `DoR pass story`, all four DoR gates checked, `passed` checked, `status` = `DoR_Pass`.
3. **Create Backlog row B** with `id` = `test-st-fail`, `title` = `DoR fail story`, all DoR gates unchecked, `passed` unchecked, `status` = `DoR_Fail`.
4. **Open Planning Worksheet → Sprint Candidates view** — confirm zero rows initially.
5. **Add worksheet row** linked to row A only; set `story_id`, `sprint_id`, `final_estimate_hours` = 3, `human_adjustment_log` = `test adjustment`, `dor_passed` checked.
6. **Verify filter:** row B must not be addable to filtered view without showing in list — if visible, fix filter (`dor_passed` is checked).
7. **Attempt bad path:** try adding row for story B with `dor_passed` unchecked — confirm facilitators treat as blocked (row should not appear in **Sprint Candidates**).
8. **Create Metrics row** for `test-sprint-1` with `story_count` = 5, `phase` = `baseline`, `planning_minutes` = 120.
9. **Compute EAR manually:** if `actual_hours_total` = 17 and `estimated_hours_total` = 15, set `ear` = 1.13 (within 0.85–1.15).
10. **Export worksheet CSV** (if available) — verify headers align with [COLUMNS.md](../exports/COLUMNS.md) for populated columns.
11. **Delete test rows** or mark `notes` = `integration test` for cleanup.

**Pass criteria:** Steps 6–7 prove DoR_Fail stories are blocked from sprint planning view; step 9 proves EAR formula is documented and applicable.

---

## Appendix C — Automated Schema Coverage Check (Local)

From repository root, run:

```bash
python3 << 'PY'
import json, re, pathlib
root = pathlib.Path("kit/notion")
spec = (root / "SPEC.md").read_text()
schemas = {
    "backlog-item.json": list(json.loads((root/"schema/backlog-item.json").read_text())["properties"]),
    "dor-checklist.json": list(json.loads((root/"schema/dor-checklist.json").read_text())["properties"]),
    "sprint-worksheet-row.json": list(json.loads((root/"schema/sprint-worksheet-row.json").read_text())["properties"]),
    "metric-snapshot.json": list(json.loads((root/"schema/metric-snapshot.json").read_text())["properties"]),
}
# Backlog embeds dor flattened on Backlog per spec
backlog_props = schemas["backlog-item.json"] + schemas["dor-checklist.json"]
sprint_contract = ["sprint_id", "sprint_name", "capacity_hours", "start_date", "end_date", "status"]
missing = []
for p in backlog_props:
    if f"`{p}`" not in spec and f"| `{p}` |" not in spec:
        missing.append(("backlog/dor", p))
for p in schemas["sprint-worksheet-row.json"]:
    if f"`{p}`" not in spec:
        missing.append(("worksheet", p))
for p in schemas["metric-snapshot.json"]:
    if f"`{p}`" not in spec:
        missing.append(("metrics", p))
for p in sprint_contract:
    if f"`{p}`" not in spec:
        missing.append(("sprints", p))
total = len(backlog_props) + len(schemas["sprint-worksheet-row.json"]) + len(schemas["metric-snapshot.json"]) + len(sprint_contract)
mapped = total - len(missing)
pct = 100 * mapped / total
print(f"Mapped: {mapped}/{total} ({pct:.1f}%)")
if missing:
    print("MISSING:", missing)
    raise SystemExit(1)
print("OK: all schema properties referenced in SPEC.md")
PY
```

Expected output: `OK: all schema properties referenced in SPEC.md` with coverage ≥80%.

---

## Related Documents

- [`schema/backlog-item.json`](schema/backlog-item.json)
- [`schema/dor-checklist.json`](schema/dor-checklist.json)
- [`schema/sprint-worksheet-row.json`](schema/sprint-worksheet-row.json)
- [`schema/metric-snapshot.json`](schema/metric-snapshot.json)
- [`../exports/COLUMNS.md`](../exports/COLUMNS.md)
- Playbook validation (task_10): `kit/playbook/validation-checklist.md`
