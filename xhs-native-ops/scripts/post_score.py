#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from package_contract import (
    expected_outline_count,
    outline_count,
    parse_frontmatter_and_sections,
    validate_package_contract,
)


def score_package(frontmatter, sections):
    issues = []
    layout = frontmatter.get("layout", "six")
    expected_outline = expected_outline_count(layout)
    actual_outline = outline_count(sections.get("Card Outline", ""))

    platform_native_fit = 14
    hook = sections.get("Hook", "")
    angle = sections.get("Angle", "")
    comments_angle = sections.get("Comments Angle", "")
    notes = sections.get("Notes", "")
    audience = frontmatter.get("audience", "")
    tone = frontmatter.get("tone", "")
    source_signals = frontmatter.get("source_signals", [])
    goal = str(frontmatter.get("goal", "")).strip()
    post_type = str(frontmatter.get("post_type", "")).strip()
    platform = str(frontmatter.get("platform", "")).strip()
    generic_goals = {"growth", "awareness", "traffic", "engagement"}

    if 8 <= len(hook) <= 18:
        platform_native_fit += 2
    elif len(hook) > 20:
        platform_native_fit -= 4
        issues.append("Hook is too long for a strong cover.")
    elif len(hook) < 6:
        platform_native_fit -= 4
        issues.append("Hook is too short for a native-looking cover.")

    if len(angle) > 36:
        platform_native_fit -= 5
        issues.append("Angle is too dense and should be tightened.")
    elif len(angle) > 28:
        platform_native_fit -= 3
        issues.append("Angle can be tightened for a cleaner cover.")
    else:
        platform_native_fit += 1

    if audience:
        platform_native_fit += 1
    if tone:
        platform_native_fit += 1

    hook_clarity = 12
    if len(hook) < 6:
        hook_clarity -= 6
        issues.append("Hook is too short to be clear.")
    elif len(hook) <= 18:
        hook_clarity += 2
    if not any(token in hook for token in ("为什么", "怎么", "别再", "不是", "先", "如果", "让")):
        hook_clarity -= 4
        issues.append("Hook may be too flat for Xiaohongshu.")
    if any(token in hook for token in ("不是", "先", "为什么", "别")):
        hook_clarity += 2

    interaction_potential = 10
    if not comments_angle:
        interaction_potential -= 6
        issues.append("Comments Angle is missing.")
    elif len(comments_angle) >= 8:
        interaction_potential += 2
    if not sections.get("CTA"):
        interaction_potential -= 8
        issues.append("CTA is missing.")
    else:
        interaction_potential += 2
    if "？" in comments_angle or "什么" in comments_angle:
        interaction_potential += 2
    if any(token in sections.get("CTA", "") for token in ("收藏", "评论", "转发", "私信", "发给")):
        interaction_potential += 1

    business_relevance = 10
    if not isinstance(source_signals, list) or not source_signals:
        business_relevance -= 8
        issues.append("source_signals is missing or empty.")
    else:
        business_relevance += min(len(source_signals), 3)
    if not goal:
        business_relevance -= 4
        issues.append("goal is missing from frontmatter.")
    elif goal in generic_goals:
        business_relevance -= 2
        issues.append("goal is too generic and should be made more specific.")
    else:
        business_relevance += 2
    if audience:
        business_relevance += 1
    if tone:
        business_relevance += 1
    if platform == "xiaohongshu":
        business_relevance += 1
    if post_type in ("opinion", "howto", "behind_the_scenes"):
        business_relevance += 1

    packaging_readiness = 10
    if actual_outline < expected_outline:
        packaging_readiness -= 12
        issues.append(f"Card Outline only has {actual_outline} items; layout {layout} needs {expected_outline}.")
    elif actual_outline == expected_outline:
        packaging_readiness += 4
    else:
        packaging_readiness -= 4
        issues.append(f"Card Outline has {actual_outline} items; layout {layout} should land cleanly on {expected_outline}.")
    if frontmatter.get("layout") not in ("six", "nine"):
        packaging_readiness -= 8
        issues.append("layout must be six or nine.")
    else:
        packaging_readiness += 1
    if notes:
        packaging_readiness += 0
    if len(angle) <= 28:
        packaging_readiness += 1

    scores = {
        "platform_native_fit": max(platform_native_fit, 0),
        "hook_clarity": max(hook_clarity, 0),
        "interaction_potential": max(interaction_potential, 0),
        "business_relevance": max(business_relevance, 0),
        "packaging_readiness": max(packaging_readiness, 0),
    }
    total = sum(scores.values())
    if total >= 82 and not issues:
        recommendation = "ready"
    elif total >= 62:
        recommendation = "revise"
    else:
        recommendation = "hold"

    next_fix = issues[0] if issues else "Package is strong enough to move into review."
    return {
        "total_score": total,
        "publish_recommendation": recommendation,
        "dimension_scores": scores,
        "top_issues": issues[:5],
        "next_fix": next_fix,
    }


def main():
    parser = argparse.ArgumentParser(description="Score a Xiaohongshu content package")
    parser.add_argument("--input", required=True, help="path to package.md")
    args = parser.parse_args()

    frontmatter, sections = parse_frontmatter_and_sections(Path(args.input))
    validate_package_contract(frontmatter, sections)

    print(json.dumps(score_package(frontmatter, sections), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        raise
