import sys
from PyQt5.QtWidgets import QApplication
from ui.login_view import LoginView

def main():
    app = QApplication(sys.argv)
    login_window = LoginView()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
