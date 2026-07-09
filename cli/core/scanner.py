from pathlib import Path
import json
import os

from core.project import Project


REQUIRED_FILES = {
    "composer": "composer.json",
    "package": "package.json",
    "docker_compose": "docker-compose.yml",
    "dockerfile": "Dockerfile",
    "readme": "README.md",
}

IGNORED_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "vendor",
    "node_modules",
    "storage",
    "dist",
    "build",
    ".ai",
    "playbooks",
    "checklists",
    "knowledge",
    "memory",
}

TEXT_FILE_EXTENSIONS = {
    ".php",
    ".json",
    ".yml",
    ".yaml",
    ".env",
    ".js",
    ".ts",
}

SEARCH_ROOT_CANDIDATES = [
    Path("app"),
    Path("src"),
    Path("routes"),
    Path("resources"),
]

ARCHITECTURE_DIR_PATTERNS = {
    "Controllers": [
        Path("app/Http/Controllers"),
        Path("src/Controller"),
        Path("src/Controllers"),
    ],
    "Models": [
        Path("app/Models"),
        Path("src/Model"),
        Path("src/Models"),
    ],
    "Services": [
        Path("app/Services"),
        Path("src/Service"),
        Path("src/Services"),
    ],
    "Repositories": [
        Path("app/Repositories"),
        Path("src/Repository"),
        Path("src/Repositories"),
    ],
    "Policies": [
        Path("app/Policies"),
        Path("src/Policy"),
        Path("src/Policies"),
    ],
    "Requests": [
        Path("app/Http/Requests"),
        Path("src/Request"),
        Path("src/Requests"),
    ],
    "Middleware": [
        Path("app/Http/Middleware"),
        Path("src/Middleware"),
    ],
    "Jobs": [
        Path("app/Jobs"),
        Path("src/Job"),
        Path("src/Jobs"),
    ],
    "Events": [
        Path("app/Events"),
        Path("src/Event"),
        Path("src/Events"),
    ],
    "Commands": [
        Path("app/Console/Commands"),
        Path("src/Command"),
        Path("src/Commands"),
    ],
    "Traits": [
        Path("app/Traits"),
        Path("src/Traits"),
    ],
}

INTEGRATION_RULES = {
    "Mercado Pago": {
        "deps": ["mercadopago/dx-php"],
        "text": ["mercadopago", "api.mercadopago.com", "auth.mercadopago.com"],
    },
    "Stripe": {
        "deps": ["stripe/stripe-php", "@stripe/stripe-js", "stripe"],
        "text": ["api.stripe.com", "js.stripe.com", "stripe/stripe-php", "stripe\\"],
    },
    "AWS": {
        "deps": ["aws/aws-sdk-php", "@aws-sdk/"],
        "text": ["aws/aws-sdk", "s3.amazonaws.com", "aws_access_key_id", "aws_secret_access_key"],
    },
    "Cloudflare": {
        "deps": ["cloudflare"],
        "text": ["cloudflare", "challenges.cloudflare.com", "turnstile"],
    },
    "SMTP": {
        "deps": ["symfony/mailer", "swiftmailer/swiftmailer"],
        "text": ["mailgun", "sendgrid", "postmark", "mailer=smtp"],
    },
    "Redis": {
        "deps": ["predis/predis", "phpredis"],
        "text": ["redis::", "redis://", "predis"],
    },
    "RabbitMQ": {
        "deps": ["php-amqplib/php-amqplib", "enqueue/amqp-lib"],
        "text": ["rabbitmq", "amqp://", "amqplib"],
    },
    "Elasticsearch": {
        "deps": ["elasticsearch/elasticsearch"],
        "text": ["elasticsearch"],
    },
    "Meilisearch": {
        "deps": ["meilisearch/meilisearch-php"],
        "text": ["meilisearch"],
    },
    "OpenAI": {
        "deps": ["openai-php/client", "openai"],
        "text": ["openai"],
    },
    "Firebase": {
        "deps": ["kreait/firebase-php", "firebase"],
        "text": ["firebase"],
    },
}

TECH_DEBT_MARKERS = ["todo", "fixme", "hack", "xxx", "deprecated"]


def _safe_load_json(path: Path) -> dict:

    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _find_files(root: Path) -> dict[str, Path]:

    remaining = {name: filename for name, filename in REQUIRED_FILES.items()}
    found: dict[str, Path] = {}

    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for key, filename in list(remaining.items()):
            if filename in files:
                found[key] = Path(current_root) / filename
                del remaining[key]

        if not remaining:
            break

    return found


