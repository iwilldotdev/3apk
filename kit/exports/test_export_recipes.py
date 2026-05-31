#!/usr/bin/env python3
"""Validate export recipe documentation against COLUMNS.md and golden CSV fixture.

Run from repository root:
  python3 kit/exports/test_export_recipes.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORTS = Path(__file__).resolve().parent
COLUMNS_MD = EXPORTS / "COLUMNS.md"
GOLDEN_CSV = ROOT / "kit" / "fixtures" / "sample-worksheet-export.csv"

JIRA_RECIPE = EXPORTS / "jira-recipe.md"
TRELLO_RECIPE = EXPORTS / "trello-recipe.md"
GENERIC_FALLBACK = EXPORTS / "generic-fallback.md"

EXPECTED_COLUMNS = [
    "story_id",
    "sprint_id",
    "title",
    "user_story",
    "acceptance_criteria",
    "ai_estimate_hours",
    "final_estimate_hours",
    "final_estimate_points",
    "human_adjustment_log",
    "assigned_to",
    "dor_passed",
    "dependencies",
    "status",
]

CORE_COLUMNS = ["title", "acceptance_criteria", "final_estimate_hours", "assigned_to"]

EXPECTED_HEADER = ",".join(EXPECTED_COLUMNS)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def column_in_mapping_table(text: str, column: str) -> bool:
    pattern = rf"\|\s*\d+\s*\|\s*`{re.escape(column)}`"
    return bool(re.search(pattern, text))


def count_mapped_columns(text: str) -> int:
    return sum(1 for col in EXPECTED_COLUMNS if column_in_mapping_table(text, col))


def assert_no_api_integration(text: str, recipe_name: str) -> None:
    positive_api_patterns = [
        r"curl\s+-",
        r"POST\s+/rest/",
        r"GET\s+/rest/",
        r"Authorization:\s*Bearer",
        r"api\.atlassian\.com",
        r"api\.trello\.com",
    ]
    for pattern in positive_api_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            raise AssertionError(
                f"{recipe_name} must not include API integration steps; matched: {pattern!r}"
            )
    assert re.search(r"No .* API|manual", text, re.IGNORECASE), (
        f"{recipe_name} must state manual-only scope"
    )


def assert_core_mappings(text: str, recipe_name: str, targets: dict[str, str]) -> None:
    for col in CORE_COLUMNS:
        assert column_in_mapping_table(text, col), f"{recipe_name} missing mapping for {col}"
    body_lower = text.lower()
    for col, target in targets.items():
        assert target.lower() in body_lower, f"{recipe_name} must map {col} to {target}"


def assert_columns_md_reference(text: str, recipe_name: str) -> None:
    assert "COLUMNS.md" in text, f"{recipe_name} must reference COLUMNS.md"
    assert "13-column" in text.lower() or "13 column" in text.lower(), (
        f"{recipe_name} must reference COLUMNS.md column order"
    )


def assert_fixture_reference(text: str, recipe_name: str) -> None:
    assert "sample-worksheet-export.csv" in text, (
        f"{recipe_name} must reference sample-worksheet-export.csv"
    )


def assert_encoding_docs(text: str, recipe_name: str) -> None:
    assert re.search(r"UTF-8", text), f"{recipe_name} must document UTF-8"
    assert re.search(r"quot|RFC 4180|comma", text, re.IGNORECASE), (
        f"{recipe_name} must document comma/quoting handling"
    )


def test_jira_recipe() -> None:
    text = read(JIRA_RECIPE)
    assert JIRA_RECIPE.exists(), "jira-recipe.md missing"
    mapped = count_mapped_columns(text)
    assert mapped >= 11, f"Jira mapping coverage {mapped}/13 < 80%"
    assert mapped == 13, f"Jira should document all 13 columns, got {mapped}"
    assert_core_mappings(
        text,
        "jira-recipe.md",
        {
            "title": "Summary",
            "acceptance_criteria": "Description",
            "final_estimate_hours": "Original Estimate",
            "assigned_to": "Assignee",
        },
    )
    assert_columns_md_reference(text, "jira-recipe.md")
    assert_fixture_reference(text, "jira-recipe.md")
    assert_encoding_docs(text, "jira-recipe.md")
    assert_no_api_integration(text, "jira-recipe.md")
    assert "Common Failure Modes" in text or "Failure Modes" in text
    assert "Smoke Test" in text


def test_trello_recipe() -> None:
    text = read(TRELLO_RECIPE)
    assert TRELLO_RECIPE.exists(), "trello-recipe.md missing"
    mapped = count_mapped_columns(text)
    assert mapped >= 11, f"Trello mapping coverage {mapped}/13 < 80%"
    assert mapped == 13, f"Trello should document all 13 columns, got {mapped}"
    assert_core_mappings(
        text,
        "trello-recipe.md",
        {
            "title": "Card name",
            "acceptance_criteria": "Description",
            "final_estimate_hours": "Custom Field",
            "assigned_to": "Members",
        },
    )
    assert_columns_md_reference(text, "trello-recipe.md")
    assert_fixture_reference(text, "trello-recipe.md")
    assert_encoding_docs(text, "trello-recipe.md")
    assert_no_api_integration(text, "trello-recipe.md")
    assert "Common Failure Modes" in text or "Failure Modes" in text
    assert "Smoke Test" in text


def test_generic_fallback() -> None:
    text = read(GENERIC_FALLBACK)
    assert GENERIC_FALLBACK.exists(), "generic-fallback.md missing"
    assert "Single-Story Markdown Template" in text or "Markdown Template" in text
    assert "{title}" in text and "{acceptance_criteria}" in text
    mapped = count_mapped_columns(text)
    assert mapped >= 11, f"Generic fallback mapping coverage {mapped}/13 < 80%"
    assert_columns_md_reference(text, "generic-fallback.md")
    assert_fixture_reference(text, "generic-fallback.md")
    assert_encoding_docs(text, "generic-fallback.md")
    assert "Worked Example" in text


def test_fixture_multiline_ac_no_column_shift() -> None:
    with GOLDEN_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    assert ",".join(header) == EXPECTED_HEADER, "fixture header mismatch"
    assert len(rows) >= 5, "fixture must have >=5 rows"

    ac_idx = header.index("acceptance_criteria")
    multiline_rows = [r for r in rows if "\n" in r[ac_idx]]
    assert multiline_rows, "fixture must include multiline acceptance_criteria"

    for row in rows:
        assert len(row) == 13, f"row {row[0]!r} has {len(row)} columns (column shift detected)"

    comma_ac = [r for r in rows if "," in r[ac_idx]]
    assert comma_ac, "fixture must include AC with comma (quoting test)"


def test_smoke_test_steps_documented() -> None:
    for path in (JIRA_RECIPE, TRELLO_RECIPE):
        text = read(path)
        assert re.search(r"Smoke Test", text), f"{path.name} missing smoke test section"
        assert "≥3" in text or ">=3" in text or "≥5" in text or ">=5" in text, (
            f"{path.name} smoke test must specify minimum issue/card count"
        )


def main() -> int:
    test_jira_recipe()
    test_trello_recipe()
    test_generic_fallback()
    test_fixture_multiline_ac_no_column_shift()
    test_smoke_test_steps_documented()

    jira_mapped = count_mapped_columns(read(JIRA_RECIPE))
    trello_mapped = count_mapped_columns(read(TRELLO_RECIPE))
    print(f"Export recipe checks: all unit/integration assertions passed.")
    print(f"Jira column mapping: {jira_mapped}/13 ({100 * jira_mapped // 13}%)")
    print(f"Trello column mapping: {trello_mapped}/13 ({100 * trello_mapped // 13}%)")
    print(f"Fixture CSV: {len(list(csv.reader(GOLDEN_CSV.open(encoding='utf-8')))) - 1} data rows, no column shift on multiline AC.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
