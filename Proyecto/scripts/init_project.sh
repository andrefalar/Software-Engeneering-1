#!/bin/bash

# FortiFile - Script de Inicialización
# Para configurar el proyecto por primera vez

set -e

# Configuración
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"  # Subir un nivel ya que estamos en scripts/
VENV_DIR="$PROJECT_DIR/venv"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_banner() {
    echo -e "${PURPLE}"
    echo "============================================"
    echo "🔐 FortiFile - Inicialización del Proyecto"
    echo "============================================"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[INIT]${NC} $1"
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

main() {
    print_banner
    
    print_step "Inicializando proyecto FortiFile..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado. Instala Python 3.8+ primero."
        exit 1
    fi
    
    print_success "Python $(python3 --version | cut -d' ' -f2) encontrado"
    
    # Crear entorno virtual si no existe
    if [ ! -d "$VENV_DIR" ]; then
        print_step "Creando entorno virtual..."
        python3 -m venv "$VENV_DIR"
        print_success "Entorno virtual creado"
    else
        print_warning "Entorno virtual ya existe"
    fi
    
    # Activar entorno virtual
    print_step "Activando entorno virtual..."
    source "$VENV_DIR/bin/activate"
    
    # Actualizar pip
    print_step "Actualizando pip..."
    pip install --upgrade pip
    
    # Instalar dependencias
    print_step "Instalando dependencias del proyecto..."
    pip install -r requirements.txt
    
    # Crear directorios necesarios si no existen
    print_step "Verificando estructura de directorios..."
    mkdir -p secure_files
    mkdir -p logs
    
    # Generar clave de cifrado si no existe
    if [ ! -f "fortifile.key" ]; then
        print_step "Generando clave de cifrado..."
        python3 -c "
from cryptography.fernet import Fernet
key = Fernet.generate_key()
with open('fortifile.key', 'wb') as f:
    f.write(key)
print('Clave de cifrado generada')
"
        print_success "Clave de cifrado creada"
    else
        print_warning "Clave de cifrado ya existe"
    fi
    
    # Inicializar base de datos
    print_step "Inicializando base de datos..."
    python3 -c "
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.database.connection import DatabaseConnection
from backend.models.base import Base

# Crear todas las tablas
db = DatabaseConnection()
engine = db.get_engine()
Base.metadata.create_all(engine)
print('Base de datos inicializada')
"
    print_success "Base de datos inicializada"
    
    # Establecer permisos seguros
    print_step "Configurando permisos de seguridad..."
    chmod 600 fortifile.key
    chmod 700 secure_files/
    
    print_success "Permisos configurados"
    
    # Mensaje final
    echo ""
    echo -e "${GREEN}🎉 Inicialización completada exitosamente!${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. Ejecuta la aplicación: ./run_fortifile.sh"
    echo "2. O usa el modo desarrollo: ./dev_run.sh"
    echo "3. Ejecuta los tests: ./run_fortifile.sh --test"
    echo ""
    echo "¡FortiFile está listo para usar! 🔐"
}

# Manejar interrupciones
trap 'print_error "Inicialización interrumpida"; exit 1' INT TERM

# Ejecutar
main "$@"
