#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


REQUIRED_FRONTMATTER = [
    "topic",
    "goal",
    "platform",
    "post_type",
    "layout",
    "cta",
    "source_signals",
    "audience",
    "tone",
]

REQUIRED_SECTIONS = ["Hook", "Angle", "Card Outline", "CTA", "Notes"]


def parse_frontmatter_and_sections(pathname: Path):
    raw = pathname.read_text(encoding="utf-8")
    lines = raw.splitlines()
    frontmatter = {}
    index = 0

    if lines and lines[0].strip() == "---":
        index = 1
        current_list_key = None
        while index < len(lines):
            line = lines[index]
            index += 1
            if line.strip() == "---":
                break
            if not line.strip():
                continue
            if line.startswith("  - ") and current_list_key:
                frontmatter.setdefault(current_list_key, []).append(line[4:].strip())
                continue
            if line.startswith("- ") and current_list_key:
                frontmatter.setdefault(current_list_key, []).append(line[2:].strip())
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                current_list_key = key
                frontmatter[key] = []
            else:
                current_list_key = None
                frontmatter[key] = value.strip("'\"")

    sections = {}
    current = None
    buffer = []
    for line in lines[index:]:
        if line.startswith("# "):
            if current:
                sections[current] = "\n".join(buffer).strip()
            current = line[2:].strip()
            buffer = []
        else:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer).strip()

    return frontmatter, sections


def validate_package_contract(frontmatter, sections):
    missing_frontmatter = [name for name in REQUIRED_FRONTMATTER if not frontmatter.get(name)]
    if missing_frontmatter:
        raise SystemExit(f"Missing required frontmatter: {', '.join(missing_frontmatter)}")

    missing_sections = [name for name in REQUIRED_SECTIONS if not sections.get(name)]
    if missing_sections:
        raise SystemExit(f"Missing required sections: {', '.join(missing_sections)}")


def outline_items(text: str):
    items = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        line = re.sub(r"^\d+\.\s+", "", line)
        if line:
            items.append(line)
    return items


def outline_count(text: str) -> int:
    return len(outline_items(text))


def split_card_item(item: str):
    for separator in ("｜", "|", ":"):
        if separator in item:
            left, right = item.split(separator, 1)
            return left.strip(), right.strip()
    trimmed = item.strip()
    if len(trimmed) <= 16:
        return trimmed, ""
    return trimmed[:16].strip(), trimmed[16:].strip()


def expected_outline_count(layout: str) -> int:
    return 5 if layout == "six" else 8
