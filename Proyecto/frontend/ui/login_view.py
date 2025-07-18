from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import os
import sys

# Agregar el directorio del proyecto al path para poder importar backend
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from themes import colors, fonts
from backend.services.user_service import UserService


class LoginView(QWidget):
    """
    Vista de login para FortiFile.
    """
    def __init__(self, on_login_success, on_register_clicked=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.on_register_clicked = on_register_clicked
        self.user_service = UserService()  # Inicializar el servicio de usuario
        self.setWindowTitle("FortiFile")
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

        title_label = QLabel("INGRESO")
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
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.hide_error)

        recordar_button = QPushButton("Recuperar Contraseña")
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
        recordar_button.clicked.connect(self.show_recover_message)

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
        register_button.clicked.connect(self.handle_register_clicked)

        login_button = QPushButton("Ingresar")
        login_button.clicked.connect(self.on_login_clicked)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.addWidget(title_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.error_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)

        record_layout = QHBoxLayout()
        record_layout.addStretch()
        record_layout.addWidget(recordar_button)

        form_layout.addLayout(record_layout)
        form_layout.addSpacing(10)
        form_layout.addWidget(login_button)
        form_layout.addWidget(register_button, alignment=Qt.AlignCenter)

        outer_layout = QVBoxLayout()
        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        outer_layout.addLayout(form_layout)
        outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        outer_layout.setContentsMargins(100, 40, 100, 40)

        self.setLayout(outer_layout)
        self.username_input.setFocus()

    def hide_error(self):
        self.error_label.hide()

    def on_login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # Validar que ambos campos estén llenos
        if not username or not password:
            self.error_label.setText("Por favor, ingresa usuario y contraseña.")
            self.error_label.show()
            return
        
        # Intentar autenticar con el backend
        try:
            result = self.user_service.authenticate_user(username, password)
            
            if result["success"]:
                # Login exitoso
                self.error_label.hide()
                # Limpiar campos por seguridad
                self.username_input.clear()
                self.password_input.clear()
                
                if callable(self.on_login_success):
                    # Pasar el user_id al callback
                    self.on_login_success(result.get("user_id"))
            else:
                # Login fallido
                self.error_label.setText(result["message"])
                self.error_label.show()
                
                # Si la cuenta está bloqueada, deshabilitar el formulario
                if result.get("locked", False):
                    self.username_input.setEnabled(False)
                    self.password_input.setEnabled(False)
                    # Mostrar mensaje adicional
                    QMessageBox.warning(
                        self, 
                        "Cuenta Bloqueada", 
                        "Tu cuenta ha sido bloqueada por múltiples intentos fallidos.\n"
                        "Por favor, reinicia la aplicación para intentar de nuevo."
                    )
        
        except Exception as e:
            # Error inesperado
            self.error_label.setText(f"Error de conexión: {str(e)}")
            self.error_label.show()
            print(f"Error en login: {e}")  # Para debugging

    def handle_register_clicked(self):
        if callable(self.on_register_clicked):
            self.on_register_clicked()

    def show_recover_message(self):
        QMessageBox.information(self, "Recuperar Contraseña", "Lo sentimos. La recuperación de contraseña no está implementada en esta versión.")
