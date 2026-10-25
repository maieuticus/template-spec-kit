"""Exercise generated projects, overwrite protection and reference isolation."""

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check import validate
from check_analyze_gate import validate_report
from container_init import prepare
from create_project import create_project, render_files


class ProjectGenerationTests(unittest.TestCase):
    def generate(self, directory, stack="none", services=None, recipe=None):
        destination = Path(directory) / "project"
        create_project(destination, render_files("test-project", stack, services or [], recipe))
        return destination

    def test_profiles_produce_consistent_self_contained_projects(self):
        for stack in ("none", "python", "typescript", "java-maven"):
            with self.subTest(stack=stack), TemporaryDirectory() as directory:
                root = self.generate(directory, stack)
                self.assertEqual(validate(root), [])
                self.assertTrue((root / "docs/DV_KONZEPT.md").is_file())
                self.assertTrue((root / "scripts/check_analyze_gate.py").is_file())
                analyze_guide = (root / "docs/DV_KONZEPT.md").read_text(encoding="utf-8")
                self.assertIn("Keine wesentlichen Befunde.", analyze_guide)
                self.assertIn("Geändertes Artefakt", analyze_guide)
                self.assertFalse((root / "templates").exists())
                self.assertFalse((root / ".env").exists())
                self.assertFalse((root / ".specify/integration.json").exists())
                self.assertFalse(any(root.rglob("*sport_app*")))
                instructions = (root / ".github/copilot-instructions.md").read_text(encoding="utf-8")
                readme = (root / "README.md").read_text(encoding="utf-8")
                self.assertIn("## Spec Kit aktivieren: Desktop und Codespaces", readme)
                self.assertIn("--integration copilot", readme)
                self.assertIn("$speckit-specify", readme)
                self.assertIn("/speckit-specify", readme)
                container = json.loads((root / ".devcontainer/devcontainer.json").read_text(encoding="utf-8"))
                self.assertEqual("bash .devcontainer/post-create.sh", container["postCreateCommand"])
                self.assertTrue((root / ".devcontainer/post-create.sh").is_file())
                self.assertIn("Nenne in jeder inhaltlichen Antwort", instructions)
                self.assertIn("`▶ Nächste Aktion`", instructions)
                self.assertIn("`⏸ Entscheidung benötigt`", instructions)
                self.assertIn("`⛔ Blockiert`", instructions)
                self.assertIn("**Fertig, wenn**", instructions)
                self.assertIn("**Ausführung:** `speckit-specify`", instructions)
                self.assertIn("**Entscheidung**, **Warum jetzt** und **Danach**", instructions)
                self.assertIn("**Blocker**, **Aufhebung** und **Danach**", instructions)
                self.assertIn("`claude-haiku-5.5`", instructions)
                self.assertIn("`gpt-5.3-codex`", instructions)
                self.assertIn("`gpt-6-luna`", instructions)
                self.assertIn("maieuticus/template-spec-kit", instructions)
                expected_agents = (
                    "speckit-specify.agent.md",
                    "speckit-clarify.agent.md",
                    "speckit-plan.agent.md",
                    "speckit-tasks.agent.md",
                    "speckit-analyze.agent.md",
                    "speckit-implement.agent.md",
                    "speckit-converge.agent.md",
                )
                for agent_file in expected_agents:
                    agent_path = root / ".github" / "agents" / agent_file
                    self.assertTrue(agent_path.is_file())
                    content = agent_path.read_text(encoding="utf-8")
                    self.assertIn("\nname: ", content)
                    self.assertIn("\ndescription: ", content)
                    self.assertIn("---\n", content)
                    self.assertIn(".specify/memory/constitution.md", content)
                    if agent_file == "speckit-analyze.agent.md":
                        self.assertIn("## Wesentliche Befunde", content)
                        self.assertIn("**Geändertes Artefakt:**", content)
                        self.assertIn("Akzeptanzkriterien", content)
                        self.assertIn("Schnittstellen, Daten, Sicherheit oder Betrieb", content)
                        self.assertIn("Redaktionelle Befunde", content)
                    if agent_file == "speckit-converge.agent.md":
                        self.assertIn("**converge**", content)
                        self.assertIn("Akzeptanzkriterium", content)
                        self.assertIn("tasks.md", content)
                        self.assertIn("keine Codeänderungen", content)
                        self.assertIn("`gpt-6-luna`", content)
                if stack == "java-maven":
                    self.assertTrue((root / "src/test/java/example/AppTest.java").is_file())
                    self.assertFalse((root / "tests").exists())

    @unittest.skipUnless(os.name == "posix" and shutil.which("bash"), "Bash-Lauf ohne Ausführungsbit benötigt POSIX")
    def test_generated_post_create_runs_without_script_execute_permission(self):
        with TemporaryDirectory() as directory:
            root = self.generate(directory)
            script = root / ".devcontainer/post-create.sh"
            script.chmod(0o644)
            bin_dir = Path(directory) / "bin"
            bin_dir.mkdir()
            copilot = bin_dir / "copilot"
            copilot.write_text("#!/bin/sh\n[ \"$1\" = \"--version\" ] || exit 2\nprintf 'copilot-test\\n'\n", encoding="utf-8")
            copilot.chmod(0o755)
            container = json.loads((root / ".devcontainer/devcontainer.json").read_text(encoding="utf-8"))
            result = subprocess.run(
                ["/bin/sh", "-c", container["postCreateCommand"]], cwd=root,
                env={**os.environ, "PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", "")},
                capture_output=True, text=True, check=True,
            )
            self.assertIn("copilot-test", result.stdout)

    def test_analyze_gate_checks_report_before_manual_gate_in_source_and_generated_project(self):
        def assert_workflow_contract(workflow_path: Path) -> None:
            workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
            steps = workflow["steps"]
            step_ids = [step["id"] for step in steps]

            analyze_index = step_ids.index("analyze")
            check_index = step_ids.index("analyze-report-check")
            gate_index = step_ids.index("analyze-gate")
            implement_index = step_ids.index("implement")
            review_index = step_ids.index("review")

            self.assertEqual(check_index, analyze_index + 1)
            self.assertEqual(gate_index, check_index + 1)
            self.assertEqual(implement_index, gate_index + 1)
            self.assertLess(implement_index, review_index)
            self.assertEqual(step_ids[implement_index:review_index + 1], ["implement", "checks", "converge", "review"])

            report_check = steps[check_index]
            self.assertEqual(report_check["type"], "shell")
            self.assertEqual(report_check["run"], "python scripts/check_analyze_gate.py")
            self.assertEqual(report_check["output_format"], "json")
            self.assertIn("## Wesentliche Befunde", steps[analyze_index]["input"]["args"])
            self.assertIn("Geändertes Artefakt", steps[analyze_index]["input"]["args"])
            self.assertIn(
                "Akzeptanzkriterien, Schnittstellen, Daten, Sicherheit oder Betrieb",
                steps[analyze_index]["input"]["args"],
            )
            self.assertIn("Redaktionelle Befunde blockieren nicht", steps[analyze_index]["input"]["args"])

            gate = steps[gate_index]
            self.assertEqual(gate["type"], "gate")
            self.assertEqual(gate["options"], ["approve", "reject"])
            self.assertEqual(gate["on_reject"], "abort")
            self.assertEqual(
                gate["show_file"],
                "{{ steps.analyze-report-check.output.data.report_path }}",
            )

        assert_workflow_contract(ROOT / ".specify/workflows/project-sdd/workflow.yml")

        with TemporaryDirectory() as directory:
            root = self.generate(directory)
            assert_workflow_contract(root / ".specify/workflows/project-sdd/workflow.yml")

    def test_analyze_report_validator_fails_closed_and_accepts_resolved_or_empty_reports(self):
        def write_report(root: Path, content: str | None) -> Path:
            feature_dir = root / "specs/004-example"
            feature_dir.mkdir(parents=True)
            (root / ".specify").mkdir()
            (root / ".specify/feature.json").write_text(
                json.dumps({"feature_directory": "specs/004-example"}),
                encoding="utf-8",
            )
            report = feature_dir / "analyze.md"
            if content is not None:
                report.write_text(content, encoding="utf-8")
            return report

        with TemporaryDirectory() as directory:
            root = Path(directory)
            report = write_report(
                root,
                "# Analyse\n\n## Wesentliche Befunde\n\n"
                "### A001 — P1: Offener Vertrag\n"
                "- **Status:** offen\n"
                "- **Begründung:** Das Verhalten ist widersprüchlich.\n",
            )
            checked_path, errors = validate_report(root)
            self.assertEqual(checked_path, report)
            self.assertTrue(any("Befund ist offen" in error for error in errors))

        with TemporaryDirectory() as directory:
            root = Path(directory)
            report = write_report(
                root,
                "# Analyse\n\n## Wesentliche Befunde\n\n"
                "### A001 — P1: Vertrag angepasst\n"
                "- **Status:** geklärt\n"
                "- **Begründung:** Die Spec wurde angeglichen.\n"
                "- **Geändertes Artefakt:** `spec.md`\n",
            )
            checked_path, errors = validate_report(root)
            self.assertEqual(checked_path, report)
            self.assertEqual(errors, [])

        with TemporaryDirectory() as directory:
            root = Path(directory)
            report = write_report(
                root,
                "# Analyse\n\n## Wesentliche Befunde\n\n"
                "### A001 — P1: Risikoentscheidung\n"
                "- **Status:** akzeptiert\n"
                "- **Begründung:** Die zuständige Person hat die dokumentierte "
                "Restrisikoentscheidung getroffen.\n",
            )
            checked_path, errors = validate_report(root)
            self.assertEqual(checked_path, report)
            self.assertEqual(errors, [])

        with TemporaryDirectory() as directory:
            root = Path(directory)
            report = write_report(
                root,
                "# Analyse\n\n## Wesentliche Befunde\n\n"
                "### A001 — P1: Fehlender Nachweis\n"
                "- **Status:** geklärt\n"
                "- **Begründung:** Änderung wurde vorgenommen.\n",
            )
            checked_path, errors = validate_report(root)
            self.assertEqual(checked_path, report)
            self.assertTrue(any("Geändertes Artefakt" in error for error in errors))

        with TemporaryDirectory() as directory:
            root = Path(directory)
            report = write_report(root, "# Analyse\n\n## Wesentliche Befunde\n\nKeine wesentlichen Befunde.\n")
            checked_path, errors = validate_report(root)
            self.assertEqual(checked_path, report)
            self.assertEqual(errors, [])

    def test_analyze_report_validator_blocks_missing_context_report_and_unknown_status(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "specs").mkdir()
            checked_path, errors = validate_report(root)
            self.assertIsNone(checked_path)
            self.assertTrue(any(".specify/feature.json" in error for error in errors))

        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".specify").mkdir()
            (root / "specs").mkdir()
            (root / "outside").mkdir()
            (root / ".specify/feature.json").write_text(
                json.dumps({"feature_directory": "outside"}),
                encoding="utf-8",
            )
            checked_path, errors = validate_report(root)
            self.assertIsNone(checked_path)
            self.assertTrue(any("direkt unter specs/" in error for error in errors))

        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_root = root / ".specify"
            write_root.mkdir()
            (write_root / "feature.json").write_text(
                json.dumps({"feature_directory": "specs/004-example"}),
                encoding="utf-8",
            )
            (root / "specs/004-example").mkdir(parents=True)
            checked_path, errors = validate_report(root)
            self.assertTrue(any("Analysebericht fehlt" in error for error in errors))
            self.assertIsNotNone(checked_path)

        with TemporaryDirectory() as directory:
            root = Path(directory)
            feature_dir = root / "specs/004-example"
            feature_dir.mkdir(parents=True)
            (root / ".specify").mkdir()
            (root / ".specify/feature.json").write_text(
                json.dumps({"feature_directory": "specs/004-example"}),
                encoding="utf-8",
            )
            (feature_dir / "analyze.md").write_text(
                "# Analyse\n\n## Wesentliche Befunde\n\n"
                "### A001 — P1: Ungültiger Status\n"
                "- **Status:** maybe\n"
                "- **Begründung:** Unbekannter Status.\n",
                encoding="utf-8",
            )
            checked_path, errors = validate_report(root)
            self.assertIsNotNone(checked_path)
            self.assertTrue(any("unbekannter Status" in error for error in errors))

        with TemporaryDirectory() as directory:
            root = Path(directory)
            feature_dir = root / "specs/004-example"
            feature_dir.mkdir(parents=True)
            (root / ".specify").mkdir()
            (root / ".specify/feature.json").write_text(
                json.dumps({"feature_directory": "specs/004-example"}),
                encoding="utf-8",
            )
            (feature_dir / "analyze.md").write_text(
                "# Analyse\n\n## Wesentliche Befunde\n\n"
                "### A001 — P1: Fehlender Status\n"
                "- **Begründung:** Statusangabe fehlt.\n",
                encoding="utf-8",
            )
            checked_path, errors = validate_report(root)
            self.assertIsNotNone(checked_path)
            self.assertTrue(any("genau ein Statusfeld ist erforderlich" in error for error in errors))
            self.assertTrue(any("Status offen, geklärt oder akzeptiert dokumentieren" in error for error in errors))

    def test_analyze_report_validator_rejects_unknown_and_duplicate_fields(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            feature_dir = root / "specs/004-example"
            feature_dir.mkdir(parents=True)
            (root / ".specify").mkdir()
            (root / ".specify/feature.json").write_text(
                json.dumps({"feature_directory": "specs/004-example"}),
                encoding="utf-8",
            )
            (feature_dir / "analyze.md").write_text(
                "# Analyse\n\n## Wesentliche Befunde\n\n"
                "### A001 — P1: Unerwartete Felder\n"
                "- **Status:** akzeptiert\n"
                "- **Begründung:** Entscheidung dokumentiert.\n"
                "- **Zusatzfeld:** darf nicht vorkommen.\n"
                "- **Geändertes Artefakt:** plan.md\n"
                "- **Geändertes Artefakt:** tasks.md\n",
                encoding="utf-8",
            )
            checked_path, errors = validate_report(root)
            self.assertIsNotNone(checked_path)
            self.assertTrue(any("unbekanntes Feld" in error for error in errors), errors)
            self.assertTrue(any("darf nur einmal vorkommen" in error for error in errors), errors)

    def test_analyze_report_validator_rejects_empty_fields_before_other_fields(self):
        reports = (
            "- **Status:** geklärt\n- **Begründung:**\n- **Geändertes Artefakt:** spec.md\n",
            "- **Status:** geklärt\n- **Begründung:** \t\n\n- **Geändertes Artefakt:** spec.md\n",
            "- **Status:** geklärt\n- **Geändertes Artefakt:**\n- **Begründung:** Behoben.\n",
            "- **Status:** geklärt\n- **Geändertes Artefakt:** \t\n\n- **Begründung:** Behoben.\n",
        )
        for fields in reports:
            with self.subTest(fields=fields), TemporaryDirectory() as directory:
                root = Path(directory)
                (root / ".specify").mkdir()
                feature = root / "specs/004-example"
                feature.mkdir(parents=True)
                (root / ".specify/feature.json").write_text(
                    json.dumps({"feature_directory": "specs/004-example"}), encoding="utf-8"
                )
                (feature / "analyze.md").write_text(
                    "## Wesentliche Befunde\n\n### A001 — P1: Test\n" + fields,
                    encoding="utf-8",
                )
                _, errors = validate_report(root)
                expected = "Begründung" if fields.index("Begründung") < fields.index("Artefakt") else "Artefakt"
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_analyze_report_validator_rejects_unparsed_findings(self):
        prefixes = (
            "Offener wesentlicher Befund: Sicherheitsvertrag fehlt.\n",
            "#### A001 — P1: Offener Befund\n- **Status:** offen\n- **Begründung:** Vertrag fehlt.\n",
            "  ### A001 — P1: Offener Befund\n- **Status:** offen\n- **Begründung:** Vertrag fehlt.\n",
        )
        accepted = "### A002 — P2: Akzeptierter Befund\n- **Status:** akzeptiert\n- **Begründung:** Bewusst akzeptiert.\n"
        for prefix in prefixes:
            with self.subTest(prefix=prefix), TemporaryDirectory() as directory:
                root = Path(directory)
                (root / ".specify").mkdir()
                feature = root / "specs/004-example"
                feature.mkdir(parents=True)
                (root / ".specify/feature.json").write_text(
                    json.dumps({"feature_directory": "specs/004-example"}), encoding="utf-8"
                )
                (feature / "analyze.md").write_text(
                    "## Wesentliche Befunde\n\n" + prefix + "\n" + accepted, encoding="utf-8"
                )
                _, errors = validate_report(root)
                self.assertTrue(errors, "Unvollständig strukturierter Bericht darf das Gate nicht passieren")

    def test_services_have_valid_files_and_only_read_access_to_foreign_contents(self):
        with TemporaryDirectory() as directory:
            root = self.generate(directory, "python", ["postgres", "keycloak", "observability"])
            self.assertEqual(validate(root), [])
            compose = yaml.safe_load((root / ".devcontainer/compose.yaml").read_text())
            container = json.loads((root / ".devcontainer/devcontainer.json").read_text())
            self.assertEqual(set(container["runServices"]), set(compose["services"]))
            self.assertEqual(set(compose["services"]), {"dev", "postgres", "keycloak", "grafana", "prometheus"})
            for service in compose["services"].values():
                self.assertNotIn("privileged", service)
                self.assertNotIn("ports", service)
                for volume in service.get("volumes", []):
                    if isinstance(volume, dict):
                        self.assertNotIn("docker.sock", volume["source"])
                        self.assertTrue((root / ".devcontainer" / volume["source"]).resolve().exists())
                        if volume["target"] != "/workspaces/project":
                            self.assertTrue(volume["read_only"])
            permissions = container["customizations"]["codespaces"]["repositories"]["maieuticus/*"]["permissions"]
            self.assertEqual(permissions, {"contents": "read", "issues": "write"})

    def test_api_recipe_selects_python_postgres_and_contract_tests(self):
        files = render_files("my-api", "none", [], "api-service")
        config = yaml.safe_load(files["config/project.yaml"])
        self.assertEqual(config["stack"], "python")
        self.assertEqual(config["services"], ["postgres"])
        self.assertIn("openapi/openapi.json", files)
        self.assertIn("tests/test_openapi_contract.py", files)
        self.assertIn("RUN_DATABASE_TESTS=1", files[".github/workflows/ci.yml"].decode())
        self.assertNotIn("POSTGRES_PASSWORD:", files[".github/workflows/ci.yml"].decode())
        instructions = files[".github/copilot-instructions.md"].decode()
        self.assertIn("Nenne in jeder inhaltlichen Antwort", instructions)
        self.assertIn("API-Projektkontext", instructions)

    def test_rejects_populated_destination_without_touching_it(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            sentinel = root / "user.txt"
            sentinel.write_text("preserve", encoding="utf-8")
            with self.assertRaises(ValueError):
                create_project(root, {"user.txt": b"overwrite"})
            self.assertEqual(sentinel.read_text(), "preserve")
            self.assertEqual(len(list(root.iterdir())), 1)

    def test_rejects_invalid_names_incompatible_profiles_and_path_escape(self):
        for name in ("../escape", "name/other", "--option", "name\nother"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                render_files(name, "python", [])
        with self.assertRaises(ValueError):
            render_files("test", "typescript", [], "api-service")
        with TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            with self.assertRaises(ValueError):
                create_project(root, {"../escape": b"no"})
            self.assertFalse(root.exists())

    def test_dry_run_creates_nothing(self):
        with TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            root = Path(directory) / "project"
            create_project(root, {"README.md": b"example"}, dry_run=True)
            self.assertFalse(root.exists())

    def test_static_checks_reject_split_concept_and_broken_links(self):
        with TemporaryDirectory() as directory:
            root = self.generate(directory)
            (root / "docs/architecture.md").write_text("# Duplicate", encoding="utf-8")
            (root / "README.md").write_text("[broken](missing.md)", encoding="utf-8")
            errors = validate(root)
            self.assertTrue(any("architecture.md" in error for error in errors))
            self.assertTrue(any("missing.md" in error for error in errors))


class ContainerTests(unittest.TestCase):
    def test_readonly_mount_random_secrets_and_preservation(self):
        with TemporaryDirectory() as directory, patch.dict(os.environ, {"CODESPACES": "false", "REFERENCE_REPOS_ROOT": ""}):
            root = Path(directory) / "project"
            root.mkdir()
            (root / ".devcontainer").mkdir()
            (root / ".env.example").write_text("PASSWORD=__GENERATE__\nOTHER=__GENERATE__\n", encoding="utf-8")
            refs = Path(directory) / "references"
            refs.mkdir()
            prepare(root, str(refs))
            env = (root / ".env").read_bytes()
            self.assertNotIn(b"__GENERATE__", env)
            self.assertNotEqual(env.splitlines()[0].split(b"=")[1], env.splitlines()[1].split(b"=")[1])
            prepare(root)
            self.assertEqual(env, (root / ".env").read_bytes())
            override = yaml.safe_load((root / ".devcontainer/compose.local.yaml").read_text())
            mount = override["services"]["dev"]["volumes"][0]
            self.assertTrue(mount["read_only"])
            self.assertFalse(mount["bind"]["create_host_path"])
            self.assertEqual(mount["target"], "/references/repos")

    def test_missing_reference_fails_before_writing_local_configuration(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".devcontainer").mkdir()
            with patch.dict(os.environ, {"CODESPACES": "false"}), self.assertRaises(FileNotFoundError):
                prepare(root, str(root / "missing"))
            self.assertFalse((root / ".devcontainer/compose.local.yaml").exists())


if __name__ == "__main__":
    unittest.main()
