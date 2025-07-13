from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QInputDialog, QMessageBox, QDialog, QDialogButtonBox,
    QLineEdit, QToolButton
)
from PyQt5.QtGui import QPixmap, QFont, QCursor, QPalette, QBrush, QPainter
from PyQt5.QtCore import Qt
import sys
import os
from themes import colors, fonts

ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

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

BASE_PATH = os.path.join(os.path.dirname(__file__), "logos")

def ruta_imagen(nombre):
    return os.path.join(BASE_PATH, nombre)

class ConfirmDeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirmar eliminación")
        self.setStyleSheet(f"background-color: {PALETTE['dark_gray2']}; color: {PALETTE['white']}; padding: 15px;")

        layout = QVBoxLayout()

        logo = QLabel()
        logo_pixmap = QPixmap(ruta_imagen("oso_logotipo.png"))
        logo.setPixmap(logo_pixmap.scaled(140, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        texto = QLabel(
            "¡Atención! Si elimina su cuenta, perderá toda la información guardada sin posibilidad de recuperarla.\n\n"
            "Esto se debe a que FortiFile está en desarrollo y, por políticas de seguridad, los datos no se almacenan permanentemente."
        )
        texto.setWordWrap(True)
        texto.setAlignment(Qt.AlignCenter)
        texto.setStyleSheet("font-size: 18px")
        layout.addWidget(texto)

        buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        buttons.button(QDialogButtonBox.Yes).setText("Sí, eliminar")
        buttons.button(QDialogButtonBox.No).setText("No, cancelar")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

class PasswordChangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modificar Contraseña")
        self.setFixedSize(370, 220)
        self.setStyleSheet("background-color: #595551; color: white; font-size: 15px;")
        layout = QVBoxLayout(self)
        etiquetas = ["Contraseña actual", "Nueva contraseña", "Confirmar contraseña"]
        self.inputs = []
        for texto in etiquetas:
            input_ = QLineEdit()
            input_.setEchoMode(QLineEdit.Password)
            input_.setPlaceholderText(texto)
            input_.setStyleSheet("background-color: #333; color: white; padding: 6px; font-size: 15px; border-radius: 4px;")
            layout.addWidget(input_)
            self.inputs.append(input_)
        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.setStyleSheet("background-color: #222; color: white; padding: 8px; font-size: 15px; border-radius: 4px;")
        self.boton_aceptar.clicked.connect(self.validar_contrasena)
        self.boton_aceptar.setEnabled(False)
        layout.addWidget(self.boton_aceptar)
        for input_ in self.inputs:
            input_.textChanged.connect(self.verificar_coincidencia)
        self.setLayout(layout)

    def verificar_coincidencia(self):
        actual, nueva, confirmar = [i.text() for i in self.inputs]
        self.boton_aceptar.setEnabled(all([actual, nueva, confirmar]) and nueva == confirmar)

    def validar_contrasena(self):
        _, nueva, confirmar = [i.text() for i in self.inputs]
        if nueva != confirmar:
            QMessageBox.critical(self, "Error", "Las contraseñas no coinciden.")
            return
        QMessageBox.information(self, "Éxito", "Su contraseña ha sido cambiada con éxito.")
        self.accept()

class AccountWindow(QMainWindow):
    def __init__(self, nombre_usuario="[Nombre de Cuenta]", go_to_start=None):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.go_to_start = go_to_start
        self.setWindowTitle("Cuenta - FortiFile")
        self.resize(900, 500)

        # Fondo igual a file_view
        fondo_base = QPixmap(os.path.join(os.path.dirname(__file__), "logos", "Design sem nome.png"))
        fondo_superior = QPixmap(os.path.join(os.path.dirname(__file__), "logos", "QComb.png"))
        fondo_combinado = QPixmap(fondo_base.size())
        fondo_combinado.fill(Qt.transparent)
        painter = QPainter(fondo_combinado)
        painter.drawPixmap(0, 0, fondo_base)
        painter.drawPixmap(0, 0, fondo_superior)
        painter.end()
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(fondo_combinado))
        self.setPalette(palette)

        main_widget = QWidget()
        main_widget.setStyleSheet(f"background-color: {colors.DARKEST};")
        outer_layout = QVBoxLayout(main_widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_widget = QWidget()
        header_widget.setStyleSheet(f"background-color: {colors.DARK};")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)

        # Título FortiFile arriba a la izquierda
        title_label = QLabel("FortiFile")
        title_label.setStyleSheet(f"color: {colors.WHITE}; font-size: 24px; font-weight: bold")
        title_label.setFont(QFont(fonts.TITLE_FONT, 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        header_layout.addWidget(title_label, alignment=Qt.AlignLeft)

        header_layout.addStretch()

        # Botón Inicio arriba a la derecha
        self.link_inicio = QLabel("Inicio")
        self.link_inicio.setStyleSheet(f"""
            color: {colors.WHITE};
            font-size: 15px;
            text-decoration: underline;
            padding: 0 10px;
        """)
        self.link_inicio.setCursor(QCursor(Qt.PointingHandCursor))
        self.link_inicio.mousePressEvent = self.volver_inicio
        header_layout.addWidget(self.link_inicio, alignment=Qt.AlignRight)

        outer_layout.addWidget(header_widget)

        # Contenedor central
        container = QFrame()
        container.setStyleSheet(f"background-color: {colors.GRAY}; border-radius: 10px;")
        container.setFixedSize(540, 400)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(25)

        # Logo FortiFile
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(logo_label)

        # Saludo formal
        self.saludo_label = QLabel(f"Bienvenido/a, <b>{self.nombre_usuario}</b>")
        self.saludo_label.setStyleSheet(f"color: {colors.WHITE}; font-size: 18px; font-weight: bold;")
        self.saludo_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.saludo_label)

        # Botones de gestión
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(20)

        editar_btn = QPushButton("Modificar Nombre")
        editar_btn.setMinimumWidth(160)
        editar_btn.setMinimumHeight(40)
        editar_btn.setStyleSheet(self.estilo_boton())
        editar_btn.setCursor(QCursor(Qt.PointingHandCursor))
        editar_btn.clicked.connect(self.abrir_dialogo_edicion)

        eliminar_btn = QPushButton("Eliminar Cuenta")
        eliminar_btn.setMinimumWidth(160)
        eliminar_btn.setMinimumHeight(40)
        eliminar_btn.setStyleSheet(self.estilo_boton())
        eliminar_btn.setCursor(QCursor(Qt.PointingHandCursor))
        eliminar_btn.clicked.connect(self.confirmar_eliminacion)

        cambiar_btn = QPushButton("Modificar Contraseña")
        cambiar_btn.setMinimumWidth(160)
        cambiar_btn.setMinimumHeight(40)
        cambiar_btn.setStyleSheet(self.estilo_boton())
        cambiar_btn.setCursor(QCursor(Qt.PointingHandCursor))
        cambiar_btn.clicked.connect(self.abrir_dialogo_contrasena)

        botones_layout.addWidget(editar_btn)
        botones_layout.addWidget(eliminar_btn)
        botones_layout.addWidget(cambiar_btn)
        container_layout.addLayout(botones_layout)

        outer_layout.addStretch()
        outer_layout.addWidget(container, alignment=Qt.AlignCenter)
        outer_layout.addStretch()

        self.setCentralWidget(main_widget)

    def estilo_boton(self):
        return f"""
            QPushButton {{
                background-color: {colors.GRAY_DARK};
                color: {colors.WHITE};
                padding: 10px 18px;
                border-radius: 6px;
                font-size: 15px;
                min-width: 160px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {colors.LIGHT};
            }}
        """

    def abrir_dialogo_edicion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Modificar Nombre")
        dialog.setFixedSize(350, 180)
        dialog.setStyleSheet(f"background-color: {colors.GRAY}; color: {colors.WHITE}; font-size: 15px;")
        layout = QVBoxLayout(dialog)
        label = QLabel("¿A qué nombre desea cambiar?")
        label.setStyleSheet("font-size: 16px; color: white;")
        layout.addWidget(label)
        input_nombre = QLineEdit()
        input_nombre.setStyleSheet("background-color: #333; color: white; padding: 6px; font-size: 15px; border-radius: 4px;")
        layout.addWidget(input_nombre)
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.button(QDialogButtonBox.Ok).setText("Aceptar")
        botones.button(QDialogButtonBox.Cancel).setText("Cancelar")
        layout.addWidget(botones)
        botones.accepted.connect(dialog.accept)
        botones.rejected.connect(dialog.reject)
        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            nuevo_nombre = input_nombre.text()
            if nuevo_nombre:
                confirm = QMessageBox(self)
                confirm.setWindowTitle("Confirmar cambio")
                confirm.setText(f"¿Está seguro de cambiar el nombre a '{nuevo_nombre}'?")
                confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirm.setStyleSheet(f"background-color: {colors.DARKEST}; color: {colors.WHITE}; font-size: 15px;")
                result = confirm.exec_()
                if result == QMessageBox.Yes:
                    self.nombre_usuario = nuevo_nombre
                    self.saludo_label.setText(f"Bienvenido/a, <b>{self.nombre_usuario}</b>")

    def abrir_dialogo_contrasena(self):
        dialog = PasswordChangeDialog(self)
        dialog.exec_()

    def confirmar_eliminacion(self):
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Eliminar Cuenta")
        confirm.setText("¿Está seguro que desea eliminar su cuenta? Esta acción no se puede deshacer.")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setStyleSheet(f"background-color: {colors.DARKEST}; color: {colors.WHITE}; font-size: 15px;")
        result = confirm.exec_()
        if result == QMessageBox.Yes:
            QMessageBox.information(self, "Cuenta eliminada", "Su cuenta ha sido eliminada permanentemente.")
            self.close()

    def volver_inicio(self, event):
        if self.go_to_start:
            self.close()
            self.go_to_start()
