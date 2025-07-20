from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QInputDialog,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QToolButton,
)
from PyQt5.QtGui import QPixmap, QFont, QCursor, QPalette, QBrush, QPainter
from PyQt5.QtCore import Qt
import sys
import os

PALETTE = {
    "black": "#000000",
    "dark_gray1": "#121111",
    "dark_gray2": "#253439",
    "gray1": "#4a4744",
    "gray2": "#595551",
    "light_gray": "#7c898b",
    "lighter_gray": "#a6a6a6",
    "white": "#ffffff",
}

# Ruta base para imágenes (carpeta 'logos' en el mismo directorio)
BASE_PATH = os.path.join(os.path.dirname(__file__), "logos")


def ruta_imagen(nombre):
    return os.path.join(BASE_PATH, nombre)


class ConfirmDeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirmar eliminación")
        self.setStyleSheet(
            f"background-color: {PALETTE['dark_gray2']}; color: {PALETTE['white']}; padding: 15px;"
        )

        layout = QVBoxLayout()

        logo = QLabel()
        logo_pixmap = QPixmap(ruta_imagen("oso_logotipo.png"))
        logo.setPixmap(
            logo_pixmap.scaled(140, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cambiar Contraseña")
        self.setStyleSheet(
            f"background-color: {PALETTE['dark_gray2']}; color: {PALETTE['white']}; padding: 15px;"
        )

        layout = QVBoxLayout()
        self.inputs = []

        etiquetas = ["Contraseña actual", "Nueva contraseña", "Confirmar contraseña"]
        for texto in etiquetas:
            h = QHBoxLayout()

            input_ = QLineEdit()
            input_.setEchoMode(QLineEdit.Password)
            input_.setPlaceholderText(texto)
            input_.setStyleSheet(
                f"background-color: {PALETTE['gray1']}; color: {PALETTE['white']}; padding: 5px"
            )

            toggle_btn = QToolButton()
            toggle_btn.setCheckable(True)
            toggle_btn.setText("👁️")
            toggle_btn.setStyleSheet(
                "color: white; background: transparent; font-size: 16px;"
            )
            toggle_btn.clicked.connect(
                lambda _, inp=input_, btn=toggle_btn: self.toggle_visibility(inp, btn)
            )

            input_.textChanged.connect(self.verificar_coincidencia)

            h.addWidget(input_)
            h.addWidget(toggle_btn)

            self.inputs.append(input_)
            layout.addLayout(h)

        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.setStyleSheet(
            f"background-color: {PALETTE['gray2']}; color: {PALETTE['white']}; padding: 6px"
        )
        self.boton_aceptar.clicked.connect(self.validar_contrasena)
        self.boton_aceptar.setEnabled(False)

        layout.addWidget(self.boton_aceptar)
        self.setLayout(layout)

    def toggle_visibility(self, input_field, button):
        input_field.setEchoMode(
            QLineEdit.Normal if button.isChecked() else QLineEdit.Password
        )

    def verificar_coincidencia(self):
        actual, nueva, confirmar = [i.text() for i in self.inputs]
        self.boton_aceptar.setEnabled(
            all([actual, nueva, confirmar]) and nueva == confirmar
        )

    def validar_contrasena(self):
        _, nueva, confirmar = [i.text() for i in self.inputs]
        if nueva != confirmar:
            QMessageBox.critical(self, "Error", "Las contraseñas no coinciden.")
            return
        QMessageBox.information(
            self, "Éxito", "Su contraseña ha sido cambiada con éxito."
        )
        self.accept()


class AccountWindow(QMainWindow):
    def __init__(self, nombre_usuario="[Nombre de Cuenta]"):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.setWindowTitle("Cuenta - FortiFile")
        self.resize(900, 500)

        fondo_base = QPixmap(ruta_imagen("Design sem nome.png"))
        fondo_superior = QPixmap(ruta_imagen("QComb.png"))
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
        layout = QVBoxLayout(main_widget)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(10, 5, 10, 0)
        header.setSpacing(15)

        logo = QLabel()
        logo_pixmap = QPixmap(ruta_imagen("oso_logotipo.png"))
        logo.setPixmap(
            logo_pixmap.scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        title = QLabel("FortiFile")
        title.setStyleSheet(
            f"color: {PALETTE['white']}; font-size: 20px; font-weight: bold"
        )
        title.setFont(QFont("Arial", 18))

        header.addWidget(logo)
        header.addWidget(title)
        header.addStretch()

        self.link_inicio = QLabel("Inicio")
        self.link_cuenta = QLabel("Cuenta")
        for link in [self.link_inicio, self.link_cuenta]:
            link.setStyleSheet(
                f"""
                QLabel {{
                    color: {PALETTE['white']};
                    font-size: 16px;
                    text-decoration: underline;
                    padding: 4px 10px;
                }}
                QLabel:hover {{
                    color: {PALETTE['lighter_gray']};
                }}
            """
            )
            link.setCursor(QCursor(Qt.PointingHandCursor))
            link.setAlignment(Qt.AlignVCenter)

        self.link_cuenta.mousePressEvent = lambda event: self.recargar_pagina()

        header.addWidget(self.link_inicio)
        header.addWidget(self.link_cuenta)

        layout.addLayout(header)

        # Panel central
        panel = QFrame()
        panel.setStyleSheet("background-color: #5e5955; border-radius: 10px;")
        panel.setFixedSize(600, 380)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(15)

        logo_usuario = QLabel()
        logo_usuario.setPixmap(
            logo_pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        logo_usuario.setAlignment(Qt.AlignCenter)

        self.saludo_label = QLabel(f"Hola de nuevo, {self.nombre_usuario}")
        self.saludo_label.setStyleSheet(
            "color: white; font-size: 16px; font-weight: bold;"
        )
        self.saludo_label.setAlignment(Qt.AlignCenter)

        logo_saludo_layout = QVBoxLayout()
        logo_saludo_layout.addStretch()
        logo_saludo_layout.addWidget(logo_usuario)
        logo_saludo_layout.addWidget(self.saludo_label)
        logo_saludo_layout.addStretch()

        panel_layout.addLayout(logo_saludo_layout)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(20)

        editar_btn = QPushButton("Editar Nombre")
        editar_btn.clicked.connect(self.abrir_dialogo_edicion)
        editar_btn.setStyleSheet(self.estilo_boton())
        editar_btn.setCursor(QCursor(Qt.PointingHandCursor))

        eliminar_btn = QPushButton("Eliminar Cuenta")
        eliminar_btn.clicked.connect(self.confirmar_eliminacion)
        eliminar_btn.setStyleSheet(self.estilo_boton())
        eliminar_btn.setCursor(QCursor(Qt.PointingHandCursor))

        cambiar_btn = QPushButton("Cambiar Contraseña")
        cambiar_btn.clicked.connect(self.abrir_dialogo_contrasena)
        cambiar_btn.setStyleSheet(self.estilo_boton())
        cambiar_btn.setCursor(QCursor(Qt.PointingHandCursor))

        botones_layout.addStretch()
        botones_layout.addWidget(editar_btn)
        botones_layout.addWidget(eliminar_btn)
        botones_layout.addWidget(cambiar_btn)
        botones_layout.addStretch()

        panel_layout.addStretch()
        panel_layout.addLayout(botones_layout)

        layout.addStretch()
        layout.addWidget(panel, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setCentralWidget(main_widget)

    def estilo_boton(self):
        return f"""
            QPushButton {{
                background-color: {PALETTE['dark_gray2']};
                color: {PALETTE['white']};
                padding: 6px 12px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {PALETTE['gray2']};
            }}
        """

    def abrir_dialogo_edicion(self):
        nuevo_nombre, ok = QInputDialog.getText(
            self, "Editar Nombre", "¿A qué nombre desea cambiar?"
        )
        if ok and nuevo_nombre:
            confirm = QMessageBox.question(
                self,
                "Confirmar cambio",
                f"¿Está seguro de cambiar el nombre a '{nuevo_nombre}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if confirm == QMessageBox.Yes:
                self.nombre_usuario = nuevo_nombre
                self.saludo_label.setText(f"Hola de nuevo, {self.nombre_usuario}")

    def abrir_dialogo_contrasena(self):
        dialog = PasswordChangeDialog()
        dialog.exec_()

    def confirmar_eliminacion(self):
        dialog = ConfirmDeleteDialog()
        if dialog.exec_() == QDialog.Accepted:
            segundo = QMessageBox.question(
                self,
                "Confirmación final",
                "¿Está completamente seguro de eliminar su cuenta? Esta acción no se puede deshacer.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if segundo == QMessageBox.Yes:
                QMessageBox.information(
                    self,
                    "Cuenta eliminada",
                    "Su cuenta ha sido eliminada permanentemente.",
                )
                self.close()

    def recargar_pagina(self):
        self.hide()
        self.nueva_ventana = AccountWindow(nombre_usuario=self.nombre_usuario)
        self.nueva_ventana.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AccountWindow()
    ventana.show()
    sys.exit(app.exec_())
