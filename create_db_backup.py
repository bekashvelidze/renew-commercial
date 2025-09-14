import subprocess
from datetime import datetime
import json
import os
import sys
import gzip
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
    backup_file_temp = f"{backup_path}/{db_name}_{timestamp}.sql"

    # First, let's test if mariadb-dump is accessible
    print("Testing mariadb-dump accessibility...")
    try:
        test_result = subprocess.run(["mariadb-dump", "--version"],
                                     capture_output=True, text=True,
                                     creationflags=subprocess.CREATE_NO_WINDOW)
        print(f"mariadb-dump version: {test_result.stdout.strip()}")
    except FileNotFoundError:
        print("mariadb-dump not found, trying mysqldump...")
        try:
            test_result = subprocess.run(["mysqldump", "--version"],
                                         capture_output=True, text=True,
                                         creationflags=subprocess.CREATE_NO_WINDOW)
            print(f"mysqldump version: {test_result.stdout.strip()}")
            # Use mysqldump instead
            dump_command = "mysqldump"
        except FileNotFoundError:
            print("Neither mariadb-dump nor mysqldump found!")
            return
    else:
        dump_command = "mariadb-dump"

    # Test database connection first
    print("Testing database connection...")
    test_command = [
        dump_command,
        f"--host={db_host}",
        f"--user={db_user}",
        f"--password={db_password}",
        "--single-transaction",
        "--no-data",  # Just structure, no data for testing
        db_name
    ]

    try:
        print(
            f"Running test command: {' '.join([cmd if '--password=' not in cmd else '--password=***' for cmd in test_command])}")
        test_result = subprocess.run(test_command,
                                     capture_output=True, text=True,
                                     creationflags=subprocess.CREATE_NO_WINDOW,
                                     timeout=30)

        if test_result.returncode != 0:
            print(f"Test connection failed!")
            print(f"Return code: {test_result.returncode}")
            print(f"Stderr: {test_result.stderr}")
            print(f"Stdout: {test_result.stdout}")
            return
        else:
            print("✓ Database connection successful!")

    except subprocess.TimeoutExpired:
        print("✗ Database connection timed out!")
        return
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return

    # Now try the actual backup
    command = [
        dump_command,
        f"--host={db_host}",
        f"--user={db_user}",
        f"--password={db_password}",
        "--single-transaction",
        "--routines",
        "--triggers",
        db_name,
        f"--result-file={backup_file_temp}"
    ]

    try:
        print(f"Creating backup at: {backup_file_temp}")
        print(f"Running backup command...")

        result = subprocess.run(command,
                                capture_output=True, text=True,
                                creationflags=subprocess.CREATE_NO_WINDOW,
                                timeout=300)  # 5 minute timeout

        print(f"Backup command completed with return code: {result.returncode}")

        if result.stdout:
            print(f"Stdout: {result.stdout}")
        if result.stderr:
            print(f"Stderr: {result.stderr}")

        # Check if file exists and its size
        if os.path.exists(backup_file_temp):
            file_size = os.path.getsize(backup_file_temp)
            print(f"✓ Backup file created! Size: {file_size} bytes ({file_size / (1024 * 1024):.2f} MB)")

            if file_size == 0:
                print("⚠ Warning: Backup file is empty!")
                # Try to see what's in the database
                count_command = [
                    dump_command.replace('dump', ''),  # mariadb or mysql
                    f"--host={db_host}",
                    f"--user={db_user}",
                    f"--password={db_password}",
                    "-e", f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{db_name}';",
                    db_name
                ]
                try:
                    count_result = subprocess.run(count_command, capture_output=True, text=True,
                                                  creationflags=subprocess.CREATE_NO_WINDOW)
                    print(f"Table count query result: {count_result.stdout}")
                except Exception as e:
                    print(f"Could not count tables: {e}")
            else:
                # Compress if file has content
                backup_file_gz = f"{backup_path}/{db_name}_{timestamp}.sql.gz"
                with open(backup_file_temp, 'rb') as f_in:
                    with gzip.open(backup_file_gz, 'wb', compresslevel=9) as f_out:
                        f_out.writelines(f_in)

                os.remove(backup_file_temp)
                compressed_size = os.path.getsize(backup_file_gz)

                print(f"✓ Compressed backup created: {compressed_size / (1024 * 1024):.2f} MB")

                app = QApplication(sys.argv)
                msgbox = QMessageBox()
                msgbox.setWindowTitle("ბაზის ასლის აღება")
                msgbox.setWindowIcon(QIcon("ui/renew.ico"))
                msgbox.setText(
                    f"მონაცემთა ბაზის ასლი შეიქმნა წარმატებით!\nზომა: {compressed_size / (1024 * 1024):.2f} MB")
                msgbox.exec()

        else:
            print("✗ Backup file was not created!")
            print("Check the database name, credentials, and permissions.")

    except subprocess.TimeoutExpired:
        print("✗ Backup process timed out!")
    except Exception as e:
        print(f"✗ Backup failed: {e}")