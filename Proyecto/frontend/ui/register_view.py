from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import os
import sys

# Agregar el directorio del proyecto al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from themes import colors, fonts
from backend.services.user_service import UserService


class RegisterView(QWidget):
    """
    Vista de registro para FortiFile.
    """
    def __init__(self, on_register_success, on_login_clicked=None):
        super().__init__()
        self.on_register_success = on_register_success
        self.on_login_clicked = on_login_clicked
        self.user_service = UserService()  # Inicializar el servicio de usuario
        self.setWindowTitle("FortiFile - Registro")
        self.setMinimumSize(500, 400)
        self.set_icon()
        self.setup_ui()

    def set_icon(self):
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.png'))
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

        title_label = QLabel("REGISTRO")
        title_label.setFont(QFont(fonts.TITLE_FONT, 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"color: {getattr(colors, 'ERROR', '#FF5555')}; font-size: 11px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.textChanged.connect(self.hide_error)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña (8+ caracteres, 1 mayúscula, 1 minúscula)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.hide_error)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar contraseña")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.textChanged.connect(self.hide_error)

        register_button = QPushButton("Registrarse")
        register_button.clicked.connect(self.on_register_clicked)

        login_button = QPushButton("¿Ya tienes cuenta? Inicia Sesión")
        login_button.setFlat(True)
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.setStyleSheet(f"""
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
        login_button.clicked.connect(self.handle_login_clicked)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.addWidget(title_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.error_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addWidget(register_button)
        form_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        outer_layout = QVBoxLayout()
        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        outer_layout.addLayout(form_layout)
        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        outer_layout.setContentsMargins(100, 40, 100, 40)

        self.setLayout(outer_layout)
        self.username_input.setFocus()

    def hide_error(self):
        self.error_label.hide()

    def on_register_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validaciones básicas
        if not username or not password or not confirm_password:
            self.error_label.setText("Por favor, completa todos los campos.")
            self.error_label.show()
            return
            
        if password != confirm_password:
            self.error_label.setText("Las contraseñas no coinciden.")
            self.error_label.show()
            return
        
        # Validaciones de complejidad de contraseña
        if len(password) < 8:
            self.error_label.setText("La contraseña debe tener al menos 8 caracteres.")
            self.error_label.show()
            return
        
        if not any(c.isupper() for c in password):
            self.error_label.setText("La contraseña debe contener al menos una letra mayúscula.")
            self.error_label.show()
            return
        
        if not any(c.islower() for c in password):
            self.error_label.setText("La contraseña debe contener al menos una letra minúscula.")
            self.error_label.show()
            return
            
        # Registrar usuario usando el servicio
        result = self.user_service.register_user(username, password)
        
        if result["success"]:
            self.error_label.setText("")
            self.error_label.hide()
            # Limpiar campos
            self.username_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()
            
            if callable(self.on_register_success):
                self.on_register_success()
        else:
            self.error_label.setText(result["message"])
            self.error_label.show()

    def handle_login_clicked(self):
        if callable(self.on_login_clicked):
            self.on_login_clicked()
