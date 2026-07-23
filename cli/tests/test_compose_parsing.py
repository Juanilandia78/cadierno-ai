from pathlib import Path
import tempfile
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core import compose as compose_module  # noqa: E402
from core.compose import match_service_for_project, parse_compose_file  # noqa: E402


SIMPLE_COMPOSE_TEXT = """
services:
  user_portal:
    build:
      context: ./user-portal
    container_name: user_portal
    ports:
      - "9000:9000"
    environment:
      - APP_ENV=production
      - APP_KEY=base64:muysecreto
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
    networks:
      - shared-db-network

networks:
  shared-db-network:
    external: true

volumes:
  db-data:
"""

# Réplica simplificada del fixture real: un nginx compartido que monta TODOS
# los portales como volumen, más un servicio dedicado por proyecto sin
# build.context propio (todos comparten context "." como en el caso real).
SHARED_NGINX_COMPOSE_TEXT = """
services:
  nginx_clearit:
    image: nginx:stable-alpine
    container_name: nginx_clearit
    volumes:
      - ./admin-portal:/var/www/html/admin-portal
      - ./user-portal:/var/www/html/user-portal
      - ./partner-portal:/var/www/html/partner-portal
    depends_on:
      - admin_portal
      - user_portal
      - partner-portal
    networks:
      - shared-db-network

  admin_portal:
    build:
      context: .
    container_name: admin_portal
    volumes:
      - ./admin-portal:/var/www/html/admin-portal
    networks:
      - shared-db-network

  user_portal:
    build:
      context: .
    container_name: user_portal
    volumes:
      - ./user-portal:/var/www/html/user-portal
    networks:
      - shared-db-network

networks:
  shared-db-network:
    external: true
"""


class ComposeParsingTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    @unittest.skipUnless(compose_module.HAS_YAML, "PyYAML no disponible en este entorno")
    def test_parses_services_networks_volumes(self):
        compose_file = self.workspace / "docker-compose.yml"
        compose_file.write_text(SIMPLE_COMPOSE_TEXT, encoding="utf-8")
        (self.workspace / "user-portal").mkdir()

        model = parse_compose_file(compose_file)

        self.assertTrue(model.parsed)
        self.assertIn("user_portal", model.services)
        self.assertIn("shared-db-network", model.networks)
        self.assertIn("db-data", model.volumes)

        service = model.services["user_portal"]
        self.assertEqual(service.build_context, "./user-portal")
        self.assertTrue(service.healthcheck)
        self.assertIn("APP_ENV", service.environment_var_names)
        self.assertIn("APP_KEY", service.environment_var_names)

    @unittest.skipUnless(compose_module.HAS_YAML, "PyYAML no disponible en este entorno")
    def test_environment_names_never_leak_values(self):
        compose_file = self.workspace / "docker-compose.yml"
        compose_file.write_text(SIMPLE_COMPOSE_TEXT, encoding="utf-8")

        model = parse_compose_file(compose_file)
        service = model.services["user_portal"]

        dump = repr(service.environment_var_names)
        self.assertNotIn("base64:muysecreto", dump)
        self.assertNotIn("production", dump)

    @unittest.skipUnless(compose_module.HAS_YAML, "PyYAML no disponible en este entorno")
    def test_match_by_build_context_high_confidence(self):
        compose_file = self.workspace / "docker-compose.yml"
        compose_file.write_text(SIMPLE_COMPOSE_TEXT, encoding="utf-8")
        project_path = self.workspace / "user-portal"
        project_path.mkdir()

        model = parse_compose_file(compose_file)
        match = match_service_for_project(model, project_path, compose_file)

        self.assertEqual(match.service_name, "user_portal")
        self.assertEqual(match.confidence, "high")

    @unittest.skipUnless(compose_module.HAS_YAML, "PyYAML no disponible en este entorno")
    def test_shared_nginx_does_not_shadow_the_real_project_service(self):
        """
        Regresión sobre el caso real: nginx_clearit monta TODOS los portales
        como volumen, pero cada portal también tiene su propio servicio
        dedicado. El match debe apuntar al servicio dedicado, no a nginx,
        aunque nginx aparezca primero en el archivo y matchee por volumen.
        """

        compose_file = self.workspace / "docker-compose.yml"
        compose_file.write_text(SHARED_NGINX_COMPOSE_TEXT, encoding="utf-8")
        project_path = self.workspace / "user-portal"
        project_path.mkdir()

        model = parse_compose_file(compose_file)
        match = match_service_for_project(model, project_path, compose_file)

        self.assertEqual(match.service_name, "user_portal")
        self.assertNotEqual(match.service_name, "nginx_clearit")

    @unittest.skipUnless(compose_module.HAS_YAML, "PyYAML no disponible en este entorno")
    def test_stale_compose_reports_no_match_instead_of_guessing(self):
        """
        Caso real: el compose compartido todavía no incluye al proyecto nuevo,
        y su nombre tampoco guarda relación con ningún servicio existente.
        No debe inventarse un match.
        """

        compose_file = self.workspace / "docker-compose.yml"
        compose_file.write_text(SHARED_NGINX_COMPOSE_TEXT, encoding="utf-8")
        project_path = self.workspace / "billing-service"
        project_path.mkdir()

        model = parse_compose_file(compose_file)
        match = match_service_for_project(model, project_path, compose_file)

        self.assertIsNone(match.service_name)
        self.assertEqual(match.confidence, "none")

    @unittest.skipUnless(compose_module.HAS_YAML, "PyYAML no disponible en este entorno")
    def test_stale_compose_with_similar_name_reports_low_confidence_not_none(self):
        """
        Variante del caso real: el compose compartido no referencia todavía a
        user-portal-new (ni por build.context ni por volumen), pero SÍ existe
        un servicio 'user_portal' cuyo nombre es prefijo del proyecto. Debe
        reportarse como pista de baja confianza a revisar, no como "no match"
        silencioso ni como una certeza.
        """

        compose_file = self.workspace / "docker-compose.yml"
        compose_file.write_text(SHARED_NGINX_COMPOSE_TEXT, encoding="utf-8")
        project_path = self.workspace / "user-portal-new"
        project_path.mkdir()

        model = parse_compose_file(compose_file)
        match = match_service_for_project(model, project_path, compose_file)

        self.assertEqual(match.service_name, "user_portal")
        self.assertEqual(match.confidence, "low")

    @unittest.skipUnless(compose_module.HAS_YAML, "PyYAML no disponible en este entorno")
    def test_name_similarity_fallback_is_low_confidence(self):
        compose_file = self.workspace / "docker-compose.yml"
        compose_file.write_text(SIMPLE_COMPOSE_TEXT, encoding="utf-8")
        # No hay build.context ni volumen que apunte a este directorio exacto.
        project_path = self.workspace / "user_portal_local_checkout"
        project_path.mkdir()

        model = parse_compose_file(compose_file)
        match = match_service_for_project(model, project_path, compose_file)

        self.assertEqual(match.service_name, "user_portal")
        self.assertEqual(match.confidence, "low")

    def test_heuristic_fallback_without_yaml_extracts_service_names(self):
        compose_file = self.workspace / "docker-compose.yml"
        compose_file.write_text(SIMPLE_COMPOSE_TEXT, encoding="utf-8")

        original_has_yaml = compose_module.HAS_YAML
        compose_module.HAS_YAML = False
        try:
            model = parse_compose_file(compose_file)
        finally:
            compose_module.HAS_YAML = original_has_yaml

        self.assertFalse(model.parsed)
        self.assertIn("user_portal", model.heuristic_service_names)

    def test_missing_compose_file_returns_unparsed_model(self):
        model = parse_compose_file(self.workspace / "docker-compose.yml")
        self.assertFalse(model.parsed)
        self.assertEqual(model.services, {})


if __name__ == "__main__":
    unittest.main()
