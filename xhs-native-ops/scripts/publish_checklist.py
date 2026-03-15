#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from package_contract import parse_frontmatter_and_sections, validate_package_contract


def main():
    parser = argparse.ArgumentParser(description="Generate a pre-publish checklist for a Xiaohongshu content package")
    parser.add_argument("--input", required=True, help="path to package.md")
    parser.add_argument("--cards-dir", required=True, help="directory containing generated cards")
    args = parser.parse_args()

    package_path = Path(args.input)
    cards_dir = Path(args.cards_dir)
    frontmatter, sections = parse_frontmatter_and_sections(package_path)

    if not cards_dir.exists():
        raise SystemExit(f"Cards directory does not exist: {cards_dir}")
    validate_package_contract(frontmatter, sections)

    titles_path = package_path.parent / "titles.json"
    title_state = "missing"
    title_note = "Run title_check.py and save titles.json before final publish."
    if titles_path.exists():
        data = json.loads(titles_path.read_text(encoding="utf-8"))
        checked = data.get("checked") if isinstance(data, dict) else None
        first = checked[0] if isinstance(checked, list) and checked else (data if isinstance(data, dict) else None)
        if isinstance(first, dict):
            title_state = "pass" if first.get("passes") else "revise"
            title_note = f"Length {first.get('length')} / {first.get('max_length')}."

    layout = frontmatter.get("layout", "six")
    expected_cards = 6 if layout == "six" else 9
    card_files = sorted(cards_dir.glob("*.svg"))
    manifest_path = cards_dir / "manifest.json"
    cover_exists = any(path.name.startswith("01-") for path in card_files)
    cards_ok = len(card_files) >= expected_cards

    lines = []
    lines.append("# XHS Native Ops Publish Checklist")
    lines.append("")
    lines.append(f"- topic: `{frontmatter.get('topic', '')}`")
    lines.append(f"- layout: `{layout}`")
    lines.append(f"- package: `{package_path}`")
    lines.append(f"- cards dir: `{cards_dir}`")
    lines.append("")
    lines.append("## Readiness")
    lines.append(f"- [ {'x' if title_state == 'pass' else ' '} ] Title status")
    lines.append(f"  - {title_note}")
    lines.append(f"- [ {'x' if cover_exists else ' '} ] Cover exists")
    lines.append(f"  - Expected first card file like `01-cover.svg`.")
    lines.append(f"- [ {'x' if manifest_path.exists() else ' '} ] Manifest exists")
    lines.append("  - Expected `cards/manifest.json` describing page-level output.")
    lines.append(f"- [ {'x' if cards_ok else ' '} ] Card count matches layout")
    lines.append(f"  - Found {len(card_files)} SVG files, expected at least {expected_cards}.")
    lines.append(f"- [ {'x' if bool(sections.get('CTA')) else ' '} ] CTA exists")
    lines.append(f"  - CTA: {sections.get('CTA', 'Missing')}")
    lines.append(f"- [ {'x' if bool(frontmatter.get('topic')) and bool(sections.get('Hook')) else ' '} ] Topic consistency")
    lines.append("  - Topic and Hook should still point to the same post thesis.")
    lines.append("")
    lines.append("## Chrome attach preflight")
    lines.append("- [ ] Google Chrome is already logged in to Xiaohongshu creator flow")
    lines.append("- [ ] Chrome DevTools MCP attach path is ready")
    lines.append("- [ ] PinchTab is not used for logged-in actions")
    lines.append("- [ ] relay-style routes are not in use")
    lines.append("")
    lines.append("## Manual confirmation")
    lines.append("- [ ] Final title looks correct in composer")
    lines.append("- [ ] Cover choice is acceptable")
    lines.append("- [ ] Image order is correct")
    lines.append("- [ ] Visibility/options reviewed")
    lines.append("- [ ] Final publish click is manual in v0.1")
    lines.append("")
    print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        raise
