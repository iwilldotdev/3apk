#!/usr/bin/env python3
"""Validate 3APK golden fixtures against JSON Schema and CSV contracts.

Developer convenience script for local verification (ADR-003: no CI gate in V1).
Run from repository root: python3 kit/fixtures/validate_fixtures.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import jsonschema
from jsonschema import RefResolver

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent
SCHEMA_DIR = ROOT / "kit" / "notion" / "schema"
COLUMNS_MD = ROOT / "kit" / "exports" / "COLUMNS.md"

EXPECTED_HEADER = (
    "story_id,sprint_id,title,user_story,acceptance_criteria,"
    "ai_estimate_hours,final_estimate_hours,final_estimate_points,"
    "human_adjustment_log,assigned_to,dor_passed,dependencies,status"
)

BACKLOG_SCHEMA = "backlog-item.json"
METRIC_SCHEMA = "metric-snapshot.json"


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def resolver_for(name: str) -> RefResolver:
    base = (SCHEMA_DIR / name).as_uri()
    store = {
        (SCHEMA_DIR / "backlog-item.json").as_uri(): load_schema("backlog-item.json"),
        (SCHEMA_DIR / "dor-checklist.json").as_uri(): load_schema("dor-checklist.json"),
        (SCHEMA_DIR / "sprint-worksheet-row.json").as_uri(): load_schema(
            "sprint-worksheet-row.json"
        ),
        (SCHEMA_DIR / "metric-snapshot.json").as_uri(): load_schema("metric-snapshot.json"),
    }
    return RefResolver(base, load_schema(name), store=store)


def validate_backlog() -> None:
    items = json.loads((FIXTURES / "sample-backlog-items.json").read_text(encoding="utf-8"))
    assert len(items) == 3, f"expected 3 backlog items, got {len(items)}"

    statuses = [item["status"] for item in items]
    assert statuses.count("Draft") == 1, "expected exactly one Draft"
    assert statuses.count("DoR_Pass") == 1, "expected exactly one DoR_Pass"
    assert statuses.count("DoR_Fail") == 1, "expected exactly one DoR_Fail"

    schema = load_schema(BACKLOG_SCHEMA)
    resolver = resolver_for(BACKLOG_SCHEMA)
    for item in items:
        jsonschema.validate(item, schema, resolver=resolver)


def validate_metrics() -> None:
    snapshots = json.loads(
        (FIXTURES / "sample-metric-snapshot.json").read_text(encoding="utf-8")
    )
    assert len(snapshots) == 2, f"expected 2 metric snapshots, got {len(snapshots)}"

    phases = {s.get("phase") for s in snapshots}
    assert "baseline" in phases, "missing baseline sprint record"
    assert "intervention" in phases, "missing intervention sprint record"

    schema = load_schema(METRIC_SCHEMA)
    resolver = resolver_for(METRIC_SCHEMA)
    for snapshot in snapshots:
        jsonschema.validate(snapshot, schema, resolver=resolver)


def validate_csv() -> None:
    csv_path = FIXTURES / "sample-worksheet-export.csv"
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    assert ",".join(header) == EXPECTED_HEADER, "CSV header mismatch vs COLUMNS.md"
    assert len(header) == 13, f"expected 13 columns, got {len(header)}"
    assert len(rows) >= 5, f"expected >=5 data rows, got {len(rows)}"

    story_idx = header.index("story_id")
    hours_idx = header.index("final_estimate_hours")
    ac_idx = header.index("acceptance_criteria")

    backlog_ids = {
        item["id"]
        for item in json.loads(
            (FIXTURES / "sample-backlog-items.json").read_text(encoding="utf-8")
        )
    }

    quoted_comma_ac = False
    for row in rows:
        assert row[story_idx].strip(), "empty story_id"
        assert row[hours_idx].strip(), "empty final_estimate_hours"
        assert row[story_idx] in backlog_ids, f"unknown story_id {row[story_idx]!r}"

        ac = row[ac_idx]
        if "," in ac and ac.strip():
            quoted_comma_ac = True

    raw = csv_path.read_text(encoding="utf-8")
    assert '"Given acceptance criteria contain commas, or line breaks"' in raw or (
        "commas, or line breaks" in raw and raw.count('"') >= 2
    ), "expected quoted acceptance_criteria with comma"
    assert quoted_comma_ac, "expected at least one AC field containing a comma"


def main() -> int:
    validate_backlog()
    validate_metrics()
    validate_csv()
    print("All fixture validations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
