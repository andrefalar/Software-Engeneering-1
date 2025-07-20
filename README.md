
<p align="center"> <img src="https://github.com/user-attachments/assets/df009338-ea3e-4e99-bbd7-bb4e2b44d965" width="300" alt="FortiFile Logo"><br> </p> <h1 align="center"> <strong><span style="color:#002147">FORTIFILE</span></strong> </h1>

# **FORTIFILE**

## Software Engineering 1 - 2025-1

**Grupo #2 - Equipo #8**

### 👥 Integrantes del equipo

* Andrés Felipe Alarcón Pulido - [analarconp@unal.edu.co](mailto:analarconp@unal.edu.co)
* Juan Daniel Jossa Soliz - [jjossa@unal.edu.co](mailto:jjossa@unal.edu.co)
* Jaime Darley Angulo Tenorio - [jangulot@unal.edu.co](mailto:jangulot@unal.edu.co)
* Michel Mauricio Castañeda Braga - [micastanedab@unal.edu.co](mailto:micastanedab@unal.edu.co)

---

## 🧠 Descripción del Proyecto

**FortiFile** es una aplicación de escritorio diseñada para ofrecer un entorno **seguro, privado y organizado** para almacenar archivos sensibles.
Gracias al uso de tecnologías de **cifrado**, **autenticación robusta** y una interfaz amigable con **PyQt5**, el usuario puede tener control completo sobre sus documentos confidenciales.

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
| Automatización | Shell Scripts, `docs/Makefile`      |

---

## 📁 Estructura del Proyecto

```
Proyecto/
├── run.sh                    # 🚀 Script de acceso rápido (desde raíz)
├── requirements.txt          # 📜 Dependencias Python
├── .gitignore                # Ignorados por Git
├── scripts/
│   ├── run_fortifile.sh      # 🧠 Script principal con verificación
│   ├── dev_run.sh            # 🧪 Ejecución rápida para desarrollo
│   ├── init_project.sh       # 🛠️ Inicialización tras clonación
│   └── SCRIPTS_README.md     # 📄 Documentación técnica de scripts
├── config/
│   ├── pyproject.toml        # Configuración del proyecto
│   ├── pytest.ini            # Configuración de pruebas
│   ├── .flake8               # Linter
│   └── .pylintrc             # Pylint
├── docs/
│   └── Makefile              # 📦 Automatización con Make
├── frontend/
│   ├── app.py                # 🎨 Aplicación principal GUI
│   ├── assets/               # Imágenes, íconos
│   ├── themes/               # Temas de interfaz
│   └── ui/                   # Interfaces gráficas
├── backend/
│   ├── main.py               # Lógica principal
│   ├── database/             # Gestión de base de datos
│   ├── models/               # Modelos de datos
│   └── services/             # Servicios de negocio
├── tests/                    # ✅ Pruebas automáticas
├── secure_files/             # 🔐 Archivos cifrados (se crea automáticamente)
├── venv/                     # 🌐 Entorno virtual
└── .vscode/                  # Configuración de Visual Studio Code
```

---

## ⚙️ Automatización y Scripts

### 📌 Script Principal (`run_fortifile.sh`)

* Verifica dependencias y entorno
* Lanza la aplicación o corre pruebas
* Soporte para virtualenv, backend-only, etc.

```bash
./scripts/run_fortifile.sh [--help] [--test] [--no-venv] [--backend-only]
```

### ⚡ Acceso Rápido desde Raíz

```bash
./run.sh                    # Ejecutar aplicación
./run.sh --check-only       # Verificar sistema
./run.sh --test             # Ejecutar con tests
```

### 🧪 Desarrollo Rápido

```bash
./scripts/dev_run.sh        # Ejecuta sin verificación
```

### 🔧 Inicialización del Proyecto

```bash
./scripts/init_project.sh   # Crea entorno, instala dependencias y configura base de datos
```

---

## 🛠️ Uso con Make (desde raíz)

El `Makefile` se encuentra en `docs/`.

```bash
make -f docs/Makefile init      # Inicializar proyecto completo
make -f docs/Makefile run       # Ejecutar aplicación
make -f docs/Makefile dev       # Modo desarrollo
make -f docs/Makefile test      # Ejecutar tests
make -f docs/Makefile check     # Verificar dependencias
make -f docs/Makefile lint      # Verificar estilo
make -f docs/Makefile format    # Formatear código
make -f docs/Makefile security  # Revisar seguridad
```

---

## 🔧 Requisitos del Sistema

### Mínimos

* **Sistema Operativo:** Linux, macOS o Windows
* **Python:** 3.8 o superior (recomendado 3.12)
* **Entorno gráfico:** Qt5 (X11, Wayland, etc.)

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-pyqt5
```

### macOS

```bash
brew install python3
```

---

## 🧩 Dependencias Clave

**Backend**

* `SQLAlchemy 2.0.41`
* `bcrypt 4.3.0`
* `cryptography 45.0.5`

**Frontend**

* `PyQt5 5.15.11`
* `PyQt5-Qt5 5.15.17`

**Desarrollo**

* `pytest 8.4.1`
* `black 25.1.0`
* `flake8 7.3.0`

---

## 🆘 Problemas Comunes y Soluciones

| Problema            | Solución                                                          |
| ------------------- | ----------------------------------------------------------------- |
| Python no instalado | `sudo apt install python3 python3-pip`                            |
| Qt5 no detectado    | `sudo apt install python3-pyqt5`                                  |
| Sin entorno gráfico | Verifica que `$DISPLAY` esté configurado o usa `ssh -X`           |
| Archivos faltantes  | Ejecuta `./run.sh --check-only` o `run_fortifile.sh --check-only` |

---

## 🔒 Seguridad y Soporte

FortiFile aplica cifrado AES, hash seguro con `bcrypt` y control de acceso.
Cuenta con verificación automatizada de entorno y diagnósticos en línea de comandos.

### Soporte técnico

1. Ejecuta `./run.sh --check-only` o `make -f docs/Makefile check`
2. Consulta `logs/` para rastrear errores
3. Revisa dependencias del sistema y entorno virtual

---

## 🟢 Comienza ya

```bash
make -f docs/Makefile init && make -f docs/Makefile run
```

