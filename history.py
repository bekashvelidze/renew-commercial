from connection import Database
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QColor
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt

db = Database()
conn = db.connect()


class PatientHistory(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/history.ui", self)
        self.search = self.search_patient.text()
        self.search_button.clicked.connect(self.search_client)
        self.patient_history.setColumnCount(4)

        self.patient_history.setColumnWidth(0, 140)
        self.patient_history.setColumnWidth(1, 90)
        self.patient_history.setColumnWidth(2, 60)
        self.patient_history.setColumnWidth(3, 748)

    def search_client(self):
        self.patient_history.clearContents()
        search = self.search_patient.text()
        conn.commit()
        cursor70 = conn.cursor()
        cursor70.execute("SELECT * FROM patient_history WHERE phone=%s", (search,))

        if cursor70.rowcount == 0:
            QMessageBox.warning(self, "შეცდომა",
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გადაამოწმეთ ნომერი.")
            self.search_patient.clear()
        else:
            self.patient_history.setRowCount(cursor70.rowcount)
            row = 0
            for client in cursor70:
                self.patient.setText(client[1])
                self.phone.setText(client[5])
                self.patient_history.setItem(row, 0, QTableWidgetItem(client[2]))
                self.patient_history.setItem(row, 1, QTableWidgetItem(client[3]))
                self.patient_history.setItem(row, 2, QTableWidgetItem(client[4]))
                self.patient_history.setItem(row, 3, QTableWidgetItem(client[6]))
                if client[2] == "კოსმეტოლოგია":
                    self.patient_history.item(row, 0).setBackground(QColor(255, 251, 193))
                    self.patient_history.item(row, 1).setBackground(QColor(255, 251, 193))
                    self.patient_history.item(row, 2).setBackground(QColor(255, 251, 193))
                    self.patient_history.item(row, 3).setBackground(QColor(255, 251, 193))
                elif client[2] == "ლაზერი":
                    self.patient_history.item(row, 0).setBackground(QColor(226, 246, 202))
                    self.patient_history.item(row, 1).setBackground(QColor(226, 246, 202))
                    self.patient_history.item(row, 2).setBackground(QColor(226, 246, 202))
                    self.patient_history.item(row, 3).setBackground(QColor(226, 246, 202))
                elif client[2] == "სოლარიუმი 1":
                    self.patient_history.item(row, 0).setBackground(QColor(184, 231, 225))
                    self.patient_history.item(row, 1).setBackground(QColor(184, 231, 225))
                    self.patient_history.item(row, 2).setBackground(QColor(184, 231, 225))
                    self.patient_history.item(row, 3).setBackground(QColor(184, 231, 225))
                elif client[2] == "სოლარიუმი 2":
                    self.patient_history.item(row, 0).setBackground(QColor(255, 222, 222))
                    self.patient_history.item(row, 1).setBackground(QColor(255, 222, 222))
                    self.patient_history.item(row, 2).setBackground(QColor(255, 222, 222))
                    self.patient_history.item(row, 3).setBackground(QColor(255, 222, 222))
                row += 1
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.search_client()
        else:
            super().keyPressEvent(event)