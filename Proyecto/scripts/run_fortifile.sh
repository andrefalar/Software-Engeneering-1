#!/bin/bash

# FortiFile - Sistema de Archivos Seguros
# Script de ejecución con verificación de dependencias
# Autor: Sistema FortiFile
# Fecha: $(date +"%Y-%m-%d")

set -e  # Salir si cualquier comando falla

# ===== CONFIGURACIÓN =====
APP_NAME="FortiFile"
APP_VERSION="1.0.0"
PYTHON_MIN_VERSION="3.8"
REQUIRED_PYTHON_VERSION="3.12"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"  # Subir un nivel ya que estamos en scripts/
VENV_DIR="$PROJECT_DIR/venv"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
FRONTEND_APP="$PROJECT_DIR/frontend/app.py"
BACKEND_APP="$PROJECT_DIR/backend/main.py"

# ===== COLORES PARA OUTPUT =====
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ===== FUNCIONES AUXILIARES =====

print_banner() {
    echo -e "${PURPLE}"
    echo "==========================================="
    echo "🔐 $APP_NAME - Sistema de Archivos Seguros"
    echo "   Versión: $APP_VERSION"
    echo "==========================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# ===== VERIFICACIÓN DE SISTEMA OPERATIVO =====
check_os() {
    print_step "Verificando sistema operativo..."
    
    case "$(uname -s)" in
        Linux*)
            print_success "Sistema Linux detectado"
            OS_TYPE="Linux"
            ;;
        Darwin*)
            print_success "Sistema macOS detectado"
            OS_TYPE="Mac"
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            print_success "Sistema Windows detectado"
            OS_TYPE="Windows"
            ;;
        *)
            print_warning "Sistema operativo no reconocido: $(uname -s)"
            OS_TYPE="Unknown"
            ;;
    esac
}

# ===== VERIFICACIÓN DE PYTHON =====
check_python() {
    print_step "Verificando instalación de Python..."
    
    # Verificar si Python está instalado
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado"
        print_step "Por favor, instala Python 3.8 o superior:"
        case $OS_TYPE in
            "Linux")
                echo "  sudo apt update && sudo apt install python3 python3-pip python3-venv"
                echo "  # o en sistemas basados en Red Hat:"
                echo "  sudo yum install python3 python3-pip"
                ;;
            "Mac")
                echo "  brew install python3"
                echo "  # o descarga desde https://www.python.org/downloads/"
                ;;
            "Windows")
                echo "  Descarga desde https://www.python.org/downloads/"
                ;;
        esac
        exit 1
    fi
    
    # Verificar versión de Python
    PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    print_success "Python $PYTHON_VERSION encontrado"
    
    # Comparar versiones
    if [ "$(printf '%s\n' "$PYTHON_MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$PYTHON_MIN_VERSION" ]; then
        print_error "Python $PYTHON_VERSION es muy antiguo. Se requiere Python $PYTHON_MIN_VERSION o superior"
        exit 1
    fi
    
    # Advertencia si no es la versión recomendada
    if [ "$PYTHON_VERSION" != "$REQUIRED_PYTHON_VERSION" ]; then
        print_warning "Se recomienda Python $REQUIRED_PYTHON_VERSION para máxima compatibilidad"
    fi
}

# ===== VERIFICACIÓN DE PIP =====
check_pip() {
    print_step "Verificando pip..."
    
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 no está instalado"
        print_step "Instalando pip..."
        case $OS_TYPE in
            "Linux")
                sudo apt update && sudo apt install python3-pip
                ;;
            "Mac")
                python3 -m ensurepip --upgrade
                ;;
            *)
                python3 -m ensurepip --upgrade
                ;;
        esac
    else
        print_success "pip3 encontrado"
    fi
    
    # Actualizar pip
    print_step "Actualizando pip..."
    python3 -m pip install --upgrade pip
}

