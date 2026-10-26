"""Portable runtime contracts, without network or changes to user installations."""

from contextlib import redirect_stdout
import io
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import venv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import bootstrap_specify as setup
import specify_tool as tool
from create_project import create_project, render_files


class SpecifyTests(unittest.TestCase):
    def test_generated_runtime_is_complete_and_generic(self):
        required = (".specify-version", "scripts/specify", "scripts/specify.ps1",
                    "scripts/specify_tool.py", "scripts/bootstrap_specify.py",
                    "scripts/uv-requirements.txt", "scripts/specify-constraints.txt")
        for stack, recipe in [(s, None) for s in ("none", "python", "typescript", "java-maven")] + [("python", "api-service")]:
            with self.subTest(stack=stack, recipe=recipe), TemporaryDirectory() as directory:
                root = Path(directory) / "neutral checkout with spaces"
                files = render_files("unrelated-product", stack, [], recipe)
                with redirect_stdout(io.StringIO()):
                    create_project(root, files)
                for name in required:
                    self.assertEqual((root / name).read_bytes(), (ROOT / name).read_bytes())
                    content = files[name].decode("utf-8")
                    self.assertNotIn(str(ROOT), content)
                    self.assertNotIn("C:\\Users\\", content)
                    self.assertNotIn("template-spec-kit", content)
                self.assertNotIn("speckit_version", files["config/project.yaml"].decode())
                self.assertEqual(files[".specify-version"].decode().strip(), tool.pinned_version())
                if os.name == "posix":
                    self.assertTrue((root / "scripts/specify").stat().st_mode & 0o111)
                    missing = subprocess.run([str(root / "scripts/specify"), "version"], cwd=directory,
                                             capture_output=True, text=True)
                    self.assertEqual(missing.returncode, 1)
                    self.assertIn("bootstrap_specify.py", missing.stderr)

    def test_version_validation_and_missing_uv(self):
        with TemporaryDirectory() as directory, patch.object(tool, "ROOT", Path(directory)):
            version = Path(directory) / ".specify-version"
            for bad in ("", "1.0", "1.0.7 --extra", "../1.0.7"):
                version.write_text(bad, encoding="utf-8")
                with self.assertRaises(ValueError):
                    tool.pinned_version()
        with TemporaryDirectory() as directory, patch.object(tool, "STATE", Path(directory)), patch.object(tool.shutil, "which", return_value=None):
            with self.assertRaisesRegex(ValueError, "bootstrap_specify"):
                tool.uv_command()

    def test_uv_environment_does_not_modify_user_environment(self):
        original = dict(os.environ)
        env = tool.tool_environment()
        self.assertEqual(dict(os.environ), original)
        self.assertTrue(Path(env["UV_TOOL_DIR"]).is_relative_to(ROOT / ".artifacts"))
        with patch.object(tool.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, str(ROOT / "arbitrary tool directory") + "\n")) as call:
            python = tool.tool_python(["uv"], env)
        self.assertEqual(call.call_args.args[0], ["uv", "tool", "dir"])
        self.assertIn("arbitrary tool directory", str(python))
        self.assertEqual(python.name, "python.exe" if os.name == "nt" else "python")

    def test_bootstrap_noop_repair_and_install_failure(self):
        with TemporaryDirectory() as directory, patch.object(setup, "signature_path", return_value=Path(directory) / "stamp"), patch.object(setup, "uv_command", return_value=["uv"]), patch.object(setup, "tool_python", return_value=Path("runtime-python")), patch.object(setup, "installation_matches", return_value=True), patch.object(setup, "installed_version", return_value=tool.pinned_version()), patch.object(setup.subprocess, "run") as run:
            setup.bootstrap()
            run.assert_not_called()
            setup.bootstrap(repair=True)
            command = run.call_args.args[0]
            self.assertIn("specify-cli==" + tool.pinned_version(), command)
            self.assertIn("--constraint", command)
            self.assertIn("--reinstall", command)
            run.side_effect = subprocess.CalledProcessError(19, command)
            with self.assertRaises(subprocess.CalledProcessError):
                setup.bootstrap(repair=True)

    def test_powershell_encoded_arguments_are_lossless(self):
        arguments = ["", "space value", 'embedded"quote', "Grüße", "--json", "trailing\\"]
        encoded = base64.b64encode(json.dumps(arguments).encode("utf-8")).decode("ascii")
        with patch.object(sys, "argv", ["specify_tool.py", "--repo-args-base64", encoded]), patch.object(tool, "run", return_value=27) as run:
            self.assertEqual(tool.main(), 27)
            run.assert_called_once_with(arguments)

    def test_init_preserves_constitution_on_cli_failure(self):
        import init_speckit
        with TemporaryDirectory() as directory:
            root = Path(directory)
            constitution = root / ".specify/memory/constitution.md"
            constitution.parent.mkdir(parents=True)
            original = b"project-owned constitution\n"
            constitution.write_bytes(original)
            def cli(command, **kwargs):
                self.assertEqual(kwargs["cwd"], root)
                self.assertIn("ps" if os.name == "nt" else "sh", command)
                constitution.write_bytes(b"changed")
                return subprocess.CompletedProcess(command, 17)
            script = root / "scripts/init_speckit.py"
            with patch.object(init_speckit, "__file__", str(script)), patch.object(sys, "argv", [str(script), "--integration", "codex"]), patch.object(init_speckit, "runtime", return_value=(Path(sys.executable), {})), patch.object(init_speckit.subprocess, "run", side_effect=cli):
                self.assertEqual(init_speckit.main(), 17)
            self.assertEqual(constitution.read_bytes(), original)

    def test_changed_constraints_block_stale_installation(self):
        with TemporaryDirectory() as directory:
            env = {"UV_TOOL_DIR": str(Path(directory) / "tools")}
            tool.signature_path(env).write_text("outdated", encoding="utf-8")
            with patch.object(tool, "installed_version", return_value=tool.pinned_version()):
                self.assertFalse(tool.installation_matches(Path("python"), env))
                tool.signature_path(env).write_text(tool.install_signature(), encoding="utf-8")
                self.assertTrue(tool.installation_matches(Path("python"), env))

    def test_real_entrypoint_preserves_arguments_cwd_and_exit_code(self):
        # A controlled package in a genuine venv tests Python's -c argv semantics.
        with TemporaryDirectory() as directory:
            root = Path(directory) / "python environment with spaces"
            venv.EnvBuilder(with_pip=False).create(root)
            python = root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            site = subprocess.check_output([str(python), "-I", "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"], text=True).strip()
            Path(site, "specify_cli.py").write_text(
                "import json, os, sys\ndef main():\n print(json.dumps([sys.argv[1:], os.getcwd()]))\n sys.exit(23)\n",
                encoding="utf-8",
            )
            arguments = ["with spaces", "", "--json", "quotes\"'", "Grüße", "a;b", "$value", "trailing\\"]
            output = Path(directory) / "output.json"
            with output.open("w", encoding="utf-8") as stream, patch.object(tool, "runtime", return_value=(python, dict(os.environ))):
                original_run = subprocess.run
                def capture(command, **kwargs):
                    return original_run(command, stdout=stream, **kwargs)
                with patch.object(tool.subprocess, "run", side_effect=capture):
                    code = tool.run(arguments)
            self.assertEqual(code, 23)
            echoed, cwd = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(echoed, arguments)
            self.assertEqual(Path(cwd), Path.cwd())

    @unittest.skipUnless(os.name == "posix" and shutil.which("sh"), "POSIX shell required")
    def test_shell_syntax(self):
        subprocess.run(["sh", "-n", str(ROOT / "scripts/specify")], check=True)
        subprocess.run(["bash", "-n", str(ROOT / ".devcontainer/post-create.sh")], check=True)


if __name__ == "__main__":
    unittest.main()
