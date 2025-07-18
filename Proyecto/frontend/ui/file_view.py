import sys
import os
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QListWidget,
    QVBoxLayout, QHBoxLayout, QListWidgetItem, QTextEdit, QFileDialog, QMessageBox,
    QComboBox, QDialog, QDialogButtonBox, QFrame
)
from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap, QPalette, QBrush, QPainter
from PyQt5.QtCore import Qt, QDateTime

# Agregar el directorio del proyecto al path para poder importar backend
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from themes import colors, fonts
from ui.account_view import AccountWindow
from backend.services.file_service import FileService

IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]

# Diccionario para mostrar el nombre completo del tipo de archivo
FILE_TYPE_NAMES = {
    "png": "Imagen PNG",
    "jpg": "Imagen JPG",
    "jpeg": "Imagen JPEG",
    "bmp": "Imagen BMP",
    "gif": "Imagen GIF",
    "pdf": "Documento PDF",
    "doc": "Documento Word",
    "docx": "Documento Word",
    "xls": "Hoja de cálculo Excel",
    "xlsx": "Hoja de cálculo Excel",
    "txt": "Archivo de texto",
    "csv": "Archivo CSV",
    "ppt": "Presentación PowerPoint",
    "pptx": "Presentación PowerPoint",
    "zip": "Archivo comprimido ZIP",
    "rar": "Archivo comprimido RAR",
    "mp3": "Audio MP3",
    "wav": "Audio WAV",
    "mp4": "Video MP4",
    "avi": "Video AVI",
    "exe": "Ejecutable",
    "": "Desconocido"
}

