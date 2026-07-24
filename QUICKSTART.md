# Quickstart V3

En cinco minutos dejás Cadierno AI operativo en un proyecto existente.

## 1. Instalar Cadierno AI

```bash
git clone https://github.com/Juanilandia78/cadierno-ai.git
cd cadierno-ai
./install/install_cli.sh
```

En Windows usá `./install/install_cli.ps1` desde PowerShell. Consultá
[INSTALL.md](INSTALL.md) para requisitos y alternativas.

## 2. Preparar un proyecto

Reemplazá `/ruta/proyecto` por la raíz del proyecto que querés analizar.

```bash
./.venv/bin/python cli/cadierno.py install /ruta/proyecto
./.venv/bin/python cli/cadierno.py bootstrap /ruta/proyecto
./.venv/bin/python cli/cadierno.py adapters enable codex claude cursor gemini vscode copilot --path /ruta/proyecto
```

Esto crea `.cadierno-ai/`, genera conocimiento inicial y configura bridges
locales. Cadierno los excluye del Git local: no se suben al proyecto.

## 3. Verificar y trabajar

```bash
./.venv/bin/python cli/cadierno.py memory status /ruta/proyecto
./.venv/bin/python cli/cadierno.py assist "Analizar expiración de pagos pendientes" /ruta/proyecto
```

Luego trabajá con tu asistente habitual. Antes de una tarea, Cadierno le indica
leer `.cadierno-ai/context.md`, que deriva a la documentación relevante.

## 4. Cerrar una tarea correctamente

```bash
./.venv/bin/python cli/cadierno.py learn propose /ruta/proyecto
./.venv/bin/python cli/cadierno.py learn apply /ruta/proyecto/.cadierno-ai/learning/proposal-AAAAMMDD-HHMMSS.md --path /ruta/proyecto
```

Cadierno sólo propone aprendizajes; aprobás, editás o rechazás cada ítem.

Siguiente paso: [MANUAL_DE_USO.md](MANUAL_DE_USO.md). Referencia completa:
[GUIA_COMANDOS_CLI.md](GUIA_COMANDOS_CLI.md).
