"""Initialize the pinned Spec Kit integration, preserving project-owned overrides."""

import argparse
from pathlib import Path
import os
import subprocess
import sys

from specify_tool import ENTRYPOINT, runtime


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integration", default="copilot")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if (root / ".specify/integration.json").exists():
        parser.error("Bereits initialisiert. Für Updates: specify integration upgrade <integration>.")
    python, env = runtime()
    command = [str(python), "-I", "-c", ENTRYPOINT]
    constitution = root / ".specify/memory/constitution.md"
    original = constitution.read_bytes()
    try:
        result = subprocess.run(
            command + ["init", "--here", "--integration", args.integration,
                       "--script", "ps" if os.name == "nt" else "sh", "--force"],
            cwd=root, env=env, check=False,
        )
    finally:
        constitution.write_bytes(original)
    return result.returncode


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
