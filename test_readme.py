#!/usr/bin/env python3
"""Validate root README — kit links, usage sections, and path resolution.

Run from repository root:
  python3 test_readme.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"

KIT_SUBDIRS = ("skills", "notion", "exports", "fixtures")

USAGE_MARKERS = (
    "Refinar um item",
    "Planejar um sprint",
    "Registrar métricas",
    "Piloto sugerido",
)

SKILL_PATHS = (
    "kit/skills/3apk-refine-story/SKILL.md",
    "kit/skills/3apk-refine-ac/SKILL.md",
    "kit/skills/3apk-refine-estimate/SKILL.md",
    "kit/skills/3apk-refine-risks/SKILL.md",
    "kit/skills/3apk-plan-sprint/SKILL.md",
)

PEX_REPORT = "docs/relatorio-pex/relatorio-pex-ads-iii-william-santos-goncalves.pdf"


def read_readme() -> str:
    assert README.is_file(), f"Missing {README}"
    return README.read_text(encoding="utf-8")


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\]]*)\]\(([^)]+)\)", text)


def resolve_link(target: str) -> Path | None:
    if target.startswith(("http://", "https://", "#")):
        return None
    clean = target.split("#", 1)[0]
    if not clean:
        return None
    return (ROOT / clean).resolve()


def test_kit_subdirectories_linked() -> None:
    text = read_readme()
    for subdir in KIT_SUBDIRS:
        assert re.search(rf"kit/{subdir}/?", text), f"README must link to kit/{subdir}/"


def test_no_playbook_references() -> None:
    text = read_readme()
    assert "kit/playbook" not in text, "README must not reference kit/playbook/"
    assert "playbook" not in text.lower() or "playbook" not in text, (
        "README must not mention playbook"
    )
    # stricter: no word playbook at all
    assert not re.search(r"\bplaybook\b", text, re.I), "README must not mention playbook"


def test_no_compozy_references() -> None:
    text = read_readme()
    assert ".compozy" not in text, "README must not reference .compozy/"
    assert "compozy" not in text.lower(), "README must not mention Compozy"


def test_usage_sections_present() -> None:
    text = read_readme()
    for marker in USAGE_MARKERS:
        assert marker in text, f"README must include section: {marker}"


def test_all_five_skills_linked() -> None:
    text = read_readme()
    for path in SKILL_PATHS:
        assert path in text, f"README must link to {path}"
        assert (ROOT / path).is_file(), f"Skill file missing: {path}"


def test_partner_company_documented() -> None:
    text = read_readme()
    assert "RODRIGO HERPICH MULLER LTDA" in text


def test_llm_agnostic_note() -> None:
    text = read_readme()
    assert re.search(r"LLM-agnóstico|LLM agnostic|LLM-agnostic", text, re.I)


def test_pex_report_linked() -> None:
    text = read_readme()
    assert PEX_REPORT in text
    assert (ROOT / PEX_REPORT).is_file(), f"PEX report missing: {PEX_REPORT}"


def test_all_relative_links_resolve() -> None:
    text = read_readme()
    broken: list[str] = []
    for _label, target in extract_markdown_links(text):
        resolved = resolve_link(target)
        if resolved is None:
            continue
        if not resolved.exists():
            broken.append(f"{target} -> {resolved}")
    assert not broken, "Broken relative links:\n  " + "\n  ".join(broken)


def test_kit_readme_linked() -> None:
    text = read_readme()
    assert "kit/README.md" in text
    assert (ROOT / "kit/README.md").is_file()


def main() -> int:
    tests = [
        test_kit_subdirectories_linked,
        test_no_playbook_references,
        test_no_compozy_references,
        test_usage_sections_present,
        test_all_five_skills_linked,
        test_partner_company_documented,
        test_llm_agnostic_note,
        test_pex_report_linked,
        test_all_relative_links_resolve,
        test_kit_readme_linked,
    ]
    failed = 0
    for test in tests:
        name = test.__name__
        try:
            test()
            print(f"PASS {name}")
        except AssertionError as exc:
            failed += 1
            print(f"FAIL {name}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
