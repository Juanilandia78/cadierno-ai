from pathlib import Path
import os
import tempfile
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.workspace import (  # noqa: E402
    WorkspaceError,
    auto_detect_workspace_root,
    detect_workspace,
    resolve_explicit_workspace_root,
    scan_workspace,
)


class WorkspaceAutoDetectionTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        os.environ.pop("CADIERNO_WORKSPACE_MAX_DEPTH", None)

    def tearDown(self):
        os.environ.pop("CADIERNO_WORKSPACE_MAX_DEPTH", None)
        self.temp_dir.cleanup()

    def test_finds_nearest_ancestor_with_docker_compose(self):
        # Réplica del caso real: workspace/docker-compose.yml, nginx/, y
        # project/ que además tiene su PROPIO .git y su propio compose local.
        workspace = self.root / "workspace"
        project = workspace / "user-portal-new"
        project.mkdir(parents=True)
        (workspace / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")
        (workspace / "nginx").mkdir()
        (project / ".git").mkdir()
        (project / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")

        detection = auto_detect_workspace_root(project)

        self.assertEqual(detection.root, workspace.resolve())
        self.assertEqual(detection.method, "auto")
        self.assertIn("docker-compose.yml", detection.evidence)

    def test_stops_at_ancestor_git_boundary_without_strong_evidence(self):
        outer = self.root / "outer"
        middle = outer / "middle"
        project = middle / "project"
        project.mkdir(parents=True)
        (outer / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")
        (middle / ".git").mkdir()

        detection = auto_detect_workspace_root(project)

        self.assertIsNone(detection.root)
        self.assertEqual(detection.method, "none")

    def test_weak_evidence_alone_never_triggers_detection(self):
        parent = self.root / "parent"
        project = parent / "project"
        project.mkdir(parents=True)
        (parent / "Makefile").write_text("build:\n\techo hi\n", encoding="utf-8")
        (parent / "package.json").write_text("{}", encoding="utf-8")

        detection = auto_detect_workspace_root(project)

        self.assertIsNone(detection.root)
        self.assertEqual(detection.method, "none")

    def test_max_depth_bounds_the_search(self):
        # project -> parent "c" (depth 0) -> "b" (depth 1) -> "a" (depth 2, evidencia).
        # Llegar a "a" requiere que el bucle todavía itere en depth=2, o sea max_depth >= 3.
        project = self.root / "a" / "b" / "c" / "project"
        project.mkdir(parents=True)
        (self.root / "a" / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")

        os.environ["CADIERNO_WORKSPACE_MAX_DEPTH"] = "2"
        try:
            detection_narrow = auto_detect_workspace_root(project)
        finally:
            os.environ.pop("CADIERNO_WORKSPACE_MAX_DEPTH", None)

        self.assertIsNone(detection_narrow.root)

        os.environ["CADIERNO_WORKSPACE_MAX_DEPTH"] = "3"
        try:
            detection_wide = auto_detect_workspace_root(project)
        finally:
            os.environ.pop("CADIERNO_WORKSPACE_MAX_DEPTH", None)

        self.assertEqual(detection_wide.root, (self.root / "a").resolve())

    def test_no_evidence_anywhere_returns_none(self):
        project = self.root / "solo-project"
        project.mkdir(parents=True)

        detection = auto_detect_workspace_root(project)

        self.assertIsNone(detection.root)
        self.assertEqual(detection.method, "none")


class WorkspaceExplicitResolutionTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_accepts_project_inside_explicit_root(self):
        workspace = self.root / "workspace"
        project = workspace / "project-a"
        project.mkdir(parents=True)

        detection = resolve_explicit_workspace_root(project, workspace)

        self.assertEqual(detection.root, workspace.resolve())
        self.assertEqual(detection.method, "explicit")

    def test_accepts_project_equal_to_explicit_root(self):
        workspace = self.root / "workspace"
        workspace.mkdir(parents=True)

        detection = resolve_explicit_workspace_root(workspace, workspace)

        self.assertEqual(detection.root, workspace.resolve())

    def test_rejects_project_outside_explicit_root(self):
        workspace = self.root / "workspace"
        other = self.root / "other-project"
        workspace.mkdir(parents=True)
        other.mkdir(parents=True)

        with self.assertRaises(WorkspaceError):
            resolve_explicit_workspace_root(other, workspace)

    def test_rejects_nonexistent_root(self):
        project = self.root / "project"
        project.mkdir(parents=True)

        with self.assertRaises(WorkspaceError):
            resolve_explicit_workspace_root(project, self.root / "no-existe")


class DetectWorkspaceDispatchTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_no_workspace_and_explicit_root_together_is_an_error(self):
        workspace = self.root / "workspace"
        project = workspace / "project"
        project.mkdir(parents=True)

        with self.assertRaises(WorkspaceError):
            detect_workspace(project, workspace, True)

    def test_disabled_returns_disabled_method(self):
        project = self.root / "project"
        project.mkdir(parents=True)

        detection = detect_workspace(project, None, True)

        self.assertIsNone(detection.root)
        self.assertEqual(detection.method, "disabled")

    def test_no_flags_falls_back_to_auto_detection(self):
        workspace = self.root / "workspace"
        project = workspace / "project"
        project.mkdir(parents=True)
        (workspace / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")

        detection = detect_workspace(project, None, False)

        self.assertEqual(detection.root, workspace.resolve())
        self.assertEqual(detection.method, "auto")


class ScanWorkspaceTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name) / "workspace"
        self.workspace.mkdir(parents=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_detects_siblings_nginx_and_env_var_names_only(self):
        project = self.workspace / "user-portal-new"
        project.mkdir()
        (project / "composer.json").write_text("{}", encoding="utf-8")

        sibling = self.workspace / "admin-portal"
        sibling.mkdir()
        (sibling / "composer.json").write_text("{}", encoding="utf-8")

        (self.workspace / "docker-compose.yml").write_text(
            "services:\n  user_portal_new:\n    build:\n      context: ./user-portal-new\n",
            encoding="utf-8",
        )

        nginx_dir = self.workspace / "nginx"
        nginx_dir.mkdir()
        (nginx_dir / "default.conf").write_text(
            "server {\n  server_name example.com;\n  location / {\n    proxy_pass http://user_portal_new:9000;\n  }\n}\n",
            encoding="utf-8",
        )

        (self.workspace / ".env").write_text(
            "DB_PASSWORD=unValorMuySecreto\nDB_HOST=mysql\n",
            encoding="utf-8",
        )

        detection = detect_workspace(project, None, False)
        info = scan_workspace(detection, project)

        sibling_names = [s.name for s in info.sibling_projects]
        self.assertIn("admin-portal", sibling_names)
        self.assertNotIn("user-portal-new", sibling_names)

        self.assertTrue(info.nginx.detected)
        self.assertIn("http://user_portal_new:9000", info.nginx.upstreams)

        self.assertIn(".env", info.root_env_files)
        self.assertEqual(info.root_env_var_names[".env"], ["DB_HOST", "DB_PASSWORD"])

        dump = repr(info.root_env_var_names)
        self.assertNotIn("unValorMuySecreto", dump)

    def test_no_workspace_returns_empty_info(self):
        project = self.workspace / "solo-project"
        project.mkdir()

        detection = detect_workspace(project, None, True)
        info = scan_workspace(detection, project)

        self.assertIsNone(info.root)
        self.assertEqual(info.sibling_projects, [])
        self.assertFalse(info.nginx.detected)


if __name__ == "__main__":
    unittest.main()
