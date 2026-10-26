#!/usr/bin/env bash

set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$script_dir/../scripts/bootstrap_specify.py"

if ! command -v copilot >/dev/null 2>&1; then
  curl -fsSL https://gh.io/copilot-install | sudo bash
fi

copilot --version
