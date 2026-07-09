# Quick Start

En menos de cinco minutos podes empezar con Cadierno AI.

## Paso 1: clonar e instalar

```bash
git clone https://github.com/TU_USUARIO/cadierno-ai.git
cd cadierno-ai
./install/install_cli.sh
```

## Paso 2: bootstrap del proyecto

```bash
./.venv/bin/python cli/cadierno.py bootstrap /ruta/proyecto
```

## Paso 3: inicializar memoria

```bash
./.venv/bin/python cli/cadierno.py memory init /ruta/proyecto
./.venv/bin/python cli/cadierno.py memory status /ruta/proyecto
```

## Paso 4: empezar a trabajar

Ejemplos de uso:

```bash
./.venv/bin/python cli/cadierno.py assist "hay que corregir bug en checkout" /ruta/proyecto
./.venv/bin/python cli/cadierno.py memory save /ruta/proyecto --title "Decision auth" --content "Se unifica middleware" --type decision --tags auth,backend
```

## SQLite

No requiere instalacion manual. Cadierno usa `sqlite3` incluido en Python.

## Filosofia

Primero comprender.

Despues disenar.

Finalmente implementar.