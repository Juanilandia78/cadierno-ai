from pathlib import Path
import shutil

from utils.git import ensure_local_cadierno_excludes
from utils.path import cadierno_root


SUPPORTED_ADAPTERS = {"codex", "claude", "cursor", "gemini", "vscode", "copilot"}

COPILOT_BRIDGE = """# Cadierno AI local instructions

Before working, read and follow `.cadierno-ai/context.md` and then the files it
indicates for the active task. Preserve Cadierno assets as local-only: do not
add `.cadierno-ai/`, agent bridge files, or this file to version control.

Respect approved scope, show evidence, run relevant tests, and stop for review
after each microtask.
"""


def enable(path: str, adapters: list[str]) -> None:
    project = Path(path).resolve()
    requested = set(adapters)
    invalid = requested - SUPPORTED_ADAPTERS
    if invalid:
        print(f"✖ Adaptadores no soportados: {', '.join(sorted(invalid))}")
        return
    if not cadierno_root(project).exists():
        print("✖ No existe .cadierno-ai/. Ejecutá 'cadierno install' primero.")
        return

    ensure_local_cadierno_excludes(project)
    framework = Path(__file__).resolve().parents[2]

    if "codex" in requested:
        target = project / "AGENTS.md"
        if target.exists():
            print("• Codex: se conserva AGENTS.md existente")
        else:
            shutil.copy2(framework / "templates" / "AGENTS.template.md", target)
            print("✔ Codex: AGENTS.md creado")

    if "claude" in requested:
        target = project / "CLAUDE.md"
        if target.exists():
            print("• Claude: se conserva CLAUDE.md existente")
        else:
            target.write_text("@.cadierno-ai/AGENTS.md\n", encoding="utf-8")
            print("✔ Claude: CLAUDE.md creado")

    if "cursor" in requested:
        target = project / ".cursor" / "rules" / "cadierno-ai.mdc"
        if target.exists():
            print("• Cursor: se conserva regla existente")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("---\ndescription: Cadierno AI local project context\nalwaysApply: true\n---\n\nRead and follow `.cadierno-ai/AGENTS.md` before working on this project.\n", encoding="utf-8")
            print("✔ Cursor: regla local creada")

    if "gemini" in requested:
        target = project / "GEMINI.md"
        if target.exists():
            print("• Gemini: se conserva GEMINI.md existente")
        else:
            target.write_text("# Cadierno AI bridge\n\n@.cadierno-ai/AGENTS.md\n", encoding="utf-8")
            print("✔ Gemini: GEMINI.md creado")

    if requested & {"vscode", "copilot"}:
        target = project / ".github" / "copilot-instructions.md"
        if target.exists():
            print("• VS Code/Copilot: se conserva copilot-instructions.md existente")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(COPILOT_BRIDGE, encoding="utf-8")
            print("✔ VS Code/Copilot: instrucciones locales creadas")
