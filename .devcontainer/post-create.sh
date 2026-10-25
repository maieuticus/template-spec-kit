#!/usr/bin/env bash

set -euo pipefail

if ! command -v copilot >/dev/null 2>&1; then
  curl -fsSL https://gh.io/copilot-install | sudo bash
fi

copilot --version
