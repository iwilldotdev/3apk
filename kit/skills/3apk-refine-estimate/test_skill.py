#!/usr/bin/env python3
"""Protocol and schema checks for kit/skills/3apk-refine-estimate/SKILL.md.

Run from repository root:
  python3 kit/skills/3apk-refine-estimate/test_skill.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml
from jsonschema import RefResolver

ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = Path(__file__).resolve().parent / "SKILL.md"
EXAMPLE_PATH = ROOT / "kit" / "fixtures" / "refine-estimate-example.md"
SCHEMA_DIR = ROOT / "kit" / "notion" / "schema"

# Estimation guardrails documented in SKILL.md (>=80% coverage target)
ESTIMATION_GUARDRAILS = [
    ("range_only", r"\*\*Range only\*\*"),
    ("rationale_required", r"\*\*Rationale required\*\*"),
    ("ac_coverage", r"\*\*AC coverage\*\*"),
    ("unknowns_widen_range", r"\*\*Unknowns widen range\*\*"),
    ("no_false_finality", r"\*\*No false finality\*\*"),
    ("human_authority", r"\*\*Human authority\*\*"),
    ("schema_mapping", r"\*\*Schema mapping\*\*"),
    ("conservative_bias", r"\*\*Conservative bias\*\*"),
    ("points_optional", r"\*\*Points optional\*\*"),
    ("no_scope_creep", r"\*\*No scope creep\*\*"),
]

FORBIDDEN_FINAL_LABELS = (
    "final estimate",
    "committed estimate",
    "sprint-ready hours",
    "team estimate",
)

COMPLEXITY_DRIVER_TOPICS = (
    r"integration",
    r"non-functional|NFR",
    r"data volume|edge-case",
    r"team familiarity|greenfield",
    r"automated test|manual QA",
)

UNIT_ASSERTIONS = [
    ("hard_gate_before_risks", r"Do NOT invoke `3apk-refine-risks`"),
    ("hard_gate_block_tag", r"<HARD-GATE>"),
    ("one_question_per_turn", r"one question per turn"),
    ("disclaimer_16_percent", r"~16%"),
    ("disclaimer_human_authority", r"human sign-off|Human authority|MUST set `final_estimate_hours`"),
    ("disclaimer_ai_hint_only", r"AI estimate hint|hints only|not a sprint commitment"),
    ("output_low_high_range", r"\*\*low:\*\*|\*\*low\*\*.*\*\*high\*\*"),
    ("schema_link_estimate_hours", r"estimate_hours"),
    ("schema_link_estimate_points", r"estimate_points"),
    ("schema_link_ai_estimate_hours", r"ai_estimate_hours"),
    ("handoff_refine_risks", r"3apk-refine-risks"),
    ("forbid_final_estimate_label", r"Do NOT label AI output as \*\*final estimate\*\*"),
    ("paste_block_not_commitment", r"NOT sprint commitment"),
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


def resolver_for(name: str) -> RefResolver:
    base = (SCHEMA_DIR / name).as_uri()
    store = {
        (SCHEMA_DIR / "backlog-item.json").as_uri(): load_schema("backlog-item.json"),
        (SCHEMA_DIR / "dor-checklist.json").as_uri(): load_schema("dor-checklist.json"),
    }
    return RefResolver(base, load_schema(name), store=store)


def extract_example_hint() -> dict:
    text = EXAMPLE_PATH.read_text(encoding="utf-8")
    match = re.search(r"```json\n(\{.*?\})\n```", text, re.DOTALL)
    assert match, "refine-estimate-example.md missing JSON hint block"
    payload = json.loads(match.group(1))
    assert "estimate_hours" in payload, "example must include optional estimate_hours hint"
    assert "acceptance_criteria" in payload and len(payload["acceptance_criteria"]) >= 3
    return payload


def extract_example_range() -> tuple[float, float, float]:
    text = EXAMPLE_PATH.read_text(encoding="utf-8")
    low_match = re.search(r"\*\*low:\*\* (\d+)", text)
    high_match = re.search(r"\*\*high:\*\* (\d+)", text)
    mid_match = re.search(r"midpoint[^:]*:\*\* (\d+)", text)
    assert low_match and high_match and mid_match, "example must document low/high/midpoint hours"
    low = float(low_match.group(1))
    high = float(high_match.group(1))
    mid = float(mid_match.group(1))
    assert low < high, "range low must be less than high"
    assert low <= mid <= high, "midpoint must fall within low/high"
    return low, high, mid


def skill_never_commits_final_estimate(body: str) -> None:
    paste_section = body.split("### Paste Block", 1)[-1]
    for label in FORBIDDEN_FINAL_LABELS:
        assert label not in paste_section.lower() or "do not" in paste_section.lower(), (
            f"Paste Block must not present '{label}' as committed output"
        )
    assert "final_estimate_hours" in body, "must reference final_estimate_hours as human-owned field"
    assert re.search(r"Do NOT.*final estimate", body, re.IGNORECASE), (
        "must forbid labeling AI output as final estimate"
    )


def run_unit_tests(body: str, frontmatter: dict) -> tuple[int, int]:
    passed = 0
    total = len(UNIT_ASSERTIONS) + len(ESTIMATION_GUARDRAILS) + len(COMPLEXITY_DRIVER_TOPICS) + 3

    assert frontmatter.get("name") == "3apk-refine-estimate", "frontmatter name mismatch"
    passed += 1
    assert frontmatter.get("description"), "frontmatter description required"
    passed += 1
    assert "hint" in frontmatter.get("description", "").lower(), "description must mention hints"
    passed += 1

    for label, pattern in UNIT_ASSERTIONS:
        assert re.search(pattern, body, re.IGNORECASE), f"unit check failed: {label}"
        passed += 1

    documented = 0
    for _label, pattern in ESTIMATION_GUARDRAILS:
        if re.search(pattern, body, re.IGNORECASE):
            documented += 1
            passed += 1

    coverage = documented / len(ESTIMATION_GUARDRAILS)
    assert coverage >= 0.8, f"estimation guardrail coverage {coverage:.0%} < 80%"

    driver_hits = sum(1 for pattern in COMPLEXITY_DRIVER_TOPICS if re.search(pattern, body, re.IGNORECASE))
    assert driver_hits >= 3, "clarification questions must cover unknown complexity drivers"
    passed += driver_hits

    skill_never_commits_final_estimate(body)
    passed += 1
    total += 1

    return passed, total


def run_integration_tests() -> None:
    payload = extract_example_hint()
    low, high, mid = extract_example_range()

    assert payload["estimate_hours"] == mid, "example estimate_hours must equal range midpoint"
    assert low <= payload["estimate_hours"] <= high, "hint must map inside documented range"

    partial_item = {
        "id": payload["id"],
        "title": "Sprint worksheet CSV export",
        "status": payload["status"],
        "acceptance_criteria": payload["acceptance_criteria"],
        "estimate_hours": payload["estimate_hours"],
        "estimate_points": payload.get("estimate_points"),
        "dor": {
            "problem_clear": True,
            "testable_ac": True,
            "dependencies_surfaced": False,
            "nfr_flags_set": True,
            "passed": False,
        },
    }

    schema = load_schema("backlog-item.json")
    resolver = resolver_for("backlog-item.json")
    jsonschema.validate(partial_item, schema, resolver=resolver)

    worksheet_row = {
        "story_id": payload["id"],
        "sprint_id": "nova-sprint-01",
        "ai_estimate_hours": payload["estimate_hours"],
        "final_estimate_hours": payload["estimate_hours"] + 2,
        "human_adjustment_log": "Team added buffer for Jira import edge cases",
    }
    ws_schema = load_schema("sprint-worksheet-row.json")
    jsonschema.validate(worksheet_row, ws_schema)


def main() -> int:
    frontmatter, body = load_skill()
    passed, total = run_unit_tests(body, frontmatter)
    run_integration_tests()
    print(f"3apk-refine-estimate protocol checks: {passed}/{total} passed.")
    print("Integration: fixture AC hint validates against backlog-item schema.")
    print("Integration: example range (low/high/midpoint) maps to optional estimate_hours.")
    print("Verification: skill never presents AI range as committed sprint estimate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
