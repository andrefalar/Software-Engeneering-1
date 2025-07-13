import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget

from ui.login_view import LoginView
from ui.start_view import StartView
from ui.register_view import RegisterView
from ui.file_view import FileManagerUI  # Asegúrate que el archivo se llame así

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121111; color: white;")
        self.setWindowTitle("FortiFile")
        self.setFixedSize(900, 500)

        self.start_view = StartView(self.show_login_view)
        self.file_view = FileManagerUI(on_logout=self.show_start_view, go_to_start=self.show_start_view)
        self.login_view = LoginView(self.show_file_view, self.show_register_view)
        self.register_view = RegisterView(self.show_login_view, self.show_login_view)

        self.addWidget(self.start_view)
        self.addWidget(self.login_view)
        self.addWidget(self.register_view)
        self.addWidget(self.file_view)

        self.setCurrentWidget(self.start_view)

    def show_login_view(self):
        self.setCurrentWidget(self.login_view)

    def show_register_view(self):
        self.setCurrentWidget(self.register_view)

    def show_file_view(self):
        self.setCurrentWidget(self.file_view)

    def show_start_view(self):
        self.setCurrentWidget(self.start_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
