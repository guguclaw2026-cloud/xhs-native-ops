#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

FILLER_PATTERNS = [
    "到底",
    "真的",
    "现在",
    "一下",
    "其实",
    "我们",
    "就是",
    "这个",
    "一个",
    "为什么",
]


def normalize_title(text: str) -> str:
    return " ".join(str(text or "").strip().split())


def shorten_title(title: str, max_length: int) -> str:
    candidate = normalize_title(title)
    if len(candidate) <= max_length:
        return candidate

    for token in FILLER_PATTERNS:
        candidate = candidate.replace(token, "")
        candidate = normalize_title(candidate)
        if len(candidate) <= max_length:
            return candidate

    compact = candidate.replace("，", " ").replace("：", " ").replace("、", " ")
    compact = normalize_title(compact)
    if len(compact) <= max_length:
        return compact

    return compact[:max_length].rstrip(" ，：、")


def build_alternatives(title: str, max_length: int):
    base = normalize_title(title)
    candidates = []
    candidates.append(shorten_title(base, max_length))
    candidates.append(shorten_title(base.replace("为什么", ""), max_length))
    candidates.append(shorten_title(base.replace("我们", ""), max_length))

    seen = []
    for item in candidates:
        item = normalize_title(item)
        if item and item not in seen:
            seen.append(item)
    return seen[:3]


def check_title(title: str, max_length: int):
    normalized = normalize_title(title)
    length = len(normalized)
    passes = length <= max_length
    reason = "within_limit" if passes else "exceeds_limit"
    alternatives = build_alternatives(normalized, max_length)
    suggested = alternatives[0] if alternatives else normalized[:max_length]
    return {
        "title": normalized,
        "length": length,
        "max_length": max_length,
        "passes": passes,
        "reason": reason,
        "suggested_shorter_title": suggested if not passes else normalized,
        "alternatives": alternatives,
    }


def load_titles_file(pathname: Path):
    data = json.loads(pathname.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("titles"), list):
        return data["titles"]
    raise ValueError("titles file must be a JSON array or an object with a 'titles' array")


def main():
    parser = argparse.ArgumentParser(description="Check Xiaohongshu title length and offer rule-based shorten suggestions")
    parser.add_argument("--title", default="", help="single title to check")
    parser.add_argument("--file", default="", help="JSON file containing titles")
    parser.add_argument("--max-length", type=int, default=20, help="maximum allowed title length")
    args = parser.parse_args()

    if not args.title and not args.file:
        raise SystemExit("Provide --title or --file")

    if args.title:
        print(json.dumps(check_title(args.title, args.max_length), ensure_ascii=False, indent=2))
        return

    titles = load_titles_file(Path(args.file))
    checked = [check_title(str(item), args.max_length) for item in titles]
    result = {
        "checked": checked,
        "passed_count": sum(1 for item in checked if item["passes"]),
        "failed_count": sum(1 for item in checked if not item["passes"]),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        raise
