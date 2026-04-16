import os
from helpers_functions import critical_error, db, BASE_DIR
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi


class PatientsEdit(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(BASE_DIR, 'ui', 'edit_patient.ui'), self)
        self.conn = db.connect()
        self.search_button.clicked.connect(self.load_patient)
        self.edit_button.clicked.connect(self.update_data)

    def load_patient(self):
        search = self.search_patient.text().strip()
        if not search:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM `clients` WHERE phone=%s", (search,))
            patient = cursor.fetchone()
            if patient:
                self.patient_id.setText(str(patient[0]))
                self.fname.setText(patient[1])
                self.lname.setText(patient[2])
                self.phone.setText(patient[3])
            else:
                QMessageBox.warning(self, "შეცდომა", f"პაციენტით ნომრით {self.phone.text()} არ მოიძებნა.")
        except Exception as e:
            critical_error(f"ჩატვირთვის შეცდომა - {e}")

    def update_data(self):
        fname = self.fname.text().strip()
        lname = self.lname.text().strip()
        phone = self.phone.text().strip()
        num = self.patient_id.text().strip()

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE clients SET fname=%s, lname=%s, phone=%s WHERE id=%s",
                           (fname, lname, phone, num)
                           )
            self.conn.commit()

            QMessageBox.information(self,
                                    "პაციენტის რედაქტირება",
                                    f"პაციენტის განახლებული მონაცემები წარმატებით ჩაიწერა ბაზაში."
                                    )
            self.fname.clear()
            self.lname.clear()
            self.phone.clear()
            self.patient_id.clear()
            self.search_patient.clear()
            self.close()

        except Exception as e:
            critical_error(f"პაციენტის მონაცემების განახლება ვერ მოხერხდა - {e}")

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.load_patient()
        else:
            super().keyPressEvent(event)
