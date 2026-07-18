from pathlib import Path
import json
import tempfile
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.scanner import scan


class ScannerFrameworkDetectionTests(unittest.TestCase):

    def _write_json(self, file_path: Path, payload: dict) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def test_detects_laravel(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "composer.json",
                {
                    "require": {
                        "php": "^8.2",
                        "laravel/framework": "^12.0",
                    }
                },
            )
            (root / "app/Http/Controllers").mkdir(parents=True)

            project = scan(root)

            self.assertEqual(project.framework, "Laravel")
            self.assertEqual(project.backend, "Laravel")
            self.assertIn("PHP", project.language)
            self.assertIn("Controllers", project.architecture_components)

    def test_detects_symfony(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "composer.json",
                {
                    "require": {
                        "php": "^8.2",
                        "symfony/framework-bundle": "^7.0",
                    }
                },
            )

            project = scan(root)

            self.assertEqual(project.framework, "Symfony")
            self.assertEqual(project.backend, "Symfony")

    def test_detects_zend_framework(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "composer.json",
                {
                    "require": {
                        "php": "^8.2",
                        "laminas/laminas-mvc": "^3.0",
                    }
                },
            )

            project = scan(root)

            self.assertEqual(project.framework, "Zend Framework")
            self.assertEqual(project.backend, "Zend Framework")

    def test_detects_php_puro(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "composer.json",
                {
                    "require": {
                        "php": "^8.2",
                        "monolog/monolog": "^3.0",
                    }
                },
            )

            project = scan(root)

            self.assertEqual(project.framework, "No detectado")
            self.assertEqual(project.backend, "PHP")
            self.assertIn("PHP", project.language)

    def test_detects_vue(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "package.json",
                {
                    "dependencies": {
                        "vue": "^3.0.0",
                    }
                },
            )

            project = scan(root)

            self.assertEqual(project.framework, "Vue")
            self.assertEqual(project.frontend, "Vue")
            self.assertIn("JavaScript", project.language)

    def test_detects_react(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "package.json",
                {
                    "dependencies": {
                        "react": "^19.0.0",
                    }
                },
            )

            project = scan(root)

            self.assertEqual(project.framework, "React")
            self.assertEqual(project.frontend, "React")
            self.assertIn("JavaScript", project.language)

    def test_detects_livewire_and_related_laravel_dirs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "composer.json",
                {
                    "require": {
                        "php": "^8.2",
                        "laravel/framework": "^12.0",
                    }
                },
            )
            for directory in [
                "app/Livewire/Admin",
                "app/Actions/Fortify",
                "app/Mail",
                "app/Notifications",
                "app/Providers",
                "app/View/Components",
            ]:
                (root / directory).mkdir(parents=True)

            project = scan(root)

            self.assertIn("Livewire", project.architecture_components)
            self.assertIn("Actions", project.architecture_components)
            self.assertIn("Mail", project.architecture_components)
            self.assertIn("Notifications", project.architecture_components)
            self.assertIn("Providers", project.architecture_components)
            self.assertIn("View Components", project.architecture_components)

    def test_detects_database_per_tenant_via_stancl_tenancy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "composer.json",
                {
                    "require": {
                        "php": "^8.2",
                        "laravel/framework": "^12.0",
                        "stancl/tenancy": "^3.9",
                    }
                },
            )
            (root / "app/Models").mkdir(parents=True)
            (root / "app/Models/Tenant.php").write_text("<?php\n", encoding="utf-8")
            (root / "database/migrations/tenant").mkdir(parents=True)
            (root / "routes").mkdir(parents=True)
            (root / "routes/tenant.php").write_text("<?php\n", encoding="utf-8")
            config_dir = root / "config"
            config_dir.mkdir(parents=True)
            (config_dir / "tenancy.php").write_text(
                """
                <?php
                return [
                    'bootstrappers' => [
                        Stancl\\Tenancy\\Bootstrappers\\DatabaseTenancyBootstrapper::class,
                    ],
                    'database' => [
                        'central_connection' => env('DB_CONNECTION', 'mysql'),
                    ],
                ];
                """,
                encoding="utf-8",
            )

            project = scan(root)

            self.assertEqual(project.multitenancy, "Detectado")
            self.assertIn("DB-per-tenant", project.multitenancy_strategy)
            self.assertTrue(any("stancl/tenancy" in item for item in project.multitenancy_evidence))

    def test_no_multitenancy_when_no_evidence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "composer.json",
                {
                    "require": {
                        "php": "^8.2",
                        "laravel/framework": "^12.0",
                    }
                },
            )

            project = scan(root)

            self.assertEqual(project.multitenancy, "No detectado")
            self.assertEqual(project.multitenancy_evidence, [])

    def test_detects_only_mercado_pago_when_present(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_json(
                root / "composer.json",
                {
                    "require": {
                        "php": "^8.2",
                    }
                },
            )
            service = root / "app/Services/MercadoPagoService.php"
            service.parent.mkdir(parents=True, exist_ok=True)
            service.write_text(
                """
                <?php
                namespace App\\Services;
                class MercadoPagoService {
                    public function call() {
                        $url = 'https://api.mercadopago.com/checkout/preferences';
                    }
                }
                """,
                encoding="utf-8",
            )

            project = scan(root)

            self.assertIn("Mercado Pago", project.integrations)
            self.assertNotIn("Stripe", project.integrations)
            self.assertNotIn("AWS", project.integrations)

    def test_detects_cloudflare_turnstile_usage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            verifier = root / "app/Services/TurnstileVerifier.php"
            verifier.parent.mkdir(parents=True, exist_ok=True)
            verifier.write_text(
                """
                <?php
                namespace App\\Services;
                class TurnstileVerifier {
                    public function verify() {
                        $url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
                    }
                }
                """,
                encoding="utf-8",
            )

            project = scan(root)

            self.assertIn("Cloudflare", project.integrations)


if __name__ == "__main__":
    unittest.main()
