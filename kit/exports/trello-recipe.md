# Trello Export Recipe — Canonical CSV → Cards

> **Scope:** Manual CSV-to-card workflow or copy-paste only. No Trello REST API, Power-Up development, or automation (ADR-001, PRD Non-Goals).
> **Source CSV contract:** [`COLUMNS.md`](COLUMNS.md) — fixed 13-column order, UTF-8, RFC 4180 quoting.
> **Golden fixture:** [`sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv)

## Prerequisites

1. Sprint locked in Notion Planning Worksheet (see [`3apk-plan-sprint`](../skills/3apk-plan-sprint/SKILL.md)).
2. Trello board with a **Sprint Commitment** list (or equivalent) ready for new cards.
3. CSV matches [`COLUMNS.md`](COLUMNS.md) header and encoding rules.
4. Team members in `assigned_to` exist as Trello board members (or map names manually).

## Column → Trello Card Field Mapping

Map every canonical column before card creation. Column order follows [`COLUMNS.md`](COLUMNS.md) § Column Order.

| # | CSV column | Trello destination | Required | Notes |
|---|------------|-------------------|----------|-------|
| 1 | `story_id` | **Card title suffix** or **Label** (`3apk:{story_id}`) | Recommended | Traceability to Notion backlog |
| 2 | `sprint_id` | **List name** or **Label** (`sprint:{sprint_id}`) | Recommended | One list per sprint, or label per sprint |
| 3 | `title` | **Card name** | **Yes** | Primary card title |
| 4 | `user_story` | **Description** (User Story section) | Recommended | Top of description |
| 5 | `acceptance_criteria` | **Description** (AC section) or **Checklist** items | **Yes** | Split `\n`-separated AC into checklist items when practical |
| 6 | `ai_estimate_hours` | **Description** (Estimates) or **Custom Field** | Optional | Informational AI hint |
| 7 | `final_estimate_hours` | **Custom Field** (Hours) or **Description** badge | **Yes** | Committed estimate for sprint |
| 8 | `final_estimate_points` | **Custom Field** (Points) or **Label** (`pts:{n}`) | Optional | If team uses story points |
| 9 | `human_adjustment_log` | **Description** (Adjustment log) or **Comment** | Recommended | PEX audit trail |
| 10 | `assigned_to` | **Members** | Recommended | Assign board member matching name |
| 11 | `dor_passed` | **Label** (`dor-passed` / `dor-failed`) | Recommended | Only create cards where `true` for sprint |
| 12 | `dependencies` | **Description** (Dependencies) or **Card links** | Optional | Link cards after creation using dependency IDs |
| 13 | `status` | **List placement** or **Label** (`backlog:{status}`) | Optional | `Planned` → Sprint list; skip `Draft` / `DoR_Fail` |

**Mapping coverage:** 13/13 columns documented (100%).

### Composed Card Description Template

```markdown
## User Story
{user_story}

## Acceptance Criteria
{acceptance_criteria}

## Estimates
- AI hint: {ai_estimate_hours}h
- Final: {final_estimate_hours}h
- Points: {final_estimate_points}

## Human Adjustment Log
{human_adjustment_log}

---
Story ID: {story_id} | Sprint: {sprint_id} | DoR: {dor_passed} | Status: {status}
Dependencies: {dependencies}
```

## Procedure A — CSV Import via Third-Party Tool (bulk)

Trello has no native CSV import on the free tier. Use a **manual import assistant** (e.g. Trello CSV import Power-Up, or spreadsheet copy workflow) without API keys:

1. **Filter rows:** `dor_passed` = `true`; skip `Draft` / `DoR_Fail`.
2. Open your CSV import tool; select **UTF-8** encoding.
3. Map columns per table above:
   - `title` → **Card Name**
   - `user_story` + `acceptance_criteria` + logs → **Description**
   - `final_estimate_hours` → **Custom Field** or description
   - `assigned_to` → **Member**
4. Target list: `{sprint_id}` or your sprint commitment list.
5. Preview first card — verify multiline AC did not truncate.

## Procedure B — Manual Card Creation (copy-paste)

Recommended for smoke tests and small sprints.

1. Open Trello board → **Add card** in sprint list.
2. **Card name:** `{title}` (optionally append `[{story_id}]`).
3. **Description:** paste from template above, filling CSV row values.
4. **Members:** add `{assigned_to}`.
5. **Labels:** `dor-passed`, `sprint:{sprint_id}`, optional `pts:{final_estimate_points}`.
6. **Checklist (optional):** split `acceptance_criteria` on `\n` into checklist items.
7. Repeat for each DoR-pass row.

## Procedure C — Tab-Separated Paste from Spreadsheet

1. Open CSV in LibreOffice Calc / Google Sheets (import as UTF-8).
2. Verify 13 columns align with [`COLUMNS.md`](COLUMNS.md) header.
3. Filter DoR-pass rows.
4. For each row, copy cells into the card template (Procedure B).

## Worked Example — `sample-worksheet-export.csv`

Fixture: [`kit/fixtures/sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv)

