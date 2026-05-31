#!/usr/bin/env python3
"""Protocol and schema checks for kit/skills/3apk-plan-sprint/SKILL.md.

Run from repository root:
  python3 kit/skills/3apk-plan-sprint/test_skill.py
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = Path(__file__).resolve().parent / "SKILL.md"
EXAMPLE_PATH = ROOT / "kit" / "fixtures" / "plan-sprint-example.md"
SCHEMA_DIR = ROOT / "kit" / "notion" / "schema"
COLUMNS_MD = ROOT / "kit" / "exports" / "COLUMNS.md"
GOLDEN_CSV = ROOT / "kit" / "fixtures" / "sample-worksheet-export.csv"
BACKLOG_FIXTURE = ROOT / "kit" / "fixtures" / "sample-backlog-items.json"

EXPECTED_HEADER = (
    "story_id,sprint_id,title,user_story,acceptance_criteria,"
    "ai_estimate_hours,final_estimate_hours,final_estimate_points,"
    "human_adjustment_log,assigned_to,dor_passed,dependencies,status"
)

PROTOCOL_STEPS = [
    ("acknowledge_input", r"Acknowledge input|restate `sprint_id`"),
    ("validate_dor", r"Validate DoR|Input Validation"),
    ("reject_non_dor", r"REJECT item|Cannot plan"),
    ("capacity_preview", r"Capacity preview|capacity summary table"),
    ("balancing_questions", r"Capacity vs Commitment Balancing|Balancing questions"),
    ("ai_hints", r"Draft AI hints|ai_estimate_hours"),
    ("per_story_estimates", r"Per-Story Estimate Prompt"),
    ("human_adjustment_log", r"Human adjustment log rules|human_adjustment_log"),
    ("capacity_check", r"Capacity check|sum `final_estimate_hours`"),
    ("over_capacity", r"Over-Capacity Protocol|Over-capacity confirmation"),
    ("draft_approval", r"Approve this sprint draft for lock"),
    ("hard_gate_lock", r"Do NOT emit the \*\*Sprint Lock Block\*\*"),
    ("sprint_lock_checklist", r"Sprint Lock Checklist"),
    ("notion_integration", r"Notion Planning Worksheet Integration|Notion Paste Field Mapping"),
    ("export_handoff", r"Export Handoff|jira-recipe\.md"),
]

UNIT_ASSERTIONS = [
    ("hard_gate_block_tag", r"<HARD-GATE>"),
    ("hard_gate_before_lock", r"Do NOT emit the \*\*Sprint Lock Block\*\*"),
    ("hard_gate_before_export", r"Do NOT.*CSV export|export before lock"),
    ("one_question_per_turn", r"one question per turn"),
    ("schema_link_worksheet_row", r"sprint-worksheet-row\.json"),
    ("schema_link_columns", r"COLUMNS\.md"),
    ("dor_passed_input", r"`dor\.passed`|dor_passed"),
    ("ai_vs_final_columns", r"AI hint vs final estimate"),
    ("worksheet_row_template", r"Worksheet Row Output Template"),
    ("sprint_lock_block", r"Sprint Lock Block"),
    ("golden_csv_reference", r"sample-worksheet-export\.csv"),
    ("spec_notion_reference", r"kit/notion/SPEC\.md"),
    ("reject_dor_fail", r"DoR_Fail|dor\.passed.*false"),
    ("planning_smoke_test", r"Planning Smoke Test Procedure"),
]


def load_skill() -> tuple[dict, str]:
    text = SKILL_PATH.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, "SKILL.md missing YAML frontmatter"
    frontmatter = yaml.safe_load(match.group(1))
    return frontmatter, text


def load_schema(name: str) -> dict:
    with (SCHEMA_DIR / name).open(encoding="utf-8") as f:
        return json.load(f)


def extract_example_worksheet_rows() -> list[dict]:
    text = EXAMPLE_PATH.read_text(encoding="utf-8")
    match = re.search(r"### worksheet_rows \(schema-validated\)\s*\n\n```json\n(\[.*?\])\n```", text, re.DOTALL)
    assert match, "plan-sprint-example.md missing worksheet_rows JSON array"
    rows = json.loads(match.group(1))
    assert isinstance(rows, list), "worksheet_rows must be a JSON array"
    assert len(rows) >= 3, "expected >=3 worksheet rows in example"
    return rows


def load_fixture_items() -> list[dict]:
    return json.loads(BACKLOG_FIXTURE.read_text(encoding="utf-8"))


def parse_columns_header() -> str:
    text = COLUMNS_MD.read_text(encoding="utf-8")
    match = re.search(r"```\n(story_id,sprint_id,.*?)\n```", text)
    assert match, "COLUMNS.md missing header block"
    return match.group(1).strip()


def row_to_csv_line(row: dict, backlog: dict) -> list[str]:
    deps = backlog.get("dependencies") or []
    dep_str = ",".join(deps) if deps else ""
    status = "Planned"
    return [
        row["story_id"],
        row["sprint_id"],
        row["title"],
        row["user_story"],
        row["acceptance_criteria"],
        str(row.get("ai_estimate_hours", "")),
        str(row["final_estimate_hours"]),
        str(row.get("final_estimate_points", "")),
        row["human_adjustment_log"],
        row.get("assigned_to", ""),
        "true" if row.get("dor_passed") else "false",
        dep_str,
        status,
    ]


def run_unit_tests(body: str, frontmatter: dict) -> tuple[int, int]:
    passed = 0
    total = len(UNIT_ASSERTIONS) + len(PROTOCOL_STEPS) + 4

    assert frontmatter.get("name") == "3apk-plan-sprint", "frontmatter name mismatch"
    passed += 1
    assert frontmatter.get("description"), "frontmatter description required"
    passed += 1
    desc = frontmatter.get("description", "").lower()
    assert "capacity" in desc or "sprint" in desc, "description must mention sprint planning"
    passed += 1
    assert "dor" in desc.lower() or "worksheet" in desc.lower(), "description must mention DoR or worksheet"
    passed += 1

    for label, pattern in UNIT_ASSERTIONS:
        assert re.search(pattern, body, re.IGNORECASE | re.DOTALL), f"unit check failed: {label}"
        passed += 1

    documented = 0
    for _label, pattern in PROTOCOL_STEPS:
        if re.search(pattern, body, re.IGNORECASE):
            documented += 1
            passed += 1

    coverage = documented / len(PROTOCOL_STEPS)
    assert coverage >= 0.8, f"planning protocol coverage {coverage:.0%} < 80%"

    assert re.search(r"human_adjustment_log", body), "must document human_adjustment_log"
    assert re.search(r"final_estimate_hours", body), "must document final_estimate_hours"

    return passed, total


def validate_adjustment_logs(rows: list[dict]) -> None:
    for row in rows:
        log = row.get("human_adjustment_log", "")
        assert log.strip(), f"{row['story_id']}: human_adjustment_log must be non-empty"
        ai = row.get("ai_estimate_hours")
        final = row["final_estimate_hours"]
        if ai is not None and final != ai:
            assert len(log) > 10, f"{row['story_id']}: changed estimate needs substantive log"


def run_integration_tests() -> None:
    schema = load_schema("sprint-worksheet-row.json")
    rows = extract_example_worksheet_rows()

    for row in rows:
        jsonschema.validate(row, schema)
        assert row["dor_passed"] is True, f"{row['story_id']} must have dor_passed true"

    validate_adjustment_logs(rows)

    capacity = 24.0
    buffer = capacity * 0.10
    effective = capacity - buffer
    committed = sum(r["final_estimate_hours"] for r in rows)
    assert committed <= effective, f"feasible sprint draft exceeds effective capacity: {committed} > {effective}"
    assert len(rows) >= 3, "integration requires >=3 DoR-passed stories in draft"

    items = load_fixture_items()
    dor_fail = next(item for item in items if item["status"] == "DoR_Fail")
    assert dor_fail["dor"]["passed"] is False
    assert dor_fail["status"] == "DoR_Fail"

    dor_pass = next(item for item in items if item["status"] == "DoR_Pass")
    assert dor_pass["id"] == "nova-003"
    assert dor_pass["dor"]["passed"] is True

    header_from_columns = parse_columns_header()
    assert header_from_columns == EXPECTED_HEADER, "COLUMNS.md header mismatch"

    with GOLDEN_CSV.open(encoding="utf-8", newline="") as f:
        golden_header = next(csv.reader(f))
    assert ",".join(golden_header) == EXPECTED_HEADER, "golden CSV header mismatch"

    backlog_by_id = {dor_pass["id"]: dor_pass}
    sample_row = rows[0]
    csv_fields = row_to_csv_line(sample_row, backlog_by_id.get(sample_row["story_id"], {}))
    assert len(csv_fields) == 13, "CSV row must have 13 columns"

    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(golden_header)
    writer.writerow(csv_fields)
    rendered = output.getvalue()
    assert "nova-003" in rendered
    assert "Planned" in rendered

    example_text = EXAMPLE_PATH.read_text(encoding="utf-8")
    assert re.search(r"Over-Capacity Variant|over-capacity", example_text, re.IGNORECASE)
    assert re.search(r"Q4|scope reduction|defer", example_text, re.IGNORECASE)
    assert "nova-002" in example_text, "example must show DoR_Fail rejection"


def main() -> int:
    frontmatter, body = load_skill()
    passed, total = run_unit_tests(body, frontmatter)
    run_integration_tests()
    print(f"3apk-plan-sprint protocol checks: {passed}/{total} passed.")
    print("Integration: example worksheet rows validate against sprint-worksheet-row schema.")
    print("Integration: feasible 3-story sprint draft within 24h capacity (10% buffer).")
    print("Integration: CSV row shape matches COLUMNS.md / sample-worksheet-export.csv header.")
    print("Integration: over-capacity variant and DoR_Fail rejection documented in example.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
