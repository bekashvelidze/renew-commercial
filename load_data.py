import json
import datetime
from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.uic import loadUi
from connection import Database

class LoadData:
    def __init__(self):
        self.load_services()

    def load_services(self):
        with open("services.json", "r", encoding="utf-8") as file:
            services = json.load(file)

        return services
    def cosmetology(self):
        db = Database()
        cursor = db.connect()
        cursor.execute("SELECT * FROM cosmetology_appointments")
        with open("times.json", "r", encoding="utf-8") as file:
            times = json.load(file)

        self.cos_appointments.setColumnWidth(0, 120)
        self.cos_appointments.setColumnWidth(1, 180)
        self.cos_appointments.setColumnWidth(2, 120)
        self.cos_appointments.setColumnWidth(3, 120)
        self.cos_appointments.setColumnWidth(4, 160)
        self.cos_appointments.setColumnWidth(5, 120)

        row = 0

        for person in cursor:
            self.cos_appointments.setItem(int(times[cursor[7]]), 0, QTableWidgetItem(cursor[1]))
            # self.cos_appointments.setItem(int(times[person["time"]]), 1, QTableWidgetItem(person["lname"]))
            # self.cos_appointments.setItem(int(times[person["time"]]), 2, QTableWidgetItem(person["phone"]))
            # self.cos_appointments.setItem(int(times[person["time"]]), 3, QTableWidgetItem(person["zone"]))
            # self.cos_appointments.setItem(int(times[person["time"]]), 4, QTableWidgetItem(person["doctor"]))
            # self.cos_appointments.setItem(int(times[person["time"]]), 5, QTableWidgetItem(person["price"]))
            row += 1