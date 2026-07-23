from dataclasses import dataclass, field
from pathlib import Path
import os
import re

from core.compose import ComposeModel, ServiceMatch, match_service_for_project, parse_compose_file
from core.env_scan import extract_env_var_names


STRONG_EVIDENCE_FILENAMES = [
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
]

WEAK_EVIDENCE_NAMES = [".git", "Makefile", "package.json"]

PROJECT_MANIFEST_NAMES = ["composer.json", "package.json", "artisan", "Dockerfile", "docker-compose.yml"]

_PROXY_PASS_PATTERN = re.compile(r"proxy_pass\s+([^\s;]+)")


def _max_depth() -> int:
    raw = os.getenv("CADIERNO_WORKSPACE_MAX_DEPTH", "").strip()
    if raw.isdigit():
        return max(1, int(raw))
    return 5


class WorkspaceError(ValueError):
    """Error de configuración de workspace (rutas inválidas o flags contradictorios)."""


@dataclass
class WorkspaceDetection:

    root: Path | None = None
    method: str = "none"  # explicit | auto | disabled | none
    evidence: list[str] = field(default_factory=list)
    reason: str = ""


@dataclass
class SiblingProject:

    name: str = ""
    path: str = ""
    markers: list[str] = field(default_factory=list)


@dataclass
class NginxInfo:

    detected: bool = False
    config_files: list[str] = field(default_factory=list)
    upstreams: list[str] = field(default_factory=list)


@dataclass
class WorkspaceInfo:

    root: Path | None = None
    detection_method: str = "none"
    evidence: list[str] = field(default_factory=list)
    compose_file: Path | None = None
    compose: ComposeModel | None = None
    matched_service: ServiceMatch = field(default_factory=ServiceMatch)
    sibling_projects: list[SiblingProject] = field(default_factory=list)
    nginx: NginxInfo = field(default_factory=NginxInfo)
    root_env_files: list[str] = field(default_factory=list)
    root_env_var_names: dict[str, list[str]] = field(default_factory=dict)


def _strong_evidence_at(path: Path) -> list[str]:

    try:
        return [name for name in STRONG_EVIDENCE_FILENAMES if (path / name).is_file()]
    except OSError:
        return []


def _weak_evidence_at(path: Path) -> list[str]:

    try:
        return [name for name in WEAK_EVIDENCE_NAMES if (path / name).exists()]
    except OSError:
        return []


def _has_own_git(path: Path) -> bool:

    try:
        return (path / ".git").exists()
    except OSError:
        return False


def auto_detect_workspace_root(project_path: Path) -> WorkspaceDetection:
    """
    Camina hacia arriba desde `project_path` buscando evidencia de workspace.

    Reglas de seguridad (nunca se cruzan):
    - Nunca sube más allá de $HOME ni de la raíz del filesystem.
    - Nunca sube más de `CADIERNO_WORKSPACE_MAX_DEPTH` niveles (default 5).
    - Si un ancestro tiene su propio `.git` (un repo distinto al del proyecto),
      se evalúa evidencia en ese nivel y no se sube más allá de él.

    Solo la evidencia FUERTE (docker-compose.yml/.yaml, compose.yml/.yaml)
    activa la detección automática por sí sola. La evidencia débil (.git,
    Makefile, package.json raíz) únicamente corrobora, nunca decide sola.
    """

    try:
        home = Path.home().resolve()
    except Exception:
        home = None

    candidate = project_path.resolve().parent
    depth = 0
    max_depth = _max_depth()

    while depth < max_depth:

        strong = _strong_evidence_at(candidate)

        if strong:
            weak = _weak_evidence_at(candidate)
            return WorkspaceDetection(
                root=candidate,
                method="auto",
                evidence=strong + weak,
                reason=f"Evidencia fuerte encontrada en {candidate}: {', '.join(strong)}.",
            )

        if _has_own_git(candidate):
            # Repo ajeno distinto al del proyecto: frontera dura, no seguimos subiendo.
            break

        if home is not None and candidate == home:
            break

        parent = candidate.parent
        if parent == candidate:
            # Raíz del filesystem.
            break

        candidate = parent
        depth += 1

    return WorkspaceDetection(
        root=None,
        method="none",
        evidence=[],
        reason="No se encontró evidencia de workspace dentro de los límites de búsqueda.",
    )


