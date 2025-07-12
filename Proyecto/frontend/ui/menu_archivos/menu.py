import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QListWidget,
    QVBoxLayout, QHBoxLayout, QListWidgetItem, QTextEdit, QFileDialog, QMessageBox,
    QComboBox, QDialog, QDialogButtonBox, QFrame
)
from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap, QPalette, QBrush, QPainter
from PyQt5.QtCore import Qt, QDateTime

PALETTE = {
    "black": "#000000",
    "dark_gray1": "#121111",
    "dark_gray2": "#253439",
    "gray1": "#4a4744",
    "gray2": "#595551",
    "light_gray": "#7c898b",
    "lighter_gray": "#a6a6a6",
    "white": "#ffffff"
}

IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]

class FilterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar Filtro")
        self.setStyleSheet(f"background-color: {PALETTE['dark_gray2']}; color: {PALETTE['white']}; padding: 10px")
        layout = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems(["Nombre", "Tipo", "Fecha (Recientes primero)", "Fecha (Antiguos primero)"])
        self.combo.setStyleSheet(f"background-color: {PALETTE['light_gray']}; color: {PALETTE['white']}; padding: 5px")
        layout.addWidget(self.combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def selected_option(self):
        return self.combo.currentText()

class FileManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FortiFile")
        self.resize(900, 500)

        base_path = os.path.dirname(os.path.abspath(__file__))

        self.setAutoFillBackground(True)
        palette = QPalette()
        fondo_base = QPixmap(os.path.join(base_path, "logos", "Design sem nome.png"))
        fondo_superior = QPixmap(os.path.join(base_path, "logos", "QComb.png"))

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
        header_widget.setStyleSheet(f"background-color: {PALETTE['dark_gray2']}")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)

        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join(base_path, "logos", "oso_logotipo.png"))
        logo_label.setPixmap(logo_pixmap.scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        title_label = QLabel("FortiFile")
        title_label.setStyleSheet(f"color: {PALETTE['white']}; font-size: 24px; font-weight: bold")
        title_label.setFont(QFont("Ancizar Sans", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignVCenter)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        link_style = f"""
            QLabel {{
                color: {PALETTE['white']};
                font-size: 14px;
                text-decoration: underline;
                padding: 0 10px;
            }}
            QLabel:hover {{
                color: {PALETTE['lighter_gray']};
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
        container.setStyleSheet(f"background-color: {PALETTE['dark_gray1']}; border-radius: 10px;")
        container.setFixedSize(820, 420)
        container_layout = QHBoxLayout(container)

        left_panel = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar archivo...")
        self.search_bar.setStyleSheet(f"background-color: {PALETTE['light_gray']}; color: {PALETTE['white']}; padding: 5px")
        self.search_bar.textChanged.connect(self.refresh_file_list)

        self.filter_button = QPushButton("Filtro")
        self.filter_button.setStyleSheet(self.get_button_style())
        self.filter_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.filter_button.clicked.connect(self.show_filter_dialog)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.filter_button)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet(f"background-color: {PALETTE['dark_gray2']}; color: {PALETTE['white']}")
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
        self.file_info_title.setStyleSheet(f"background-color: {PALETTE['gray1']}; color: {PALETTE['white']}; padding: 5px; font-weight: bold")

        self.file_info_text = QTextEdit()
        self.file_info_text.setReadOnly(True)
        self.file_info_text.setStyleSheet(f"background-color: {PALETTE['gray1']}; color: {PALETTE['white']}")

        self.preview_label = QLabel()
        self.preview_label.setFixedHeight(140)
        self.preview_label.setStyleSheet("border: 1px solid #333")
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

    def get_button_style(self):
        return f"""
            QPushButton {{
                background-color: {PALETTE['gray2']};
                color: {PALETTE['white']};
                padding: 5px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {PALETTE['light_gray']};
            }}
        """

    def add_file(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos")
        for file_path in files:
            if not file_path:
                continue
            file_name = os.path.basename(file_path)
            if any(f['name'] == file_name for f in self.files_data):
                continue
            file_size = os.path.getsize(file_path) // 1024
            file_ext = os.path.splitext(file_path)[-1].lower()
            file_type = file_ext.upper().replace('.', '')
            upload_time = QDateTime.currentDateTime()
            file_info = {
                "name": file_name,
                "path": file_path,
                "size": f"{file_size} KB",
                "type": file_type,
                "datetime": upload_time,
                "thumbnail": file_path if file_ext in IMAGE_EXTENSIONS else None
            }
            self.files_data.append(file_info)
        self.refresh_file_list()

    def delete_checked_files(self):
        checked_files = self.get_checked_files()
        if not checked_files:
            QMessageBox.information(self, "Aviso", "Seleccione al menos un archivo para eliminar.")
            return
        confirm = QMessageBox.question(self, "Confirmar eliminación",
                                       f"¿Está seguro de eliminar {len(checked_files)} archivo(s)? Esta acción no se puede deshacer.",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            for file in checked_files:
                self.files_data.remove(file)
            self.refresh_file_list()
            self.file_info_text.clear()
            self.file_info_title.setText("Detalles del Archivo")
            self.preview_label.clear()

    def download_checked_files(self):
        checked_files = self.get_checked_files()
        if not checked_files:
            QMessageBox.information(self, "Aviso", "Seleccione al menos un archivo para descargar.")
            return
        for file in checked_files:
            save_path, _ = QFileDialog.getSaveFileName(self, f"Guardar {file['name']}", file['name'])
            if save_path:
                try:
                    with open(file['path'], 'rb') as f_src, open(save_path, 'wb') as f_dst:
                        f_dst.write(f_src.read())
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{e}")
        QMessageBox.information(self, "Éxito", "Archivos descargados correctamente.")

    def get_checked_files(self):
        checked = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.checkState() == Qt.Checked:
                checked.append(next((f for f in self.files_data if f['name'] == item.text()), None))
        return [f for f in checked if f]

    def refresh_file_list(self):
        filter_text = self.search_bar.text().lower()
        self.file_list.clear()
        sorted_files = sorted(self.files_data, key=lambda x: x['name'].lower())
        if self.current_filter == "Tipo":
            sorted_files.sort(key=lambda x: x['type'])
        elif self.current_filter == "Fecha (Recientes primero)":
            sorted_files.sort(key=lambda x: x['datetime'], reverse=True)
        elif self.current_filter == "Fecha (Antiguos primero)":
            sorted_files.sort(key=lambda x: x['datetime'])

        for file in sorted_files:
            if filter_text in file['name'].lower():
                item = QListWidgetItem(file['name'])
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Unchecked)
                if file['thumbnail'] and os.path.exists(file['thumbnail']):
                    pixmap = QPixmap(file['thumbnail']).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    item.setIcon(QIcon(pixmap))
                self.file_list.addItem(item)

    def show_file_details(self, item):
        file_name = item.text()
        file = next((f for f in self.files_data if f['name'] == file_name), None)
        if not file:
            return

        self.file_info_title.setText(file['name'])
        self.file_info_text.setText(f"""
Tipo:
{file['type']}

Peso:
{file['size']}

Fecha de Subida:
{file['datetime'].date().toString('dd de MMMM de yyyy')}

Hora de Subida:
{file['datetime'].time().toString('hh:mm AP')}
""")

        if file['thumbnail'] and os.path.exists(file['thumbnail']):
            pixmap = QPixmap(file['thumbnail']).scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_label.setPixmap(pixmap)
        else:
            self.preview_label.clear()

    def show_filter_dialog(self):
        dialog = FilterDialog()
        if dialog.exec_():
            self.current_filter = dialog.selected_option()
            self.refresh_file_list()

    def confirm_logout(self, event):
        confirm = QMessageBox.question(self, "Confirmar salida", "¿Desea cerrar sesión?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            QMessageBox.information(self, "Sesión cerrada", "Ha salido de su cuenta.")
            self.close()

    def confirm_account_details(self, event):
        QMessageBox.information(self, "Cuenta", "Aquí se mostrarían los detalles de su cuenta.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileManagerUI()
    window.show()
    sys.exit(app.exec_())
