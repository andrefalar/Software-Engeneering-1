# FortiFile - Scripts de Ejecución y Automatización

Este directorio contiene scripts y herramientas para ejecutar, desarrollar y mantener la aplicación FortiFile con verificación automática de dependencias.

## Scripts Disponibles

### 0. `../run.sh` (Acceso Rápido desde Raíz)

Script de acceso rápido ubicado en el directorio raíz del proyecto que permite ejecutar FortiFile sin necesidad de navegar a la carpeta `scripts/`.

**Características:**
- 🚀 Ejecución directa desde el directorio raíz del proyecto
- 🔗 Redirecciona automáticamente a `scripts/run_fortifile.sh`
- 📋 Acepta todas las opciones del script principal

**Uso desde el directorio raíz:**
```bash
# Desde /home/andres/projects/python/Software-Engeneering-1/Proyecto/
./run.sh                    # Ejecución normal
./run.sh --help             # Mostrar ayuda
./run.sh --check-only       # Solo verificar sistema
./run.sh --test             # Ejecutar con tests
```

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

### 4. `../docs/Makefile` (Automatización con Make)

Sistema de automatización completo usando Make, ubicado en la carpeta `docs/`.

**Comandos principales:**
```bash
# Desde el directorio raíz:
make -f docs/Makefile help      # Mostrar ayuda
make -f docs/Makefile init      # Inicializar proyecto
make -f docs/Makefile run       # Ejecutar aplicación
make -f docs/Makefile dev       # Modo desarrollo
make -f docs/Makefile test      # Ejecutar tests
make -f docs/Makefile check     # Verificar dependencias
make -f docs/Makefile lint      # Linting del código
make -f docs/Makefile format    # Formatear código
make -f docs/Makefile clean     # Limpiar archivos temporales
make -f docs/Makefile deps      # Información de dependencias
make -f docs/Makefile security  # Verificar configuración de seguridad
make -f docs/Makefile backup    # Crear backup del proyecto
```

## Guía de Uso Rápido

### **🚀 Acceso rápido desde el directorio raíz:**
```bash
# Desde el directorio principal del proyecto
./run.sh                    # Ejecutar FortiFile
./run.sh --check-only       # Solo verificar sistema  
./run.sh --help             # Mostrar ayuda
```

### **📋 Uso desde la carpeta scripts:**
```bash
# Navegar a scripts/ y ejecutar directamente
cd scripts/
./run_fortifile.sh          # Ejecución completa
./dev_run.sh               # Desarrollo rápido
./init_project.sh          # Inicialización (primera vez)
```

### **⚙️ Uso con Make (desde raíz):**
```bash
# El Makefile está en docs/, usar desde el directorio raíz:
make -f docs/Makefile run    # Ejecutar aplicación
make -f docs/Makefile dev    # Desarrollo rápido
make -f docs/Makefile test   # Ejecutar tests
make -f docs/Makefile help   # Ver todas las opciones
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
├── run.sh                    # 🚀 Script de acceso rápido (desde raíz)
├── requirements.txt          # Dependencias Python
├── .gitignore               # Archivos ignorados por Git
├── scripts/
│   ├── run_fortifile.sh      # Script principal de ejecución
│   ├── dev_run.sh            # Script de desarrollo rápido
│   ├── init_project.sh       # Script de inicialización
│   └── SCRIPTS_README.md     # Este archivo
├── config/
│   ├── pyproject.toml        # Configuración del proyecto
│   ├── pytest.ini           # Configuración de pytest
│   ├── .flake8              # Configuración de flake8
│   └── .pylintrc            # Configuración de pylint
├── docs/
│   └── Makefile             # Automatización con Make
├── frontend/
│   ├── app.py               # Aplicación principal GUI
│   ├── assets/              # Recursos (iconos, imágenes)
│   ├── themes/              # Temas y estilos
│   └── ui/                  # Interfaces de usuario
├── backend/
│   ├── main.py              # Backend principal
│   ├── database/            # Gestión de base de datos
│   ├── models/              # Modelos de datos
│   └── services/            # Servicios de negocio
├── tests/                   # Tests del proyecto
├── secure_files/            # Archivos cifrados (creado automáticamente)
├── venv/                    # Entorno virtual (creado automáticamente)
└── .vscode/                 # Configuración de VS Code
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
# o desde el directorio raíz:
../run.sh --check-only
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
1. Ejecuta `./run_fortifile.sh --check-only` (o `../run.sh --check-only` desde raíz) para diagnosticar
2. Verifica que todas las dependencias estén instaladas
3. Consulta los logs de error para más detalles
