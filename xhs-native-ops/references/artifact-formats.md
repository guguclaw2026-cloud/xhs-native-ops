# Artifact Formats

Use this file when implementing, validating, or extending the output contract of
`xhs-native-ops`.

The goal is not to define a permanent public standard. The goal is to keep
v0.1 outputs stable enough that Codex, OpenClaw, and human reviewers can all
read the same package shape without guessing.

## Scope

This file defines the recommended structure for:

- `titles.json`
- `score.json`
- `cards/manifest.json`

These are the minimum machine-readable artifacts expected from a successful
v0.1 package run.

## `titles.json`

### Purpose

Record the result of title checking in a way that can be re-read before
publishing.

### Recommended v0.1 shape

```json
{
  "title": "做二次元出海后我最想交给AI的五件事",
  "length": 18,
  "max_length": 20,
  "passes": true,
  "reason": "within_limit",
  "suggested_shorter_title": "做二次元出海后我最想交给AI的五件事",
  "alternatives": [
    "做二次元出海后我最想交给AI的五件事"
  ]
}
```

### Field notes

- `title`: original title that was checked
- `length`: measured length
- `max_length`: active limit used for this run
- `passes`: whether the title passed the current limit
- `reason`: compact machine-readable explanation
- `suggested_shorter_title`: first recommended shorter fallback
- `alternatives`: optional list of alternate titles

### Stability rule

`title_check.py` may later return more metadata, but these fields should remain
stable unless there is a very strong reason to break compatibility.

## `score.json`

### Purpose

Capture whether the package is actually ready for review, needs revision, or
should be held.

### Recommended v0.1 shape

```json
{
  "total_score": 100,
  "publish_recommendation": "ready",
  "dimension_scores": {
    "platform_native_fit": 20,
    "hook_clarity": 20,
    "interaction_potential": 20,
    "business_relevance": 20,
    "packaging_readiness": 20
  },
  "top_issues": [],
  "next_fix": "Package is strong enough to move into review."
}
```

### Field notes

- `total_score`: sum score for the package
- `publish_recommendation`: one of `ready`, `revise`, `hold`
- `dimension_scores`: per-dimension sub-scores
- `top_issues`: short list of the most important problems
- `next_fix`: first recommended fix if the package is not clean

### Stability rule

New dimensions may be added later, but the recommendation vocabulary should
stay small and stable.

## `cards/manifest.json`

### Purpose

Describe page-level card output in a way that is easy to inspect, review, or
transform later.

### Recommended v0.1 shape

```json
{
  "ok": true,
  "topic": "小团队先让AI接手什么",
  "layout": "six",
  "card_count": 6,
  "audience": "正在用 AI 重跑分工的小团队操盘者",
  "tone": "清楚、直接、可执行",
  "source_package": "/ABSOLUTE/PATH/TO/package.md",
  "pages": [
    {
      "index": 1,
      "role": "cover",
      "title": "小团队最该先交给 AI 的，不是创意",
      "path": "01-cover.svg"
    },
    {
      "index": 2,
      "role": "content",
      "title": "别先让 AI 代替判断",
      "path": "02-card.svg"
    }
  ],
  "warnings": []
}
```

### Field notes

- `ok`: success status for this card generation run
- `topic`: frontmatter topic
- `layout`: `six` or `nine`
- `card_count`: total number of generated pages including cover
- `audience`: target audience from the package
- `tone`: package tone
- `source_package`: absolute path used for the generation run
- `pages`: ordered page list
- `warnings`: non-blocking packaging warnings

### `pages[]` shape

Each page should include:

- `index`: one-based page index
- `role`: `cover` or `content`
- `title`: the visible page title or page hook
- `path`: relative asset path inside the cards directory

## Reviewer guidance

When reviewing a package:

- use `titles.json` to decide if the title is safe to carry into composer
- use `score.json` to decide whether the package is `ready`, `revise`, or `hold`
- use `manifest.json` to confirm the post is genuinely page-based, not article-based

## v0.1 compatibility rule

Do not change all three output shapes at once.

If one artifact shape changes, update:

1. the generating script
2. the sample package output
3. this reference file
4. any checklist logic that reads the artifact
