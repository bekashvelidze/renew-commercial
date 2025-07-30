import subprocess
from datetime import datetime
import json
import os
import sys
import zipfile
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon

def load_database_data():
    try:
        with open("database.json", "r") as file:
            database_data = json.load(file)
        return database_data
    except FileNotFoundError:
        show_error_message("database.json ფაილი არ მოიძებნა!")
        sys.exit(1)
    except json.JSONDecodeError:
        show_error_message("database.json ფაილი არასწორადაა ფორმატირებული!")
        sys.exit(1)

def show_error_message(message):
    app = QApplication(sys.argv)
    msgbox = QMessageBox()
    msgbox.setWindowTitle("შეცდომა")
    msgbox.setWindowIcon(QIcon("ui/renew.ico"))
    msgbox.setText(message)
    msgbox.exec()

def create_backup():
    data = load_database_data()
    
    db_host = data["HOST"]
    db_user = data["USER"]
    db_password = data["PASSWORD"]
    db_name = data["DATABASE"]

    backup_path = r'D:\Backups\databases'
    os.makedirs(backup_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sql_filename = f"{db_name}_{timestamp}.sql"
    zip_filename = f"{db_name}_{timestamp}.zip"
    sql_filepath = os.path.join(backup_path, sql_filename)
    zip_filepath = os.path.join(backup_path, zip_filename)

    # Create database dump
    command = [
        "mariadb-dump",
        f"--host={db_host}",
        f"--user={db_user}",
        f"--password={db_password}",
        db_name,
        f"--result-file={sql_filepath}"
    ]

    try:
        # Execute the backup command
        subprocess.run(command, check=True)
        
        # Create zip file
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(sql_filepath, os.path.basename(sql_filepath))
        
        # Remove the original SQL file after zipping
        os.remove(sql_filepath)
        
        # Show success message
        app = QApplication(sys.argv)
        msgbox = QMessageBox()
        msgbox.setWindowTitle("ბაზის ასლის აღება")
        msgbox.setWindowIcon(QIcon("ui/renew.ico"))
        msgbox.setText(f"მონაცემთა ბაზის ასლი შეიქმნა წარმატებით!\nფაილი: {zip_filename}")
        msgbox.exec()

    except subprocess.CalledProcessError as e:
        show_error_message(f"ბაზის ასლის აღების პროცესში შეცდომა: {e}")
    except FileNotFoundError:
        show_error_message("mariadb-dump ბრძანება არ მოიძებნა. დარწმუნდით, რომ ის თქვენს სისტემურ PATH-შია.")
    except Exception as e:
        show_error_message(f"მოულოდნელი შეცდომა: {e}")

if __name__ == "__main__":
    create_backup()