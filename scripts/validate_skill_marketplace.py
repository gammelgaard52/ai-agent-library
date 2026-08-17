#!/usr/bin/env python3
"""Validate 1:1 consistency between skills/ and .plugin/marketplace.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MARKETPLACE_PATH = ROOT / ".plugin" / "marketplace.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_frontmatter_name(skill_md: Path) -> str:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"{skill_md.relative_to(ROOT)} must start with YAML frontmatter")

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        fail(f"{skill_md.relative_to(ROOT)} has no closing YAML frontmatter delimiter")

    names: list[str] = []
    for line in lines[1:end]:
        match = re.match(r"^name\s*:\s*(.+?)\s*$", line)
        if match:
            value = match.group(1).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            names.append(value)

    if len(names) != 1:
        fail(
            f"{skill_md.relative_to(ROOT)} must contain exactly one top-level frontmatter name"
        )
    return names[0]


def main() -> None:
    if not SKILLS_DIR.is_dir():
        fail("skills/ directory is missing")
    if not MARKETPLACE_PATH.is_file():
        fail(".plugin/marketplace.json is missing")

    try:
        marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f".plugin/marketplace.json is invalid JSON: {exc}")

    entries = marketplace.get("skills") if isinstance(marketplace, dict) else None
    if not isinstance(entries, list):
        fail(".plugin/marketplace.json must contain a 'skills' array")

    library_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    library_names = {path.name for path in library_dirs}

    if not library_names:
        fail("skills/ contains no skill directories")

    for path in library_dirs:
        name = path.name
        if not NAME_RE.fullmatch(name):
            fail(f"Invalid skill directory name: skills/{name}")
        skill_md = path / "SKILL.md"
        if not skill_md.is_file():
            fail(f"skills/{name}/SKILL.md is missing")
        frontmatter_name = read_frontmatter_name(skill_md)
        if frontmatter_name != name:
            fail(
                f"skills/{name}/SKILL.md frontmatter name is {frontmatter_name!r}; expected {name!r}"
            )

    marketplace_names: list[str] = []
    marketplace_sources: list[str] = []

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(f"marketplace skills[{index}] must be an object")

        name = entry.get("name")
        source = entry.get("source")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            fail(f"marketplace skills[{index}] has invalid name: {name!r}")
        if not isinstance(source, str):
            fail(f"marketplace skill {name!r} has invalid source")

        expected_source = f"./skills/{name}"
        if source != expected_source:
            fail(
                f"marketplace skill {name!r} source is {source!r}; expected {expected_source!r}"
            )

        source_dir = ROOT / source.removeprefix("./")
        if not source_dir.is_dir() or not (source_dir / "SKILL.md").is_file():
            fail(f"marketplace skill {name!r} points to a missing/invalid skill directory")

        marketplace_names.append(name)
        marketplace_sources.append(source)

    if len(marketplace_names) != len(set(marketplace_names)):
        fail(".plugin/marketplace.json contains duplicate skill names")
    if len(marketplace_sources) != len(set(marketplace_sources)):
        fail(".plugin/marketplace.json contains duplicate skill sources")

    marketplace_name_set = set(marketplace_names)
    missing_from_marketplace = sorted(library_names - marketplace_name_set)
    missing_from_library = sorted(marketplace_name_set - library_names)

    if missing_from_marketplace:
        fail(
            "skills present in library but missing from marketplace: "
            + ", ".join(missing_from_marketplace)
        )
    if missing_from_library:
        fail(
            "skills present in marketplace but missing from library: "
            + ", ".join(missing_from_library)
        )

    print(f"OK: {len(library_names)} skills are in strict 1:1 marketplace sync")


if __name__ == "__main__":
    main()
