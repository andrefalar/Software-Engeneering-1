from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import os

from themes import colors, fonts


class RegisterView(QWidget):
    def __init__(self, go_to_login):
        super().__init__()
        self.setAutoFillBackground(True)
        self.go_to_login = go_to_login
        self.setWindowTitle("FortiFile - Registro")
        self.setMinimumSize(500, 400)
        self.set_icon()
        self.setup_ui()

    def set_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.png')
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

        title_label = QLabel("REGISTRO")
        title_label.setFont(QFont(fonts.TITLE_FONT, 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar contraseña")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        login_link_button = QPushButton("¿Ya tienes cuenta? Iniciar sesión")
        login_link_button.setFlat(True)
        login_link_button.setCursor(Qt.PointingHandCursor)
        login_link_button.clicked.connect(self.go_to_login)
        login_link_button.setStyleSheet(f"""
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

        register_button = QPushButton("Registrarse")
        register_button.clicked.connect(self.on_register_clicked)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.addWidget(title_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addWidget(register_button)
        form_layout.addWidget(login_link_button, alignment=Qt.AlignCenter)

        outer_layout = QVBoxLayout()
        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        outer_layout.addLayout(form_layout)
        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        outer_layout.setContentsMargins(100, 40, 100, 40)

        self.setLayout(outer_layout)

    def on_register_clicked(self):
        print("Registro (sin funcionalidad backend por ahora)")
