# Refine Risks — Example Run (Redacted)

Fictional fixture: **`nova-003`** — combined inputs from refinement steps 1–3 ([`refine-story-example.md`](refine-story-example.md), [`refine-ac-example.md`](refine-ac-example.md), [`refine-estimate-example.md`](refine-estimate-example.md)).

| Field | Fixture value |
|-------|----------------|
| `id` | `nova-003` |
| `title` | Sprint worksheet CSV export |
| `raw_request` | We need to push sprint plans into Jira without copy-paste hell |
| `user_story` | As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello. |
| `status` | Refining |

### Input acceptance_criteria (approved in step 2)

1. Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md
2. Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted
3. Given a completed export, when I import into Jira using the recipe, then all required issue fields populate

### Input estimate hints (approved in step 3)

- Hours: low **6** / high **10** / midpoint **8** (AI hint only)
- Points: low **2** / high **3**

---

## Turn 1 — Facilitator

> Run `3apk-refine-risks`. Backlog id: `nova-003`.
>
> Combined approved inputs from steps 1–3 (story, AC, estimate hints above).

## Turn 2 — Agent

Restated: CSV export for DoR-passed worksheet rows with canonical columns, RFC 4180 quoting, and Jira recipe verification. Estimate hint 6–10 h (midpoint 8).

**Does this story depend on any other backlog item or external prerequisite before export work can start?**

- **A)** No — export is self-contained within worksheet + COLUMNS.md
- **B)** Yes — depends on another backlog story (name id/title)
- **C)** Yes — depends on frozen export spec or Jira recipe docs only
- **D)** Other — describe briefly

## Turn 3 — Facilitator

> C — `kit/exports/COLUMNS.md` and Jira recipe must be current before verification AC

## Turn 4 — Agent

**Does UTF-8 / Excel compatibility need an explicit risk flag for this export story?**

- **A)** Yes — Windows Excel encoding is a known risk
- **B)** No — team only uses tools that handle UTF-8
- **C)** Unknown — flag until verified on target OS
- **D)** Other — describe briefly

## Turn 5 — Facilitator

> A

## Turn 6 — Agent (NFR summary + draft)

**NFR evaluation:**

| Area | Result | Notes |
|------|--------|-------|
| Performance | N/A for gate | No latency AC; export size bounded by worksheet row count |
| Security | Evaluated — low | CSV export of planning data; no new auth surface |
| Accessibility | Evaluated — N/A | Tech-lead tooling; no end-user UI change |

**Proposed dependencies:**

- `kit/exports/COLUMNS.md` — canonical column order frozen before AC #1 verification
- Jira import recipe (`kit/exports/jira-recipe.md`) — required for AC #3 spot-check

**Proposed risks:**

- UTF-8 encoding edge cases on Windows Excel when opening exported CSV

**DoR self-assessment (draft):**

| Gate | Schema field | Result | Rationale |
|------|--------------|--------|-----------|
| 1 — Problem clear | `problem_clear` | true | User story states actor, capability, and Jira/Trello benefit |
| 2 — Testable AC | `testable_ac` | true | Three Given/When/Then AC with measurable outcomes |
| 3 — Dependencies surfaced | `dependencies_surfaced` | true | Spec + recipe prerequisites documented |
| 4 — NFR flags set | `nfr_flags_set` | true | Performance/security/a11y explicitly evaluated |

**Aggregate:** `passed` = **true** → recommended **`DoR_Pass`**

**Approve dependencies, risks, and DoR self-assessment?**

- **A)** Approved — ready for Notion paste block
- **B)** Revise dependencies (tell me what to add/remove)
- **C)** Revise risks or NFR flags (tell me what to change)
- **D)** Reject — restart clarification from inputs

## Turn 7 — Facilitator

> A

## Turn 8 — Agent (approved Notion Paste Block)

```markdown
## 3APK Refine Risks — Approved Backlog Entry (paste-ready)

**id:** nova-003
**title:** Sprint worksheet CSV export
**status:** Refining

### raw_request
We need to push sprint plans into Jira without copy-paste hell

### user_story
As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello.

### acceptance_criteria
- Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md
- Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted
- Given a completed export, when I import into Jira using the recipe, then all required issue fields populate

### estimate_hours
8

### estimate_points
2

### dependencies
- kit/exports/COLUMNS.md — canonical column order frozen before AC #1 verification
- Jira import recipe (kit/exports/jira-recipe.md) — required for AC #3 spot-check

### risks
- UTF-8 encoding edge cases on Windows Excel when opening exported CSV

### dor_self_assessment
| Gate | Schema field | Result | Rationale |
|------|--------------|--------|-----------|
| 1 — Problem clear | `problem_clear` | true | Actor, capability, and benefit are explicit |
| 2 — Testable AC | `testable_ac` | true | Three verifiable Given/When/Then criteria |
| 3 — Dependencies surfaced | `dependencies_surfaced` | true | COLUMNS.md and Jira recipe prerequisites listed |
| 4 — NFR flags set | `nfr_flags_set` | true | Performance N/A; security/a11y evaluated |

**passed:** true
**recommended_status:** DoR_Pass
```

**Notion paste:** Copy sections per field mapping table in `SKILL.md`. Set checkboxes from DoR table; set **Status** to **`DoR_Pass`** and check **Passed**.

**Handoff:** Backlog entry ready for sprint planning. When sprint starts, run **`3apk-plan-sprint`**. Path: `kit/skills/3apk-plan-sprint/SKILL.md`.

---

## Schema conformance

Example backlog entry extracted for automated validation (see `test_skill.py`):

```json
{
  "id": "nova-003",
  "title": "Sprint worksheet CSV export",
  "raw_request": "We need to push sprint plans into Jira without copy-paste hell",
  "user_story": "As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello.",
  "acceptance_criteria": [
    "Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md",
    "Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted",
    "Given a completed export, when I import into Jira using the recipe, then all required issue fields populate"
  ],
  "estimate_hours": 8,
  "estimate_points": 2,
  "dependencies": [
    "kit/exports/COLUMNS.md — canonical column order frozen before AC #1 verification",
    "Jira import recipe (kit/exports/jira-recipe.md) — required for AC #3 spot-check"
  ],
  "risks": [
    "UTF-8 encoding edge cases on Windows Excel when opening exported CSV"
  ],
  "dor": {
    "problem_clear": true,
    "testable_ac": true,
    "dependencies_surfaced": true,
    "nfr_flags_set": true,
    "passed": true
  },
  "status": "DoR_Pass"
}
```

- Validates against [`backlog-item.json`](../notion/schema/backlog-item.json).
- Matches golden fixture `nova-003` in [`sample-backlog-items.json`](sample-backlog-items.json) for DoR_Pass pattern (dependencies may differ in wording; gates must align).

## DoR_Fail pattern (fixture nova-002)

For integration testing **`testable_ac: false`** path, use backlog item **`nova-002`** from [`sample-backlog-items.json`](sample-backlog-items.json):

- Single AC without full Given/When/Then coverage → `testable_ac: false`
- `passed: false`, `status: DoR_Fail`
- Skill must **not** recommend sprint planning or `DoR_Pass`
