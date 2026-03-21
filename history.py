from connection import Database
from helpers_functions import critical_error
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QColor
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt

db = Database()


class PatientHistory(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/history.ui", self)
        self.showMaximized()
        self.patient_history.setColumnWidth(0, 150)
        self.patient_history.horizontalHeader().setStretchLastSection(True)

        self.conn = db.connect()

        self.search_button.clicked.connect(self.search_client)

    def search_client(self):
        search = self.search_patient.text().strip()
        if not search:
            return

        self.patient_history.setRowCount(0)
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM patient_history WHERE phone=%s ORDER BY date DESC", (search,))
            records = cursor.fetchall()

            if not records:
                QMessageBox.warning(self, "შეცდომა",
                                    f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გადაამოწმეთ ნომერი.")
                self.search_patient.clear()
                return

            self.patient_history.setRowCount(len(records))

            color_map = {
                "კოსმეტოლოგია": QColor(255, 251, 193),
                "ლაზერი": QColor(226, 264, 202),
                "სოლარიუმი 1": QColor(184, 231, 225),
                "სოლარიუმი 2": QColor(255, 222, 222)
            }
            for row, client in enumerate(records):
                self.phone.setText(f"ტელეფონი: {client[5]}")
                self.title.setText(f"პაციენტის ისტორია [{client[1]}]")

                columns = [2, 3, 4, 6]
                category = client[2]
                row_color = color_map.get(category, QColor("white"))

                for col_id, data_id in enumerate(columns):
                    item = QTableWidgetItem(str(client[data_id]))
                    item.setBackground(row_color)
                    self.patient_history.setItem(row, col_id, item)

        except Exception as e:
            critical_error(f"მონაცემთა ბაზასთან კავშირი პრობლემა - {e}")

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.search_client()
        else:
            super().keyPressEvent(event)