def _detect_language(composer_data: dict, package_data: dict) -> str:

    languages: list[str] = []

    if composer_data:
        languages.append("PHP")

    if package_data:
        deps = {
            **package_data.get("dependencies", {}),
            **package_data.get("devDependencies", {}),
        }

        if "typescript" in deps:
            languages.append("TypeScript")
        else:
            languages.append("JavaScript")

    if not languages:
        return "No detectado"

    return " + ".join(dict.fromkeys(languages))


def _detect_framework(composer_data: dict, package_data: dict) -> str:

    deps = {
        **composer_data.get("require", {}),
        **composer_data.get("require-dev", {}),
    }
    node_deps = {
        **package_data.get("dependencies", {}),
        **package_data.get("devDependencies", {}),
    }

    if "laravel/framework" in deps:
        return "Laravel"

    if any(key.startswith("symfony/") for key in deps):
        return "Symfony"

    if "zendframework/zendframework" in deps or "laminas/laminas-mvc" in deps:
        return "Zend Framework"

    if "react" in node_deps:
        return "React"

    if "vue" in node_deps:
        return "Vue"

    return "No detectado"


def _detect_frontend(package_data: dict) -> str:

    node_deps = {
        **package_data.get("dependencies", {}),
        **package_data.get("devDependencies", {}),
    }

    if "vue" in node_deps:
        return "Vue"

    if "react" in node_deps:
        return "React"

    if package_data:
        return "JavaScript/TypeScript"

    return "No detectado"


def _detect_database(composer_data: dict, package_data: dict, docker_compose_text: str) -> str:

    content = docker_compose_text.lower()
    all_deps = " ".join(
        list(composer_data.get("require", {}).keys())
        + list(composer_data.get("require-dev", {}).keys())
        + list(package_data.get("dependencies", {}).keys())
        + list(package_data.get("devDependencies", {}).keys())
    ).lower()

    detected: list[str] = []

    if any(token in content for token in ["mysql", "mariadb"]) or "mysql" in all_deps:
        detected.append("MySQL")

    if any(token in content for token in ["postgres", "postgresql", "pgsql"]) or any(
        token in all_deps for token in ["postgres", "postgresql", "pgsql"]
    ):
        detected.append("PostgreSQL")

    if not detected:
        return "No detectado"

    return " / ".join(dict.fromkeys(detected))


def _detect_infrastructure(docker_compose_text: str, dockerfile_text: str) -> str:

    info = "\n".join([docker_compose_text.lower(), dockerfile_text.lower()])
    detected: list[str] = []

    if docker_compose_text or dockerfile_text:
        detected.append("Docker")

    if "nginx" in info:
        detected.append("Nginx")

    if any(token in info for token in ["apache", "httpd"]):
        detected.append("Apache")

    if not detected:
        return "No detectado"

    return " / ".join(dict.fromkeys(detected))


def _detect_backend(framework: str, composer_data: dict) -> str:

    if framework in {"Laravel", "Symfony", "Zend Framework"}:
        return framework

    if composer_data:
        return "PHP"

    return "No detectado"


def _collect_dependencies(composer_data: dict, package_data: dict) -> list[str]:

    dependencies: list[str] = []

    for key in composer_data.get("require", {}).keys():
        if key != "php":
            dependencies.append(key)

    for key in package_data.get("dependencies", {}).keys():
        dependencies.append(key)

    return dependencies[:12]


def _collect_architecture_components(root: Path) -> list[str]:

    detected: list[str] = []

    def ends_with_pattern(relative_path: Path, pattern: Path) -> bool:
        rel_parts = relative_path.parts
        pattern_parts = pattern.parts

        if len(rel_parts) < len(pattern_parts):
            return False

        return rel_parts[-len(pattern_parts):] == pattern_parts

    existing_dirs: list[Path] = []
    for current_root, dirs, _ in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for directory in dirs:
            full = Path(current_root) / directory
            existing_dirs.append(full.relative_to(root))

    for name, patterns in ARCHITECTURE_DIR_PATTERNS.items():
        for pattern in patterns:
            if (root / pattern).exists() or any(ends_with_pattern(path, pattern) for path in existing_dirs):
                detected.append(name)
                break

    return detected


