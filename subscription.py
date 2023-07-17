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
        self.show_window()
        # self.buy.clicked.connect(self.buy_subscription)

    def load_clients(self):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = [client for client in cursor]
        return clients

    # def show_window(self):
    #     subs_window = QDialog()
    #     subs_window.addWidget(subs_window)
    #     subs_window.setWindowTitle('აბონემენტის შეძენა')
    #     subs_window.setFixedWidth(490)
    #     subs_window.setFixedHeight(250)
    #     x = (subs_window.screen().geometry().width() // 2) - (subs_window.width() // 2)
    #     y = (subs_window.screen().geometry().height() // 2) - (subs_window.height() // 2)
    #     subs_window.move(x, y)
    #     subs_window.setCurrentIndex(subs_window.currentIndex() + 1)

    # def buy_subscription(self):
    #     clients = self.load_clients()
    #     first_name = self.fname.text()
    #     last_name = self.lname.text()
    #     phone = self.phone.text()
    #     minutes = self.minutes.text()
    #     print(type(minutes))
    #
    #     cursor2 = conn.cursor()
    #     cursor2.execute("SELECT * FROM clients")
    #     if cursor2.rowcount == 0:
    #         cursor3 = conn.cursor()
    #         cursor3.execute("INSERT INTO clients (fname, lname, phone, minutes) "
    #                         "VALUES (?, ?, ?, ?)", (first_name, last_name, phone, minutes))
    #         conn.commit()
    #     else:
    #         client_phones = [client[3] for client in clients]
    #         if phone not in client_phones:
    #             cursor3 = conn.cursor()
    #             cursor3.execute("INSERT INTO clients (fname, lname, phone, minutes) "
    #                             "VALUES (?, ?, ?, ?)", (first_name, last_name, phone, minutes))
    #             conn.commit()
    #         else:
    #             cursor4 = conn.cursor()
    #             cursor4.execute("SELECT * FROM clients WHERE phone=%s", (phone,))
    #             existing = [minute[5] for minute in cursor4]
    #             existing_minutes = existing[0]
    #             if minutes == "":
    #                 minutes = 0
    #             updated_minutes = existing_minutes + minutes
    #             cursor5 = conn.cursor()
    #             cursor5.execute(f"UPDATE clients SET 'minutes'='{updated_minutes}' WHERE phone=%s", (phone,))
    #             conn.commit()




