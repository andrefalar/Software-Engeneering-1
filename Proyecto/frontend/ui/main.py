from PyQt5.QtWidgets import QApplication
import sys
from start_view import StartView
from login_view import LoginView
from register_view import RegisterView


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.show_start_view()

    def show_start_view(self):
        self.window = StartView(go_to_login=self.show_login_view)
        self.window.show()

    def show_login_view(self):
        self.window.close()
        self.window = LoginView(go_to_register=self.show_register_view)
        self.window.show()

    def show_register_view(self):
        self.window.close()
        self.window = RegisterView(go_to_login=self.show_login_view)
        self.window.show()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
