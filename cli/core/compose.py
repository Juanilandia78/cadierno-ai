from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class ComposeService:

    name: str = ""
    image: str = ""
    build_context: str = ""
    container_name: str = ""
    ports: list[str] = field(default_factory=list)
    volumes: list[str] = field(default_factory=list)
    networks: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    healthcheck: bool = False
    environment_var_names: list[str] = field(default_factory=list)
    env_files: list[str] = field(default_factory=list)


@dataclass
class ComposeModel:

    parsed: bool = False
    compose_file: str = ""
    services: dict[str, ComposeService] = field(default_factory=dict)
    networks: list[str] = field(default_factory=list)
    volumes: list[str] = field(default_factory=list)
    heuristic_service_names: list[str] = field(default_factory=list)


@dataclass
class ServiceMatch:

    service_name: str | None = None
    confidence: str = "none"  # high | low | none
    reason: str = "No se encontró un servicio Docker que corresponda a este proyecto."


def _environment_names(raw_environment) -> list[str]:
    """
    Extrae solo los NOMBRES de variables declaradas en el bloque `environment`
    de un servicio compose. Nunca conserva valores.
    """

    names: list[str] = []

    if isinstance(raw_environment, dict):
        names.extend(str(key) for key in raw_environment.keys())
    elif isinstance(raw_environment, list):
        for entry in raw_environment:
            text = str(entry)
            if "=" in text:
                names.append(text.split("=", 1)[0].strip())
            else:
                names.append(text.strip())

    return sorted(dict.fromkeys(name for name in names if name))


def _as_list(value) -> list[str]:

    if value is None:
        return []

    if isinstance(value, list):
        return [str(item) for item in value]

    return [str(value)]


def _parse_service(name: str, raw: dict) -> ComposeService:

    raw = raw or {}

    build = raw.get("build")
    build_context = ""
    if isinstance(build, dict):
        build_context = str(build.get("context", "") or "")
    elif isinstance(build, str):
        build_context = build

    return ComposeService(
        name=name,
        image=str(raw.get("image", "") or ""),
        build_context=build_context,
        container_name=str(raw.get("container_name", "") or ""),
        ports=_as_list(raw.get("ports")),
        volumes=_as_list(raw.get("volumes")),
        networks=_as_list(raw.get("networks")),
        depends_on=_as_list(raw.get("depends_on")),
        healthcheck=bool(raw.get("healthcheck")),
        environment_var_names=_environment_names(raw.get("environment")),
        env_files=_as_list(raw.get("env_file")),
    )


def _heuristic_service_names(text: str) -> list[str]:
    """
    Detección de nombres de servicio sin PyYAML: busca la sección `services:`
    de nivel superior y toma las claves indentadas al primer nivel dentro de
    ella. Es deliberadamente conservador (nunca extrae puertos/volúmenes/redes
    sin un parser YAML real).
    """

    lines = text.splitlines()
    names: list[str] = []
    in_services = False
    service_indent: int | None = None

    for line in lines:
        stripped = line.strip()

        if not in_services:
            if stripped == "services:":
                in_services = True
            continue

        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))

        if indent == 0:
            # Salimos de la sección services (llegamos a networks:, volumes:, etc.)
            break

        if service_indent is None:
            service_indent = indent

        if indent == service_indent and stripped.endswith(":"):
            names.append(stripped[:-1].strip())

    return names


def parse_compose_file(compose_file: Path) -> ComposeModel:

    model = ComposeModel(compose_file=str(compose_file))

    if not compose_file.exists():
        return model

    try:
        text = compose_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return model

    if not HAS_YAML:
        model.heuristic_service_names = _heuristic_service_names(text)
        return model

    try:
        data = yaml.safe_load(text)
    except Exception:
        model.heuristic_service_names = _heuristic_service_names(text)
        return model

    if not isinstance(data, dict):
        return model

    services_raw = data.get("services") or {}
    if isinstance(services_raw, dict):
        for name, raw_service in services_raw.items():
            model.services[name] = _parse_service(name, raw_service if isinstance(raw_service, dict) else {})

    networks_raw = data.get("networks") or {}
    if isinstance(networks_raw, dict):
        model.networks = list(networks_raw.keys())

    volumes_raw = data.get("volumes") or {}
    if isinstance(volumes_raw, dict):
        model.volumes = list(volumes_raw.keys())

    model.parsed = True

    return model


