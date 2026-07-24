from pathlib import Path
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.context import generate_context
from commands.adapters import enable
from commands.learning import apply
from commands.skills import source_is_trusted


class V3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()
        os.environ["CADIERNO_USER_MEMORY_DIR"] = str(Path(self.tmp.name) / "user")

    def tearDown(self):
        os.environ.pop("CADIERNO_USER_MEMORY_DIR", None)
        self.tmp.cleanup()

    def test_context_is_generated_inside_cadierno_root(self):
        target = generate_context(self.project)
        self.assertEqual(target, self.project / ".cadierno-ai" / "context.md")
        self.assertIn("Filosofía de trabajo", target.read_text(encoding="utf-8"))

    def test_catalog_has_context7(self):
        catalog = Path(__file__).resolve().parents[2] / "skills" / "catalog.json"
        data = json.loads(catalog.read_text(encoding="utf-8"))
        self.assertIn("context7", [skill["id"] for skill in data["skills"]])

    def test_context7_catalog_has_trusted_official_source(self):
        catalog = Path(__file__).resolve().parents[2] / "skills" / "catalog.json"
        skill = json.loads(catalog.read_text(encoding="utf-8"))["skills"][0]
        self.assertTrue(source_is_trusted(skill))
        self.assertIn("SKILL.md", skill["expected_files"])

    def test_adapter_creates_local_bridges(self):
        (self.project / ".cadierno-ai").mkdir()
        enable(str(self.project), ["codex", "claude", "cursor"])
        self.assertTrue((self.project / "AGENTS.md").is_file())
        self.assertEqual((self.project / "CLAUDE.md").read_text(encoding="utf-8"), "@.cadierno-ai/AGENTS.md\n")
        self.assertTrue((self.project / ".cursor" / "rules" / "cadierno-ai.mdc").is_file())

    def test_learning_apply_marks_audited_outcomes(self):
        root = self.project / ".cadierno-ai"
        (root / "learning").mkdir(parents=True)
        proposal = root / "learning" / "proposal.md"
        proposal.write_text("## Decisiones propuestas\n\n- [ ] Conservar expiración de 30 minutos.\n\n## Deuda técnica propuesta\n\n- [ ] Incorporar alerta de pagos tardíos.\n", encoding="utf-8")
        with patch("builtins.input", side_effect=["1", "3"]):
            apply(str(self.project), str(proposal))
        content = proposal.read_text(encoding="utf-8")
        self.assertIn("_(aprobada)_", content)
        self.assertIn("_(rechazada)_", content)
        decisions = (root / "knowledge" / "decisions.md").read_text(encoding="utf-8")
        self.assertIn("Conservar expiración", decisions)
