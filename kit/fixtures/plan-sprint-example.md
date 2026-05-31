# Plan Sprint — Example Run (Redacted)

Example sprint planning session using DoR-passed candidates derived from the refinement chain. Fixture backlog anchor: **`nova-003`** from [`sample-backlog-items.json`](sample-backlog-items.json). Additional candidates **`nova-004`** and **`nova-005`** are example DoR-passed stories for multi-story planning smoke tests.

| Field | Value |
|-------|-------|
| `sprint_id` | `sprint-baseline-01` |
| `capacity_hours` | 24 |
| `buffer` | 10% (2.4h) → effective capacity **21.6h** |
| DoR-passed candidates | 3 (`nova-003`, `nova-004`, `nova-005`) |
| Rejected input (control) | `nova-002` (`DoR_Fail`) |

---

## Candidate Backlog Items (DoR-passed)

### nova-003 (from fixture)

| Field | Value |
|-------|-------|
| `status` | `DoR_Pass` |
| `dor.passed` | `true` |
| `estimate_hours` | 4 (AI hint midpoint) |
| `title` | Sprint worksheet CSV export |

### nova-004 (example — planning smoke)

| Field | Value |
|-------|-------|
| `status` | `DoR_Pass` |
| `dor.passed` | `true` |
| `estimate_hours` | 6 |
| `title` | Jira import field mapping validator |
| `user_story` | As a tech lead, I want to validate Jira field mappings against the export recipe so that imported issues match worksheet columns. |
| `acceptance_criteria` | Given a locked sprint CSV, when I run the validator checklist, then every required Jira field maps to a worksheet column |

### nova-005 (example — planning smoke)

| Field | Value |
|-------|-------|
| `status` | `DoR_Pass` |
| `dor.passed` | `true` |
| `estimate_hours` | 8 |
| `title` | Planning metrics capture widget |
| `user_story` | As a facilitator, I want to record planning_minutes in the Metrics DB so that PEX evidence includes planning time KPIs. |
| `acceptance_criteria` | Given a locked sprint, when I enter planning_minutes, then the Metrics row links to sprint_id and EAR inputs remain valid |

---

## Turn 1 — Facilitator

> Run `3apk-plan-sprint`.
>
> **sprint_id:** sprint-baseline-01  
> **capacity_hours:** 24  
>
> DoR-passed candidates: nova-003, nova-004, nova-005 (details above).  
> Also including nova-002 by mistake for validation test.

## Turn 2 — Agent

**Input acknowledged:** sprint `sprint-baseline-01`, capacity **24h**, 4 items supplied.

**DoR validation:**

| story_id | status | dor.passed | Result |
|----------|--------|------------|--------|
| nova-003 | DoR_Pass | true | ✅ eligible |
| nova-004 | DoR_Pass | true | ✅ eligible |
| nova-005 | DoR_Pass | true | ✅ eligible |
| nova-002 | DoR_Fail | false | ❌ **rejected** |

> **Cannot plan:** `nova-002` — Billing webhook retry logic is not DoR-passed. Fix Notion gates or complete refinement before sprint planning.

**Capacity preview:** hint sum = 4 + 6 + 8 = **18h** (within 24h before buffer).

**How much capacity should we reserve for unplanned work?**

- **A)** 0% — commit full capacity
- **B)** 10% buffer
- **C)** 20% buffer
- **D)** Other — specify hours

## Turn 3 — Facilitator

> B

## Turn 4 — Agent

Effective capacity: **21.6h** (24h − 10% buffer).

**Story `nova-003` — Sprint worksheet CSV export**  
AI hint: **4h**.  
**What is the team's final estimate?**

- **A)** Accept AI hint — final = 4h
- **B)** Increase — specify hours and reason
- **C)** Decrease — specify hours and reason
- **D)** Defer this story from sprint
- **E)** Other — describe briefly

## Turn 5 — Facilitator

> B — 5h, CSV quoting edge cases

## Turn 6 — Agent

**Record human adjustment log for `nova-003`:** Why change from 4h to 5h?

## Turn 7 — Facilitator

> Increased from 4h — CSV quoting and cross-tool import edge cases

## Turn 8 — Agent

**Story `nova-004` — Jira import field mapping validator**  
AI hint: **6h**.  
**What is the team's final estimate?**

- **A)** Accept AI hint — final = 6h
- **B)** Increase
- **C)** Decrease
- **D)** Defer
- **E)** Other

## Turn 9 — Facilitator

> A

## Turn 10 — Agent

Log recorded: `No adjustment — team aligned with AI range midpoint`.

**Story `nova-005` — Planning metrics capture widget**  
AI hint: **8h**.  
**What is the team's final estimate?**

