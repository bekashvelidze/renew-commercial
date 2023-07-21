from datetime import datetime
from connection import Database
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.uic import loadUi

today = datetime.now().date().strftime("%d.%m.%Y")
db = Database()
# today = "22.07.2023"

class TimeTable(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/timetable.ui", self)
        self.conn = db.connect()
        self.load_appointments()

    def load_appointments(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * from payments WHERE date=%s", (today,))

        self.all_appointments.sortItems(5)
        self.all_appointments.setRowCount(cursor.rowcount)
        self.all_appointments.setColumnCount(7)

        self.all_appointments.setColumnWidth(0, 110)
        self.all_appointments.setColumnWidth(1, 150)
        self.all_appointments.setColumnWidth(2, 90)
        self.all_appointments.setColumnWidth(3, 170)
        self.all_appointments.setColumnWidth(4, 160)
        self.all_appointments.setColumnWidth(5, 100)
        self.all_appointments.setColumnWidth(5, 90)

        self.load_payments(cursor)
    def load_payments(self, cursor):

        payments = [payment for payment in cursor]
        row = 0
        for item in payments:
            self.all_appointments.setItem(row, 0, QTableWidgetItem(item[1]))
            self.all_appointments.setItem(row, 1, QTableWidgetItem(item[2]))
            self.all_appointments.setItem(row, 2, QTableWidgetItem(item[3]))
            self.all_appointments.setItem(row, 3, QTableWidgetItem(item[4]))
            self.all_appointments.setItem(row, 4, QTableWidgetItem(item[5]))
            self.all_appointments.setItem(row, 5, QTableWidgetItem(item[6]))
            self.all_appointments.setItem(row, 6, QTableWidgetItem(str(item[7])))
            row += 1
