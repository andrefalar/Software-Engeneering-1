# FortiFile - Sistema de Archivos Seguros
# Makefile para automatización de tareas

.PHONY: help init run dev test clean lint format check install deps

# Variables
PYTHON := python3
VENV_DIR := venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip

# Colores para output
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RED := \033[31m
NC := \033[0m

# Comando por defecto
help:
	@echo "$(BLUE)FortiFile - Sistema de Archivos Seguros$(NC)"
	@echo "=========================================="
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  $(GREEN)make init$(NC)     - Inicializar proyecto (primera vez)"
	@echo "  $(GREEN)make run$(NC)      - Ejecutar aplicación con verificaciones completas"
	@echo "  $(GREEN)make dev$(NC)      - Ejecutar en modo desarrollo (rápido)"
	@echo "  $(GREEN)make test$(NC)     - Ejecutar tests"
	@echo "  $(GREEN)make check$(NC)    - Solo verificar dependencias"
	@echo "  $(GREEN)make lint$(NC)     - Ejecutar linting (flake8, pylint)"
	@echo "  $(GREEN)make format$(NC)   - Formatear código (black, autopep8)"
	@echo "  $(GREEN)make install$(NC)  - Instalar/actualizar dependencias"
	@echo "  $(GREEN)make clean$(NC)    - Limpiar archivos temporales"
	@echo "  $(GREEN)make deps$(NC)     - Mostrar información de dependencias"
	@echo ""
	@echo "Scripts bash alternativos:"
	@echo "  ./init_project.sh  - Inicialización"
	@echo "  ./run_fortifile.sh - Ejecución principal" 
	@echo "  ./dev_run.sh       - Desarrollo rápido"

# Inicializar proyecto
init:
	@echo "$(BLUE)🔐 Inicializando FortiFile...$(NC)"
	@./init_project.sh

# Ejecutar aplicación completa
run:
	@echo "$(BLUE)🚀 Ejecutando FortiFile...$(NC)"
	@./run_fortifile.sh

# Modo desarrollo
dev:
	@echo "$(BLUE)⚡ Modo desarrollo FortiFile...$(NC)"
	@./dev_run.sh

# Solo verificar dependencias
check:
	@echo "$(BLUE)🔍 Verificando sistema...$(NC)"
	@./run_fortifile.sh --check-only

# Ejecutar tests
test:
	@echo "$(BLUE)🧪 Ejecutando tests...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		. $(VENV_DIR)/bin/activate && pytest tests/ -v; \
	else \
		pytest tests/ -v; \
	fi

# Ejecutar tests con coverage
test-coverage:
	@echo "$(BLUE)🧪 Ejecutando tests con coverage...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		. $(VENV_DIR)/bin/activate && pytest tests/ -v --cov=backend --cov=frontend; \
	else \
		pytest tests/ -v --cov=backend --cov=frontend; \
	fi

# Linting
lint:
	@echo "$(BLUE)🔍 Ejecutando linting...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		. $(VENV_DIR)/bin/activate && \
		echo "$(YELLOW)Running flake8...$(NC)" && \
		flake8 backend/ frontend/ --max-line-length=88 --extend-ignore=E203,W503 || true; \
		echo "$(YELLOW)Running pylint...$(NC)" && \
		pylint backend/ frontend/ || true; \
	else \
		echo "$(RED)Entorno virtual no encontrado. Ejecuta 'make init' primero.$(NC)"; \
	fi

# Formatear código
format:
	@echo "$(BLUE)🎨 Formateando código...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		. $(VENV_DIR)/bin/activate && \
		echo "$(YELLOW)Running black...$(NC)" && \
		black backend/ frontend/ --line-length=88; \
		echo "$(YELLOW)Running autopep8...$(NC)" && \
		autopep8 --in-place --recursive backend/ frontend/; \
		echo "$(YELLOW)Running isort...$(NC)" && \
		isort backend/ frontend/; \
	else \
		echo "$(RED)Entorno virtual no encontrado. Ejecuta 'make init' primero.$(NC)"; \
	fi

# Instalar dependencias
install:
	@echo "$(BLUE)📦 Instalando dependencias...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		. $(VENV_DIR)/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements.txt; \
	else \
		echo "$(RED)Entorno virtual no encontrado. Ejecuta 'make init' primero.$(NC)"; \
	fi

# Mostrar información de dependencias
deps:
	@echo "$(BLUE)📋 Información de dependencias:$(NC)"
	@echo ""
	@echo "$(YELLOW)Python version:$(NC)"
	@python3 --version
	@echo ""
	@echo "$(YELLOW)Pip version:$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_PIP) --version; \
	else \
		pip3 --version; \
	fi
	@echo ""
	@echo "$(YELLOW)Paquetes instalados:$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_PIP) list; \
	else \
		pip3 list; \
	fi

# Limpiar archivos temporales
clean:
	@echo "$(BLUE)🧹 Limpiando archivos temporales...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + || true
	@find . -type f -name ".coverage" -delete || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + || true
	@echo "$(GREEN)Limpieza completada$(NC)"

# Limpiar todo (incluyendo entorno virtual)
clean-all: clean
	@echo "$(BLUE)🧹 Limpieza completa...$(NC)"
	@rm -rf $(VENV_DIR)
	@rm -rf logs/
	@echo "$(GREEN)Limpieza completa finalizada$(NC)"

# Verificar estructura del proyecto
structure:
	@echo "$(BLUE)📁 Estructura del proyecto:$(NC)"
	@tree -I '__pycache__|*.pyc|venv|.git' || ls -la

# Crear release
release: clean format lint test
	@echo "$(BLUE)📦 Preparando release...$(NC)"
	@echo "$(GREEN)Release preparado exitosamente$(NC)"

# Backup del proyecto
backup:
	@echo "$(BLUE)💾 Creando backup...$(NC)"
	@tar -czf "fortifile_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz" \
		--exclude='venv' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.git' \
		.
	@echo "$(GREEN)Backup creado$(NC)"

# Verificar seguridad
security:
	@echo "$(BLUE)🔒 Verificando configuración de seguridad...$(NC)"
	@echo "$(YELLOW)Permisos de archivos críticos:$(NC)"
	@ls -la fortifile.key fortifile.db secure_files/ 2>/dev/null || echo "Algunos archivos no existen aún"
	@echo ""
	@echo "$(YELLOW)Verificando dependencias vulnerables:$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		. $(VENV_DIR)/bin/activate && \
		pip list --format=json | python3 -c "import json, sys; [print(f\"{pkg['name']}=={pkg['version']}\") for pkg in json.load(sys.stdin)]"; \
	fi

# Información del sistema
info:
	@echo "$(BLUE)ℹ️  Información del sistema:$(NC)"
	@echo "$(YELLOW)OS:$(NC) $(shell uname -s)"
	@echo "$(YELLOW)Arch:$(NC) $(shell uname -m)"
	@echo "$(YELLOW)Python:$(NC) $(shell python3 --version)"
	@echo "$(YELLOW)Proyecto:$(NC) FortiFile"
	@echo "$(YELLOW)Directorio:$(NC) $(PWD)"
	@echo "$(YELLOW)Entorno Virtual:$(NC) $(if $(wildcard $(VENV_DIR)),✅ Disponible,❌ No encontrado)"
