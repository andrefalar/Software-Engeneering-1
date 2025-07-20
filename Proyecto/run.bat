@echo off
REM FortiFile - Script de ejecución para Windows
REM Autor: Sistema FortiFile

echo 🔐 FortiFile - Sistema de Archivos Seguros
echo ==========================================

REM Verificar Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.8 o superior desde https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar si existe el entorno virtual, si no, crearlo
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar PyQt5 directamente (sin usar la versión específica de PyQt5-Qt5)
echo [INFO] Instalando PyQt5...
pip install PyQt5==5.15.11

REM Instalar otras dependencias
echo [INFO] Instalando otras dependencias...
pip install SQLAlchemy==2.0.41 greenlet==3.2.3 bcrypt==4.3.0 cryptography==45.0.5 cffi==1.17.1 pycparser==2.22 PyQt5_sip==12.17.0 typing_extensions==4.14.1

REM Ejecutar la aplicación
echo [INFO] Iniciando FortiFile...
python frontend\app.py

REM Desactivar entorno virtual al salir
call venv\Scripts\deactivate.bat

pause