#!/usr/bin/env bash
set -euo pipefail

TARGET_WORKSPACE="${1:-$HOME/.openclaw/workspace}"

if [[ ! -d "$TARGET_WORKSPACE" ]]; then
  echo "Target workspace not found: $TARGET_WORKSPACE" >&2
  exit 1
fi

REPO_DIR="$TARGET_WORKSPACE/projects/openclaw-knowledge-factory"
mkdir -p "$TARGET_WORKSPACE/projects"

if [[ -d "$REPO_DIR/.git" ]]; then
  echo "[info] repo exists, pulling latest"
  git -C "$REPO_DIR" pull --ff-only
else
  echo "[info] cloning repository"
  git clone https://github.com/zhoucehuang-arch/openclaw-knowledge-factory.git "$REPO_DIR"
fi

mkdir -p "$TARGET_WORKSPACE/memory"
STATE_PATH="$TARGET_WORKSPACE/memory/heartbeat-state.json"
if [[ ! -f "$STATE_PATH" ]]; then
  cp "$REPO_DIR/examples/heartbeat-state.json" "$STATE_PATH"
  echo "[ok] initialized $STATE_PATH"
else
  echo "[skip] existing state file kept: $STATE_PATH"
fi

chmod +x "$REPO_DIR/scripts/health_check.py"
chmod +x "$REPO_DIR/install.sh"

echo "[ok] install completed"
echo "Run check: python3 $REPO_DIR/scripts/health_check.py --state $STATE_PATH"