def resolve_explicit_workspace_root(project_path: Path, workspace_root: Path) -> WorkspaceDetection:

    resolved_root = workspace_root.resolve()
    resolved_project = project_path.resolve()

    if not resolved_root.exists() or not resolved_root.is_dir():
        raise WorkspaceError(f"El workspace indicado no existe o no es un directorio: {resolved_root}")

    if resolved_project != resolved_root and resolved_root not in resolved_project.parents:
        raise WorkspaceError(
            f"El proyecto ({resolved_project}) no está dentro del workspace indicado ({resolved_root})."
        )

    return WorkspaceDetection(
        root=resolved_root,
        method="explicit",
        evidence=["Workspace indicado explícitamente (--infra-root/--monorepo-root)"],
        reason="Workspace indicado explícitamente por el usuario.",
    )


def detect_workspace(project_path: Path, explicit_root: Path | None, disabled: bool) -> WorkspaceDetection:

    if disabled and explicit_root is not None:
        raise WorkspaceError(
            "No se puede combinar --no-workspace con --infra-root/--monorepo-root: son opciones contradictorias."
        )

    if disabled:
        return WorkspaceDetection(
            root=None,
            method="disabled",
            evidence=[],
            reason="Workspace deshabilitado explícitamente (--no-workspace).",
        )

    if explicit_root is not None:
        return resolve_explicit_workspace_root(project_path, explicit_root)

    return auto_detect_workspace_root(project_path)


def find_compose_file(workspace_root: Path) -> Path | None:

    for filename in STRONG_EVIDENCE_FILENAMES:
        candidate = workspace_root / filename
        if candidate.is_file():
            return candidate

    return None


def _detect_sibling_projects(workspace_root: Path, project_path: Path) -> list[SiblingProject]:

    from core.scanner import IGNORED_DIRS

    siblings: list[SiblingProject] = []
    project_resolved = project_path.resolve()

    try:
        entries = sorted((entry for entry in workspace_root.iterdir() if entry.is_dir()), key=lambda p: p.name)
    except OSError:
        return siblings

    for entry in entries:
        if entry.name in IGNORED_DIRS:
            continue

        if entry.resolve() == project_resolved:
            continue

        markers = [name for name in PROJECT_MANIFEST_NAMES if (entry / name).exists()]
        if markers:
            siblings.append(SiblingProject(name=entry.name, path=str(entry), markers=markers))

    return siblings


def _detect_nginx(workspace_root: Path, compose: ComposeModel | None) -> NginxInfo:

    info = NginxInfo()

    if compose is not None:
        for service in compose.services.values():
            if "nginx" in service.image.lower() or "nginx" in service.name.lower():
                info.detected = True
        for name in compose.heuristic_service_names:
            if "nginx" in name.lower():
                info.detected = True

    nginx_dir = workspace_root / "nginx"
    if nginx_dir.is_dir():
        for conf_file in sorted(nginx_dir.rglob("*.conf")):
            info.detected = True
            info.config_files.append(str(conf_file.relative_to(workspace_root)))

            try:
                text = conf_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            for match in _PROXY_PASS_PATTERN.finditer(text):
                target = match.group(1).strip()
                if target not in info.upstreams:
                    info.upstreams.append(target)

    return info


def _discover_root_env_files(workspace_root: Path, compose: ComposeModel | None) -> list[Path]:

    candidates: list[Path] = []

    direct = workspace_root / ".env"
    if direct.is_file():
        candidates.append(direct)

    if compose is not None:
        for service in compose.services.values():
            for env_file in service.env_files:
                try:
                    resolved = (workspace_root / env_file).resolve()
                except Exception:
                    continue
                if resolved.is_file() and resolved not in candidates:
                    candidates.append(resolved)

    return candidates


def scan_workspace(detection: WorkspaceDetection, project_path: Path) -> WorkspaceInfo:

    info = WorkspaceInfo(
        root=detection.root,
        detection_method=detection.method,
        evidence=list(detection.evidence),
    )

    if detection.root is None:
        return info

    compose_file = find_compose_file(detection.root)
    info.compose_file = compose_file

    compose_model: ComposeModel | None = None
    if compose_file is not None:
        compose_model = parse_compose_file(compose_file)
        info.compose = compose_model
        info.matched_service = match_service_for_project(compose_model, project_path, compose_file)

    info.sibling_projects = _detect_sibling_projects(detection.root, project_path)
    info.nginx = _detect_nginx(detection.root, compose_model)

    for env_file in _discover_root_env_files(detection.root, compose_model):
        try:
            relative_name = str(env_file.relative_to(detection.root))
        except ValueError:
            relative_name = str(env_file)

        info.root_env_files.append(relative_name)
        info.root_env_var_names[relative_name] = extract_env_var_names(env_file)

    return info
