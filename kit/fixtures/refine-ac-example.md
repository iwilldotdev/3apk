# Refine AC — Example Run (Redacted)

Fictional fixture: **`nova-003`** from [`sample-backlog-items.json`](sample-backlog-items.json) (status: `DoR_Pass` — used here as **input user story** for the AC skill smoke test).

| Field | Fixture value |
|-------|----------------|
| `id` | `nova-003` |
| `title` | Sprint worksheet CSV export |
| `user_story` | As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello. |
| `status` | DoR_Pass (fixture reference; skill run keeps `Refining` until full chain completes) |

---

## Turn 1 — Facilitator

> Run `3apk-refine-ac`. Backlog id: `nova-003`.
>
> Approved user story: "As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello."

## Turn 2 — Agent

Restated: tech lead needs a canonical CSV export of DoR-passed worksheet rows for Jira/Trello import.

**Which success boundary should the AC emphasize for the canonical format?**

- **A)** Strict 13-column order and types from COLUMNS.md only
- **B)** Column order plus RFC 4180 quoting for commas/newlines in AC text
- **C)** Both A and B plus verified Jira recipe import on a sample export
- **D)** Other — describe briefly

## Turn 3 — Facilitator

> C

## Turn 4 — Agent (draft AC)

**Proposed acceptance criteria:**

1. Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md
2. Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted
3. Given a completed export, when I import into Jira using the recipe, then all required issue fields populate

**Approve these acceptance criteria?**

- **A)** Approved — output is final; ready for estimate refinement
- **B)** Revise specific AC items (tell me which numbers to change)
- **C)** Add or remove scope (tell me what to include/exclude)
- **D)** Reject — restart clarification from user story

## Turn 5 — Facilitator

> A

## Turn 6 — Agent (approved Paste Block)

```markdown
## 3APK Refine AC — Approved Output

**id:** nova-003
**status:** Refining

### acceptance_criteria
- Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md
- Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted
- Given a completed export, when I import into Jira using the recipe, then all required issue fields populate
```

**Handoff:** Run **`3apk-refine-estimate`** with the approved `acceptance_criteria` above. Path: `kit/skills/3apk-refine-estimate/SKILL.md`.

---

## Notion paste check

| Notion Backlog field | Paste from block | Rename required? |
|----------------------|------------------|------------------|
| Acceptance Criteria | Each bullet under `### acceptance_criteria` | No |
| DoR → Testable AC | Set checkbox **true** after facilitator review | No |

## Schema conformance

Example AC extracted for automated validation (see `test_skill.py`):

```json
{
  "acceptance_criteria": [
    "Given DoR-passed stories in the worksheet, when I export CSV, then the file uses the 13-column order from COLUMNS.md",
    "Given acceptance criteria contain commas or line breaks, when exported, then fields are RFC 4180 quoted",
    "Given a completed export, when I import into Jira using the recipe, then all required issue fields populate"
  ]
}
```

- Array matches [`backlog-item.json`](../notion/schema/backlog-item.json) `acceptance_criteria` items (array of strings).
- Lines satisfy AC quality rules: testable, observable, Given/When/Then form, no vague terms.
- Enables DoR **`testable_ac: true`** when pasted (matches golden fixture `nova-003` intent).
