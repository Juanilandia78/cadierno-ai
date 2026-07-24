#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN=""

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "ERROR: No se encontro Python 3 en el sistema."
  exit 1
fi

echo "==> Cadierno AI installer"
echo "Repo: ${ROOT_DIR}"
echo "Python: ${PYTHON_BIN}"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "==> Creando entorno virtual en ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

echo "==> Actualizando pip/setuptools/wheel"
"${VENV_DIR}/bin/python" -m pip install --upgrade pip setuptools wheel

if [[ -f "${ROOT_DIR}/requirements.txt" ]]; then
  echo "==> Instalando dependencias de Cadierno"
  "${VENV_DIR}/bin/python" -m pip install -r "${ROOT_DIR}/requirements.txt"
fi

echo "==> Verificando instalacion de Cadierno"
"${VENV_DIR}/bin/python" "${ROOT_DIR}/cli/cadierno.py" --version
"${VENV_DIR}/bin/python" "${ROOT_DIR}/cli/cadierno.py" doctor

cat <<EOF

Instalacion finalizada.

Uso rapido:
  ${VENV_DIR}/bin/python ${ROOT_DIR}/cli/cadierno.py install /ruta/proyecto
  ${VENV_DIR}/bin/python ${ROOT_DIR}/cli/cadierno.py bootstrap /ruta/proyecto
  ${VENV_DIR}/bin/python ${ROOT_DIR}/cli/cadierno.py adapters enable codex claude cursor gemini vscode copilot --path /ruta/proyecto

Nota SQLite:
  Cadierno usa sqlite3 del standard library de Python.
  No necesitas instalar SQLite por separado para usar memoria local.
EOF
