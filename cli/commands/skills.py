from pathlib import Path
import json
import subprocess
import shutil
import tempfile
from datetime import datetime, timezone

from utils.path import cadierno_root
from ui import console, banner, warning, success, info

KNOWN_OFFICIAL_SOURCES = {
    "context7": {
        "official_source": "https://github.com/netresearch/context7-skill",
        "skill_path": "skills/context7",
        "expected_files": ["SKILL.md"],
    },
}


def catalog_for(project: Path) -> dict:
    catalog_path = cadierno_root(project) / "skills" / "catalog.json"
    if not catalog_path.exists():
        raise FileNotFoundError("No existe catálogo de skills. Ejecutá 'cadierno install' o 'cadierno update'.")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    # Compatibilidad segura con catálogos instalados por Cadierno V3 antes de
    # que se agregaran metadatos de verificación. Sólo completa datos para IDs
    # y URLs oficiales conocidos por esta versión del CLI.
    for skill in catalog.get("skills", []):
        trusted = KNOWN_OFFICIAL_SOURCES.get(skill.get("id"))
        if trusted and skill.get("source") == trusted["official_source"]:
            for key, value in trusted.items():
                skill.setdefault(key, value)
    return catalog


def source_is_trusted(skill: dict) -> bool:
    return skill.get("source") == skill.get("official_source") and skill["source"].startswith("https://github.com/")


def verify(path: str, skill_id: str | None = None) -> bool:
    project = Path(path).resolve()
    try:
        catalog = catalog_for(project)
    except FileNotFoundError as error:
        print(f"✖ {error}")
        return False
    skills = [skill for skill in catalog["skills"] if skill_id in (None, skill["id"])]
    if not skills:
        print(f"✖ Skill no registrada: {skill_id}")
        return False

    all_valid = True
    for skill in skills:
        if not source_is_trusted(skill):
            print(f"✖ {skill['id']}: origen no confiable o no coincide con el oficial.")
            all_valid = False
            continue
        result = subprocess.run(["git", "ls-remote", "--exit-code", skill["source"], "HEAD"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print(f"✖ {skill['id']}: no se pudo verificar el origen remoto.")
            all_valid = False
            continue
        revision = result.stdout.split()[0]
        print(f"✔ {skill['id']}: origen oficial verificado ({revision[:12]})")
    return all_valid


def suggest(path: str, task: str) -> None:
    project = Path(path).resolve()
    try:
        catalog = catalog_for(project)
    except FileNotFoundError as error:
        print(f"✖ {error}")
        return
    normalized = task.lower()
    matches = [skill for skill in catalog["skills"] if any(trigger in normalized for trigger in skill["triggers"])]
    banner(); console.print("\n[bold]Skills sugeridas[/]\n")
    if not matches:
        info("No hay skills sugeridas. Continuá con documentación oficial o agregá una skill al catálogo.")
        return
    for skill in matches:
        console.print(f"[cyan]•[/] [bold]{skill['id']}[/]: {skill['purpose']}")
        console.print(f"  [dim]Fuente:[/] {skill['source']}")
        console.print("  [yellow]Estado:[/] no instalada; requiere aprobación explícita.")


def install(path: str, skill_id: str, scope: str, assume_yes: bool = False) -> None:
    project = Path(path).resolve()
    try:
        catalog = catalog_for(project)
    except FileNotFoundError as error:
        print(f"✖ {error}")
        return
    skill = next((item for item in catalog["skills"] if item["id"] == skill_id), None)
    if not skill:
        print(f"✖ Skill no registrada: {skill_id}")
        return
    if scope not in {"project", "global"}:
        print("✖ Scope inválido: project o global.")
        return
    if not source_is_trusted(skill):
        print("✖ El origen configurado no coincide con el origen oficial registrado.")
        return

    destination_root = cadierno_root(project) / "skills" if scope == "project" else Path.home() / ".cadierno-ai" / "skills"
    destination = destination_root / skill_id
    print(f"\nInstalar skill: {skill_id}\nFuente: {skill['source']}\nScope: {scope}\nDestino: {destination}")
    if not assume_yes:
        answer = input("¿Confirmás la instalación? [s/N]: ").strip().lower()
        if answer not in {"s", "si", "sí", "y", "yes"}:
            print("• Instalación cancelada.")
            return
    if destination.exists():
        print("• La skill ya está instalada; no se modifica.")
        return
    destination_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cadierno-skill-") as temporary:
        repository = Path(temporary) / "repository"
        result = subprocess.run(["git", "clone", "--depth=1", skill["source"], str(repository)], check=False)
        if result.returncode != 0:
            print("✖ No se pudo descargar la skill.")
            return
        candidate = repository / skill.get("skill_path", ".")
        expected_files = skill.get("expected_files", ["SKILL.md"])
        missing = [filename for filename in expected_files if not (candidate / filename).is_file()]
        if missing:
            print(f"✖ La descarga no contiene los archivos esperados: {', '.join(missing)}.")
            return
        revision = subprocess.run(["git", "-C", str(repository), "rev-parse", "HEAD"], capture_output=True, text=True, check=False).stdout.strip()
        shutil.copytree(candidate, destination)
    registry = destination_root / "installed.json"
    installed = json.loads(registry.read_text(encoding="utf-8")) if registry.exists() else {"skills": []}
    installed["skills"].append({"id": skill_id, "source": skill["source"], "revision": revision, "installed_at": datetime.now(timezone.utc).isoformat()})
    registry.write_text(json.dumps(installed, indent=2) + "\n", encoding="utf-8")
    print("✔ Skill instalada y registrada localmente.")
