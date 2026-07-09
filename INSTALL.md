# Instalacion de Cadierno AI

## Requisitos

- Python 3.10 o superior
- Git
- Shell bash/zsh (macOS o Linux)
- PowerShell (Windows, opcional)

Cadierno AI funciona con asistentes que puedan leer Markdown:

- Claude Code
- GitHub Copilot (modo agente)
- Cursor
- ChatGPT
- Otros compatibles

## Instalacion local recomendada (1 comando)

1. Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/cadierno-ai.git
cd cadierno-ai
```

2. Ejecutar instalador:

```bash
./install/install_cli.sh
```

Ese script crea `.venv`, actualiza pip y valida Cadierno con `--version` + `doctor`.

## Instalacion en Windows

Desde PowerShell en la raiz del repo:

```powershell
.\install\install_cli.ps1
```

Ese script crea `.venv`, actualiza pip y valida Cadierno con `--version` + `doctor`.

Si queres instalar sin entorno virtual:

```powershell
.\install\install_cli.ps1 -NoVenv
```

## Uso inicial

Con el entorno creado:

```bash
./.venv/bin/python cli/cadierno.py bootstrap /ruta/proyecto
./.venv/bin/python cli/cadierno.py memory init /ruta/proyecto
```

En Windows:

```powershell
.\.venv\Scripts\python.exe .\cli\cadierno.py bootstrap C:\ruta\proyecto
.\.venv\Scripts\python.exe .\cli\cadierno.py memory init C:\ruta\proyecto
```

## .venv es obligatorio?

No es obligatorio, pero si muy recomendado.

Ventajas de `.venv`:

- Aisla dependencias de Cadierno de otros proyectos.
- Evita conflictos de versiones de Python/pip.
- Hace reproducible la instalacion en cualquier PC.

Sin `.venv` funciona, pero usa el Python global del sistema.

## SQLite: se instala aparte?

No. Cadierno usa `sqlite3` del standard library de Python.

No necesitas instalar SQLite por separado para la memoria local.

Archivos que crea automaticamente:

- `~/.cadierno-ai/brain.db` (memoria de usuario)
- `/ruta/proyecto/memory/.cadierno/brain.db` (memoria de workspace)

## Actualizacion

```bash
git pull
./install/install_cli.sh
```

## Filosofia

Cadierno AI se adapta al proyecto.

Nunca intenta que el proyecto se adapte a Cadierno AI.