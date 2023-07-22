from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from connection import Database

db = Database()

class Settings(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/settings.ui", self)
        self.conn = db.connect()
        # Load data to tables
        self.load_doctors()
        self.load_zones()
        self.load_procedures()
        self.add_doctor_button.clicked.connect(self.add_doctor)
        self.add_zone_button.clicked.connect(self.add_zone)
        self.add_procedure_button.clicked.connect(self.add_procedure)

    def load_doctors(self):
        # Load doctors
        self.doc_category.setCurrentText('აირჩიეთ კატეგორია')
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        doctors_list = []
        if cursor.rowcount != 0:
            doctors_list = [doctor for doctor in cursor]
        self.doctors.setColumnWidth(0, 190)
        self.doctors.setColumnWidth(1, 100)
        self.doctors.setColumnWidth(2, 130)
        self.doctors.setRowCount(len(doctors_list))
        self.doctors.setColumnCount(3)
        doc_row = 0
        for doctor in doctors_list:
            self.doctors.setItem(doc_row, 0, QTableWidgetItem(doctor[1]))
            self.doctors.setItem(doc_row, 1, QTableWidgetItem(doctor[2]))
            self.doctors.setItem(doc_row, 2, QTableWidgetItem(doctor[3]))
            doc_row += 1

    def load_zones(self):
        # Load zones
        cursor2 = self.conn.cursor()
        cursor2.execute("SELECT * FROM zones")
        zones = []
        if cursor2.rowcount != 0:
            zones = [zone for zone in cursor2]
        self.zones.setColumnWidth(0, 400)
        self.zones.setRowCount(len(zones))
        self.zones.setColumnCount(1)
        zone_row = 0
        for zone in zones:
            self.zones.setItem(zone_row, 0, QTableWidgetItem(zone[1]))
            zone_row += 1

    def load_procedures(self):
        # Load procedures_list
        cursor3 = self.conn.cursor()
        cursor3.execute("SELECT * FROM procedures")
        procedures = []
        if cursor3.rowcount != 0:
            procedures = [procedure for procedure in cursor3]
        self.procedures.setColumnWidth(0, 400)
        self.procedures.setRowCount(len(procedures))
        self.procedures.setColumnCount(1)
        proc_row = 0
        for procedure in procedures:
            self.procedures.setItem(proc_row, 0, QTableWidgetItem(procedure[1]))
            proc_row += 1

    def add_doctor(self):
        new_doctor = self.doc_fname_lname.text()
        phone = self.doc_phone.text()
        category = self.doc_category.currentText()

        if self.doc_fname_lname.text() == 0:
            QMessageBox.warning(self, 'შეცდომა', 'ჩაწერეთ ექიმის სახელი და გვარი.')
        elif self.doc_category.currentText() == "აირჩიეთ კატეგორია":
            QMessageBox.warning(self, 'შეცდომა', 'აირჩიეთ კატეგორია.')
        else:
            cursor4 = self.conn.cursor()
            cursor4.execute("INSERT INTO doctors (doctor, phone, category) "
                            "VALUES (?, ?, ?)", (new_doctor, phone, category))
            self.conn.commit()

            self.doc_fname_lname.clear()
            self.doc_phone.clear()
            self.doc_category.setCurrentText('აირჩიეთ კატეგორია')

            QMessageBox.information(self, 'ახალი ექიმის დამატება', 'ახალი ექიმი დაემატა ბაზაში.')
            self.doctors.clearContents()
            self.load_doctors()

    def add_zone(self):
        new_zone = self.zone_name.text()

        if self.zone_name.text() == 0:
            QMessageBox.warning(self, 'შეცდომა', 'ჩაწერეთ ზონის სახელი.')
        else:
            cursor5 = self.conn.cursor()
            cursor5.execute("INSERT INTO zones (zone) VALUES (?)", (new_zone,))
            self.conn.commit()

            self.zone_name.clear()
            QMessageBox.information(self, 'ახალი ზონის დამატება', 'ახალი ზონა დაემატა ბაზაში.')
            self.zone_name.clear()
            self.zones.clearContents()
            self.load_zones()

    def add_procedure(self):
        new_procedure = self.procedure_name.text()

        if self.procedure_name.text() == 0:
            QMessageBox.warning(self, 'შეცდომა', 'ჩაწერეთ პროცედურის სახელი.')
        else:
            cursor6 = self.conn.cursor()
            cursor6.execute("INSERT INTO procedures (procedure_name) "
                            "VALUES (?)", (new_procedure,))
            self.conn.commit()

            self.procedure_name.clear()

            QMessageBox.information(self, 'ახალი პროცედურის დამატება', 'ახალი პროცედურა დაემატა ბაზაში.')
            self.procedure_name.clear()
            self.procedures.clearContents()
            self.load_procedures()
