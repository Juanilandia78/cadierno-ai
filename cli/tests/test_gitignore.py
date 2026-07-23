from pathlib import Path
import tempfile
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.gitignore import GITIGNORE_ENTRIES, ensure_gitignore_entries  # noqa: E402


class GitignoreTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_creates_gitignore_when_missing(self):
        result = ensure_gitignore_entries(self.project)

        self.assertEqual(result, "created")
        content = (self.project / ".gitignore").read_text(encoding="utf-8")
        for entry in [".ai/", "playbooks/", "checklists/", "knowledge/", "memory/", "AGENTS.md", "CLAUDE.md"]:
            self.assertIn(entry, content)

    def test_appends_without_touching_existing_rules(self):
        gitignore_path = self.project / ".gitignore"
        gitignore_path.write_text("node_modules/\nvendor/\n.env\n", encoding="utf-8")

        result = ensure_gitignore_entries(self.project)

        self.assertEqual(result, "updated")
        content = gitignore_path.read_text(encoding="utf-8")
        self.assertIn("node_modules/", content)
        self.assertIn("vendor/", content)
        self.assertIn(".env", content)
        self.assertIn("knowledge/", content)
        self.assertIn("AGENTS.md", content)

    def test_idempotent_second_run_reports_unchanged(self):
        ensure_gitignore_entries(self.project)

        second_result = ensure_gitignore_entries(self.project)

        self.assertEqual(second_result, "unchanged")

    def test_preserves_manual_edits_outside_managed_block(self):
        gitignore_path = self.project / ".gitignore"
        gitignore_path.write_text("# reglas propias del equipo\n.DS_Store\n", encoding="utf-8")

        ensure_gitignore_entries(self.project)
        # El equipo agrega una regla propia despues de que Cadierno gestiono su bloque.
        content = gitignore_path.read_text(encoding="utf-8")
        gitignore_path.write_text(content + "\ndist/\n", encoding="utf-8")

        ensure_gitignore_entries(self.project)

        final_content = gitignore_path.read_text(encoding="utf-8")
        self.assertIn(".DS_Store", final_content)
        self.assertIn("dist/", final_content)
        self.assertIn("knowledge/", final_content)

    def test_entries_constant_matches_the_seven_installed_paths(self):
        for entry in [".ai/", "playbooks/", "checklists/", "knowledge/", "memory/", "AGENTS.md", "CLAUDE.md"]:
            self.assertIn(entry, GITIGNORE_ENTRIES)


if __name__ == "__main__":
    unittest.main()
