import subprocess
from datetime import datetime
import json
import os
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon

def load_database_data():
    with open("database.json", "r") as file:
        database_data = json.load(file)

    return database_data

data = load_database_data()

def create_backup():

    db_host = data["HOST"]
    db_user = data["USER"]
    db_password = data["PASSWORD"]
    db_name = data["DATABASE"]

    backup_path = r'D:\Backups\databases'
    os.makedirs(backup_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_path}/{db_name}_{timestamp}.sql"

    command = [
        "mariadb-dump",
        f"--host={db_host}",
        f"--user={db_user}",
        f"--password={db_password}",
        db_name,
        f"--result-file={backup_file}"
    ]

    try:
        subprocess.run(command, check=True)
        app = QApplication(sys.argv)
        msgbox = QMessageBox()
        msgbox.setWindowTitle("ბაზის ასლის აღება")
        msgbox.setWindowIcon(QIcon("ui/renew.ico"))
        msgbox.setText("მონაცემთა ბაზის ასლი შეიქმნა წარმატებით!")
        msgbox.exec()

    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
    except FileNotFoundError:
        print("Error: mysqldump (or mariadb-dump) command not found. Ensure it's in your system's PATH.")
