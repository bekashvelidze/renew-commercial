import mariadb
from connection import Database
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

db = Database()
conn = db.connect()


class Subscription(QDialog):

    def __init__(self):
        super(Subscription, self).__init__()
        loadUi("ui/subscription.ui", self)
        self.buy.clicked.connect(self.buy_subscription)

    def load_clients(self):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = [client for client in cursor]
        return clients

    def buy_subscription(self):
        clients = self.load_clients()
        first_name = self.fname.text()
        last_name = self.lname.text()
        phone = self.phone.text()
        minutes = int(self.minutes.text())

        cursor2 = conn.cursor("SELECT * FROM clients")
        cursor2.execute()
        if cursor2.rowcount == 0:
            cursor3 = conn.cursor()
            cursor3.execute("INSERT INTO clients (fname, lname, phone, minutes) "
                            "VALUES (?, ?, ?, ?)", (first_name, last_name, phone, minutes))
            conn.commit()
        else:
            client_phones = [client[3] for client in clients]
            if phone not in client_phones:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone, minutes) "
                                "VALUES (?, ?, ?, ?)", (first_name, last_name, phone, minutes))
                conn.commit()
            else:
                cursor4 = conn.cursor()
                cursor4.execute("SELECT * FROM clients WHERE phone=%s", (phone,))
                existing_minutes = int(cursor4[5])
                updated_minutes = existing_minutes + minutes
                cursor5 = conn.cursor()
                cursor5.execute(f"UPDATE clients SET 'minutes'={updated_minutes} WHERE phone=%s", (phone,))
                conn.commit()




