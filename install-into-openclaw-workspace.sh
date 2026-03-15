#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$REPO_ROOT/xhs-native-ops"
TARGET_ROOT="${1:-${OPENCLAW_HOME:-$HOME/.openclaw}/workspace/skills}"
TARGET_DIR="$TARGET_ROOT/xhs-native-ops"

if [[ ! -d "$SKILL_SRC" ]]; then
  echo "Skill source not found: $SKILL_SRC" >&2
  exit 1
fi

mkdir -p "$TARGET_ROOT"

python3 - "$SKILL_SRC" "$TARGET_DIR" <<'PY'
from pathlib import Path
import shutil
import sys

src = Path(sys.argv[1])
dst = Path(sys.argv[2])

if dst.exists():
    shutil.rmtree(dst)

shutil.copytree(
    src,
    dst,
    ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
)
PY

echo "Installed xhs-native-ops to: $TARGET_DIR"
