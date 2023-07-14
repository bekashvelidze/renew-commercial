import mariadb
import sys
import json


def load_database_data():
    with open("database.json", "r") as file:
        database_data = json.load(file)

    return database_data


class Database:

    def __init__(self):
        self.database_data = load_database_data()

    def connect(self):
        try:
            connection = mariadb.connect(
                host = self.database_data["HOST"],
                port = 3306,
                database = self.database_data["DATABASE"],
                user = self.database_data["USER"],
                password = self.database_data["PASSWORD"]
            )
        except mariadb.Error as error:
            print(error)
            sys.exit(1)

        cursor = connection.cursor()

        return cursor
