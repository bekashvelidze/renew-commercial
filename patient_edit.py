from connection import Database
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi

db = Database()


class PatientsEdit(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/edit_patient.ui", self)
        self.conn = db.connect()
        self.search_button.clicked.connect(self.load_patient)
        self.edit_button.clicked.connect(self.update_data)

    def load_patient(self):
        search = self.search_patient.text()
        cursor102 = self.conn.cursor()
        cursor102.execute("SELECT * FROM `clients` WHERE phone=%s", (search,))
        for patient in cursor102:
            self.patient_id.setText(str(patient[0]))
            self.fname.setText(patient[1])
            self.lname.setText(patient[2])
            self.phone.setText(patient[3])

    def update_data(self):
        fname = self.fname.text()
        lname = self.lname.text()
        phone = self.phone.text()
        num = self.patient_id.text()
        cursor103 = self.conn.cursor()
        cursor103.execute("UPDATE clients SET fname=%s, lname=%s, phone=%s WHERE id=%s", (fname, lname, phone, num))
        self.conn.commit()

        QMessageBox.information(self,
                                "პაციენტის რედაქტირება",
                                f"პაციენტის განახლებული მონაცემები წარმატებით ჩაიწერა ბაზაში."
                                )
        self.fname.clear()
        self.lname.clear()
        self.phone.clear()
        self.patient_id.clear()
        self.close()
