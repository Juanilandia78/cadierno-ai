from pathlib import Path
import tempfile
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.env_scan import extract_env_var_names  # noqa: E402


class EnvScanTests(unittest.TestCase):

    def test_extracts_only_names_never_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join([
                    "# comentario",
                    "",
                    "APP_NAME=Cadierno",
                    "AWS_SECRET_ACCESS_KEY=SUPERSECRETO123XYZ",
                    "export DB_PASSWORD=otroSecretoMuyLargo",
                    "MAIL_MAILER=smtp",
                ]),
                encoding="utf-8",
            )

            names = extract_env_var_names(env_path)

            self.assertEqual(
                names,
                sorted(["APP_NAME", "AWS_SECRET_ACCESS_KEY", "DB_PASSWORD", "MAIL_MAILER"]),
            )

            dump = repr(names)
            self.assertNotIn("SUPERSECRETO123XYZ", dump)
            self.assertNotIn("otroSecretoMuyLargo", dump)
            self.assertNotIn("Cadierno", dump)
            self.assertNotIn("smtp", dump)

    def test_missing_file_returns_empty_list(self):
        names = extract_env_var_names(Path("/no/existe/.env"))
        self.assertEqual(names, [])

    def test_deduplicates_and_sorts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("B_VAR=1\nA_VAR=2\nA_VAR=3\n", encoding="utf-8")

            names = extract_env_var_names(env_path)

            self.assertEqual(names, ["A_VAR", "B_VAR"])


if __name__ == "__main__":
    unittest.main()
