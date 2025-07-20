# FortiFile - Scripts de Ejecución y Automatización

Este directorio contiene scripts y herramientas para ejecutar, desarrollar y mantener la aplicación FortiFile con verificación automática de dependencias.

## Scripts Disponibles

### 1. `run_fortifile.sh` (Script Principal)

Script completo con verificación exhaustiva de dependencias y configuración del entorno.

**Características:**
- ✅ Verificación de sistema operativo
- ✅ Verificación de Python (3.8+ requerido, 3.12 recomendado)
- ✅ Verificación e instalación de pip
- ✅ Verificación de herramientas del sistema
- ✅ Verificación de dependencias gráficas (PyQt5)
- ✅ Configuración automática de entorno virtual
- ✅ Instalación de dependencias desde requirements.txt
- ✅ Verificación de archivos críticos del proyecto
- ✅ Verificación de base de datos
- ✅ Ejecución opcional de tests
- ✅ Lanzamiento de la aplicación

**Uso básico:**
```bash
./run_fortifile.sh
```

**Opciones disponibles:**
```bash
./run_fortifile.sh --help           # Mostrar ayuda
./run_fortifile.sh --version        # Mostrar versión
./run_fortifile.sh --test           # Ejecutar tests antes de lanzar
./run_fortifile.sh --no-venv        # No usar entorno virtual
./run_fortifile.sh --backend-only   # Solo ejecutar backend
./run_fortifile.sh --check-only     # Solo verificar dependencias
```

### 2. `dev_run.sh` (Script de Desarrollo)

Script simplificado para desarrollo rápido sin verificaciones extensas.

**Uso:**
```bash
./dev_run.sh
```

### 3. `init_project.sh` (Script de Inicialización)

Script para configurar el proyecto por primera vez o después de un git clone.

**Características:**
- 🔧 Creación de entorno virtual
- 📦 Instalación de dependencias
- 🔐 Generación de claves de cifrado
- 🗄️ Inicialización de base de datos
- 🛡️ Configuración de permisos de seguridad

**Uso:**
```bash
./init_project.sh
```

### 4. `Makefile` (Automatización con Make)

Sistema de automatización completo usando Make.

**Comandos principales:**
```bash
make help      # Mostrar ayuda
make init      # Inicializar proyecto
make run       # Ejecutar aplicación
make dev       # Modo desarrollo
make test      # Ejecutar tests
make check     # Verificar dependencias
make lint      # Linting del código
make format    # Formatear código
make clean     # Limpiar archivos temporales
make deps      # Información de dependencias
make security  # Verificar configuración de seguridad
make backup    # Crear backup del proyecto
```

## Requisitos del Sistema

### Mínimos
- **Sistema Operativo:** Linux, macOS, o Windows
- **Python:** 3.8 o superior (3.12 recomendado)
- **pip:** Para instalación de paquetes
- **Entorno gráfico:** Para PyQt5 (X11, Wayland, etc.)

### Dependencias del Sistema (Linux)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-pyqt5

# Red Hat/Fedora/CentOS
sudo yum install python3 python3-pip python3-pyqt5
```

### Dependencias del Sistema (macOS)
```bash
# Con Homebrew
brew install python3

# Python se puede descargar desde https://www.python.org/downloads/
```

## Estructura del Proyecto

```
Proyecto/
├── run_fortifile.sh          # Script principal de ejecución
├── dev_run.sh                # Script de desarrollo rápido
├── init_project.sh           # Script de inicialización
├── Makefile                  # Automatización con Make
├── SCRIPTS_README.md         # Este archivo
├── requirements.txt          # Dependencias Python
├── pyproject.toml           # Configuración del proyecto
├── frontend/
│   ├── app.py               # Aplicación principal GUI
│   └── ui/                  # Interfaces de usuario
├── backend/
│   ├── main.py              # Backend principal
│   ├── database/            # Gestión de base de datos
│   ├── models/              # Modelos de datos
│   └── services/            # Servicios de negocio
├── tests/                   # Tests del proyecto
├── secure_files/            # Archivos cifrados (creado automáticamente)
├── logs/                    # Logs de la aplicación (creado automáticamente)
└── venv/                    # Entorno virtual (creado automáticamente)
```

## Dependencias Principales

### Backend
- **SQLAlchemy 2.0.41:** ORM para base de datos
- **bcrypt 4.3.0:** Hashing de contraseñas
- **cryptography 45.0.5:** Operaciones criptográficas

### Frontend
- **PyQt5 5.15.11:** Framework GUI
- **PyQt5-Qt5 5.15.17:** Bibliotecas Qt5

### Desarrollo
- **pytest 8.4.1:** Framework de testing
- **black 25.1.0:** Formateador de código
- **flake8 7.3.0:** Linter

## Solución de Problemas

### Error: "Python 3 no está instalado"
Instala Python 3.8 o superior desde:
- **Linux:** `sudo apt install python3 python3-pip`
- **macOS:** `brew install python3` o desde python.org
- **Windows:** Desde python.org

### Error: "No se detectó sistema gráfico"
Asegúrate de estar ejecutando en un entorno con GUI:
- **Linux:** Verifica que `$DISPLAY` esté configurado
- **SSH:** Usa `ssh -X` para forwarding X11
- **WSL:** Instala un servidor X como VcXsrv

### Error: "Dependencias Qt5 faltantes"
**Linux:**
```bash
sudo apt install python3-pyqt5 python3-pyqt5.qtwidgets
```

### Error: "Archivo crítico faltante"
Verifica que todos los archivos del proyecto estén presentes:
```bash
./run_fortifile.sh --check-only
```

## Logs y Debug

El script proporciona salida colorizada:
- 🔵 **[INFO]** Información general
- ✅ **[✓]** Operación exitosa  
- ⚠️  **[⚠]** Advertencia
- ❌ **[✗]** Error

## Desarrollo

Para modificar los scripts:
1. Edita `run_fortifile.sh` para el script principal
2. Edita `dev_run.sh` para desarrollo rápido
3. Mantén permisos de ejecución: `chmod +x *.sh`

## Soporte

Para problemas con los scripts:
1. Ejecuta `./run_fortifile.sh --check-only` para diagnosticar
2. Verifica que todas las dependencias estén instaladas
3. Consulta los logs de error para más detalles