class FilterDialog(QDialog):
    """Diálogo para seleccionar filtro de archivos."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {colors.DARKEST}; color: {colors.WHITE};")
        self.setWindowTitle("Seleccionar Filtro")
        layout = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems(["Nombre", "Tipo", "Fecha (Recientes primero)", "Fecha (Antiguos primero)"])
        self.combo.setStyleSheet(f"background-color: {colors.LIGHT}; color: {colors.WHITE}; padding: 5px")
        layout.addWidget(self.combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def selected_option(self):
        return self.combo.currentText()

class FileManagerUI(QMainWindow):
    """Interfaz principal para gestión de archivos."""
    def __init__(self, on_logout=None, go_to_start=None, user_id=None):
        super().__init__()
        self.on_logout = on_logout
        self.go_to_start = go_to_start
        self.user_id = user_id  # ID del usuario actual
        self.file_service = FileService()  # Inicializar el servicio de archivos
        self.setWindowTitle("FortiFile")
        self.resize(900, 500)

        base_path = os.path.dirname(os.path.abspath(__file__))

        self.setAutoFillBackground(True)
        palette = QPalette()
        fondo_base_path = os.path.join(base_path, "logos", "Design sem nome.png")
        fondo_superior_path = os.path.join(base_path, "logos", "QComb.png")
        fondo_base = QPixmap(fondo_base_path) if os.path.exists(fondo_base_path) else QPixmap()
        fondo_superior = QPixmap(fondo_superior_path) if os.path.exists(fondo_superior_path) else QPixmap()

        fondo_combinado = QPixmap(fondo_base.size())
        fondo_combinado.fill(Qt.transparent)

        painter = QPainter(fondo_combinado)
        painter.drawPixmap(0, 0, fondo_base)
        painter.drawPixmap(0, 0, fondo_superior)
        painter.end()

        palette.setBrush(QPalette.Window, QBrush(fondo_combinado))
        self.setPalette(palette)

        self.files_data = []
        self.current_filter = "Nombre"

        main_widget = QWidget()
        outer_layout = QVBoxLayout(main_widget)

        header_widget = QWidget()
        header_widget.setStyleSheet(f"background-color: {colors.DARK};")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)

        logo_label = QLabel()
        logo_path = os.path.join(base_path, "logos", "oso_logotipo.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        title_label = QLabel("FortiFile")
        title_label.setStyleSheet(f"color: {colors.WHITE}; font-size: 24px; font-weight: bold")
        title_label.setFont(QFont(fonts.TITLE_FONT, 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignVCenter)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        link_style = f"""
            QLabel {{
                color: {colors.WHITE};
                font-size: 14px;
                text-decoration: underline;
                padding: 0 10px;
            }}
            QLabel:hover {{
                color: {colors.LIGHT};
            }}
        """

        self.link_inicio = QLabel("Inicio")
        self.link_inicio.setStyleSheet(link_style)
        self.link_inicio.setCursor(QCursor(Qt.PointingHandCursor))
        self.link_inicio.mousePressEvent = self.confirm_logout

        self.link_cuenta = QLabel("Cuenta")
        self.link_cuenta.setStyleSheet(link_style)
        self.link_cuenta.setCursor(QCursor(Qt.PointingHandCursor))
        self.link_cuenta.mousePressEvent = self.confirm_account_details

        links_layout = QHBoxLayout()
        links_layout.setContentsMargins(0, 0, 10, 0)
        links_layout.addWidget(self.link_inicio)
        links_layout.addWidget(self.link_cuenta)

        links_widget = QWidget()
        links_widget.setLayout(links_layout)
        header_layout.addWidget(links_widget)

        container = QFrame()
        container.setStyleSheet(f"background-color: {colors.DARKEST}; border-radius: 10px;")
        container.setFixedSize(820, 420)
        container_layout = QHBoxLayout(container)

        left_panel = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar archivo...")
        self.search_bar.setStyleSheet(f"background-color: {colors.LIGHT}; color: {colors.WHITE}; padding: 5px")
        self.search_bar.textChanged.connect(self.refresh_file_list)

        self.filter_button = QPushButton("Filtro")
        self.filter_button.setStyleSheet(self.get_button_style())
        self.filter_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.filter_button.setToolTip("Filtrar archivos")
        self.filter_button.clicked.connect(self.show_filter_dialog)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.filter_button)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet(f"background-color: {colors.DARK}; color: {colors.WHITE}")
        self.file_list.itemClicked.connect(self.show_file_details)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Agregar")
        self.delete_button = QPushButton("Eliminar")
        self.download_button = QPushButton("Descargar")

        for btn in [self.add_button, self.delete_button, self.download_button]:
            btn.setStyleSheet(self.get_button_style())
            btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.add_button.clicked.connect(self.add_file)
        self.delete_button.clicked.connect(self.delete_checked_files)
        self.download_button.clicked.connect(self.download_checked_files)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.download_button)

        left_panel.addLayout(search_layout)
        left_panel.addWidget(self.file_list)
        left_panel.addLayout(button_layout)

        right_panel = QVBoxLayout()

        self.file_info_title = QLabel("Detalles del Archivo")
        self.file_info_title.setAlignment(Qt.AlignCenter)
        self.file_info_title.setStyleSheet(f"""
            background-color: {colors.GRAY};
            color: {colors.WHITE};
            padding: 8px;
            font-weight: bold;
            font-size: 16px;
            border-bottom: 1px solid {colors.GRAY_LIGHT};
        """)

        self.file_info_text = QTextEdit()
        self.file_info_text.setReadOnly(True)
        self.file_info_text.setStyleSheet(f"""
            background-color: {colors.DARK};
            color: {colors.WHITE};
            font-size: 14px;
            border-radius: 6px;
            padding: 10px;
        """)

        self.preview_label = QLabel()
        self.preview_label.setFixedHeight(140)
        self.preview_label.setStyleSheet("border: 1px solid #333; background-color: #222;")
        self.preview_label.setAlignment(Qt.AlignCenter)

        right_panel.addWidget(self.file_info_title)
        right_panel.addWidget(self.file_info_text)
        right_panel.addWidget(self.preview_label)

        container_layout.addLayout(left_panel, 2)
        container_layout.addLayout(right_panel, 1)

        outer_layout.addWidget(header_widget)
        outer_layout.addSpacing(10)
        outer_layout.addWidget(container, alignment=Qt.AlignCenter)
        outer_layout.addStretch()

        self.setCentralWidget(main_widget)
        
        # Cargar archivos del usuario al inicializar
        self.load_user_files()

    def load_user_files(self):
        """Carga los archivos del usuario desde la base de datos."""
        if not self.user_id:
            print("❌ No hay usuario logueado")
            return
        
        try:
            result = self.file_service.get_user_files(self.user_id)
            
            if result["success"]:
                self.files_data = []
                self.file_list.clear()
                
                for file_info in result["files"]:
                    # Convertir información del backend al formato esperado por la UI
                    file_data = {
                        "id": file_info["id"],
                        "name": file_info["nombre"],
                        "path": "",  # No necesitamos la ruta cifrada en la UI
                        "type": self._get_file_extension(file_info["nombre"]),
                        "size": int(file_info["size_mb"] * 1024 * 1024) if file_info["size_mb"] else 0,  # Convertir MB a bytes
                        "date": file_info["fecha_subida"].strftime("%d/%m/%Y %H:%M") if file_info["fecha_subida"] else "Desconocida"
                    }
                    
                    self.files_data.append(file_data)
                    
                    # Agregar a la lista visual
                    item = QListWidgetItem(file_data["name"])
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    item.setCheckState(Qt.Unchecked)
                    self.file_list.addItem(item)
                
                print(f"✅ Cargados {result['count']} archivos del usuario")
            else:
                print(f"❌ Error cargando archivos: {result.get('message', 'Error desconocido')}")
                
        except Exception as e:
            print(f"❌ Error inesperado cargando archivos: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar los archivos: {str(e)}")

    def _get_file_extension(self, filename):
        """Obtiene la extensión de un archivo."""
        ext = os.path.splitext(filename)[1].lower()
        return ext[1:] if ext else ""

    def get_button_style(self):
        """Devuelve el estilo para los botones principales."""
        return f"""
            QPushButton {{
                background-color: {colors.GRAY_DARK};
                color: {colors.WHITE};
                padding: 5px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {colors.LIGHT};
            }}
        """

    def confirm_logout(self, event):
        reply = QMessageBox.question(
            self,
            "Cerrar sesión",
            "¿Seguro que deseas salir de la cuenta?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes and callable(self.on_logout):
            self.on_logout()

    def confirm_account_details(self, event):
        self.close()
        self.account_window = AccountWindow(go_to_start=self.go_to_start)
        self.account_window.show()

    def refresh_file_list(self):
        search_text = self.search_bar.text().lower()
        self.file_list.clear()
        for file_info in self.files_data:
            if search_text in file_info["name"].lower():
                item = QListWidgetItem(file_info["name"])
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Unchecked)
                self.file_list.addItem(item)

    def show_filter_dialog(self):
        dialog = FilterDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.current_filter = dialog.selected_option()
            self.refresh_file_list()

    def show_file_details(self, item):
        # Muestra detalles y previsualiza imagen si corresponde
        file_name = item.text()
        file_info = next((f for f in self.files_data if f["name"] == file_name), None)
        if file_info:
            # Mejor estética y tipo de archivo con nombre completo y sigla
            ext = file_info["type"]
            type_full = FILE_TYPE_NAMES.get(ext, "Desconocido")
            details = (
                f"<b>Nombre:</b> {file_info['name']}<br>"
                f"<b>Tipo:</b> {type_full} ({ext})<br>"
                f"<b>Peso:</b> {file_info['size']} bytes<br>"
                f"<b>Fecha de agregado:</b> {file_info['date']}"
            )
            self.file_info_text.setHtml(details)
            ext_dot = f".{ext}"
            if ext_dot in IMAGE_EXTENSIONS and os.path.exists(file_info["path"]):
                pixmap = QPixmap(file_info["path"])
                self.preview_label.setPixmap(pixmap.scaled(
                    self.preview_label.width(), self.preview_label.height(),
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                ))
            else:
                self.preview_label.clear()
        else:
            self.file_info_text.clear()
            self.preview_label.clear()

    def add_file(self):
        """Agrega un archivo usando el backend con cifrado automático."""
        if not self.user_id:
            QMessageBox.warning(self, "Error", "No hay usuario logueado.")
            return
            
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo")
        if not file_path:
            return
        
        try:
            # Mostrar mensaje de carga
            QMessageBox.information(self, "Subiendo archivo", "Subiendo y cifrando archivo, por favor espere...")
            
            # Usar el servicio del backend para subir y cifrar el archivo
            result = self.file_service.upload_file(self.user_id, file_path)
            
            if result["success"]:
                # Archivo subido exitosamente
                QMessageBox.information(self, "Éxito", result["message"])
                
                # Recargar la lista de archivos
                self.load_user_files()
                
            else:
                # Error al subir archivo
                QMessageBox.warning(self, "Error", f"Error al subir archivo: {result['message']}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Error inesperado: {str(e)}")
            print(f"❌ Error en add_file: {e}")

    def delete_checked_files(self):
        checked = [i for i in range(self.file_list.count())
                   if self.file_list.item(i).checkState() == Qt.Checked]
        if not checked:
            QMessageBox.information(self, "Eliminar", "No hay archivos seleccionados para eliminar.")
            return
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar los archivos seleccionados?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        for i in reversed(checked):
            item = self.file_list.item(i)
            self.file_list.takeItem(i)
            self.files_data = [f for f in self.files_data if f["name"] != item.text()]

    def download_checked_files(self):
        checked_files = [self.files_data[i] for i in range(self.file_list.count())
                         if self.file_list.item(i).checkState() == Qt.Checked]
        if not checked_files:
            QMessageBox.information(self, "Descargar", "No hay archivos seleccionados para descargar.")
            return
        reply = QMessageBox.question(
            self,
            "Confirmar descarga",
            "¿Seguro que deseas descargar los archivos seleccionados?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        dest_dir = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de destino")
        if dest_dir:
            for file_info in checked_files:
                src = file_info["path"]
                dst = os.path.join(dest_dir, file_info["name"])
                try:
                    with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                        fdst.write(fsrc.read())
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo copiar {file_info['name']}: {e}")
            QMessageBox.information(self, "Descargar", "Archivos descargados exitosamente.")