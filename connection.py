import mariadb
from helpers import load_database_data, critical_error


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

