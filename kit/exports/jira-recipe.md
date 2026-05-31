# Jira Export Recipe — Canonical CSV → Issues

> **Scope:** Manual CSV import or copy-paste only. No Jira REST API, webhooks, or automation (ADR-001, PRD Non-Goals).
> **Source CSV contract:** [`COLUMNS.md`](COLUMNS.md) — fixed 13-column order, UTF-8, RFC 4180 quoting.
> **Golden fixture:** [`sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv)

## Prerequisites

1. Sprint locked in Notion Planning Worksheet (see [`3apk-plan-sprint`](../skills/3apk-plan-sprint/SKILL.md) Sprint Lock Block).
2. Exported CSV matches the header in [`COLUMNS.md`](COLUMNS.md) **character-for-character**.
3. Jira Cloud or Data Center project with permission to create issues and import CSV (admin or project admin).
4. CSV saved as **UTF-8 without BOM** (see [Encoding & Quoting](#encoding--quoting)).

## Column → Jira Field Mapping

Map every canonical column before import. Column order follows [`COLUMNS.md`](COLUMNS.md) § Column Order.

| # | CSV column | Jira field (Cloud) | Jira field (Server/DC) | Required on import | Notes |
|---|------------|-------------------|------------------------|-------------------|-------|
| 1 | `story_id` | **External issue ID** or **Labels** (`3apk:{story_id}`) | Same | Recommended | Preserves backlog traceability; use External ID if your project supports it |
| 2 | `sprint_id` | **Fix Version/s** or **Sprint** (if board configured) or **Labels** (`sprint:{sprint_id}`) | Same | Recommended | Jira Sprint field requires board association; labels are a safe fallback |
| 3 | `title` | **Summary** | **Summary** | **Yes** | Primary issue title |
| 4 | `user_story` | **Description** (prepend block) | **Description** | Recommended | Place above AC in description |
| 5 | `acceptance_criteria` | **Description** (append block) or **Acceptance Criteria** (if team uses that custom field) | Same | **Yes** | Preserve `\n` line breaks; see multiline handling below |
| 6 | `ai_estimate_hours` | **Description** (Estimate section) or custom **AI Estimate** field | Same | Optional | Informational only — not the committed estimate |
| 7 | `final_estimate_hours` | **Original Estimate** (hours) or **Time Tracking** estimate | Same | **Yes** | Use `h` suffix if importer expects duration string (e.g. `5h`) |
| 8 | `final_estimate_points` | **Story Points** (custom field) | Same | Optional | Map only if your project uses points |
| 9 | `human_adjustment_log` | **Description** (Adjustment log section) or **Comment** on create | Same | Recommended | Audit trail for PEX evidence |
| 10 | `assigned_to` | **Assignee** | **Assignee** | Recommended | Must match Jira username/email; leave blank if user not in directory |
| 11 | `dor_passed` | **Labels** (`dor-passed` / `dor-failed`) or **Description** footer | Same | Recommended | Import only rows where `dor_passed=true` for sprint commitment |
| 12 | `dependencies` | **Issue Links** (blocks/is blocked by) or **Description** (Dependencies) | Same | Optional | Comma-separated IDs from backlog; link after import if CSV import cannot create links |
| 13 | `status` | **Status** (on create) or **Labels** (`backlog:{status}`) | Same | Optional | Map `Planned` → `To Do`; do not import `Draft` / `DoR_Fail` rows into active sprint |

**Mapping coverage:** 13/13 columns documented (100%).

### Composed Description Template

When Jira accepts a single Description field, merge worksheet narrative fields:

```markdown
## User Story
{user_story}

## Acceptance Criteria
{acceptance_criteria}

## Estimates
- AI hint (hours): {ai_estimate_hours}
- Final estimate (hours): {final_estimate_hours}
- Story points: {final_estimate_points}

## Human Adjustment Log
{human_adjustment_log}

## Metadata
- Story ID: {story_id}
- Sprint ID: {sprint_id}
- DoR passed: {dor_passed}
- Dependencies: {dependencies}
- Backlog status: {status}
```

## Procedure A — CSV Import (bulk, ≥5 issues)

1. **Filter rows:** Keep rows where `dor_passed` = `true` and `status` is `Planned` or `DoR_Pass`. Skip `Draft` and `DoR_Fail` (see fixture rows 4–5).
2. **Open Jira:** **Settings (⚙) → System → Import & Export → External System Import → CSV**.
3. **Upload** your locked sprint CSV (or [`sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv) for smoke test).
4. **Map columns** using the table above. Minimum mappings for a valid sprint import:
   - `title` → **Summary**
   - `acceptance_criteria` + `user_story` → **Description** (use template)
   - `final_estimate_hours` → **Original Estimate**
   - `assigned_to` → **Assignee**
5. **Encoding:** Select **UTF-8** if the importer offers encoding choice.
6. **Validate preview:** Confirm preview shows **5 columns per row** in the importer's field preview — if AC text spans lines, the row must still show one logical record (no column shift).
7. **Import** and note created issue keys (e.g. `NOVA-101` … `NOVA-105`).

