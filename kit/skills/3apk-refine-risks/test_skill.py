#!/usr/bin/env python3
"""Protocol and schema checks for kit/skills/3apk-refine-risks/SKILL.md.

Run from repository root:
  python3 kit/skills/3apk-refine-risks/test_skill.py
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
EXAMPLE_PATH = ROOT / "kit" / "fixtures" / "refine-risks-example.md"
SCHEMA_DIR = ROOT / "kit" / "notion" / "schema"
BACKLOG_FIXTURE = ROOT / "kit" / "fixtures" / "sample-backlog-items.json"

DOR_GATES = [
    ("problem_clear", r"`problem_clear`|Problem clear"),
    ("testable_ac", r"`testable_ac`|Testable AC"),
    ("dependencies_surfaced", r"`dependencies_surfaced`|Dependencies surfaced"),
    ("nfr_flags_set", r"`nfr_flags_set`|NFR flags set"),
]

NFR_PROMPT_TOPICS = [
    ("performance", r"### Performance|performance bounds|Performance"),
    ("security", r"### Security|security-sensitive|Security"),
    ("accessibility", r"### Accessibility|accessibility evaluation|Accessibility"),
]

DEP_RISK_QUALITY_RULES = [
    ("specific", r"\*\*Specific\*\*"),
    ("actionable", r"\*\*Actionable\*\*"),
    ("story_linked", r"\*\*Story-linked\*\*"),
    ("no_duplicates", r"\*\*No duplicates\*\*"),
    ("empty_valid", r"\*\*Empty is valid\*\*"),
    ("risk_not_ac", r"\*\*Risk ≠ AC\*\*"),
    ("dependency_not_risk", r"\*\*Dependency ≠ risk\*\*"),
    ("nfr_cross_check", r"\*\*NFR cross-check\*\*"),
]

UNIT_ASSERTIONS = [
    ("hard_gate_before_notion_paste", r"Do NOT emit the final \*\*Notion Paste Block\*\*"),
    ("hard_gate_block_tag", r"<HARD-GATE>"),
    ("one_question_per_turn", r"one question per turn"),
    ("output_dependencies_array", r"`dependencies`"),
    ("output_risks_array", r"`risks`"),
    ("schema_link_backlog_item", r"backlog-item\.json"),
    ("schema_link_dor_checklist", r"dor-checklist\.json"),
    ("dor_self_assessment_template", r"### dor_self_assessment"),
    ("notion_paste_field_mapping", r"Notion Paste Field Mapping"),
    ("chain_test_04_to_07", r"End-to-End Chain Test Procedure \(Steps 04→07\)"),
    ("four_skill_chain_summary", r"Four-Skill Refinement Chain Summary"),
    ("handoff_plan_sprint", r"3apk-plan-sprint"),
    ("status_dor_pass_fail", r"DoR_Pass|DoR_Fail"),
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


def extract_example_backlog_item() -> dict:
    text = EXAMPLE_PATH.read_text(encoding="utf-8")
    match = re.search(r"```json\n(\{.*?\})\n```", text, re.DOTALL)
    assert match, "refine-risks-example.md missing JSON backlog block"
    payload = json.loads(match.group(1))
    assert isinstance(payload.get("dependencies"), list), "example must include dependencies array"
    assert isinstance(payload.get("risks"), list), "example must include risks array"
    assert "dor" in payload and isinstance(payload["dor"], dict)
    return payload


def load_fixture_items() -> list[dict]:
    return json.loads(BACKLOG_FIXTURE.read_text(encoding="utf-8"))


def run_unit_tests(body: str, frontmatter: dict) -> tuple[int, int]:
    passed = 0
    total = (
        len(UNIT_ASSERTIONS)
        + len(DOR_GATES)
        + len(NFR_PROMPT_TOPICS)
        + len(DEP_RISK_QUALITY_RULES)
        + 3
    )

    assert frontmatter.get("name") == "3apk-refine-risks", "frontmatter name mismatch"
    passed += 1
    assert frontmatter.get("description"), "frontmatter description required"
    passed += 1
    desc = frontmatter.get("description", "").lower()
    assert "dependencies" in desc and "risks" in desc, "description must mention dependencies and risks"
    passed += 1

    for label, pattern in UNIT_ASSERTIONS:
        assert re.search(pattern, body, re.IGNORECASE), f"unit check failed: {label}"
        passed += 1

    documented_gates = 0
    for _label, pattern in DOR_GATES:
        if re.search(pattern, body, re.IGNORECASE):
            documented_gates += 1
            passed += 1

    coverage = documented_gates / len(DOR_GATES)
    assert coverage >= 0.8, f"DoR gate coverage {coverage:.0%} < 80%"

    for label, pattern in NFR_PROMPT_TOPICS:
        assert re.search(pattern, body, re.IGNORECASE), f"NFR prompt missing: {label}"
        passed += 1

    documented_rules = 0
    for _label, pattern in DEP_RISK_QUALITY_RULES:
        if re.search(pattern, body, re.IGNORECASE):
            documented_rules += 1
            passed += 1

    rules_coverage = documented_rules / len(DEP_RISK_QUALITY_RULES)
    assert rules_coverage >= 0.8, f"dep/risk quality rule coverage {rules_coverage:.0%} < 80%"

    assert re.search(r"dependencies_surfaced", body), "must document dependencies_surfaced gate"
    assert re.search(r"nfr_flags_set", body), "must document nfr_flags_set gate"

    return passed, total


def run_integration_tests() -> None:
    payload = extract_example_backlog_item()
    schema = load_schema("backlog-item.json")
    resolver = resolver_for("backlog-item.json")
    jsonschema.validate(payload, schema, resolver=resolver)

    dor = payload["dor"]
    assert dor["problem_clear"] is True
    assert dor["testable_ac"] is True
    assert dor["dependencies_surfaced"] is True
    assert dor["nfr_flags_set"] is True
    assert dor["passed"] is True
    assert payload["status"] == "DoR_Pass"

    items = load_fixture_items()
    dor_pass = next(item for item in items if item["status"] == "DoR_Pass")
    dor_fail = next(item for item in items if item["status"] == "DoR_Fail")

    assert dor_pass["id"] == "nova-003"
    assert dor_pass["dor"]["passed"] is True
    assert all(dor_pass["dor"][gate] is True for gate in (
        "problem_clear", "testable_ac", "dependencies_surfaced", "nfr_flags_set"
    ))

    assert dor_fail["id"] == "nova-002"
    assert dor_fail["dor"]["testable_ac"] is False
    assert dor_fail["dor"]["passed"] is False

    fail_item = {
        "id": dor_fail["id"],
        "title": dor_fail["title"],
        "user_story": dor_fail["user_story"],
        "acceptance_criteria": dor_fail["acceptance_criteria"],
        "dependencies": dor_fail["dependencies"],
        "risks": dor_fail["risks"],
        "dor": dor_fail["dor"],
        "status": dor_fail["status"],
    }
    jsonschema.validate(fail_item, schema, resolver=resolver)


def main() -> int:
    frontmatter, body = load_skill()
    passed, total = run_unit_tests(body, frontmatter)
    run_integration_tests()
    print(f"3apk-refine-risks protocol checks: {passed}/{total} passed.")
    print("Integration: example backlog entry validates against backlog-item schema.")
    print("Integration: DoR_Pass (nova-003) and DoR_Fail (nova-002) fixture patterns verified.")
    print("Integration: full chain 04→07 documented with fixture references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
