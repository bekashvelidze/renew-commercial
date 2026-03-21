from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.uic import loadUi
from connection import Database

db = Database()


class PatientsList(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/patients_list.ui", self)
        self.conn = db.connect()
        self.load_patients()

    def load_patients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * from clients")
        patients = cursor.fetchall()

        self.patients_table.setRowCount(0)
        self.patients_table.setRowCount(len(patients))
        self.patients_num.setText(f"სულ რეგისტრირებულია {str(len(patients))} პაციენტი.")
        self.patients_table.setColumnWidth(0, 50)
        self.patients_table.setColumnWidth(1, 150)
        self.patients_table.setColumnWidth(2, 170)
        self.patients_table.setColumnWidth(3, 150)

        for row_id, patient in enumerate(patients):
            patient_id = str(patient[0])
            fname = str(patient[1])
            lname = str(patient[2])
            phone = str(patient[3])

            self.patients_table.setItem(row_id, 0, QTableWidgetItem(patient_id))
            self.patients_table.setItem(row_id, 1, QTableWidgetItem(fname))
            self.patients_table.setItem(row_id, 2, QTableWidgetItem(lname))
            self.patients_table.setItem(row_id, 3, QTableWidgetItem(phone))

