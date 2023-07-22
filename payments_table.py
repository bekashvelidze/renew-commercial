from datetime import datetime
from connection import Database
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi

today = datetime.now().date().strftime("%d.%m.%Y")
db = Database()


class PaymentsTable(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("ui/table.ui", self)
        self.load_payments_table()
        self.load_payments()
        self.load_payments_table()
        self.update_button.clicked.connect(self.update_cursor)

    def update_cursor(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * from payments WHERE date=%s", (today,))
        self.load_payments()

        return cursor

    def closeEvent(self, event):
        self.destroy()

    def load_payments_table(self):

        self.all_payments.setColumnWidth(0, 110)
        self.all_payments.setColumnWidth(1, 150)
        self.all_payments.setColumnWidth(2, 90)
        self.all_payments.setColumnWidth(3, 150)
        self.all_payments.setColumnWidth(4, 160)
        self.all_payments.setColumnWidth(5, 100)
        self.all_payments.setColumnWidth(5, 90)

        # self.load_payments(cursor)

    def load_payments(self):
        self.all_payments.clearContents()
        cursor = self.update_cursor()
        print(cursor)
        payments = [payment for payment in cursor]
        print(payments)
        total_cash = [pay[7] for pay in payments if pay[5] == "ნაღდი"]
        total_card = [pay[7] for pay in payments if pay[5] == "უნაღდო"]
        total_by_minutes = [pay[7] for pay in payments if pay[5] == "წუთები"]
        self.total_daily.setText(str(sum(total_cash) + sum(total_card)))
        self.cash.setText(str(sum(total_cash)))
        self.card.setText(str(sum(total_card)))
        self.pay_by_minutes.setText(str(sum(total_by_minutes)))
        self.all_payments.setRowCount(cursor.rowcount)
        self.all_payments.setColumnCount(7)

        row = 0
        for item in payments:
            print(item[1], item[2], item[3], item[4], item[5], item[6], item[7])
            self.all_payments.setItem(row, 0, QTableWidgetItem(item[1]))
            self.all_payments.setItem(row, 1, QTableWidgetItem(item[2]))
            self.all_payments.setItem(row, 2, QTableWidgetItem(item[3]))
            self.all_payments.setItem(row, 3, QTableWidgetItem(item[4]))
            self.all_payments.setItem(row, 4, QTableWidgetItem(item[5]))
            self.all_payments.setItem(row, 5, QTableWidgetItem(item[6]))
            self.all_payments.setItem(row, 6, QTableWidgetItem(str(item[7])))
            row += 1
