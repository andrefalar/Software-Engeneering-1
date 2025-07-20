# FortiFile - Script de ejecución para Windows (PowerShell)
# Autor: Sistema FortiFile

Write-Host "🔐 FortiFile - Sistema de Archivos Seguros" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] $pythonVersion encontrado" -ForegroundColor Green
} catch {
    Write-Host "[✗] Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor, instala Python 3.8 o superior desde https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar si existe el entorno virtual, si no, crearlo
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "[INFO] Creando entorno virtual..." -ForegroundColor Blue
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[✗] No se pudo crear el entorno virtual" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Activar entorno virtual
Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

# Instalar dependencias si no están instaladas
Write-Host "[INFO] Verificando dependencias..." -ForegroundColor Blue
pip install -r requirements.txt

# Ejecutar la aplicación
Write-Host "[INFO] Iniciando FortiFile..." -ForegroundColor Green
python frontend\app.py

# Desactivar entorno virtual al salir
deactivate

Read-Host "Presiona Enter para salir"