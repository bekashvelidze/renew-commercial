import json
import datetime
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from connection import Database


def load_services():
    with open("services.json", "r", encoding="utf-8") as file:
        services = json.load(file)

    return services


def load_times():
    with open("times.json", "r", encoding="utf-8") as file:
        times = json.load(file)

    return times


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)
        self.load_data()
        # self.load_data(self.tabWidget.tabText(self.tabWidget.currentIndex()))
        self.tabWidget.currentChanged.connect(self.load_data)
        self.cos_make_an_appointment_button.clicked.connect(self.make_an_appointment_cos)
        self.cos_appointments.cellClicked.connect(self.get_cell_information)

    def load_data(self):
        service = self.tabWidget.tabText(self.tabWidget.currentIndex())
        if service == "კოსმეტოლოგია":
            self.cosmetology()
        elif service == "ლაზერი":
            self.laser()
        elif service == "სოლარიუმი 1":
            self.solarium_1()
        elif service == "სოლარიუმი 2":
            self.solarium_2()

    def cosmetology(self):
        db = Database()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `cosmetology_appointments`")
        times = load_times()
        self.cos_patients.setText(str(cursor.rowcount))


        self.cos_appointments.setColumnWidth(0, 200)
        self.cos_appointments.setColumnWidth(1, 130)
        self.cos_appointments.setColumnWidth(2, 150)
        self.cos_appointments.setColumnWidth(3, 120)
        self.cos_appointments.setColumnWidth(4, 220)

        row = 0
        for cos in cursor:
            self.cos_appointments.setItem(int(times[cos[7]]), 0, QTableWidgetItem(cos[1]))
            self.cos_appointments.setItem(int(times[cos[7]]), 1, QTableWidgetItem(cos[2]))
            self.cos_appointments.setItem(int(times[cos[7]]), 2, QTableWidgetItem(cos[3]))
            self.cos_appointments.setItem(int(times[cos[7]]), 3, QTableWidgetItem(cos[4]))
            self.cos_appointments.setItem(int(times[cos[7]]), 4, QTableWidgetItem(cos[5]))

            row += 1

        conn.close()
    def laser(self):
        db = Database()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `laser_appointments`")
        times = load_times()

        self.las_appointments.setColumnWidth(0, 170)
        self.las_appointments.setColumnWidth(1, 140)
        self.las_appointments.setColumnWidth(2, 120)
        self.las_appointments.setColumnWidth(3, 120)
        self.las_appointments.setColumnWidth(4, 120)
        self.las_appointments.setColumnWidth(5, 150)

        row = 0
        for las in cursor:
            self.las_appointments.setItem(int(times[las[8]]), 0, QTableWidgetItem(las[1]))
            self.las_appointments.setItem(int(times[las[8]]), 1, QTableWidgetItem(las[2]))
            self.las_appointments.setItem(int(times[las[8]]), 2, QTableWidgetItem(las[3]))
            self.las_appointments.setItem(int(times[las[8]]), 3, QTableWidgetItem(las[4]))
            self.las_appointments.setItem(int(times[las[8]]), 4, QTableWidgetItem(las[5]))
            self.las_appointments.setItem(int(times[las[8]]), 5, QTableWidgetItem(las[6]))

            row += 1

    def solarium_1(self):
        db = Database()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `laser_appointments`")
        times = load_times()

        self.las_appointments.setColumnWidth(0, 200)
        self.las_appointments.setColumnWidth(1, 140)
        self.las_appointments.setColumnWidth(2, 130)
        self.las_appointments.setColumnWidth(3, 120)
        self.las_appointments.setColumnWidth(4, 160)
        self.las_appointments.setColumnWidth(5, 120)
        self.las_appointments.setColumnWidth(6, 120)

        row = 0
        for las in cursor:
            self.las_appointments.setItem(int(times[las[8]]), 0, QTableWidgetItem(las[1]))
            self.las_appointments.setItem(int(times[las[8]]), 1, QTableWidgetItem(las[2]))
            self.las_appointments.setItem(int(times[las[8]]), 2, QTableWidgetItem(las[3]))
            self.las_appointments.setItem(int(times[las[8]]), 3, QTableWidgetItem(las[4]))
            self.las_appointments.setItem(int(times[las[8]]), 4, QTableWidgetItem(las[5]))
            self.las_appointments.setItem(int(times[las[8]]), 5, QTableWidgetItem(las[6]))
            self.las_appointments.setItem(int(times[las[8]]), 5, QTableWidgetItem(str(las[9])))

            row += 1

    def solarium_2(self):
        print("სოლარიუმი 2")

    def get_cell_information(self):
        current_row = self.cos_appointments.currentRow()
        current_column = self.cos_appointments.currentColumn()
        time = self.cos_appointments.verticalHeaderItem(current_row).text()
        date = datetime.now().date().strftime("%d.%m.%Y")
        self.cos_time.setText(time)
        self.cos_date.setText(date)
        if self.cos_appointments.item(current_row, current_column):
            QMessageBox.information(self, "დრო დაკავებულია", "ეს დრო დაკავებულია, აირჩიეთ სხვა დრო.")
        else:
            print("empty")

    def make_an_appointment_cos(self):

        first_name = self.cos_fname.text()
        last_name = self.cos_lname.text()
        phone = self.cos_phone.text()
        zone = self.cos_zone.currentText()
        doctor = self.cos_doctor.currentText()
        date = self.cos_date.text()
        time = self.cos_time.text()

        db = Database()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cosmetology_appointments (procedure_name, fname, lname, phone, doctor, date, time) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?)", (zone, first_name, last_name, phone, doctor, date, time))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'პაციენტი ჩაიწერა',
                                f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                f"\nდრო: {time}")
        self.load_data()

    def buy_subscription(self):
        #TODO 2: ახალი ფანჯარა, სახელი, გვარი, წუთების რაოდენობა
        # იხსნება ცხრილი 'clients', მოწმდება კლიენტის ნომრის მიხედვით წუთების რაოდენობა, ემატება და კეთდება 'UPDATE"
        # იხურება ფანჯარა და ბრუნდება ძირითად ფანჯარაში
        QMessageBox.information(self, 'აბონემენტის შეძება',
                                f"აბონემენტი დარეგისტრირებულია:"
                                f"\nსახელი, გვარი: {self.clients[0]['name']} {self.clients[0]['lname']}\nწუთი: 50")
        