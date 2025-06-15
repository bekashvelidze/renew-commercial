from PyQt6.QtGui import QIcon

from connection import Database
from patient_edit import PatientsEdit
from PyQt6.QtWidgets import QWidget, QPushButton, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi


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
        patients = [patient for patient in cursor if cursor.rowcount != 0]

        # self.patients_table.setColumnWidth(0, 110)
        self.patients_table.setColumnWidth(0, 30)
        self.patients_table.setColumnWidth(1, 150)
        self.patients_table.setColumnWidth(2, 170)
        self.patients_table.setColumnWidth(3, 170)
        self.patients_table.setRowCount(len(patients))
        self.patients_num.setText(f"სულ რეგისტრირებულია {str(len(patients))} პაციენტი.")
        self.patients_table.setColumnCount(4)
        patients_row = 0
        for patient in patients:
            # btn_edit = QPushButton(self)
            # btn_edit.setText("რედაქტირება")
            # btn_edit.setStyleSheet("color: red; font-weight: bold;")
            # btn_edit.pressed.connect(self.edit_patient)
            # btn_delete = QPushButton(self)
            # btn_delete.setText("რედაქტირება")
            # btn_delete.setStyleSheet("color: red; font-weight: bold;")
            # btn_delete.pressed.connect(self.delete_patient)
            # self.patients_table.setCellWidget(patients_row, 0, btn_delete)
            # self.patients_table.setCellWidget(patients_row, 0, btn_edit)
            self.patients_table.setItem(patients_row, 0, QTableWidgetItem(str(patient[0])))
            self.patients_table.setItem(patients_row, 1, QTableWidgetItem(patient[1]))
            self.patients_table.setItem(patients_row, 2, QTableWidgetItem(patient[2]))
            self.patients_table.setItem(patients_row, 3, QTableWidgetItem(patient[3]))
            patients_row += 1

    # Reserved functions

    # def edit_patient(self):
    #     current_row = self.patients_table.currentRow()
    #     num = int(self.patients_table.item(current_row, 1).text())
    #     self.patients_edit_window = PatientsEdit(num)
    #     self.patients_edit_window.setFixedWidth(560)
    #     self.patients_edit_window.setFixedHeight(275)
    #     x = (self.patients_edit_window.screen().availableGeometry().width() // 2) - (self.patients_edit_window.width() // 2)
    #     y = (self.patients_edit_window.screen().availableGeometry().height() // 2) - (self.patients_edit_window.height() // 2)
    #     self.patients_edit_window.move(x, y)
    #     self.patients_edit_window.setWindowTitle("პაციენტის რედაქტირება")
    #     self.patients_edit_window.setWindowIcon(QIcon("ui/renew.ico"))
    #     self.patients_edit_window.show()
    #     self.patients_edit_window.load_patient()

    # def delete_patient(self):
    #     current_row = self.patients_table.currentRow()
    #     num = int(self.patients_table.item(current_row, 1).text())
    #     cursor101 = self.conn.cursor()
    #     cursor101.execute("DELETE FROM `clients` WHERE id=%s", (num,))
    #     self.conn.commit()
    #     QMessageBox.information(self,
    #                             "პაციენტის წაშლა ბაზიდან",
    #                             f"პაციენტის {self.patients_table.item(current_row, 1).text()}"
    #                             f" {self.patients_table.item(current_row, 2).text()} წაიშალა ბაზიდან")
    #     self.load_patients()
