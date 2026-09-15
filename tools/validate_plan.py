"""Check the fixed curriculum and interview map without third-party packages.

Run from any working directory:
    python tools/validate_plan.py

This checks document structure, not whether a student has mastered a subject.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
COUNTS = {"A": 8, "B": 10, "C": 8, "D": 8, "E": 16, "F": 12, "G": 6, "H": 4}


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def check_ids(label: str, found: list[str], expected: set[str], errors: list[str]) -> None:
    missing = expected - set(found)
    extra = set(found) - expected
    duplicate = [item for item, count in Counter(found).items() if count > 1]
    if missing or extra or duplicate:
        errors.append(f"{label}: missing={sorted(missing)}, extra={sorted(extra)}, duplicate={duplicate}")


def main() -> int:
    errors: list[str] = []
    required = ["MASTER_PLAN.md", "INTERVIEW_MAP.md", "LEARNING_STATE.md", "TEACHING_RULES.md", "AGENTS.md"]
    for name in required:
        if not (ROOT / name).is_file():
            errors.append(f"Missing required file: {name}")
    if errors:
        print("\n".join(errors))
        return 1

    expected_units = {f"{group}{i:02d}" for group, count in COUNTS.items() for i in range(1, count + 1)}
    units = re.findall(r"^\|\s*([A-H]\d{2})\s*\|", read("MASTER_PLAN.md"), flags=re.MULTILINE)
    check_ids("Curriculum", units, expected_units, errors)

    expected_questions = {f"Q{i:03d}" for i in range(1, 96)}
    interview = read("INTERVIEW_MAP.md")
    questions = re.findall(r"^\|\s*(Q\d{3})\s*\|", interview, flags=re.MULTILINE)
    check_ids("Interview map", questions, expected_questions, errors)
    for line in interview.splitlines():
        if not re.match(r"^\|\s*Q\d{3}\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 6:
            errors.append(f"Malformed interview row: {line}")
            continue
        mapped = [item.strip() for item in cells[3].split(",") if item.strip()]
        if not mapped or any(item not in expected_units for item in mapped):
            errors.append(f"Invalid unit mapping for {cells[1]}: {cells[3]}")

    current = re.search(r"^当前知识单元：([A-H]\d{2})\s*$", read("LEARNING_STATE.md"), flags=re.MULTILINE)
    if current is None or current.group(1) not in expected_units:
        errors.append("LEARNING_STATE.md needs a valid 当前知识单元：A01-style field.")

    # Check relative Markdown file links; external URLs and anchors are out of scope.
    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", text):
            parsed = urlparse(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.exists():
                errors.append(f"Broken local link in {path.relative_to(ROOT)}: {target}")

    if errors:
        print("FAIL\n" + "\n".join(errors))
        return 1
    print(f"PASS: {len(units)} units, {len(questions)} questions, valid mappings and local links.")
    print("This validates documentation structure only; it does not certify learning progress.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, UnicodeError) as exc:
        print(f"Cannot validate plan files: {exc}", file=sys.stderr)
        raise SystemExit(1)