- **A)** Accept AI hint — final = 8h
- **B)** Increase
- **C)** Decrease
- **D)** Defer
- **E)** Other

## Turn 11 — Facilitator

> A

## Turn 12 — Agent

**Sprint draft**

| story_id | ai_estimate_hours | final_estimate_hours | human_adjustment_log |
|----------|-------------------|----------------------|----------------------|
| nova-003 | 4 | 5 | Increased from 4h — CSV quoting and cross-tool import edge cases |
| nova-004 | 6 | 6 | No adjustment — team aligned with AI range midpoint |
| nova-005 | 8 | 8 | No adjustment — team aligned with AI range midpoint |

**Committed:** 19h / **effective capacity:** 21.6h ✅

**Approve this sprint draft for lock?**

- **A)** Approved — ready for Sprint Lock Block
- **B)** Revise estimates
- **C)** Revise scope
- **D)** Reject

## Turn 13 — Facilitator

> A

## Turn 14 — Agent (Sprint Lock Block — excerpt)

Locked commitment for `sprint-baseline-01`. Export handoff → [`jira-recipe.md`](../exports/jira-recipe.md).

### worksheet_rows (schema-validated)

```json
[
  {
    "story_id": "nova-003",
    "sprint_id": "sprint-baseline-01",
    "title": "Sprint worksheet CSV export",
    "user_story": "As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello.",
    "acceptance_criteria": "Given DoR-passed stories in the worksheet\nWhen I export CSV\nThen the file uses the 13-column order from COLUMNS.md\nGiven acceptance criteria contain commas or line breaks\nWhen exported\nThen fields are RFC 4180 quoted\nGiven a completed export\nWhen I import into Jira using the recipe\nThen all required issue fields populate",
    "ai_estimate_hours": 4,
    "final_estimate_hours": 5,
    "final_estimate_points": 5,
    "human_adjustment_log": "Increased from 4h — CSV quoting and cross-tool import edge cases",
    "assigned_to": "Alex Chen",
    "dor_passed": true
  },
  {
    "story_id": "nova-004",
    "sprint_id": "sprint-baseline-01",
    "title": "Jira import field mapping validator",
    "user_story": "As a tech lead, I want to validate Jira field mappings against the export recipe so that imported issues match worksheet columns.",
    "acceptance_criteria": "Given a locked sprint CSV, when I run the validator checklist, then every required Jira field maps to a worksheet column",
    "ai_estimate_hours": 6,
    "final_estimate_hours": 6,
    "final_estimate_points": 3,
    "human_adjustment_log": "No adjustment — team aligned with AI range midpoint",
    "assigned_to": "Sam Rivera",
    "dor_passed": true
  },
  {
    "story_id": "nova-005",
    "sprint_id": "sprint-baseline-01",
    "title": "Planning metrics capture widget",
    "user_story": "As a facilitator, I want to record planning_minutes in the Metrics DB so that PEX evidence includes planning time KPIs.",
    "acceptance_criteria": "Given a locked sprint, when I enter planning_minutes, then the Metrics row links to sprint_id and EAR inputs remain valid",
    "ai_estimate_hours": 8,
    "final_estimate_hours": 8,
    "final_estimate_points": 5,
    "human_adjustment_log": "No adjustment — team aligned with AI range midpoint",
    "assigned_to": "Jordan Lee",
    "dor_passed": true
  }
]
```

### csv_export_readiness (row shape vs COLUMNS.md)

Example CSV row for `nova-003` (13 columns):

```
nova-003,sprint-baseline-01,Sprint worksheet CSV export,"As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello.","Given DoR-passed stories in the worksheet
When I export CSV
Then the file uses the 13-column order from COLUMNS.md",4,5,5,"Increased from 4h — CSV quoting and cross-tool import edge cases",Alex Chen,true,,Planned
```

Header matches [`COLUMNS.md`](../exports/COLUMNS.md) and [`sample-worksheet-export.csv`](sample-worksheet-export.csv).

---

## Over-Capacity Variant (integration test)

**Input change:** same three stories, **`capacity_hours: 8`**, 0% buffer → effective capacity **8h**.

**Hint sum:** 18h → **over capacity**.

Agent must:

1. Stop before draft approval.
2. Present over-capacity table (committed 19h vs capacity 8h in full draft scenario).
3. Ask **Q4 Over-capacity confirmation** — defer `nova-005` (8h) and `nova-004` (6h) or reduce scope.
4. Feasible locked draft example: **nova-003 only** at 5h final estimate.

**Scope reduction answer (facilitator):**

> A — defer lowest-priority: nova-005

Resulting feasible commitment: nova-003 (5h) + nova-004 (6h) = 11h still over 8h → defer nova-004 → **nova-003 only at 5h** ✅
