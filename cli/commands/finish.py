from pathlib import Path
import subprocess

from core.memory import add_history_event, initialize_memory


def _run_git(project_path: Path, args: list[str]) -> tuple[int, str]:

    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=project_path,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return 127, "git no esta disponible en este sistema."

    output = (completed.stdout or "") + (completed.stderr or "")
    return completed.returncode, output.strip()


def _run_git_stream(project_path: Path, args: list[str]) -> int:

    try:
        completed = subprocess.run(["git", *args], cwd=project_path, check=False)
    except FileNotFoundError:
        print("✖ git no esta disponible en este sistema.")
        return 127

    return completed.returncode


def finish(path: str, push: bool = False, branch_name: str | None = None, tag_name: str | None = None):

    project_path = Path(path).resolve()

    print("\nCadierno Finish\n")

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    initialize_memory(project_path)

    exit_code, branch = _run_git(project_path, ["branch", "--show-current"])
    if exit_code != 0 or not branch:
        branch = "(sin rama detectada)"

    status_code, status = _run_git(project_path, ["status", "--short"])
    if status_code != 0:
        print("✖ No se pudo leer el estado de git.")
        print(status)
        return

    remote_code, remote = _run_git(project_path, ["remote", "-v"])
    if remote_code != 0:
        remote = "(sin remotos detectados)"

    add_history_event(project_path, "finish", f"branch={branch} status={len(status.splitlines())}")

    print(f"Proyecto........... {project_path}")
    print(f"Rama actual........ {branch}")
    print("Remotos............")
    print(remote if remote else "(sin remotos)")
    print("\nEstado git.........")
    print(status if status else "(limpio)")

    if status:
        print("\nSiguiente paso.....")
        print("- Revisar los cambios pendientes.")
        print("- Hacer commit.")
        print("- Hacer push a GitHub.")
        print("- Crear o actualizar release si corresponde.")
    else:
        print("\nRepo limpio....... listo para push/release si ya hiciste commit.")

    print("\nComandos sugeridos:")
    print("- git status")
    print("- git add -A && git commit -m \"mensaje\"")
    print("- git push origin <rama>")
    print("- git push origin v2.2.0")
    print("- Publicar release en GitHub con RELEASE_NOTES_v2.2.0.md")

    if push:
        target_branch = branch_name or branch

        if status:
            print("\n⚠ No se puede hacer push automatico con cambios sin commit.")
            print("   Primero hace commit, luego ejecuta finish --push.")
            return

        print("\nEjecutando push automatico...")

        if target_branch and target_branch not in {"(sin rama detectada)", ""}:
            branch_exit = _run_git_stream(project_path, ["push", "origin", target_branch])
            if branch_exit != 0:
                print(f"✖ Fallo el push de la rama: {target_branch}")
                return
            print(f"✔ Push de rama completado: {target_branch}")

        if tag_name:
            tag_exit = _run_git_stream(project_path, ["push", "origin", tag_name])
            if tag_exit != 0:
                print(f"✖ Fallo el push del tag: {tag_name}")
                return
            print(f"✔ Push de tag completado: {tag_name}")

        print("\nGitHub actualizado por push de Git.")
