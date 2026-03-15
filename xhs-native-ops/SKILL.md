---
name: xhs-native-ops
description: >-
  Shared Xiaohongshu-native operations skill for agents that need to turn
  signals into publish-ready content packages. Use when the work needs
  Xiaohongshu research synthesis, topic and angle design, page-level card
  planning, visual packaging, title-length checks, pre-publish checklists, or
  review-ready handoff packages. Best triggers include "小红书运营", "小红书原生感",
  "xhs native ops", "图文卡片", "封面怎么做", "发布前检查", "把这个主题做成小红书",
  "标题超长检查", and "根据热点做小红书图文". Do not use it for account-level
  growth strategy ownership, generic social scheduling, or logged-in browser
  publishing without a prepared content package.
metadata:
  display_name: XHS Native Ops
  version: "0.1.1"
  tags: [xiaohongshu, xhs, content, packaging, cards, publishing, review]
---

# XHS Native Ops

## Purpose

Build Xiaohongshu content packages that feel platform-native, not tool-native.

This skill owns the execution layer for Xiaohongshu content:

1. research synthesis
2. topic and angle design
3. page-level card planning
4. visual packaging
5. pre-publish checks
6. review-ready handoff

It is a shared workspace skill. Do not bind it to a single agent persona,
single account, or private business context.

## Relationship to other skills

- `xhs-native-ops` is the Xiaohongshu content execution layer
- a separate account-strategy skill should own growth cadence, acquisition
  targets, and weekly account direction

If the work is "what should this account do this week?", use your
account-strategy layer.

If the work is "turn this approved direction into a Xiaohongshu-native
package", use this skill.

## Hard rules

- shared skill only; no account-specific voice or defaults
- compatible with upstream research outputs, but must not require them
- v0.1 stops before the final publish click
- logged-in publishing must use Google Chrome + Chrome DevTools MCP attach
- do not use PinchTab for logged-in publishing actions
- do not use relay-style browser paths

## Workflow order

Always move in this order:

1. `research`
2. `topic-design`
3. `visual-packaging`
4. `publish-and-review`

Do not jump straight from a long paragraph to final cards. The core unit here is
the page, not the article.

## Package contract

This skill uses a single package directory contract:

- `package.md`
- `titles.json`
- `score.json`
- `cards/`
- `publish-checklist.md`

`package.md` is the source of truth. Read the contract described in:

- `references/topic-design.md`
- `references/visual-packaging.md`

## When to read each reference

- Read `references/research.md` when signals are still messy and need to be
  turned into a usable direction.
- Read `references/topic-design.md` when converting a topic into a hook, angle,
  and page-level card outline.
- Read `references/visual-packaging.md` before generating or reviewing cards.
- Read `references/publishing.md` before any Chrome attach publishing work.
- Read `references/review-rubric.md` when deciding whether a package is ready,
  needs revision, or should be held.
- Read `references/artifact-formats.md` when implementing or validating the
  JSON output contract.
- Read `references/implementation-pitfalls.md` before extending the skill or
  handing it to another coding agent for first-pass implementation.
- Read `references/sample-run.md` when you need the fastest possible terminal,
  Codex, or OpenClaw invocation pattern.

## Script entrypoints

### Title checking

```bash
python3 skills/xhs-native-ops/scripts/title_check.py \
  --title "为什么小团队应该先让 AI 接手重复工作"
```

### Card generation

```bash
python3 skills/xhs-native-ops/scripts/md_to_xhs_cards.py \
  --input skills/xhs-native-ops/examples/sample-package/package.md \
  --output-dir skills/xhs-native-ops/examples/sample-package/cards \
  --layout six
```

### Package scoring

```bash
python3 skills/xhs-native-ops/scripts/post_score.py \
  --input skills/xhs-native-ops/examples/sample-package/package.md
```

### Pre-publish checklist

```bash
python3 skills/xhs-native-ops/scripts/publish_checklist.py \
  --input skills/xhs-native-ops/examples/sample-package/package.md \
  --cards-dir skills/xhs-native-ops/examples/sample-package/cards
```

## Quality bar

The package should feel:

- clear
- native to Xiaohongshu
- page-structured
- reviewable by a human operator

It should not feel like:

- a technical memo
- a generic social caption
- an overstuffed infographic
- a fully automated black-box output

## Assets and examples

- `assets/cover-templates/` contains the base cover template
- `assets/card-templates/` contains 6-card and 9-card content templates
- `examples/sample-package/` is the smoke-test package

Use the sample package to validate behavior before adapting the skill to a live
workflow.

For immediate handoff examples, see:

- `references/sample-run.md`
- `references/implementation-pitfalls.md`
