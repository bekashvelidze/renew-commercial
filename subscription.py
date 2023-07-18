from connection import Database
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi

db = Database()


class Subscription(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/subscription.ui", self)
        self.conn = db.connect()
        self.search_button.clicked.connect(self.search_client)
        self.buy.clicked.connect(self.buy_subscription)

    def load_clients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = [client for client in cursor]
        return clients

    def search_client(self):
        search = self.search.text()
        cursor6 = self.conn.cursor()
        cursor6.execute("SELECT * FROM clients WHERE phone=%s", (search,))

        if cursor6.rowcount == 0:
            QMessageBox.warning(self, 'შეცდომა',
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში"
                                f"\nგთხოვთ შეავსეთ შესაბამისი ველები აბონემენტის დასარეგისტრირებლად.")
        else:
            for client in cursor6:
                if search == client[3]:
                    self.fname.setText(client[1])
                    self.lname.setText(client[2])
                    self.phone.setText(client[3])
                    # self.minutes.setText(str(client[5]))

    def buy_subscription(self):
        clients = self.load_clients()
        first_name = self.fname.text()
        last_name = self.lname.text()
        phone = self.phone.text()
        minutes = self.minutes.text()

        if first_name == "" or last_name == "" or phone == "" or minutes == "":
            QMessageBox.information(self, 'შეცდომა',
                                    f"ყველა ველის შევსება სავალდებულოა")
        else:
            cursor2 = self.conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = self.conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone, minutes) "
                                "VALUES (?, ?, ?, ?)", (first_name, last_name, phone, minutes))
                self.conn.commit()
            else:
                client_phones = [client[3] for client in clients]
                if phone not in client_phones:
                    cursor3 = self.conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone, minutes) "
                                    "VALUES (?, ?, ?, ?)", (first_name, last_name, phone, minutes))
                    self.conn.commit()
                else:
                    cursor4 = self.conn.cursor()
                    cursor4.execute("SELECT * FROM clients WHERE phone=%s", (phone,))
                    existing = [minute[5] for minute in cursor4]
                    existing_minutes = sum(existing)
                    updated_minutes = existing_minutes + int(minutes)
                    cursor5 = self.conn.cursor()
                    cursor5.execute("UPDATE clients SET minutes=%s WHERE phone=%s", (updated_minutes, phone,))
                    self.conn.commit()
                    self.fname.clear()
                    self.lname.clear()
                    self.phone.clear()
                    self.minutes.clear()
                    self.search.clear()
                    QMessageBox.information(self, 'აბონემენტის შეძენა',
                                            f"აბონემენტი დარეგისტრირდა:\nსახელი, გვარი: {first_name} {last_name}"
                                            f"\nწუთი: {minutes}")