# ===== VERIFICACIÓN DE HERRAMIENTAS DEL SISTEMA =====
check_system_tools() {
    print_step "Verificando herramientas del sistema..."
    
    # Lista de herramientas opcionales pero recomendadas
    local tools=("git" "curl" "wget")
    
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            print_success "$tool encontrado"
        else
            print_warning "$tool no encontrado (opcional pero recomendado)"
        fi
    done
}

# ===== VERIFICACIÓN DE DEPENDENCIAS GRÁFICAS (PARA PYQT5) =====
check_gui_dependencies() {
    print_step "Verificando dependencias gráficas para PyQt5..."
    
    case $OS_TYPE in
        "Linux")
            # Verificar si es un sistema con GUI
            if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
                print_success "Sistema gráfico detectado"
            else
                print_warning "No se detectó sistema gráfico. PyQt5 puede no funcionar correctamente"
            fi
            
            # Verificar librerías Qt
            local qt_libs=("libqt5core5a" "libqt5gui5" "libqt5widgets5")
            local missing_libs=()
            
            for lib in "${qt_libs[@]}"; do
                if ! dpkg -l | grep -q "$lib" 2>/dev/null; then
                    missing_libs+=("$lib")
                fi
            done
            
            if [ ${#missing_libs[@]} -gt 0 ]; then
                print_warning "Algunas librerías Qt5 pueden estar faltando"
                print_step "Para instalar las dependencias Qt5:"
                echo "  sudo apt update"
                echo "  sudo apt install python3-pyqt5 python3-pyqt5.qtwidgets python3-pyqt5.qtcore python3-pyqt5.qtgui"
            else
                print_success "Dependencias Qt5 del sistema encontradas"
            fi
            ;;
        "Mac")
            print_success "macOS: PyQt5 debería funcionar correctamente"
            ;;
        "Windows")
            print_success "Windows: PyQt5 debería funcionar correctamente"
            ;;
    esac
}

# ===== CONFIGURACIÓN DE ENTORNO VIRTUAL =====
setup_virtual_environment() {
    print_step "Configurando entorno virtual..."
    
    if [ ! -d "$VENV_DIR" ]; then
        print_step "Creando entorno virtual..."
        python3 -m venv "$VENV_DIR"
        print_success "Entorno virtual creado en $VENV_DIR"
    else
        print_success "Entorno virtual existente encontrado"
    fi
    
    # Activar entorno virtual
    print_step "Activando entorno virtual..."
    source "$VENV_DIR/bin/activate"
    print_success "Entorno virtual activado"
}

# ===== INSTALACIÓN DE DEPENDENCIAS =====
install_dependencies() {
    print_step "Instalando dependencias del proyecto..."
    
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        print_error "Archivo requirements.txt no encontrado en $REQUIREMENTS_FILE"
        exit 1
    fi
    
    print_step "Actualizando pip en el entorno virtual..."
    pip install --upgrade pip
    
    print_step "Instalando paquetes desde requirements.txt..."
    pip install -r "$REQUIREMENTS_FILE"
    print_success "Dependencias instaladas correctamente"
}

# ===== VERIFICACIÓN DE ARCHIVOS CRÍTICOS =====
check_critical_files() {
    print_step "Verificando archivos críticos del proyecto..."
    
    local critical_files=(
        "$FRONTEND_APP"
        "$BACKEND_APP"
        "$PROJECT_DIR/backend/database/connection.py"
        "$PROJECT_DIR/backend/models"
        "$PROJECT_DIR/backend/services"
        "$PROJECT_DIR/frontend/ui"
    )
    
    for file in "${critical_files[@]}"; do
        if [ -e "$file" ]; then
            print_success "$(basename "$file") encontrado"
        else
            print_error "Archivo crítico faltante: $file"
            exit 1
        fi
    done
}

# ===== VERIFICACIÓN DE BASE DE DATOS =====
check_database() {
    print_step "Verificando configuración de base de datos..."
    
    local db_file="$PROJECT_DIR/fortifile.db"
    
    if [ -f "$db_file" ]; then
        print_success "Base de datos SQLite encontrada"
    else
        print_warning "Base de datos no encontrada. Se creará al ejecutar la aplicación"
    fi
}

