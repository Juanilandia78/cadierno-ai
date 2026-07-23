from pathlib import Path
import re


_ENV_VAR_PATTERN = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")


def extract_env_var_names(env_file: Path) -> list[str]:
    """
    Devuelve únicamente los NOMBRES de variables declaradas en un archivo .env.

    Regla de seguridad no negociable: esta función jamás debe devolver, loguear
    ni conservar en memoria el valor de una variable. Solo el nombre (lado
    izquierdo del `=`) sale de esta función.
    """

    if not env_file.exists() or not env_file.is_file():
        return []

    names: list[str] = []

    try:
        with env_file.open("r", encoding="utf-8", errors="ignore") as handle:
            for raw_line in handle:
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                match = _ENV_VAR_PATTERN.match(line)
                if match:
                    names.append(match.group(1))
    except Exception:
        return []

    return sorted(dict.fromkeys(names))
