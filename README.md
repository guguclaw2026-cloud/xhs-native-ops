# xhs-native-ops

`xhs-native-ops` is a shared OpenClaw/Codex skill for turning Xiaohongshu topics
into review-ready publish packages.

It focuses on the execution layer:

1. research synthesis
2. topic and angle design
3. page-level card planning
4. visual packaging
5. pre-publish checks
6. review-ready handoff

It does **not** own account strategy, growth cadence, or final publish
decisions.

## Repo layout

```text
xhs-native-ops/
├── README.md
├── .gitignore
├── install-into-openclaw-workspace.sh
└── xhs-native-ops/
    ├── SKILL.md
    ├── _meta.json
    ├── agents/openai.yaml
    ├── references/
    ├── scripts/
    ├── assets/
    └── examples/sample-package/
```

## What is included

- a standalone skill folder that can be copied into an OpenClaw workspace
- Python scripts for title checks, card generation, scoring, and checklist
  generation
- SVG-based cover and card templates
- a sample content package with generated outputs for smoke testing

## Hard boundaries

- shared skill only; no account-specific persona
- compatible with upstream research outputs, but does not require them
- final publish click remains human-owned by default
- logged-in publish work must use Google Chrome + Chrome DevTools MCP attach
- PinchTab must not be used for logged-in publish actions
- relay-style browser paths are out of scope

## Install into OpenClaw workspace

Default install target:

- `${OPENCLAW_HOME:-$HOME/.openclaw}/workspace/skills`

Run:

```bash
bash install-into-openclaw-workspace.sh
```

Install into a custom skill root:

```bash
bash install-into-openclaw-workspace.sh /path/to/skills-root
```

After install, the skill directory should be:

```text
/path/to/skills-root/xhs-native-ops
```

## Minimum smoke run

Run these commands from the repo root:

```bash
python3 xhs-native-ops/scripts/title_check.py \
  --title "做二次元出海后我最想交给AI的五件事" \
  > xhs-native-ops/examples/sample-package/titles.json

python3 xhs-native-ops/scripts/md_to_xhs_cards.py \
  --input xhs-native-ops/examples/sample-package/package.md \
  --output-dir xhs-native-ops/examples/sample-package/cards \
  --layout six

python3 xhs-native-ops/scripts/post_score.py \
  --input xhs-native-ops/examples/sample-package/package.md \
  > xhs-native-ops/examples/sample-package/score.json

python3 xhs-native-ops/scripts/publish_checklist.py \
  --input xhs-native-ops/examples/sample-package/package.md \
  --cards-dir xhs-native-ops/examples/sample-package/cards \
  > xhs-native-ops/examples/sample-package/publish-checklist.md
```

Expected outputs:

- `xhs-native-ops/examples/sample-package/titles.json`
- `xhs-native-ops/examples/sample-package/score.json`
- `xhs-native-ops/examples/sample-package/cards/`
- `xhs-native-ops/examples/sample-package/publish-checklist.md`

## Key files

- skill entry: `xhs-native-ops/SKILL.md`
- sample run contract:
  `xhs-native-ops/references/sample-run.md`
- artifact formats:
  `xhs-native-ops/references/artifact-formats.md`
- implementation pitfalls:
  `xhs-native-ops/references/implementation-pitfalls.md`

## Status

Current repo state is a GitHub-ready project skeleton for the `xhs-native-ops`
skill, with a runnable v0.1 sample package.
