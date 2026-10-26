"""Opt-in real installation smoke in a neutral generated repository (network needed)."""

import argparse
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from create_project import create_project, render_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-only", action="store_true",
                        help="Validate the shared runtime when local policy forbids PowerShell scripts")
    args = parser.parse_args()
    with TemporaryDirectory(prefix="specify-smoke-") as directory:
        root = Path(directory) / "neutral project with spaces"
        with redirect_stdout(io.StringIO()):
            create_project(root, render_files("independent-product", "none", []))
        setup = [sys.executable, str(root / "scripts/bootstrap_specify.py")]
        subprocess.run(setup, cwd=directory, check=True)
        receipts = list((root / ".artifacts/specify").rglob("uv-receipt.toml"))
        before = {p: p.stat().st_mtime_ns for p in receipts}
        assert before, "uv installation receipt missing"
        subprocess.run(setup, cwd=directory, check=True)
        assert before == {p: p.stat().st_mtime_ns for p in receipts}, "unexpected reinstall"
        if args.python_only:
            command = [sys.executable, str(root / "scripts/specify_tool.py")]
        elif os.name == "nt":
            command = ["powershell.exe", "-NoProfile", "-File", str(root / "scripts/specify.ps1")]
        else:
            command = [str(root / "scripts/specify")]
        result = subprocess.run(command + ["version", "--features", "--json"],
                                cwd=directory, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
        data = json.loads(result.stdout)
        expected = (root / ".specify-version").read_text().strip()
        assert data["version"] == expected, data
        assert isinstance(data["features"], dict) and data["features"], data
        invalid = subprocess.run(command + ["version", "--unsupported-repo-smoke-option"],
                                 cwd=directory, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert invalid.returncode == 2, invalid
        subprocess.run(setup + ["--repair"], cwd=directory, check=True)
        subprocess.run(command + ["version", "--features", "--json"], cwd=directory, check=True)
        print("Neutral repository: version, cwd/path, arguments, exit code, idempotence and repair OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
