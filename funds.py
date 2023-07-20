from connection import Database
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi


db = Database()

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
        self.payment_methods = load_payment_methods()
        for method in self.payment_methods:
            self.payment_method.addItem(method[1])
        self.payment_method.setCurrentText("გადახდის მეთოდი")
        self.pay_button.clicked.connect(self.pay)

    def closeEvent(self, event):
        self.clear_fields()
        self.search_by_phone.setFocus()

    def clear_fields(self):
        self.conn.commit()
        self.fname.clear()
        self.lname.clear()
        self.phone.clear()
        self.amount.clear()
        self.search_by_phone.clear()
        self.balance.setText("0 წუთი")
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
                    print(type(client[3]))
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
        method = self.payment_method.currentText()

        if self.payment_method.currentText() == "გადახდის მეთოდი":
            QMessageBox.information(self, "შეცდომა", "აირჩიეთ გადახდის მეთოდი")
        elif method == "წუთები":
            cursor16 = self.conn.cursor()
            cursor16.execute("SELECT * FROM clients WHERE phone=%s", (phone,))
            existing = [minute[5] for minute in cursor16]
            existing_minutes = sum(existing)
            if existing_minutes < int(amount):
                QMessageBox.warning(self, "არასაკმარისი წუთები",
                                    f"აბონემენტი ნომრით: {phone} არ აქვს საკმარისი წუთები ბალანსზე,"
                                    f"\nბალანსი: {existing_minutes} წუთი.")
                self.clear_fields()
            else:
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
                    cursor13.execute("INSERT INTO payments (fname, lname, phone, payment_method, amount) "
                                     "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, method, amount))
                    self.conn.commit()
                    balance = 0
                    init_minutes = 0
                    cursor14 = self.conn.cursor()
                    cursor14.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                     "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                    self.conn.commit()
                    self.clear_fields()
                else:
                    cursor15 = self.conn.cursor()
                    cursor15.execute("INSERT INTO payments (fname, lname, phone, payment_method, amount) "
                                     "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, method, amount))
                    self.conn.commit()
                    QMessageBox.information(self, "წარმატებული გადახდა", "გადახდა წარმატებით განხორციელდა!")
                    self.clear_fields()

