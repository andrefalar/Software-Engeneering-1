from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import os

from themes import colors, fonts
from register_view import RegisterView  # Importa la vista de registro


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setWindowTitle("FortiFile")
        self.setMinimumSize(500, 400)
        self.set_icon()
        self.setup_ui()

    def set_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors.DARKEST};
                font-family: '{fonts.BODY_FONT}';
                color: {colors.WHITE};
            }}
            QLineEdit {{
                background-color: {colors.DARK};
                color: {colors.WHITE};
                border: 1px solid {colors.GRAY_LIGHT};
                border-radius: 4px;
                padding: 6px;
            }}
            QPushButton {{
                background-color: {colors.DARK};
                color: {colors.WHITE};
                border: none;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {colors.GRAY};
            }}
            QLabel {{
                font-family: '{fonts.BODY_FONT}';
            }}
        """)

        # Título
        title_label = QLabel("INGRESO")
        title_label.setFont(QFont(fonts.TITLE_FONT, 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        # Campos de entrada
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Botón tipo enlace: Recordar contraseña
        recordar_button = QPushButton("Recordar contraseña")
        recordar_button.setFlat(True)
        recordar_button.setCursor(Qt.PointingHandCursor)
        recordar_button.setStyleSheet(f"""
            QPushButton {{
                color: {colors.GRAY_LIGHT};
                background: none;
                border: none;
                font-size: 10px;
                text-align: right;
            }}
            QPushButton:hover {{
                color: {colors.GRAY};
            }}
        """)

        # Botón tipo enlace: Registrarse
        register_button = QPushButton("o Registrarse")
        register_button.setFlat(True)
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.setStyleSheet(f"""
            QPushButton {{
                color: {colors.GRAY_LIGHT};
                background: none;
                border: none;
                font-size: 10px;
            }}
            QPushButton:hover {{
                color: {colors.GRAY};
            }}
        """)
        register_button.clicked.connect(self.on_register_clicked)

        # Botón principal
        login_button = QPushButton("Ingresar")
        login_button.clicked.connect(self.on_login_clicked)

        # Layouts
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.addWidget(title_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)

        record_layout = QHBoxLayout()
        record_layout.addStretch()
        record_layout.addWidget(recordar_button)

        form_layout.addLayout(record_layout)
        form_layout.addSpacing(10)
        form_layout.addWidget(login_button)
        form_layout.addWidget(register_button, alignment=Qt.AlignCenter)

        # Espaciado interno
        outer_layout = QVBoxLayout()
        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        outer_layout.addLayout(form_layout)
        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        outer_layout.setContentsMargins(100, 40, 100, 40)

        self.setLayout(outer_layout)

    def on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        print(f"Intento de login con usuario: {username} y contraseña: {password}")

    def on_register_clicked(self):
        self.register_window = RegisterView(go_to_login=self.show_again)
        self.register_window.show()
        self.close()

    def show_again(self):
        self.show()
