import sys
import json
import datetime
from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem
from PyQt6.uic import loadUi
from PyQt6 import QtGui
from main_window import MainWindow


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('ui/login.ui', self)
        self.login_button.clicked.connect(self.authorize)

    def authorize(self):
        with open("users.json", "r") as file:
            users = json.load(file)
        if self.username.text() != users["username"] or self.password.text() != users["password"]:
            QMessageBox.information(self, "შეცდომა!", "სახელი ან პაროლი არასწორია.")
        else:
            self.main_window()

    def main_window(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setWindowTitle('მრავალპროფილური ესთეტიკური მედიცინის ცენტრი "რენიუ"')
        widget.setFixedWidth(1000)
        widget.setFixedHeight(550)
        x = (mainwindow.screen().geometry().width() // 2) - (widget.width() // 2)
        y = (mainwindow.screen().geometry().height() // 2) - (widget.height() // 2)
        widget.move(x, y)
        widget.setCurrentIndex(widget.currentIndex() + 1)


app = QApplication(sys.argv)
loginwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(loginwindow)
widget.setWindowTitle('მრავალპროფილური ესთეტიკური მედიცინის ცენტრი "რენიუ"')
widget.setFixedWidth(600)
widget.setFixedHeight(300)
widget.show()
app.exec()
