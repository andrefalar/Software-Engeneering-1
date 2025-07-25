import sys
import os
from PyQt5.QtWidgets import QApplication, QStackedWidget

# Agregar el directorio del proyecto al path para poder importar backend
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from ui.login_view import LoginView
from ui.start_view import StartView
from ui.register_view import RegisterView
from ui.file_view import FileManagerUI  # Asegúrate que el archivo se llame así
from ui.account_view import AccountWindow


class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121111; color: white;")
        self.setWindowTitle("FortiFile")
        self.setFixedSize(900, 500)

        # Variable para almacenar información del usuario actual
        self.current_user_id = None

        self.start_view = StartView(self.show_login_view)
        self.file_view = FileManagerUI(
            on_logout=self.show_start_view, go_to_start=self.show_start_view
        )
        self.account_view = None  # Se creará cuando sea necesario
        self.login_view = LoginView(self.handle_login_success, self.show_register_view)
        self.register_view = RegisterView(self.show_login_view, self.show_login_view)

        self.addWidget(self.start_view)
        self.addWidget(self.login_view)
        self.addWidget(self.register_view)
        self.addWidget(self.file_view)

        self.setCurrentWidget(self.start_view)

    def handle_login_success(self, user_id=None):
        """Maneja el login exitoso y actualiza el user_id."""
        if user_id:
            self.current_user_id = user_id
        else:
            # Fallback: usar ID 1 (para sistemas con un solo usuario)
            self.current_user_id = 1

        try:
            # Crear nueva instancia de FileManagerUI con el user_id correcto
            new_file_view = FileManagerUI(
                on_logout=self.handle_logout,
                go_to_start=self.show_start_view,
                go_to_account=self.show_account_view,
                user_id=self.current_user_id,
            )

            # Crear nueva instancia de AccountView con el user_id correcto
            new_account_view = AccountWindow(
                user_id=self.current_user_id,
                go_to_start=self.show_file_view,
                on_logout=self.handle_logout,
            )

            # Reemplazar las vistas anteriores
            old_file_view_index = None
            old_account_view_index = None

            for i in range(self.count()):
                widget = self.widget(i)
                if isinstance(widget, FileManagerUI):
                    old_file_view_index = i
                elif isinstance(widget, AccountWindow):
                    old_account_view_index = i

            if old_file_view_index is not None:
                self.removeWidget(self.widget(old_file_view_index))
            if old_account_view_index is not None:
                self.removeWidget(self.widget(old_account_view_index))

            # Agregar las nuevas vistas
            self.file_view = new_file_view
            self.account_view = new_account_view
            self.addWidget(self.file_view)
            self.addWidget(self.account_view)

            self.show_file_view()

            print(f"✅ Login exitoso para usuario ID: {self.current_user_id}")

        except Exception as e:
            print(f"❌ Error en handle_login_success: {e}")
            self.show_file_view()  # Fallback

    def handle_logout(self):
        """Maneja el logout y limpia la información del usuario."""
        self.current_user_id = None

        # Limpiar las vistas que dependen del usuario
        if self.account_view:
            try:
                self.removeWidget(self.account_view)
                self.account_view = None
            except BaseException:
                pass

        self.show_start_view()

    def show_login_view(self):
        self.setCurrentWidget(self.login_view)

    def show_register_view(self):
        self.setCurrentWidget(self.register_view)

    def show_file_view(self):
        self.setCurrentWidget(self.file_view)

    def show_account_view(self):
        if self.account_view:
            self.setCurrentWidget(self.account_view)
        else:
            print("❌ AccountView no está disponible")

    def show_start_view(self):
        self.setCurrentWidget(self.start_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
