#!/bin/bash

# FortiFile - Script de acceso rápido
# Este script permite ejecutar FortiFile desde el directorio raíz del proyecto

# Ejecutar el script principal desde la carpeta scripts
exec bash "$(dirname "${BASH_SOURCE[0]}")/scripts/run_fortifile.sh" "$@"