# ===== VERIFICACIÓN DE ARCHIVOS DE CONFIGURACIÓN =====
check_config_files() {
    print_step "Verificando archivos de configuración..."
    
    local config_files=(
        "$PROJECT_DIR/fortifile.key"
        "$PROJECT_DIR/pyproject.toml"
        "$PROJECT_DIR/pytest.ini"
    )
    
    for file in "${config_files[@]}"; do
        if [ -f "$file" ]; then
            print_success "$(basename "$file") encontrado"
        else
            print_warning "Archivo de configuración faltante: $(basename "$file")"
        fi
    done
}

# ===== EJECUCIÓN DE TESTS (OPCIONAL) =====
run_tests() {
    if [ "$RUN_TESTS" = "true" ]; then
        print_step "Ejecutando tests del proyecto..."
        
        if command -v pytest &> /dev/null; then
            pytest tests/ -v
            print_success "Tests ejecutados correctamente"
        else
            print_warning "pytest no disponible, saltando tests"
        fi
    fi
}

# ===== LANZAMIENTO DE LA APLICACIÓN =====
launch_application() {
    print_step "Iniciando FortiFile..."
    
    echo -e "${CYAN}"
    echo "=========================================="
    echo "🚀 Lanzando $APP_NAME"
    echo "=========================================="
    echo -e "${NC}"
    
    # Cambiar al directorio del proyecto
    cd "$PROJECT_DIR"
    
    # Ejecutar la aplicación frontend (GUI principal)
    print_step "Ejecutando interfaz gráfica..."
    python3 "$FRONTEND_APP"
}

# ===== FUNCIÓN DE AYUDA =====
show_help() {
    echo "Uso: $0 [opciones]"
    echo ""
    echo "Opciones:"
    echo "  --help, -h          Mostrar esta ayuda"
    echo "  --version, -v       Mostrar versión"
    echo "  --test              Ejecutar tests antes de lanzar"
    echo "  --no-venv           No usar entorno virtual"
    echo "  --backend-only      Solo ejecutar backend"
    echo "  --check-only        Solo verificar dependencias"
    echo ""
    echo "Ejemplos:"
    echo "  $0                  Ejecutar aplicación normalmente"
    echo "  $0 --test          Ejecutar con tests"
    echo "  $0 --check-only    Solo verificar sistema"
}

# ===== FUNCIÓN PRINCIPAL =====
main() {
    # Parsear argumentos
    USE_VENV=true
    RUN_TESTS=false
    BACKEND_ONLY=false
    CHECK_ONLY=false
    
    for arg in "$@"; do
        case $arg in
            --help|-h)
                show_help
                exit 0
                ;;
            --version|-v)
                echo "$APP_NAME versión $APP_VERSION"
                exit 0
                ;;
            --test)
                RUN_TESTS=true
                ;;
            --no-venv)
                USE_VENV=false
                ;;
            --backend-only)
                BACKEND_ONLY=true
                ;;
            --check-only)
                CHECK_ONLY=true
                ;;
            *)
                print_error "Opción desconocida: $arg"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Mostrar banner
    print_banner
    
    # Ejecutar verificaciones
    check_os
    check_python
    check_pip
    check_system_tools
    check_gui_dependencies
    
    if [ "$USE_VENV" = "true" ]; then
        setup_virtual_environment
    fi
    
    install_dependencies
    check_critical_files
    check_database
    check_config_files
    
    if [ "$CHECK_ONLY" = "true" ]; then
        print_success "Todas las verificaciones completadas exitosamente"
        exit 0
    fi
    
    run_tests
    
    # Lanzar aplicación
    if [ "$BACKEND_ONLY" = "true" ]; then
        print_step "Ejecutando solo backend..."
        python3 "$BACKEND_APP"
    else
        launch_application
    fi
}

# ===== MANEJO DE ERRORES =====
trap 'print_error "Script interrumpido"; exit 1' INT TERM

# ===== EJECUTAR FUNCIÓN PRINCIPAL =====
main "$@"
