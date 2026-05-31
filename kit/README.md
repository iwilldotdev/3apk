# 3APK Kit

AI-Augmented Agile Planning Kit — portable artifacts for refinement, sprint planning, and export.

## Directory Map

| Directory | Purpose | Key files |
|-----------|---------|-----------|
| [`notion/`](notion/) | Notion hub setup + JSON Schema contracts | `SPEC.md`, `schema/*.json` |
| [`skills/`](skills/) | Portable LLM skills (4 refinement + 1 planning) | `3apk-refine-*/SKILL.md`, `3apk-plan-sprint/SKILL.md` |
| [`exports/`](exports/) | Canonical CSV + Jira/Trello/generic recipes | `COLUMNS.md`, `jira-recipe.md`, `trello-recipe.md` |
| [`fixtures/`](fixtures/) | Sample CSV/JSON for validation | `sample-backlog-items.json`, `sample-worksheet-export.csv` |

## Quick Start

1. **Notion hub** — [`notion/SPEC.md`](notion/SPEC.md): Backlog, Sprints, Planning Worksheet, Metrics.
2. **Skills** — copy `skills/*/SKILL.md` to your LLM chat/IDE.
3. **Refinement chain** — `3apk-refine-story` → `ac` → `estimate` → `risks`; paste into Notion.
4. **Sprint planning** — `3apk-plan-sprint` on DoR-passed items; export via [`exports/COLUMNS.md`](exports/COLUMNS.md).
5. **Validate** — [`fixtures/`](fixtures/) + `python3 fixtures/validate_fixtures.py`.

Full usage guide: root [`README.md`](../README.md).

## Architecture

JSON Schema files in `notion/schema/` are the single source of truth for Notion fields, skill outputs, and CSV columns. No application server or Notion API integration in V1.

- **Human-in-the-loop:** the team approves every story layer and final estimates.
- **LLM-agnostic:** Markdown skills work in any chat or IDE.
- **Canonical CSV:** [`exports/COLUMNS.md`](exports/COLUMNS.md) for Jira/Trello import.
