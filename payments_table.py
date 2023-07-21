from datetime import datetime
from connection import Database
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.uic import loadUi

today = datetime.now().date().strftime("%d.%m.%Y")
db = Database()
# today = "22.07.2023"

class PaymentsTable(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/payments_table.ui", self)
        self.conn = db.connect()
        self.load_payments_table()

    def load_payments_table(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * from payments WHERE date=%s", (today,))

        self.all_payments.sortItems(5)
        self.all_payments.setRowCount(cursor.rowcount)
        self.all_payments.setColumnCount(7)

        self.all_payments.setColumnWidth(0, 110)
        self.all_payments.setColumnWidth(1, 150)
        self.all_payments.setColumnWidth(2, 90)
        self.all_payments.setColumnWidth(3, 170)
        self.all_payments.setColumnWidth(4, 160)
        self.all_payments.setColumnWidth(5, 100)
        self.all_payments.setColumnWidth(5, 90)

        self.load_payments(cursor)
    def load_payments(self, cursor):
        self.all_payments.clearContents()
        payments = [payment for payment in cursor]
        row = 0
        for item in payments:
            self.all_payments.setItem(row, 0, QTableWidgetItem(item[1]))
            self.all_payments.setItem(row, 1, QTableWidgetItem(item[2]))
            self.all_payments.setItem(row, 2, QTableWidgetItem(item[3]))
            self.all_payments.setItem(row, 3, QTableWidgetItem(item[4]))
            self.all_payments.setItem(row, 4, QTableWidgetItem(item[5]))
            self.all_payments.setItem(row, 5, QTableWidgetItem(item[6]))
            self.all_payments.setItem(row, 6, QTableWidgetItem(str(item[7])))
            row += 1
