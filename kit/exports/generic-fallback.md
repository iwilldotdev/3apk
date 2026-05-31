# Generic Export Fallback — CSV & Markdown Copy-Paste

> **Scope:** Manual copy-paste to **any** task tool (ClickUp, Monday, GitHub Issues, Linear, Asana, etc.). No tool-specific API steps (ADR-001).
> **Source CSV contract:** [`COLUMNS.md`](COLUMNS.md) — fixed 13-column order.
> **Golden fixture:** [`sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv)

Use this fallback when your team does not use Jira or Trello. For Jira/Trello, prefer the dedicated recipes:

- [`jira-recipe.md`](jira-recipe.md)
- [`trello-recipe.md`](trello-recipe.md)

## When to Use

- Target tool has no CSV import or no documented 3APK recipe in V1.
- Facilitator needs a **single-story Markdown block** for Slack/email/PR description.
- Pilot evidence requires tool-agnostic artifact paste.

## Canonical CSV (whole sprint)

Export the locked worksheet as CSV per [`COLUMNS.md`](COLUMNS.md). Import into any tool that accepts generic CSV:

1. Confirm header row (13 columns, exact order):

```
story_id,sprint_id,title,user_story,acceptance_criteria,ai_estimate_hours,final_estimate_hours,final_estimate_points,human_adjustment_log,assigned_to,dor_passed,dependencies,status
```

2. Filter `dor_passed=true` before import.
3. Map columns using the **Generic Column Map** below.
4. Preserve UTF-8 encoding and quoted multiline fields.

### Generic Column Map

| # | CSV column | Suggested target in any tool | Notes |
|---|------------|------------------------------|-------|
| 1 | `story_id` | External ID / reference field | |
| 2 | `sprint_id` | Sprint / iteration field | |
| 3 | `title` | Title / name | **Required** |
| 4 | `user_story` | Description (part 1) | |
| 5 | `acceptance_criteria` | Description (part 2) or checklist | **Required** |
| 6 | `ai_estimate_hours` | Custom number / notes | |
| 7 | `final_estimate_hours` | Estimate / effort field | **Required** |
| 8 | `final_estimate_points` | Points field | |
| 9 | `human_adjustment_log` | Comments / notes | |
| 10 | `assigned_to` | Assignee | |
| 11 | `dor_passed` | Tag / label | |
| 12 | `dependencies` | Depends-on links | |
| 13 | `status` | Status / column | |

## Single-Story Markdown Template

Copy one row from the CSV into this block for paste into any issue tracker:

```markdown
### {title}

**Story ID:** {story_id}  
**Sprint:** {sprint_id}  
**Assignee:** {assigned_to}  
**Status:** {status} | **DoR passed:** {dor_passed}

#### User Story
{user_story}

#### Acceptance Criteria
{acceptance_criteria}

#### Estimates
| Field | Value |
|-------|-------|
| AI hint (hours) | {ai_estimate_hours} |
| Final estimate (hours) | {final_estimate_hours} |
| Story points | {final_estimate_points} |

#### Human Adjustment Log
{human_adjustment_log}

#### Dependencies
{dependencies}
```

Replace `{placeholders}` from the CSV row. For multiline `acceptance_criteria`, paste verbatim — line breaks become Markdown list items if prefixed with `- `.

## Worked Example — Row 1 from `sample-worksheet-export.csv`

Source: [`kit/fixtures/sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv), row 1.

```markdown
### Sprint worksheet CSV export

**Story ID:** nova-003  
**Sprint:** sprint-baseline-01  
**Assignee:** Alex Chen  
**Status:** DoR_Pass | **DoR passed:** true

#### User Story
As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello.

#### Acceptance Criteria
Given DoR-passed stories in the worksheet
When I export CSV
Then the file uses the 13-column order from COLUMNS.md
Given acceptance criteria contain commas, or line breaks
When exported
Then fields are RFC 4180 quoted

#### Estimates
| Field | Value |
|-------|-------|
| AI hint (hours) | 4 |
| Final estimate (hours) | 5 |
| Story points | 5 |

#### Human Adjustment Log
Increased from 4h — CSV quoting and cross-tool import edge cases

#### Dependencies
(none)
```

## Worked Example — Row 3 (minimal adjustment log)

```markdown
### Sprint worksheet CSV export

**Story ID:** nova-003  
**Sprint:** sprint-evidence-03  
**Assignee:** Sam Rivera  
**Status:** Planned | **DoR passed:** true

#### User Story
As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello.

#### Acceptance Criteria
Given a completed export
When I import into Jira using the recipe
Then all required issue fields populate

#### Estimates
| Field | Value |
|-------|-------|
| AI hint (hours) | 3.5 |
| Final estimate (hours) | 3.5 |
| Story points | 3 |

#### Human Adjustment Log
No adjustment — team aligned with AI range midpoint

#### Dependencies
(none)
```

## Encoding & Quoting

All CSV exports MUST follow [`COLUMNS.md`](COLUMNS.md) § Quoting Rules:

- UTF-8, no BOM
- Quote fields containing commas, quotes, or newlines
- Escape `"` as `""`
- Boolean: lowercase `true` / `false`

When pasting Markdown, encoding is plain UTF-8 text — no CSV escaping needed.

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Broken Markdown tables | Pipe `\|` in AC text | Escape or use bullet list instead of table |
| Lost line breaks | Pasted into single-line field | Use tool's rich-text / Markdown mode |
| Wrong column data in assignee | CSV column shift | Validate CSV with `validate_fixtures.py` |
| Draft stories committed | No DoR filter | Import only `dor_passed=true` |

## Batch Markdown Export (optional)

For tools accepting bulk Markdown (e.g. wiki sprint page):

1. Filter DoR-pass rows from CSV.
2. For each row, render the **Single-Story Markdown Template**.
3. Concatenate with `---` horizontal rules between stories.
4. Paste into sprint wiki / Notion export page.

## Smoke Test

1. Render row 1 from [`sample-worksheet-export.csv`](../fixtures/sample-worksheet-export.csv) using the template above.
2. Paste into a blank GitHub Issue or your team's tool.
3. Confirm title, 4-line AC block, estimate table, and adjustment log render correctly.
4. Record in [`recipe-validation-log.md`](recipe-validation-log.md).

## Related

- [`COLUMNS.md`](COLUMNS.md) — column order reference
- [`jira-recipe.md`](jira-recipe.md) · [`trello-recipe.md`](trello-recipe.md)
