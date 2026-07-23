from pathlib import Path

from core.managed_sections import upsert_managed_section


GITIGNORE_MANAGED_KEY = "assets"

# Todo lo que "install"/"bootstrap" crean en el proyecto destino: framework
# vendorizado (.ai/, playbooks/, checklists/), conocimiento generado
# (knowledge/), memoria local (memory/, incluye SQLite) y los archivos de
# contexto para agentes (AGENTS.md, CLAUDE.md). Nada de esto debe terminar
# commiteado al repo del proyecto: si hace falta en otro checkout, se
# reinstala con `cadierno install` + `cadierno bootstrap`.
GITIGNORE_ENTRIES = """
# Cadierno AI: framework instalado + conocimiento/memoria generados.
# No se commitea: reinstalar con `cadierno install` + `cadierno bootstrap`.
.ai/
playbooks/
checklists/
knowledge/
memory/
AGENTS.md
CLAUDE.md
""".strip()


def ensure_gitignore_entries(project_path: Path) -> str:
    """
    Asegura que el `.gitignore` del proyecto ignore los archivos/directorios
    que Cadierno instala. Usa un bloque gestionado (`# cadierno:managed:...`):
    no toca ninguna otra regla que el proyecto ya tuviera.

    Devuelve "created", "updated" o "unchanged".
    """

    gitignore_path = project_path / ".gitignore"
    existed_before = gitignore_path.exists()
    existing = gitignore_path.read_text(encoding="utf-8", errors="ignore") if existed_before else ""

    updated = upsert_managed_section(existing, GITIGNORE_MANAGED_KEY, GITIGNORE_ENTRIES, style="hash")

    if existed_before and updated == existing:
        return "unchanged"

    gitignore_path.write_text(updated, encoding="utf-8")
    return "created" if not existed_before else "updated"
