from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QInputDialog, QMessageBox, QDialog, QDialogButtonBox,
    QLineEdit, QToolButton
)
from PyQt5.QtGui import QPixmap, QFont, QCursor, QPalette, QBrush, QPainter
from PyQt5.QtCore import Qt
import sys
import os

# Agregar el directorio del proyecto al path para poder importar backend
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from themes import colors, fonts
from backend.services.user_service import UserService

class ConfirmDeleteDialog(QDialog):
    def __init__(self, user_service=None, user_id=None, parent=None):
        super().__init__(parent)
        self.user_service = user_service
        self.user_id = user_id
        self.setWindowTitle("Confirmar eliminación de cuenta")
        self.setFixedSize(450, 350)
        self.setStyleSheet(f"background-color: {colors.GRAY}; color: {colors.WHITE}; padding: 15px;")

        layout = QVBoxLayout()

        logo = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "logos", "oso_logotipo.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo.setPixmap(logo_pixmap.scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        texto = QLabel(
            "⚠️ ¡ATENCIÓN! ⚠️\n\n"
            "Si elimina su cuenta, se perderá TODA la información:\n"
            "• Todos sus archivos cifrados\n"
            "• Su cuenta de usuario\n"
            "• Todo el historial\n\n"
            "Esta acción NO se puede deshacer.\n\n"
            "Para confirmar, ingrese su contraseña:"
        )
        texto.setWordWrap(True)
        texto.setAlignment(Qt.AlignCenter)
        texto.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffeb3b;")
        layout.addWidget(texto)
        
        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Ingrese su contraseña actual")
        self.password_input.setStyleSheet(f"""
            background-color: {colors.DARK}; 
            color: {colors.WHITE}; 
            padding: 8px; 
            font-size: 14px; 
            border-radius: 4px;
            border: 2px solid #d32f2f;
        """)
        layout.addWidget(self.password_input)

        # Botones
        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors.GRAY_DARK};
                color: {colors.WHITE};
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors.LIGHT};
            }}
        """)
        cancel_button.clicked.connect(self.reject)
        
        delete_button = QPushButton("SÍ, ELIMINAR CUENTA")
        delete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #d32f2f;
                color: {colors.WHITE};
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #b71c1c;
            }}
        """)
        delete_button.clicked.connect(self.confirm_deletion)
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(delete_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
    
    def confirm_deletion(self):
        password = self.password_input.text()
        
        if not password:
            QMessageBox.critical(self, "Error", "Debe ingresar su contraseña para confirmar.")
            return
        
        if not self.user_service or not self.user_id:
            QMessageBox.critical(self, "Error", "Error del sistema: No se puede eliminar la cuenta.")
            return
        
        try:
            # Usar el servicio del backend para eliminar la cuenta
            result = self.user_service.delete_account(self.user_id, password)
            
            if result["success"]:
                QMessageBox.information(self, "Cuenta Eliminada", 
                                      f"Su cuenta ha sido eliminada permanentemente.\n\n"
                                      f"Todos sus archivos y datos han sido eliminados de forma segura.")
                self.accept()  # Cerrar el diálogo exitosamente
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la cuenta:\n{result['message']}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
            print(f"❌ Error en confirm_deletion: {e}")

class PasswordChangeDialog(QDialog):
    def __init__(self, user_id=None, user_service=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.user_service = user_service
        self.setWindowTitle("Cambiar Contraseña")
        self.setFixedSize(370, 220)
        self.setStyleSheet("background-color: #595551; color: white; font-size: 15px;")
        layout = QVBoxLayout(self)
        etiquetas = ["Contraseña actual", "Nueva contraseña (8+ caracteres, 1 mayúscula, 1 minúscula)", "Confirmar nueva contraseña"]
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
        actual, nueva, confirmar = [i.text() for i in self.inputs]
        
        # Validar que las contraseñas coincidan
        if nueva != confirmar:
            QMessageBox.critical(self, "Error", "Las contraseñas no coinciden.")
            return
        
        # Validar longitud mínima de contraseña
        if len(nueva) < 8:
            QMessageBox.critical(self, "Error", "La nueva contraseña debe tener al menos 8 caracteres.")
            return
        
        # Validar que tenga al menos una letra mayúscula
        if not any(c.isupper() for c in nueva):
            QMessageBox.critical(self, "Error", "La nueva contraseña debe contener al menos una letra mayúscula.")
            return
        
        # Validar que tenga al menos una letra minúscula
        if not any(c.islower() for c in nueva):
            QMessageBox.critical(self, "Error", "La nueva contraseña debe contener al menos una letra minúscula.")
            return
        
        # Intentar cambiar la contraseña usando el backend
        if not self.user_service or not self.user_id:
            QMessageBox.critical(self, "Error", "Error del sistema: No se puede cambiar la contraseña.")
            return
        
        try:
            # Usar el servicio del backend para cambiar la contraseña
            result = self.user_service.change_password(self.user_id, actual, nueva)
            
            if result["success"]:
                QMessageBox.information(self, "Éxito", "Su contraseña ha sido cambiada exitosamente.\n\nPor seguridad, debe iniciar sesión nuevamente.")
                self.accept()  # Cerrar el diálogo exitosamente
            else:
                QMessageBox.critical(self, "Error", f"Error al cambiar contraseña: {result['message']}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
            print(f"❌ Error en validar_contrasena: {e}")

class AccountWindow(QMainWindow):
    def __init__(self, user_id=None, go_to_start=None, on_logout=None):
        super().__init__()
        self.user_id = user_id
        self.go_to_start = go_to_start
        self.on_logout = on_logout  # Callback para cerrar sesión
        self.user_service = UserService()
        
        # Obtener información del usuario
        self.nombre_usuario = "[Usuario]"  # Valor por defecto
        if self.user_id:
            try:
                user_info = self.user_service.get_user_info(self.user_id)
                if user_info["success"]:
                    self.nombre_usuario = user_info["username"]
                    print(f"✅ Usuario cargado: {self.nombre_usuario}")
                else:
                    print(f"❌ Error cargando usuario: {user_info.get('message', 'Error desconocido')}")
            except Exception as e:
                print(f"❌ Error inesperado cargando usuario: {e}")
        
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
        botones_layout.setSpacing(30)

        cambiar_btn = QPushButton("Cambiar Contraseña")
        cambiar_btn.setMinimumWidth(180)
        cambiar_btn.setMinimumHeight(45)
        cambiar_btn.setStyleSheet(self.estilo_boton())
        cambiar_btn.setCursor(QCursor(Qt.PointingHandCursor))
        cambiar_btn.clicked.connect(self.abrir_dialogo_contrasena)

        eliminar_btn = QPushButton("Eliminar Cuenta")
        eliminar_btn.setMinimumWidth(180)
        eliminar_btn.setMinimumHeight(45)
        eliminar_btn.setStyleSheet(self.estilo_boton_eliminar())
        eliminar_btn.setCursor(QCursor(Qt.PointingHandCursor))
        eliminar_btn.clicked.connect(self.confirmar_eliminacion)

        botones_layout.addWidget(cambiar_btn)
        botones_layout.addWidget(eliminar_btn)
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
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                min-width: 180px;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {colors.LIGHT};
            }}
        """
    
    def estilo_boton_eliminar(self):
        return f"""
            QPushButton {{
                background-color: #d32f2f;
                color: {colors.WHITE};
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                min-width: 180px;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: #b71c1c;
            }}
        """

    def abrir_dialogo_contrasena(self):
        dialog = PasswordChangeDialog(
            user_id=self.user_id,
            user_service=self.user_service,
            parent=self
        )
        
        # Si el diálogo se acepta (contraseña cambiada exitosamente)
        if dialog.exec_() == QDialog.Accepted:
            # Cerrar sesión y volver al login
            QMessageBox.information(
                self, 
                "Sesión Cerrada", 
                "Su contraseña ha sido cambiada exitosamente.\n\nPor seguridad, debe iniciar sesión nuevamente."
            )
            
            # Cerrar la ventana actual y activar el callback de logout
            self.close()
            if callable(self.on_logout):
                self.on_logout()

    def confirmar_eliminacion(self):
        # Mostrar diálogo de confirmación con contraseña
        dialog = ConfirmDeleteDialog(
            user_service=self.user_service,
            user_id=self.user_id,
            parent=self
        )
        
        # Si el usuario confirma la eliminación
        if dialog.exec_() == QDialog.Accepted:
            # Mostrar mensaje final de confirmación
            QMessageBox.information(
                self, 
                "Cuenta Eliminada", 
                "Su cuenta y todos sus archivos han sido eliminados permanentemente.\n\n"
                "Será redirigido al inicio de la aplicación."
            )
            
            # Cerrar la ventana y activar el callback de logout
            self.close()
            if callable(self.on_logout):
                self.on_logout()

    def volver_inicio(self, event):
        if self.go_to_start:
            self.close()
            self.go_to_start()
