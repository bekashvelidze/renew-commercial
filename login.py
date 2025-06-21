import sys
import json
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from main_window import MainWindow
from create_db_backup import create_backup


def get_version():
    with open("version.json", "r") as file:
        version = json.load(file)

    return version["version"]


def main_window():
    mainwindow = MainWindow()
    widget.addWidget(mainwindow)
    widget.setWindowTitle(f'მრავალპროფილური ესთეტიკური მედიცინის ცენტრი "რენიუ" - {get_version()}')
    widget.setFixedWidth(1000)
    widget.setFixedHeight(560)
    x = (mainwindow.screen().geometry().width() // 2) - (widget.width() // 2)
    y = (mainwindow.screen().geometry().height() // 2) - (widget.height() // 2)
    widget.move(x, y)
    widget.setCurrentIndex(widget.currentIndex() + 1)


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('ui/login.ui', self)
        self.login_button.clicked.connect(self.authorize)
        self.version.setText(f"ვერსია: {get_version()}")
        self.database_backup.clicked.connect(create_backup)

    def authorize(self):
        with open("users.json", "r") as file:
            users = json.load(file)
        if self.username.text() != users["username"] or self.password.text() != users["password"]:
            QMessageBox.information(self, "შეცდომა!", "სახელი ან პაროლი არასწორია.")
        else:
            main_window()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.authorize()
        else:
            super().keyPressEvent(event)


app = QApplication(sys.argv)
loginwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(loginwindow)
widget.setWindowTitle('მრავალპროფილური ესთეტიკური მედიცინის ცენტრი "რენიუ"')
widget.setWindowIcon(QIcon("ui/renew.ico"))
widget.setFixedWidth(600)
widget.setFixedHeight(280)
widget.show()
app.exec()
