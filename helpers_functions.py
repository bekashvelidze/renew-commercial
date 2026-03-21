import os
import sys
import json
import webbrowser
from connection import Database
from PyQt6.QtWidgets import QApplication, QMessageBox


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = Database()

def critical_error(message):
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        msgbox = QMessageBox()
        msgbox.setWindowTitle("შეცდომა")
        msgbox.setText(message)
        msgbox.exec()
        sys.exit(1)

def success_message(message):
    app = QApplication.instance()
    created_new_app = False
    if not app:
        app = QApplication(sys.argv)
        created_new_app = True
    msgbox = QMessageBox()
    msgbox.setIcon(QMessageBox.Icon.Information)
    msgbox.setWindowTitle("წარმატება")
    msgbox.setText(message)
    msgbox.exec()

def load_json_files(filename):
    try:
        with open(os.path.join(BASE_DIR, filename), "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        critical_error(e)
        return {}

def load_times():
    return load_json_files("times.json")


def load_days():
    return load_json_files("days.json")

def get_version():
    try:
        with open(os.path.join(BASE_DIR, 'version.json'), "r") as file:
            version = json.load(file)
            return version["version"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        critical_error("ფაილი არ მოიძებნა")

def check_integer(number):
    try:
        if int(number):
            return True
    except (ValueError, TypeError):
        return False

def open_documentation():
    webbrowser.open('https://google.ge')

def get_data_from_db(query, params=None):
    conn = db.connect()

    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except Exception as e:
        critical_error(e)
        return []
    finally:
        conn.close()

def load_procedures():
    return get_data_from_db("SELECT * FROM procedures")

def load_doctors(category):
    return get_data_from_db("SELECT * FROM doctors WHERE category=%s", (category,))

def load_zones():
    return get_data_from_db("SELECT * FROM zones")

def load_types():
    return get_data_from_db("SELECT * FROM types")

def close_main_application():
    sys.exit()