def _is_bind_mount_source(source: str) -> bool:

    return source.startswith((".", "/", "~")) or (len(source) > 1 and source[1] == ":")


def _resolve_mount_source(source: str, compose_dir: Path) -> Path | None:

    if not _is_bind_mount_source(source):
        return None

    try:
        return (compose_dir / source).expanduser().resolve()
    except Exception:
        return None


def _normalize_name(value: str) -> str:

    return "".join(char for char in value.lower() if char.isalnum())


def match_service_for_project(compose: ComposeModel, project_path: Path, compose_file: Path) -> ServiceMatch:
    """
    Busca qué servicio compose corresponde al proyecto, en dos pasadas
    ordenadas por especificidad:

    1. `build.context`: un servicio que se BUILDEA desde el directorio del
       proyecto es una señal fuerte e inequívoca de que ese servicio ES el
       proyecto.
    2. Bind-mount por volumen: señal más débil, porque un mismo directorio
       puede estar montado en varios servicios a la vez (por ejemplo, un
       nginx compartido que sirve a todos los proyectos del workspace). Por
       eso se evalúa recién si ningún build.context matcheó.
    """

    compose_dir = compose_file.parent
    project_resolved = project_path.resolve()

    for name, service in compose.services.items():
        if not service.build_context:
            continue

        resolved = _resolve_mount_source(service.build_context, compose_dir)
        if resolved is not None and resolved == project_resolved:
            return ServiceMatch(
                service_name=name,
                confidence="high",
                reason=f"El build.context del servicio '{name}' apunta a este proyecto.",
            )

    volume_candidates: list[tuple[str, ComposeService, str]] = []
    for name, service in compose.services.items():
        for volume in service.volumes:
            source = volume.split(":", 1)[0].strip()
            resolved = _resolve_mount_source(source, compose_dir)
            if resolved is not None and resolved == project_resolved:
                volume_candidates.append((name, service, volume))
                break

    if volume_candidates:
        # Un servicio tipo reverse-proxy (nginx/traefik/...) suele montar TODOS
        # los proyectos del workspace como volumen, no solo el propio. Se lo
        # descarta como candidato mientras exista una alternativa más específica.
        proxy_keywords = ("nginx", "traefik", "haproxy", "caddy", "envoy", "apache", "httpd")

        def _is_proxy_like(name: str, service: ComposeService) -> bool:
            text = f"{name} {service.image}".lower()
            return any(keyword in text for keyword in proxy_keywords)

        non_proxy_candidates = [c for c in volume_candidates if not _is_proxy_like(c[0], c[1])]
        pool = non_proxy_candidates or volume_candidates

        best_name, _best_service, best_volume = min(pool, key=lambda candidate: len(candidate[1].volumes))

        return ServiceMatch(
            service_name=best_name,
            confidence="high",
            reason=f"El servicio '{best_name}' monta este proyecto como volumen ({best_volume}).",
        )

    project_normalized = _normalize_name(project_path.name)

    for name, service in compose.services.items():
        candidates = [name, service.container_name]
        for candidate in candidates:
            if not candidate:
                continue
            normalized = _normalize_name(candidate)
            if normalized and (normalized in project_normalized or project_normalized in normalized):
                return ServiceMatch(
                    service_name=name,
                    confidence="low",
                    reason=(
                        f"Coincidencia heurística de nombre entre el servicio '{name}' "
                        f"y el proyecto '{project_path.name}' (revisar manualmente)."
                    ),
                )

    return ServiceMatch()
