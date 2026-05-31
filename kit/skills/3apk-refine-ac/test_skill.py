#!/usr/bin/env python3
"""Protocol and schema checks for kit/skills/3apk-refine-ac/SKILL.md.

Run from repository root:
  python3 kit/skills/3apk-refine-ac/test_skill.py
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
EXAMPLE_PATH = ROOT / "kit" / "fixtures" / "refine-ac-example.md"
SCHEMA_DIR = ROOT / "kit" / "notion" / "schema"
BACKLOG_FIXTURE = ROOT / "kit" / "fixtures" / "sample-backlog-items.json"

# Must appear in SKILL.md body (unit / protocol coverage)
AC_QUALITY_RULES = [
    ("testable", r"\*\*Testable\*\*"),
    ("observable", r"\*\*Observable\*\*"),
    ("no_vague_terms", r"\*\*No vague terms\*\*"),
    ("no_implementation_leakage", r"\*\*No implementation leakage\*\*"),
    ("single_behavior", r"\*\*Single behavior\*\*"),
    ("story_traceability", r"\*\*Story traceability\*\*"),
    ("given_when_then", r"Given/When/Then"),
    ("minimum_coverage", r"\*\*Minimum coverage\*\*"),
    ("edge_paths", r"\*\*Edge paths when implied\*\*"),
    ("no_duplicates", r"\*\*No duplicates\*\*"),
]

VAGUE_TERMS = ("fast", "user-friendly", "easy", "robust", "scalable", "seamless", "intuitive", "performant", "quick")

UNIT_ASSERTIONS = [
    ("hard_gate_before_estimate", r"Do NOT invoke `3apk-refine-estimate`"),
    ("hard_gate_block_tag", r"<HARD-GATE>"),
    ("one_question_per_turn", r"one question per turn"),
    ("output_array_of_strings", r"array of strings"),
    ("schema_link_acceptance_criteria", r"backlog-item\.json"),
    ("schema_link_testable_ac", r"testable_ac"),
    ("forbid_vague_fast", r"\*fast\*"),
    ("forbid_vague_user_friendly", r"\*user-friendly\*"),
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


def extract_example_ac() -> list[str]:
    text = EXAMPLE_PATH.read_text(encoding="utf-8")
    match = re.search(r"```json\n(\{.*?\})\n```", text, re.DOTALL)
    assert match, "refine-ac-example.md missing JSON AC block"
    payload = json.loads(match.group(1))
    ac = payload["acceptance_criteria"]
    assert isinstance(ac, list) and len(ac) >= 3, "example must have >=3 AC items"
    return ac


def ac_passes_quality(ac: list[str]) -> bool:
    joined = " ".join(ac).lower()
    for term in VAGUE_TERMS:
        if term in joined:
            return False
    for line in ac:
        if not line.strip():
            return False
        if "given" not in line.lower() or "when" not in line.lower() or "then" not in line.lower():
            return False
    return True


def run_unit_tests(body: str, frontmatter: dict) -> tuple[int, int]:
    passed = 0
    total = len(UNIT_ASSERTIONS) + len(AC_QUALITY_RULES) + 2  # frontmatter fields

    assert frontmatter.get("name") == "3apk-refine-ac", "frontmatter name mismatch"
    passed += 1
    assert frontmatter.get("description"), "frontmatter description required"
    passed += 1

    for label, pattern in UNIT_ASSERTIONS:
        assert re.search(pattern, body, re.IGNORECASE), f"unit check failed: {label}"
        passed += 1

    documented = 0
    for _label, pattern in AC_QUALITY_RULES:
        if re.search(pattern, body, re.IGNORECASE):
            documented += 1
            passed += 1

    coverage = documented / len(AC_QUALITY_RULES)
    assert coverage >= 0.8, f"AC quality rule coverage {coverage:.0%} < 80%"

    return passed, total


def run_integration_tests() -> None:
    ac = extract_example_ac()
    assert len(ac) >= 3, "DoR_Pass fixture example must produce >=3 AC items"
    assert ac_passes_quality(ac), "example AC fail quality heuristics (vague terms or G/W/T)"

    dor_pass = next(
        item
        for item in json.loads(BACKLOG_FIXTURE.read_text(encoding="utf-8"))
        if item["status"] == "DoR_Pass"
    )
    assert dor_pass["id"] == "nova-003"
    assert dor_pass["dor"]["testable_ac"] is True

    partial_item = {
        "id": dor_pass["id"],
        "title": dor_pass["title"],
        "status": "Refining",
        "acceptance_criteria": ac,
        "dor": {
            "problem_clear": dor_pass["dor"]["problem_clear"],
            "testable_ac": True,
            "dependencies_surfaced": dor_pass["dor"]["dependencies_surfaced"],
            "nfr_flags_set": dor_pass["dor"]["nfr_flags_set"],
            "passed": False,
        },
    }

    schema = load_schema("backlog-item.json")
    resolver = resolver_for("backlog-item.json")
    jsonschema.validate(partial_item, schema, resolver=resolver)


def main() -> int:
    frontmatter, body = load_skill()
    passed, total = run_unit_tests(body, frontmatter)
    run_integration_tests()
    print(f"3apk-refine-ac protocol checks: {passed}/{total} passed.")
    print("Integration: DoR_Pass fixture AC validates against backlog-item schema.")
    print("Integration: example AC enables testable_ac gate (>=3 testable items).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
