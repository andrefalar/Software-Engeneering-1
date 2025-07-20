
<p align="center">
  <img src="https://github.com/user-attachments/assets/df009338-ea3e-4e99-bbd7-bb4e2b44d965" width="300" alt="FortiFile Logo"><br>
</p>

<h1 align="center">
  <strong><span style="color:#002147">FORTIFILE</span></strong>
</h1>

# Software Engineering 1 - 2025-1

**Grupo #2 - Equipo #8**

## 👥 Integrantes del equipo

* Andrés Felipe Alarcón Pulido - [analarconp@unal.edu.co](mailto:analarconp@unal.edu.co)
* Juan Daniel Jossa Soliz - [jjossa@unal.edu.co](mailto:jjossa@unal.edu.co)
* Jaime Darley Angulo Tenorio - [jangulot@unal.edu.co](mailto:jangulot@unal.edu.co)
* Michel Mauricio Castañeda Braga - [micastanedab@unal.edu.co](mailto:micastanedab@unal.edu.co)

---

## 🧠 Descripción del Proyecto

**FortiFile** es una aplicación de escritorio diseñada para ofrecer un entorno **seguro, privado y organizado** para almacenar archivos sensibles. Gracias al uso de tecnologías de **cifrado**, **autenticación** robusta y una interfaz amigable con **PyQt5**, el usuario puede tener control completo sobre sus documentos confidenciales.

> El objetivo de FortiFile es brindar una solución segura pero simple para usuarios que desean proteger su información sin complejidad técnica.

---

## 🛠️ Tecnologías Principales

| Componente     | Tecnología                          |
| -------------- | ----------------------------------- |
| Lenguaje       | Python 3.8+                         |
| GUI            | PyQt5                               |
| Seguridad      | `cryptography`, `bcrypt`, `hashlib` |
| Base de Datos  | SQLite                              |
| Pruebas        | `pytest`, `unittest`                |
| Estilo Código  | PEP8, Clean Code                    |
| Automatización | `Makefile`, Shell Scripts           |

---

## 📁 Estructura del Proyecto

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

---

## ⚡ Ejecución del Proyecto

### Opción 1: Acceso rápido desde raíz

```bash
# Ejecutar normalmente
./run.sh

# Verificar el entorno sin ejecutar
./run.sh --check-only

# Mostrar ayuda
./run.sh --help
```

### Opción 2: Uso directo desde `scripts/`

```bash
cd scripts/

# Verificación completa + ejecución
./run_fortifile.sh

# Modo test
./run_fortifile.sh --test

# Sin entorno virtual
./run_fortifile.sh --no-venv
```

### Opción 3: Automatización con Makefile

```bash
make init       # Inicializa entorno y dependencias
make run        # Ejecuta FortiFile
make dev        # Modo desarrollo
make test       # Corre pruebas
make check      # Verifica sistema
make lint       # Linter del código
make format     # Formateo automático
```

---

## 🧩 Dependencias Clave

**Backend**

* `SQLAlchemy`: ORM para interacción con la base de datos
* `bcrypt`, `cryptography`: Manejo seguro de contraseñas y cifrado

**Frontend**

* `PyQt5`: Interfaz de usuario moderna basada en Qt

**Desarrollo**

* `pytest`, `unittest`: Pruebas automáticas
* `flake8`, `black`: Linter y formateador de código

---

## 🆘 Problemas Comunes y Soluciones

| Problema            | Solución                                               |
| ------------------- | ------------------------------------------------------ |
| Python no instalado | `sudo apt install python3 python3-pip`                 |
| Qt5 no detectado    | `sudo apt install python3-pyqt5`                       |
| Sin entorno gráfico | Asegúrate de tener `$DISPLAY` en Linux o usar `ssh -X` |
| Archivos faltantes  | Ejecuta `./run.sh --check-only` para diagnosticar      |

---

## ✅ Verificación y Diagnóstico

Para verificar si todo está listo para ejecutar el proyecto:

```bash
# Diagnóstico general
./run.sh --check-only
# o
make check
```

---

## 🔒 Seguridad y Soporte

FortiFile maneja cifrado seguro, hash de contraseñas con `bcrypt`, control de acceso basado en roles y claves generadas automáticamente.

Para soporte:

1. Ejecutar los scripts con `--check-only`
2. Consultar los logs en la carpeta `logs/`
3. Revisar las dependencias del sistema y Python

---

¿Listo para comenzar? Ejecuta:

```bash
make init && make run
```

