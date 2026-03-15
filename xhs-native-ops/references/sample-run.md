# Sample Run

Use this file as the **minimum runnable acceptance contract** for
`xhs-native-ops`.

When handing this project to Codex, OpenClaw, or a local terminal workflow,
treat this file as the fastest path to verify that the v0.1 loop is working.

## What this sample run proves

A valid v0.1 implementation must complete this loop:

1. check the title
2. generate Xiaohongshu cards from `package.md`
3. score the package
4. generate a pre-publish checklist
5. stop before final publish by default

This sample run is not complete unless all expected outputs are produced
successfully.

## Default operating mode

Use **review-first** mode by default.

- The agent may prepare the full package
- The agent may prepare the Chrome attach workflow
- The human operator owns the final publish confirmation by default

Only proceed to a real publish flow if the caller explicitly requests it.

## Required sample package

The built-in smoke package should live at:

- `skills/xhs-native-ops/examples/sample-package/package.md`

Expected outputs:

- `skills/xhs-native-ops/examples/sample-package/titles.json`
- `skills/xhs-native-ops/examples/sample-package/score.json`
- `skills/xhs-native-ops/examples/sample-package/cards/`
- `skills/xhs-native-ops/examples/sample-package/publish-checklist.md`

## Package contract

The package input file must be `package.md`.

### Required frontmatter

```yaml
topic:
goal:
platform: xiaohongshu
post_type:
layout:
cta:
source_signals:
audience:
tone:
```

### Required sections

- `# Hook`
- `# Angle`
- `# Card Outline`
- `# CTA`
- `# Notes`

## Card output contract

The generated `cards/` directory must contain page-level output, not
article-style output.

Minimum expected structure for the current v0.1 SVG implementation:

```text
cards/
  manifest.json
  01-cover.svg
  02-card.svg
  03-card.svg
  ...
```

If the implementation later also generates HTML or PNG assets, keep the same
page-level structure and do not collapse the post back into article output.

## Terminal: minimum smoke run

Run these commands from the workspace root:

```bash
python3 skills/xhs-native-ops/scripts/title_check.py \
  --title "做二次元出海后我最想交给AI的五件事" \
  > skills/xhs-native-ops/examples/sample-package/titles.json

python3 skills/xhs-native-ops/scripts/md_to_xhs_cards.py \
  --input skills/xhs-native-ops/examples/sample-package/package.md \
  --output-dir skills/xhs-native-ops/examples/sample-package/cards \
  --layout six

python3 skills/xhs-native-ops/scripts/post_score.py \
  --input skills/xhs-native-ops/examples/sample-package/package.md \
  > skills/xhs-native-ops/examples/sample-package/score.json

python3 skills/xhs-native-ops/scripts/publish_checklist.py \
  --input skills/xhs-native-ops/examples/sample-package/package.md \
  --cards-dir skills/xhs-native-ops/examples/sample-package/cards \
  > skills/xhs-native-ops/examples/sample-package/publish-checklist.md
```

## Terminal: nine-card validation

Use this when validating the alternate card layout:

```bash
python3 skills/xhs-native-ops/scripts/md_to_xhs_cards.py \
  --input skills/xhs-native-ops/examples/sample-package/package.md \
  --output-dir skills/xhs-native-ops/examples/sample-package/cards-nine \
  --layout nine
```

## Agent handoff: run on an existing package

Use this when an agent must execute the full v0.1 loop on an existing package
directory:

```text
Use the `xhs-native-ops` skill in this workspace to turn this Xiaohongshu
content package into a review-ready publish package:
`/PATH/TO/PACKAGE/package.md`

Follow this order:
1. research sanity check if needed
2. topic and angle validation
3. title check
4. card generation
5. package scoring
6. pre-publish checklist

Requirements:
- keep the package platform-native
- use page-level card structure, not article-style output
- keep the result review-first by default
- do not use PinchTab for logged-in actions
- do not use relay
- if a publish step is requested later, use Chrome attach only
- stop before the final publish click unless explicit publish authorization is given

Deliver:
- updated `titles.json`
- updated card output directory
- updated `score.json`
- updated `publish-checklist.md`
```

## Agent handoff: create package first, then execute

Use this when an agent must create the package from a topic and then run the
loop:

```text
Use the `xhs-native-ops` skill in this workspace to create and execute a
Xiaohongshu-native package for this topic:
"小团队最该先让 AI 接手什么"

Create a package directory with:
- `package.md`
- `titles.json`
- `score.json`
- `cards/`
- `publish-checklist.md`

The package must follow the skill contract:
- frontmatter with `topic`, `goal`, `platform`, `post_type`, `layout`, `cta`,
  `source_signals`, `audience`, `tone`
- sections `Hook`, `Angle`, `Card Outline`, `CTA`, `Notes`

Then run:
1. title check
2. card generation
3. package scoring
4. pre-publish checklist

Requirements:
- keep the output Xiaohongshu-native
- keep the cards page-based
- do not use PinchTab for logged-in actions
- do not use relay
- use Chrome attach only if a manual or explicitly authorized publish step is requested later
- stop before final publish by default
```

## Publish boundary

If this package moves into a real Xiaohongshu posting session:

- title, cards, score, and checklist must already be complete
- the agent may prepare the attach workflow
- the agent may fill draft fields if explicitly requested
- the final publish action remains human-owned by default

## Acceptance rule

Do not mark `xhs-native-ops` v0.1 as working unless this sample run completes
end-to-end on the sample package and produces all required outputs.
