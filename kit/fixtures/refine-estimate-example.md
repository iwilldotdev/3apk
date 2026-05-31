# Refine Estimate — Example Run (Redacted)

Fictional fixture: **`nova-003`** — approved AC from [`refine-ac-example.md`](refine-ac-example.md) (worksheet CSV export story).

| Field | Fixture value |
|-------|----------------|
| `id` | `nova-003` |
| `title` | Sprint worksheet CSV export |
| `user_story` | As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello. |
| `status` | Refining |

### Input acceptance_criteria (approved in step 2)

1. Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md
2. Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted
3. Given a completed export, when I import into Jira using the recipe, then all required issue fields populate

---

## Turn 1 — Facilitator

> Run `3apk-refine-estimate`. Backlog id: `nova-003`.
>
> Approved AC (from refine-ac Paste Block):
> - Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md
> - Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted
> - Given a completed export, when I import into Jira using the recipe, then all required issue fields populate

## Turn 2 — Agent

Restated: three AC for canonical CSV export with RFC 4180 quoting and Jira recipe verification.

**AI estimate hint — not a sprint commitment.** Research shows LLM-only estimation accuracy around ~16% when used as final numbers. These ranges are prep for planning only. The tech lead must adjust and sign off on `final_estimate_hours` during sprint planning per ADR-001.

**Which complexity driver best describes the Jira verification AC?**

- **A)** Manual spot-check on one sample export using existing recipe docs
- **B)** Automated fixture test plus manual Jira import on staging project
- **C)** Full cross-tool QA (Jira + Trello) with edge-case AC strings
- **D)** Other — describe briefly

## Turn 3 — Facilitator

> A

## Turn 4 — Agent (draft hint)

| Driver | Impact on range |
|--------|-----------------|
| 13-column canonical order + RFC 4180 quoting | Moderate export logic; encoding/quoting edge cases |
| Jira recipe manual spot-check (AC #3) | Adds verification time, not new feature surface |
| Three testable AC with integration touchpoint | Low–medium spread; no large data migration |

**Proposed estimate hint (NOT sprint commitment):**

- Hours: **low 6** / **high 10** (midpoint **8** for optional `estimate_hours` / `ai_estimate_hours`)
- Points (optional): **low 2** / **high 3**
- T-shirt: **M**

**Approve this estimate hint range?**

- **A)** Approved — hints are final for this refinement step; ready for dependency/risk check
- **B)** Revise range (tell me which drivers or bounds to change)
- **C)** Widen/narrow range after new context (describe)
- **D)** Reject — restart clarification from AC

## Turn 5 — Facilitator

> A

## Turn 6 — Agent (approved Paste Block)

```markdown
## 3APK Refine Estimate — Approved Hint (NOT sprint commitment)

**id:** nova-003
**status:** Refining

### estimate_hint_hours
- **low:** 6
- **high:** 10
- **midpoint (for ai_estimate_hours / optional estimate_hours):** 8

### estimate_hint_points (optional)
- **low:** 2
- **high:** 3

### tshirt_size (optional)
M

### rationale
| Driver | Impact on range |
|--------|-----------------|
| 13-column order + RFC 4180 quoting | Export formatter and edge-case quoting work |
| Jira recipe manual spot-check | Verification pass on sample export per AC #3 |

### human_signoff_required
AI hints only. Tech lead MUST set `final_estimate_hours` and `human_adjustment_log` during sprint planning (ADR-001). Do NOT use this block as committed sprint estimate.
```

**Handoff:** Run **`3apk-refine-risks`** with approved AC, user story, and estimate hints above. Path: `kit/skills/3apk-refine-risks/SKILL.md`.

---

## Schema conformance

Example hint extracted for automated validation (see `test_skill.py`):

```json
{
  "id": "nova-003",
  "status": "Refining",
  "acceptance_criteria": [
    "Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md",
    "Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted",
    "Given a completed export, when I import into Jira using the recipe, then all required issue fields populate"
  ],
  "estimate_hours": 8,
  "estimate_points": 2
}
```

- `estimate_hours` / `estimate_points` are **optional hints** (midpoint / low band) — validate against [`backlog-item.json`](../notion/schema/backlog-item.json).
- Worksheet planning would copy midpoint **8** to `ai_estimate_hours`; team still sets `final_estimate_hours` separately.
- Output is a **range** (6–10 h); never presented as committed sprint estimate.
