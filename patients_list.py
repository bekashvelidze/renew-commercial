from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.uic import loadUi
from connection import Database

db = Database()


class PatientsList(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/patients_list.ui", self)
        self.conn = db.connect()

        self.patients_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.patients_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

    def showEvent(self, event):
        self.load_patients()
        self.patients_table.scrollToTop()
        self.patients_table.clearSelection()

        event.accept()

    def load_patients(self):
        cursor = self.conn.cursor()
        self.conn.commit()
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
            patient_id = QTableWidgetItem(str(patient[0]))
            fname = QTableWidgetItem(str(patient[1]))
            lname = QTableWidgetItem(str(patient[2]))
            phone = QTableWidgetItem(str(patient[3]))

            patient_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            fname.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            lname.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            phone.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.patients_table.setItem(row_id, 0, patient_id)
            self.patients_table.setItem(row_id, 1, fname)
            self.patients_table.setItem(row_id, 2, lname)
            self.patients_table.setItem(row_id, 3, phone)
