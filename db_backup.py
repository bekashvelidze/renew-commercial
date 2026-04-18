import subprocess
from datetime import datetime
import json
import os
import sys
import zipfile
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication

from helpers_functions import BASE_DIR, critical_error, success_message

def load_database_data():
    try:
        with open(os.path.join(BASE_DIR, "database.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        critical_error("database.json ფაილი არ მოიძებნა!")
        sys.exit(1)
    except json.JSONDecodeError:
        critical_error("database.json ფაილი არასწორადაა ფორმატირებული!")
        sys.exit(1)

def create_backup():
    QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
    data = load_database_data()

    db_host = data["HOST"]
    db_user = data["USER"]
    db_password = data["PASSWORD"]
    db_name = data["DATABASE"]

    if os.path.exists("D:\\"):
        backup_path = r'D:\Backups\databases'
    else:
        backup_path = os.path.join(BASE_DIR, "Backups")

    os.makedirs(backup_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sql_filename = f"{db_name}_{timestamp}.sql"
    zip_filename = f"{db_name}_{timestamp}.zip"
    sql_filepath = os.path.join(backup_path, sql_filename)
    zip_filepath = os.path.join(backup_path, zip_filename)

    command = [
        "mariadb-dump",
        f"--host={db_host}",
        f"--user={db_user}",
        f"--password={db_password}",
        db_name,
        f"--single-transaction",
        f"--quick",
        f"--result-file={sql_filepath}"
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, shell=True, text=True)

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(sql_filepath, os.path.basename(sql_filepath))

        if os.path.exists(sql_filepath):
            os.remove(sql_filepath)

        QApplication.restoreOverrideCursor()
        success_message(f"მონაცემთა ბაზის ასლი შეიქმნა წარმატებით!\nმისამართი: {backup_path}\\{zip_filename}")

    except subprocess.TimeoutExpired:
        critical_error("პროცესი შეჩერდა: ბაზის ასლის აღებას ძალიან დიდი დრო დასჭირდა (Timeout).")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else e.stdout
        critical_error(f"ბაზის შეცდომა: {error_msg}")
    except FileNotFoundError:
        critical_error("mariadb-dump ბრძანება არ მოიძებნა. დარწმუნდით, რომ ის თქვენს სისტემურ PATH-შია.")
    except Exception as e:
        critical_error(f"მოულოდნელი შეცდომა: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    create_backup()