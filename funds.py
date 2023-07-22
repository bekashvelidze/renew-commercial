from datetime import datetime
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from connection import Database

db = Database()
today = datetime.now().date().strftime("%d.%m.%Y")


def load_categories():
    conn = db.connect()
    cursor_cats = conn.cursor()
    cursor_cats.execute("SELECT * FROM categories")

    return cursor_cats


def load_payment_methods():
    conn = db.connect()
    cursor_methods = conn.cursor()
    cursor_methods.execute("SELECT * FROM payment_methods")

    return cursor_methods


class Funds(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/pay.ui", self)
        self.conn = db.connect()
        self.search_button.clicked.connect(self.search_client)
        cursor_init = self.conn.cursor()
        cursor_init.execute("SELECT * from payments WHERE date=%s", (today,))
        self.load_payments_table(cursor_init)
        self.new_date.dateChanged.connect(self.change_date_daily)

        self.categories = load_categories()
        for category in self.categories:
            self.category.addItem(category[1])
        self.category.setCurrentText("კატეგორია")

        self.payment_methods = load_payment_methods()
        for method in self.payment_methods:
            self.payment_method.addItem(method[1])
        self.payment_method.setCurrentText("გადახდის მეთოდი")

        self.pay_button.clicked.connect(self.pay)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "ფანჯრის დახურვა",
            "დარწმუნებული ხართ, რომ გსურთ ფანჯრის დახურვა?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            self.clear_fields()
            self.search_by_phone.setFocus()
        else:
            event.ignore()

    def change_date_daily(self):
        global today

        today = self.new_date.text()
        self.all_payments.clearContents()
        cursor20 = self.conn.cursor()
        cursor20.execute("SELECT * from payments WHERE date=%s", (today,))
        self.load_payments_table(cursor20)

    def clear_fields(self):
        self.conn.commit()
        self.fname.clear()
        self.lname.clear()
        self.phone.clear()
        self.amount.clear()
        self.search_by_phone.clear()
        self.balance.setText("0 წუთი")
        self.category.setCurrentText("კატეგორია")
        self.payment_method.setCurrentText("გადახდის მეთოდი")

    def load_clients(self):
        cursor10 = self.conn.cursor()
        cursor10.execute("SELECT * FROM clients")
        clients = [client for client in cursor10]
        return clients

    def search_client(self):
        search = self.search_by_phone.text()
        cursor11 = self.conn.cursor()
        cursor11.execute("SELECT * FROM clients WHERE phone=%s", (search,))

        if cursor11.rowcount == 0:
            QMessageBox.warning(self, "შეცდომა",
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                f"გადახდის დასაფიქსირებლად.")
        else:
            for client in cursor11:
                if search == client[3]:
                    self.fname.setText(client[1])
                    self.lname.setText(client[2])
                    self.phone.setText(client[3])
                    self.balance.setText(f"{client[5]} წუთი")

    def pay(self):
        clients = self.load_clients()
        first_name = self.fname.text()
        last_name = self.lname.text()
        phone = self.phone.text()
        amount = self.amount.text()
        category = self.category.currentText()
        method = self.payment_method.currentText()

        if self.payment_method.currentText() == "გადახდის მეთოდი":
            QMessageBox.warning(self, "შეცდომა", "აირჩიეთ გადახდის მეთოდი")
        elif self.category.currentText() == "კატეგორია":
            QMessageBox.warning(self, "შეცდომა", "აირჩიეთ კატეგორია")
        elif method == "წუთები":
            cursor16 = self.conn.cursor()
            cursor16.execute("SELECT * FROM clients WHERE phone=%s", (phone,))
            if cursor16.rowcount == 0:
                QMessageBox.warning(self, "შეცდომა",
                                    f"პაციენტი ნომრით: {phone} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                    f"გადახდის დასაფიქსირებლად.")
            else:
                existing = [minute[5] for minute in cursor16]
                existing_minutes = sum(existing)
                if existing_minutes < int(amount):
                    QMessageBox.warning(self, "არასაკმარისი წუთები",
                                        f"აბონემენტი ნომრით: {phone} არ აქვს საკმარისი წუთები ბალანსზე,"
                                        f"\nბალანსი: {existing_minutes} წუთი.")
                    self.clear_fields()
                else:
                    cursor18 = self.conn.cursor()
                    cursor18.execute("INSERT INTO payments (fname, lname, phone, category, payment_method, date, "
                                     "amount) VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                              method, today, amount))
                    self.conn.commit()
                    cursor20 = self.conn.cursor()
                    cursor20.execute("SELECT * from payments WHERE date=%s", (today,))
                    self.load_payments_table(cursor20)
                    updated_minutes = existing_minutes - int(amount)
                    cursor17 = self.conn.cursor()
                    cursor17.execute("UPDATE clients SET minutes=%s WHERE phone=%s", (updated_minutes, phone,))
                    self.conn.commit()
                    self.clear_fields()
                    QMessageBox.information(self, "წარმატებული გადახდა", "გადახდა წარმატებით განხორციელდა!")

        else:
            if first_name == "" or last_name == "" or phone == "" or amount == "":
                QMessageBox.information(self, "შეცდომა",
                                        f"ყველა ველის შევსება სავალდებულოა")
            else:
                cursor12 = self.conn.cursor()
                cursor12.execute("SELECT * FROM payments")

                client_phones = [client[3] for client in clients]
                if phone not in client_phones:
                    cursor13 = self.conn.cursor()
                    cursor13.execute("INSERT INTO payments (fname, lname, phone, category, payment_method, date, "
                                     "amount) VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                              method, today, amount))
                    self.conn.commit()
                    cursor20 = self.conn.cursor()
                    cursor20.execute("SELECT * from payments WHERE date=%s", (today,))
                    self.load_payments_table(cursor20)
                    balance = 0
                    init_minutes = 0
                    cursor14 = self.conn.cursor()
                    cursor14.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                     "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                    self.conn.commit()
                    self.clear_fields()
                    cursor20 = self.conn.cursor()
                    cursor20.execute("SELECT * from payments WHERE date=%s", (today,))
                    self.load_payments_table(cursor20)

                else:
                    cursor15 = self.conn.cursor()
                    cursor15.execute("INSERT INTO payments (fname, lname, phone, category, payment_method, date, "
                                     "amount) VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                              method, today, amount))
                    self.conn.commit()
                    cursor20 = self.conn.cursor()
                    cursor20.execute("SELECT * from payments WHERE date=%s", (today,))
                    QMessageBox.information(self, "წარმატებული გადახდა", "გადახდა წარმატებით განხორციელდა!")
                    self.clear_fields()
                    self.load_payments_table(cursor20)

    def load_payments_table(self, data):

        # self.all_payments.sortItems(5)
        self.all_payments.setRowCount(data.rowcount)
        self.all_payments.setColumnCount(7)

        self.all_payments.setColumnWidth(0, 100)
        self.all_payments.setColumnWidth(1, 160)
        self.all_payments.setColumnWidth(2, 90)
        self.all_payments.setColumnWidth(3, 150)
        self.all_payments.setColumnWidth(4, 160)
        self.all_payments.setColumnWidth(5, 100)
        self.all_payments.setColumnWidth(6, 100)

        self.all_payments.clearContents()
        payments = [payment for payment in data]
        total_cash = [pay[7] for pay in payments if pay[5] == "ნაღდი"]
        total_card = [pay[7] for pay in payments if pay[5] == "უნაღდო"]
        total_by_minutes = [pay[7] for pay in payments if pay[5] == "წუთები"]
        self.total_daily.setText(str(sum(total_cash) + sum(total_card)))
        self.cash.setText(str(sum(total_cash)))
        self.card.setText(str(sum(total_card)))
        self.new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.pay_by_minutes.setText(str(sum(total_by_minutes)))
        self.all_payments.horizontalHeader().setVisible(True)
        self.all_payments.verticalHeader().setVisible(True)
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