| Row | story_id | sprint_id | title | assigned_to | final_estimate_hours | Import? |
|-----|----------|-----------|-------|-------------|---------------------|---------|
| 1 | nova-003 | sprint-baseline-01 | Sprint worksheet CSV export | Alex Chen | 5 | ✅ Card 1 |
| 2 | nova-003 | sprint-intervention-02 | Sprint worksheet CSV export | Alex Chen | 4 | ✅ Card 2 |
| 3 | nova-003 | sprint-evidence-03 | Sprint worksheet CSV export | Sam Rivera | 3.5 | ✅ Card 3 |
| 4 | nova-001 | … | Add OAuth provider… | Jordan Lee | 8 | ❌ Skip |
| 5 | nova-002 | … | Billing webhook retry logic | Sam Rivera | 6 | ❌ Skip |

**Card 1 — multiline AC test:**

Card name: `Sprint worksheet CSV export`

Description AC section must render:

```
Given DoR-passed stories in the worksheet
When I export CSV
Then the file uses the 13-column order from COLUMNS.md
Given acceptance criteria contain commas, or line breaks
When exported
Then fields are RFC 4180 quoted
```

Member: **Alex Chen**. Custom field / description: **5h** final estimate.

**Checklist variant:** Create 4 checklist items from the four Given/When/Then blocks above.

## Encoding & Quoting

Per [`COLUMNS.md`](COLUMNS.md):

| Rule | Requirement |
|------|-------------|
| Encoding | UTF-8, no BOM |
| Commas / newlines in fields | Must be quoted in CSV source |
| Paste into Trello | Markdown code blocks optional; plain text preserves newlines |
| Special characters | Trello accepts UTF-8 in descriptions (emoji, accented names) |

**Validation:** Run `python3 kit/fixtures/validate_fixtures.py` before import to confirm fixture integrity.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| AC collapsed to one line | CSV newline lost on Excel open | Open CSV in text editor; re-export UTF-8 from Notion |
| Wrong member assigned | Display name mismatch | Use Trello @mention after card create |
| Cards for Draft stories | Skipped DoR filter | Only import `dor_passed=true` rows |
| Column shift in spreadsheet | Unquoted multiline field | Fix quoting per COLUMNS.md |
| Missing estimate on card | Mapped `ai_estimate_hours` instead of final | Use `final_estimate_hours` |
| Duplicate cards | Re-ran import | Dedupe by `story_id` + `sprint_id` label |
| Dependency IDs orphaned | No matching card | Create placeholder cards or note in description |

## Smoke Test Procedure

Run before pilot kickoff (validation checklist item 5).

1. Create Trello test board **NOVA-SMOKE**.
2. Create list `sprint-baseline-01`.
3. Recreate cards from [`sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv) rows 1–3 (Procedure B).
4. **Assert:**
   - [ ] ≥3 cards created (≥5 if using extended test data)
   - [ ] Card 1 name = `Sprint worksheet CSV export`
   - [ ] Card 1 description preserves multiline AC with comma
   - [ ] Card 1 member = Alex Chen
   - [ ] Card 1 shows 5h final estimate
   - [ ] Rows 4–5 intentionally skipped
5. Record results in [`recipe-validation-log.md`](recipe-validation-log.md).

## Related

- [`COLUMNS.md`](COLUMNS.md)
- [`jira-recipe.md`](jira-recipe.md)
- [`generic-fallback.md`](generic-fallback.md)
- [`3apk-plan-sprint`](../skills/3apk-plan-sprint/SKILL.md)
