from pathlib import Path
from contextlib import redirect_stdout
import io
import os
import tempfile
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from commands.bootstrap import bootstrap  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_TEMPLATE = REPO_ROOT / "templates" / "AGENTS.template.md"


def _run_bootstrap(*args, **kwargs):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        bootstrap(*args, **kwargs)
    return buffer.getvalue()


class BootstrapWorkspaceIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)

        self.user_mem_dir = self.base / "user-memory"
        os.environ["CADIERNO_USER_MEMORY_DIR"] = str(self.user_mem_dir)

        self.workspace = self.base / "workspace"
        self.project = self.workspace / "user-portal-new"
        self.project.mkdir(parents=True)
        (self.project / "composer.json").write_text(
            '{"require": {"php": "^8.2", "laravel/framework": "^12.0"}}',
            encoding="utf-8",
        )
        (self.project / ".git").mkdir()

        sibling = self.workspace / "admin-portal"
        sibling.mkdir()
        (sibling / "composer.json").write_text("{}", encoding="utf-8")

        (self.workspace / "docker-compose.yml").write_text(
            "\n".join([
                "services:",
                "  nginx_clearit:",
                "    image: nginx:stable-alpine",
                "    volumes:",
                "      - ./admin-portal:/var/www/html/admin-portal",
                "      - ./user-portal-new:/var/www/html/user-portal-new",
                "  user_portal_new:",
                "    build:",
                "      context: ./user-portal-new",
                "  admin_portal:",
                "    build:",
                "      context: ./admin-portal",
                "",
            ]),
            encoding="utf-8",
        )

        nginx_dir = self.workspace / "nginx"
        nginx_dir.mkdir()
        (nginx_dir / "default.conf").write_text(
            "server { location / { proxy_pass http://user_portal_new:9000; } }\n",
            encoding="utf-8",
        )

    def tearDown(self):
        os.environ.pop("CADIERNO_USER_MEMORY_DIR", None)
        self.temp_dir.cleanup()

    def test_auto_detects_workspace_and_generates_new_knowledge_files(self):
        _run_bootstrap(str(self.project))

        knowledge = self.project / "knowledge"
        self.assertTrue((knowledge / "project.md").exists())
        self.assertTrue((knowledge / "architecture.md").exists())
        self.assertTrue((knowledge / "integrations.md").exists())
        self.assertTrue((knowledge / "technical-debt.md").exists())
        self.assertTrue((knowledge / "workspace.md").exists())
        self.assertTrue((knowledge / "infrastructure.md").exists())

        workspace_text = (knowledge / "workspace.md").read_text(encoding="utf-8")
        self.assertIn("admin-portal", workspace_text)
        self.assertIn("user_portal_new", workspace_text)

        infra_text = (knowledge / "infrastructure.md").read_text(encoding="utf-8")
        self.assertIn("nginx_clearit", infra_text)

        agents_text = (self.project / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("cadierno:managed:start:workspace", agents_text)
        self.assertIn(str(self.workspace.resolve()), agents_text)

    def test_no_workspace_flag_preserves_simple_project_behavior(self):
        _run_bootstrap(str(self.project), no_workspace=True)

        knowledge = self.project / "knowledge"
        self.assertTrue((knowledge / "project.md").exists())
        self.assertFalse((knowledge / "workspace.md").exists())
        self.assertFalse((knowledge / "infrastructure.md").exists())

    def test_repeated_bootstrap_without_edits_has_no_conflicts(self):
        _run_bootstrap(str(self.project))
        _run_bootstrap(str(self.project))

        knowledge = self.project / "knowledge"
        conflict_files = list(knowledge.glob("*.cadierno-new"))
        self.assertEqual(conflict_files, [])

    def test_manual_edit_to_generated_knowledge_file_is_never_overwritten(self):
        _run_bootstrap(str(self.project))

        workspace_md = self.project / "knowledge" / "workspace.md"
        manual_content = "# Workspace\n\nNota manual del equipo: no tocar esto.\n"
        workspace_md.write_text(manual_content, encoding="utf-8")

        _run_bootstrap(str(self.project))

        self.assertEqual(workspace_md.read_text(encoding="utf-8"), manual_content)

        conflict_file = self.project / "knowledge" / "workspace.md.cadierno-new"
        self.assertTrue(conflict_file.exists())
        self.assertIn("admin-portal", conflict_file.read_text(encoding="utf-8"))

    def test_agents_md_preserves_manual_sections_outside_managed_block(self):
        template_text = AGENTS_TEMPLATE.read_text(encoding="utf-8")
        agents_path = self.project / "AGENTS.md"
        agents_path.write_text(
            template_text.replace(
                "## Convenciones",
                "## Convenciones\n\nNota manual: usamos PSR-12 estrictamente.",
            ),
            encoding="utf-8",
        )

        _run_bootstrap(str(self.project))

        agents_text = agents_path.read_text(encoding="utf-8")
        self.assertIn("Nota manual: usamos PSR-12 estrictamente.", agents_text)
        self.assertIn(str(self.workspace.resolve()), agents_text)
        self.assertNotIn("Pendiente de ejecutar", agents_text)

    def test_stale_shared_compose_reports_no_match_for_new_project(self):
        # docker-compose.yml en este fixture SÍ referencia a user-portal-new,
        # a diferencia del caso real (donde todavía no lo hacía). Se agrega
        # un segundo proyecto que el compose compartido no conoce en absoluto.
        orphan_project = self.workspace / "partner-portal"
        orphan_project.mkdir()
        (orphan_project / "composer.json").write_text("{}", encoding="utf-8")

        _run_bootstrap(str(orphan_project))

        workspace_text = (orphan_project / "knowledge" / "workspace.md").read_text(encoding="utf-8")
        self.assertIn("No identificado", workspace_text)


if __name__ == "__main__":
    unittest.main()
