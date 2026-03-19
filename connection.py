import os
import sys
import json
import mariadb
from PyQt6.QtWidgets import QApplication, QMessageBox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def critical_error(message):
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        msgbox = QMessageBox()
        msgbox.setWindowTitle("შეცდომა")
        msgbox.setText(message)
        msgbox.exec()
        sys.exit(1)

def load_database_data():
    try:
        with open(os.path.join(BASE_DIR, 'database.json'), "r") as file:
            database_data = json.load(file)

        return database_data
    except FileNotFoundError:
        critical_error("მონაცემთა ბაზის ფაილი არ მოიძებნა")


class Database:

    def __init__(self):
        self.database_data = load_database_data()

    def connect(self):
        try:
            connection = mariadb.connect(
                host=self.database_data["HOST"],
                port=3306,
                database=self.database_data["DATABASE"],
                user=self.database_data["USER"],
                password=self.database_data["PASSWORD"]
            )
            return connection
        except mariadb.Error:
            critical_error("მონაცემთა ბაზასთან დაკავშირება ვერ მოხერხდა,"
                           "\nგადაამოწმეთ ინტერნეთან კავშირი ან სცადეთ მოგვიანებით")