## Procedure B — Copy-Paste (single issue)

Use when CSV import is unavailable or for one-off fixes.

1. Create issue → set **Summary** from `title`.
2. Paste composed **Description** from template above.
3. Set **Original Estimate** from `final_estimate_hours`.
4. Set **Assignee** from `assigned_to`.
5. Add label `3apk:{story_id}` and `sprint:{sprint_id}`.

## Worked Example — `sample-worksheet-export.csv`

Fixture path: [`kit/fixtures/sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv)

| Row | story_id | sprint_id | title | dor_passed | status | Import? |
|-----|----------|-----------|-------|------------|--------|---------|
| 1 | nova-003 | sprint-baseline-01 | Sprint worksheet CSV export | true | DoR_Pass | ✅ Yes |
| 2 | nova-003 | sprint-intervention-02 | Sprint worksheet CSV export | true | Planned | ✅ Yes |
| 3 | nova-003 | sprint-evidence-03 | Sprint worksheet CSV export | true | Planned | ✅ Yes |
| 4 | nova-001 | sprint-baseline-01 | Add OAuth provider… | false | Draft | ❌ Skip (DoR gate) |
| 5 | nova-002 | sprint-baseline-01 | Billing webhook retry logic | false | DoR_Fail | ❌ Skip (DoR gate) |

**Row 1 — multiline AC (column-shift test):**

The `acceptance_criteria` cell contains commas *and* embedded newlines. It is RFC 4180 quoted in the fixture:

```csv
"Given DoR-passed stories in the worksheet
When I export CSV
Then the file uses the 13-column order from COLUMNS.md
Given acceptance criteria contain commas, or line breaks
When exported
Then fields are RFC 4180 quoted"
```

After import, issue **Summary** = `Sprint worksheet CSV export`; **Description** AC block must show **four** Given/When/Then lines with the comma in *"commas, or line breaks"* preserved.

**Expected smoke-test outcome:** Importing rows 1–3 yields **≥3 issues** (≥5 if you include negative-row validation as skipped). Full checklist target: **≥5 issues** when using an expanded test CSV or importing all DoR-pass rows plus linked sub-tasks — with the golden fixture, **3 committed sprint issues** plus **2 rejected rows** validates the DoR filter.

## Encoding & Quoting

Follow [`COLUMNS.md`](COLUMNS.md) § Type Rules and § Quoting Rules:

| Rule | Requirement |
|------|-------------|
| Encoding | UTF-8, no BOM |
| Line endings | LF preferred; CRLF acceptable on input |
| Commas in text | Field MUST be double-quoted |
| Newlines in AC | Field MUST be double-quoted; join AC lines with `\n` |
| Embedded `"` | Escape as `""` |
| Boolean | Lowercase `true` / `false` |

**Pre-import check:** Open CSV in a text editor (not Excel alone). Confirm header matches:

```
story_id,sprint_id,title,user_story,acceptance_criteria,ai_estimate_hours,final_estimate_hours,final_estimate_points,human_adjustment_log,assigned_to,dor_passed,dependencies,status
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Columns shifted; AC fragments in Assignee | Unquoted multiline `acceptance_criteria` | Re-export with quoting per COLUMNS.md; validate with [`validate_fixtures.py`](../fixtures/validate_fixtures.py) |
| Mojibake (`Ã©`, `â€™`) | Wrong encoding (Latin-1/Windows-1252) | Re-save CSV as UTF-8 without BOM |
| Import rejects Assignee | Name not in Jira user directory | Map to email; or leave blank and assign manually post-import |
| Duplicate issues on re-import | Same CSV imported twice | Use `story_id` as External ID or label dedup |
| Empty Original Estimate | Column mapped to wrong field | Map `final_estimate_hours` not `ai_estimate_hours` |
| Draft stories in sprint | Imported rows 4–5 without filtering | Filter `dor_passed=true` before import |
| Missing dependencies | CSV import cannot create links | Add **Issue Links** manually using `dependencies` column post-import |

## Smoke Test Procedure

Run before pilot kickoff (validation checklist item 4).

1. Create a Jira test project (e.g. `NOVA-SMOKE`).
2. Import [`sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv) per **Procedure A**.
3. **Assert:**
   - [ ] ≥3 issues created from DoR-pass rows (rows 1–3)
   - [ ] Row 1 Summary = `Sprint worksheet CSV export`
   - [ ] Row 1 Description contains multiline AC with comma *"commas, or line breaks"*
   - [ ] Row 1 Original Estimate = `5` (hours) or `5h` per project config
   - [ ] Row 1 Assignee = `Alex Chen` (or mapped user)
   - [ ] Rows 4–5 **not** imported when DoR filter applied
4. Record results in [`recipe-validation-log.md`](recipe-validation-log.md).

## Related

- [`COLUMNS.md`](COLUMNS.md) — canonical column order
- [`trello-recipe.md`](trello-recipe.md) — Trello card mapping
- [`generic-fallback.md`](generic-fallback.md) — other tools
- [`3apk-plan-sprint`](../skills/3apk-plan-sprint/SKILL.md) — export handoff after lock
