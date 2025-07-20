#!/bin/bash

# FortiFile - Script de desarrollo rápido
# Para uso durante desarrollo (sin todas las verificaciones)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"  # Subir un nivel ya que estamos en scripts/
VENV_DIR="$PROJECT_DIR/venv"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔐 FortiFile - Desarrollo Rápido${NC}"

# Activar entorno virtual si existe
if [ -d "$VENV_DIR" ]; then
    echo -e "${GREEN}Activando entorno virtual...${NC}"
    source "$VENV_DIR/bin/activate"
fi

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR"

# Ejecutar la aplicación
echo -e "${GREEN}Ejecutando FortiFile...${NC}"
python3 frontend/app.py
