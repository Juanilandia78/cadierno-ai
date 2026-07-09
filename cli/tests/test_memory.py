from pathlib import Path
import os
import tempfile
import unittest
import uuid

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.memory import (  # noqa: E402
    add_history_event,
    get_effective_style,
    get_history,
    initialize_memory,
    save_observation,
    search_observations,
    set_style,
)


class MemorySQLiteTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)
        self.project = self.base / "project"
        self.project.mkdir(parents=True, exist_ok=True)

        self.user_mem_dir = self.base / "user-memory"
        os.environ["CADIERNO_USER_MEMORY_DIR"] = str(self.user_mem_dir)

    def tearDown(self):
        os.environ.pop("CADIERNO_USER_MEMORY_DIR", None)
        self.temp_dir.cleanup()

    def test_style_resolution_workspace_over_user(self):
        initialize_memory(self.project)

        set_style(self.project, "professional", scope="user")
        set_style(self.project, "argentino", scope="workspace")

        effective = get_effective_style(self.project)
        self.assertEqual(effective, "argentino")

    def test_save_and_search_observations(self):
        initialize_memory(self.project)

        unique_token = str(uuid.uuid4())
        save_observation(
            self.project,
            title="Bug de cobro",
            content=f"Se detecto doble cobro en checkout {unique_token}",
            observation_type="bugfix",
            tags=["pagos", "mercadopago"],
            scope="workspace",
        )

        rows = search_observations(self.project, query=unique_token, scope="workspace", limit=5)

        self.assertEqual(len(rows), 1)
        self.assertIn(unique_token, rows[0]["content"])
        self.assertEqual(rows[0]["type"], "bugfix")

    def test_history_events_are_persisted(self):
        initialize_memory(self.project)
        add_history_event(self.project, "bootstrap", "Generacion de knowledge")

        rows = get_history(self.project, scope="workspace", limit=5)
        self.assertTrue(rows)
        self.assertEqual(rows[-1]["event"], "bootstrap")


if __name__ == "__main__":
    unittest.main()
