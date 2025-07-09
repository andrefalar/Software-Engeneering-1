import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget

from ui.login_view import LoginView
from ui.start_view import StartView
from ui.register_view import RegisterView

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121111;")  # Este es colors.DARKEST
        self.setWindowTitle("FortiFile")
        self.setFixedSize(500, 400)

        # Crear vistas con funciones de navegación
        self.start_view = StartView(self.show_login_view)
        self.login_view = LoginView(
            go_to_register=self.show_register_view
        )
        self.register_view = RegisterView(
            go_to_login=self.show_login_view
        )

        # Añadir vistas al stack
        self.addWidget(self.start_view)
        self.addWidget(self.login_view)
        self.addWidget(self.register_view)

        # Mostrar vista inicial
        self.setCurrentWidget(self.start_view)

    def show_login_view(self):
        self.setCurrentWidget(self.login_view)

    def show_register_view(self):
        self.setCurrentWidget(self.register_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
