from connection import Database
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi

db = Database()
conn = db.connect()


class PatientHistory(QWidget):

    def __init__(self, *args):
        super().__init__()
        loadUi("ui/history.ui", self)

        if args:
            args_list = [arg for arg in args]
            phone = args_list[3]
            self.search_client_2(phone)

    def search_client_2(self, *args):
        if args:
            search = args[0]
            cursor70 = conn.cursor()
            cursor70.execute("SELECT * FROM patient_history WHERE phone=%s", (search,))

            if cursor70.rowcount == 0:
                QMessageBox.warning(self, "შეცდომა",
                                    f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                    f"გადახდის დასაფიქსირებლად.")
            else:
                for client in cursor70:
                    if search == client[5]:
                        self.patient.setText(client[1])
                        self.phone.setText(client[5])
        else:
            search = self.phone.text()
            cursor70 = self.conn.cursor()
            cursor70.execute("SELECT * FROM patient_history WHERE phone=%s", (search,))

            if cursor70.rowcount == 0:
                QMessageBox.warning(self, "შეცდომა",
                                    f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                    f"გადახდის დასაფიქსირებლად.")
            else:
                for client in cursor70:
                    if search == client[5]:
                        self.patient.setText(client[1])
                        self.phone.setText(client[5])