def _collect_searchable_text(root: Path) -> str:

    chunks: list[str] = []

    search_roots = [candidate for candidate in SEARCH_ROOT_CANDIDATES if (root / candidate).exists()]
    if not search_roots:
        search_roots = [Path(".")]

    for search_root in search_roots:
        base_dir = (root / search_root).resolve()

        for current_root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for filename in files:
                full_path = Path(current_root) / filename

                if full_path.suffix.lower() not in TEXT_FILE_EXTENSIONS and filename != ".env":
                    continue

                try:
                    content = full_path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue

                if len(content) > 20000:
                    content = content[:20000]

                chunks.append(content.lower())

    return "\n".join(chunks)


def _collect_integrations(root: Path, composer_data: dict, package_data: dict) -> list[str]:

    dep_keys = list(composer_data.get("require", {}).keys())
    dep_keys += list(composer_data.get("require-dev", {}).keys())
    dep_keys += list(package_data.get("dependencies", {}).keys())
    dep_keys += list(package_data.get("devDependencies", {}).keys())
    dep_keys = [dep.lower() for dep in dep_keys]

    text_scope = "\n".join(dep_keys)
    text_scope += "\n" + _collect_searchable_text(root)

    detected: list[str] = []
    for integration, rules in INTEGRATION_RULES.items():
        dep_match = any(any(marker in dep for marker in rules["deps"]) for dep in dep_keys)
        text_match = any(keyword in text_scope for keyword in rules["text"])

        if dep_match or text_match:
            detected.append(integration)

    return detected


def _collect_technical_debt(root: Path) -> list[str]:

    findings: list[str] = []

    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in files:
            full_path = Path(current_root) / filename

            if full_path.suffix.lower() not in TEXT_FILE_EXTENSIONS:
                continue

            relative_path = full_path.relative_to(root)

            try:
                lines = full_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except Exception:
                continue

            # Heurística 1: marcadores explícitos (TODO/FIXME/HACK/...)
            for index, line in enumerate(lines, start=1):
                lowered = line.lower()
                if any(marker in lowered for marker in TECH_DEBT_MARKERS):
                    snippet = line.strip()
                    if len(snippet) > 100:
                        snippet = snippet[:100] + "..."
                    findings.append(f"{relative_path}:{index} -> {snippet}")
                    if len(findings) >= 20:
                        return findings

            # Heurística 2: archivos potencialmente muy grandes
            if "controller" in filename.lower() and len(lines) > 350:
                findings.append(
                    f"{relative_path} -> Controller extenso ({len(lines)} líneas), revisar separación de responsabilidades"
                )

            if len(findings) >= 20:
                return findings

    return findings


def scan(path: Path) -> Project:

    project = Project()

    project.path = str(path)
    project.name = path.name

    found = _find_files(path)

    for filename in REQUIRED_FILES.values():
        key = next((k for k, v in REQUIRED_FILES.items() if v == filename), None)
        file_path = found.get(key) if key else None
        if file_path:
            project.detected_files.append(str(file_path.relative_to(path)))

    composer_data = _safe_load_json(found["composer"]) if "composer" in found else {}
    package_data = _safe_load_json(found["package"]) if "package" in found else {}

    analysis_root = path
    if "composer" in found:
        analysis_root = found["composer"].parent
    elif "package" in found:
        analysis_root = found["package"].parent

    docker_compose_text = ""
    if "docker_compose" in found:
        docker_compose_text = found["docker_compose"].read_text(encoding="utf-8", errors="ignore")

    dockerfile_text = ""
    if "dockerfile" in found:
        dockerfile_text = found["dockerfile"].read_text(encoding="utf-8", errors="ignore")

    project.language = _detect_language(composer_data, package_data)
    project.framework = _detect_framework(composer_data, package_data)
    project.backend = _detect_backend(project.framework, composer_data)
    project.frontend = _detect_frontend(package_data)
    project.database = _detect_database(composer_data, package_data, docker_compose_text)
    project.infrastructure = _detect_infrastructure(docker_compose_text, dockerfile_text)
    project.dependencies = _collect_dependencies(composer_data, package_data)
    project.architecture_components = _collect_architecture_components(analysis_root)
    project.integrations = _collect_integrations(analysis_root, composer_data, package_data)
    project.technical_debt_items = _collect_technical_debt(analysis_root)

    return project
    