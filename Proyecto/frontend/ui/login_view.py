from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FortiFile - Inicio de Sesión")
        self.setFixedSize(400, 250)
        self.setup_ui()

    def setup_ui(self):
        # Título
        title_label = QLabel("Iniciar Sesión")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Campos
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Botón
        login_button = QPushButton("Ingresar")
        login_button.clicked.connect(self.on_login_clicked)

        # Diseño vertical
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addSpacing(20)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(login_button)
        layout.setContentsMargins(40, 30, 40, 30)

        self.setLayout(layout)

    def on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        print(f"Intento de login con usuario: {username} y contraseña: {password}")
        # Aquí luego puedes conectar con el backend o lógica de autenticación
