# Instalación de Cadierno AI V3

## Requisitos

- Python 3.10 o superior.
- Git.
- macOS/Linux: bash o zsh. Windows: PowerShell.

Cadierno funciona localmente con Codex, Claude, Cursor, Gemini CLI y VS
Code/GitHub Copilot mediante adapters opcionales.

## macOS y Linux

```bash
git clone https://github.com/Juanilandia78/cadierno-ai.git
cd cadierno-ai
./install/install_cli.sh
```

El script crea `.venv`, instala las dependencias de Cadierno, y ejecuta
`--version` y `doctor`.

## Windows

Desde PowerShell, en la raíz del repositorio:

```powershell
.\install\install_cli.ps1
```

Para usar Python global sin entorno virtual:

```powershell
.\install\install_cli.ps1 -NoVenv
```

## Comprobar la instalación

```bash
./.venv/bin/python cli/cadierno.py --version
./.venv/bin/python cli/cadierno.py doctor
```

En Windows: `.\.venv\Scripts\python.exe .\cli\cadierno.py doctor`.

## Actualizar Cadierno

```bash
git pull
./install/install_cli.sh
```

Después sincronizá el contexto de cada proyecto consumidor:

```bash
./.venv/bin/python cli/cadierno.py update /ruta/proyecto
```

## Datos locales

Cadierno no necesita instalar SQLite: usa `sqlite3` incluido con Python.

- Memoria de usuario: `~/.cadierno-ai/brain.db`.
- Memoria del proyecto: `/ruta/proyecto/.cadierno-ai/memory/.cadierno/brain.db`.

La instalación en un proyecto se explica en [QUICKSTART.md](QUICKSTART.md).
