from pathlib import Path
import subprocess


LOCAL_CADIERNO_EXCLUDES = (
    ".cadierno-ai/",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursor/rules/cadierno-ai.mdc",
    ".github/copilot-instructions.md",
)


def ensure_local_cadierno_excludes(project: Path) -> bool:
    """Excluye assets locales sin modificar ningún archivo versionable."""
    result = subprocess.run(
        ["git", "-C", str(project), "rev-parse", "--git-path", "info/exclude"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return False

    exclude_file = Path(result.stdout.strip())
    if not exclude_file.is_absolute():
        exclude_file = project / exclude_file
    exclude_file.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude_file.read_text(encoding="utf-8") if exclude_file.exists() else ""
    missing = [entry for entry in LOCAL_CADIERNO_EXCLUDES if entry not in existing.splitlines()]
    if missing:
        suffix = "" if not existing or existing.endswith("\n") else "\n"
        exclude_file.write_text(existing + suffix + "\n".join(missing) + "\n", encoding="utf-8")
    return True
