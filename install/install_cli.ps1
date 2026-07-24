#!/usr/bin/env pwsh

param(
    [switch]$NoVenv
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$venv = Join-Path $root ".venv"
$python = "python"

if (Get-Command py -ErrorAction SilentlyContinue) {
    $python = "py -3"
} elseif (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "No se encontro Python 3. Instala Python 3.10+ y reintenta."
}

Write-Host "==> Cadierno AI installer (Windows)"
Write-Host "Repo: $root"
Write-Host "Python launcher: $python"

if (-not $NoVenv) {
    if (-not (Test-Path $venv)) {
        Write-Host "==> Creando entorno virtual en $venv"
        Invoke-Expression "$python -m venv `"$venv`""
    }

    Write-Host "==> Actualizando pip/setuptools/wheel"
    & "$venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel

    if (Test-Path "$root\requirements.txt") {
        Write-Host "==> Instalando dependencias de Cadierno"
        & "$venv\Scripts\python.exe" -m pip install -r "$root\requirements.txt"
    }

    Write-Host "==> Verificando instalacion de Cadierno"
    & "$venv\Scripts\python.exe" "$root\cli\cadierno.py" --version
    & "$venv\Scripts\python.exe" "$root\cli\cadierno.py" doctor

    Write-Host ""
    Write-Host "Instalacion finalizada."
    Write-Host "Uso rapido:"
    Write-Host "  .\.venv\Scripts\python.exe .\cli\cadierno.py install C:\ruta\proyecto"
    Write-Host "  .\.venv\Scripts\python.exe .\cli\cadierno.py bootstrap C:\ruta\proyecto"
    Write-Host "  .\.venv\Scripts\python.exe .\cli\cadierno.py adapters enable codex claude cursor gemini vscode copilot --path C:\ruta\proyecto"
} else {
    Write-Host "==> Instalacion sin venv (NoVenv)"
    Invoke-Expression "$python -m pip install --upgrade pip setuptools wheel"
    if (Test-Path "$root\requirements.txt") {
        Invoke-Expression "$python -m pip install -r `"$root\requirements.txt`""
    }

    Write-Host "==> Verificando instalacion de Cadierno"
    Invoke-Expression "$python `"$root\cli\cadierno.py`" --version"
    Invoke-Expression "$python `"$root\cli\cadierno.py`" doctor"

    Write-Host ""
    Write-Host "Instalacion finalizada (sin venv)."
    Write-Host "Uso rapido:"
    Write-Host "  py -3 .\cli\cadierno.py install C:\ruta\proyecto"
    Write-Host "  py -3 .\cli\cadierno.py bootstrap C:\ruta\proyecto"
}

Write-Host ""
Write-Host "Nota SQLite:"
Write-Host "  Cadierno usa sqlite3 del standard library de Python."
Write-Host "  No necesitas instalar SQLite por separado."
