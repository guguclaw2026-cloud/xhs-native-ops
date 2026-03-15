#!/usr/bin/env python3
import argparse
import html
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from package_contract import (
    outline_items,
    parse_frontmatter_and_sections,
    split_card_item,
    validate_package_contract,
)


def fill_template(template: str, mapping):
    output = template
    for key, value in mapping.items():
        output = output.replace(f"{{{{{key}}}}}", str(value))
    return output


def read_template(pathname: Path):
    return pathname.read_text(encoding="utf-8")


def choose_templates(skill_root: Path, layout: str):
    cover = skill_root / "assets" / "cover-templates" / "minimal-cover.svg.tmpl"
    card = skill_root / "assets" / "card-templates" / f"{layout}-card.svg.tmpl"
    return read_template(cover), read_template(card)


def write_svg(pathname: Path, content: str):
    pathname.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate Xiaohongshu SVG cards from a package markdown file")
    parser.add_argument("--input", required=True, help="path to package.md")
    parser.add_argument("--output-dir", required=True, help="directory for generated SVG cards")
    parser.add_argument("--layout", choices=["six", "nine"], required=True, help="card layout")
    args = parser.parse_args()

    package_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    skill_root = Path(__file__).resolve().parents[1]
    cover_template, card_template = choose_templates(skill_root, args.layout)
    frontmatter, sections = parse_frontmatter_and_sections(package_path)
    validate_package_contract(frontmatter, sections)

    layout_count = 6 if args.layout == "six" else 9
    content_needed = layout_count - 1
    outline = outline_items(sections["Card Outline"])
    if len(outline) < content_needed:
        raise SystemExit(f"Card outline has {len(outline)} items, but layout '{args.layout}' needs {content_needed}")

    warnings = []
    if len(sections["Hook"]) > 18:
        warnings.append("hook exceeds the suggested cover headline density")
    if len(sections["Angle"]) > 28:
        warnings.append("angle exceeds the suggested cover support-line density")

    cover_svg = fill_template(cover_template, {
        "TOPIC": html.escape(str(frontmatter.get("topic", "Untitled Topic"))),
        "HOOK": html.escape(sections["Hook"]),
        "ANGLE": html.escape(sections["Angle"]),
        "LAYOUT_TAG": "6-card" if args.layout == "six" else "9-card",
    })
    write_svg(output_dir / "01-cover.svg", cover_svg)

    generated = [str(output_dir / "01-cover.svg")]
    manifest_pages = [{
        "index": 1,
        "role": "cover",
        "title": sections["Hook"],
        "path": "01-cover.svg",
    }]
    for index, item in enumerate(outline[:content_needed], start=2):
        title, body = split_card_item(item)
        if len(title) > 16:
            warnings.append(f"card {index:02d} title exceeds suggested density")
        if len(body) > 60:
            warnings.append(f"card {index:02d} body exceeds suggested density")
        svg = fill_template(card_template, {
            "CARD_NO": f"{index - 1}",
            "TITLE": html.escape(title),
            "BODY": html.escape(body or "Keep one clear point on this page."),
            "FOOTER": html.escape(str(frontmatter.get("cta", sections["CTA"]))),
        })
        target = output_dir / f"{index:02d}-card.svg"
        write_svg(target, svg)
        generated.append(str(target))
        manifest_pages.append({
            "index": index,
            "role": "content",
            "title": title,
            "path": target.name,
        })

    manifest_path = output_dir / "manifest.json"
    manifest = {
        "ok": True,
        "topic": frontmatter["topic"],
        "layout": args.layout,
        "card_count": len(manifest_pages),
        "audience": frontmatter["audience"],
        "tone": frontmatter["tone"],
        "source_package": str(package_path),
        "pages": manifest_pages,
        "warnings": warnings,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    report = {
        "ok": True,
        "layout": args.layout,
        "generated": generated,
        "manifest": str(manifest_path),
        "warnings": warnings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        raise
