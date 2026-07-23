from pathlib import Path
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.managed_sections import extract_managed_section, upsert_managed_section  # noqa: E402


class ManagedSectionsTests(unittest.TestCase):

    def test_appends_block_when_missing(self):
        original = "# AGENTS\n\n## Convenciones\n\nUsar PSR-12.\n"

        updated = upsert_managed_section(original, "workspace", "Contenido A")

        self.assertTrue(updated.startswith(original.rstrip("\n")))
        self.assertIn("<!-- cadierno:managed:start:workspace -->", updated)
        self.assertIn("Contenido A", updated)
        self.assertIn("<!-- cadierno:managed:end:workspace -->", updated)

    def test_replaces_only_the_matching_block(self):
        original = (
            "# AGENTS\n\n"
            "## Convenciones\n\nNota manual del equipo, no tocar.\n\n"
            "<!-- cadierno:managed:start:workspace -->\nViejo contenido\n<!-- cadierno:managed:end:workspace -->\n"
        )

        updated = upsert_managed_section(original, "workspace", "Nuevo contenido")

        self.assertIn("Nota manual del equipo, no tocar.", updated)
        self.assertNotIn("Viejo contenido", updated)
        self.assertIn("Nuevo contenido", updated)

    def test_untouched_content_outside_block_is_byte_identical(self):
        prefix = "# AGENTS\n\n## Convenciones\n\nNota manual antes.\n\n"
        suffix = "\n\n## Observaciones\n\nNota manual después.\n"
        original = (
            prefix
            + "<!-- cadierno:managed:start:workspace -->\nViejo\n<!-- cadierno:managed:end:workspace -->"
            + suffix
        )

        updated = upsert_managed_section(original, "workspace", "Nuevo")

        self.assertTrue(updated.startswith(prefix))
        self.assertTrue(updated.endswith(suffix))

    def test_does_not_touch_other_managed_keys(self):
        original = (
            "<!-- cadierno:managed:start:stack -->\nStack info\n<!-- cadierno:managed:end:stack -->\n"
        )

        updated = upsert_managed_section(original, "workspace", "Workspace info")

        self.assertIn("Stack info", updated)
        self.assertIn("Workspace info", updated)

    def test_idempotent_on_repeated_upsert(self):
        original = "# AGENTS\n\nTexto libre.\n"

        first = upsert_managed_section(original, "workspace", "Contenido estable")
        second = upsert_managed_section(first, "workspace", "Contenido estable")

        self.assertEqual(first, second)

    def test_extract_managed_section_returns_inner_content(self):
        original = upsert_managed_section("", "workspace", "Hola\nMundo")

        extracted = extract_managed_section(original, "workspace")

        self.assertEqual(extracted, "Hola\nMundo")

    def test_extract_managed_section_returns_none_when_absent(self):
        self.assertIsNone(extract_managed_section("# AGENTS\n\nSin bloques.\n", "workspace"))


if __name__ == "__main__":
    unittest.main()
