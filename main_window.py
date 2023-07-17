import json
import datetime
import locale
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QDialog
from PyQt6.uic import loadUi
from connection import Database
from subscription import Subscription

locale.setlocale(locale.LC_ALL, "ka_GE.utf-8")
today = datetime.now().date().strftime("%d.%m.%Y")
db = Database()


def load_settings():
    with open("settings.json", "r", encoding="utf-8") as data:
        settings = json.load(data)
    return settings


def load_times():
    with open("times.json", "r", encoding="utf-8") as file:
        times = json.load(file)

    return times


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)
        self.settings = load_settings()
        self.load_data()
        self.tabWidget.currentChanged.connect(self.load_data)
        # Cosmetics
        self.cos_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.cos_new_date.dateChanged.connect(self.change_date_cos)
        for doctor_cos in self.settings["კოსმეტოლოგია"]["ექიმები"]:
            self.cos_doctor.addItem(doctor_cos)
        for zone_cos in self.settings["კოსმეტოლოგია"]["პროცედურები"]:
            self.cos_zone.addItem(zone_cos)
        # Laser
        self.las_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.las_new_date.dateChanged.connect(self.change_date_las)
        for doctor_las in self.settings["ლაზერი"]["ექიმები"]:
            self.las_doctor.addItem(doctor_las)
        for type_las in self.settings["ლაზერი"]["ლაზერის ტიპები"]:
            self.las_type.addItem(type_las)
        for zone_las in self.settings["ლაზერი"]["ზონები"]:
            self.las_zone.addItem(zone_las)
        # Solarium 1
        self.sol_1_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.sol_1_new_date.dateChanged.connect(self.change_date_sol_1)
        # Solarium 2
        self.sol_2_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.sol_2_new_date.dateChanged.connect(self.change_date_sol_2)
        # Button click events
        self.cos_make_an_appointment_button.clicked.connect(self.make_an_appointment_cos)
        self.las_make_an_appointment_button.clicked.connect(self.make_an_appointment_las)
        self.sol_1_make_an_appointment_button.clicked.connect(self.make_an_appointment_sol_1)
        self.sol_2_make_an_appointment_button.clicked.connect(self.make_an_appointment_sol_2)
        self.sol_1_buy_subscription_button.clicked.connect(self.sol_1_buy_subscription)
        self.sol_2_buy_subscription_button.clicked.connect(self.sol_2_buy_subscription)
        # Cell click events
        self.cos_appointments.cellClicked.connect(self.get_cos_cell_information)
        self.las_appointments.cellClicked.connect(self.get_las_cell_information)
        self.sol_1_appointments.cellClicked.connect(self.get_sol_1_cell_information)
        self.sol_2_appointments.cellClicked.connect(self.get_sol_2_cell_information)

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

    # კოსმეტოლოგია

    def change_date_cos(self):
        global today

        today = self.cos_new_date.text()
        self.current_date.clear()
        self.current_date.setText(today)
        self.cos_appointments.clearContents()
        self.load_data()

    def cosmetology(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `cosmetology_appointments` WHERE date=%s", (today,))
        times = load_times()
        self.cos_date.setText(self.cos_new_date.text())

        self.cos_patients.setText(str(cursor.rowcount))
        self.cos_current_day.setText(datetime.now().strftime("%A"))
        self.current_date.setText(datetime.now().date().strftime("%d.%m.%Y"))

        self.cos_appointments.setColumnWidth(0, 300)
        self.cos_appointments.setColumnWidth(1, 120)
        self.cos_appointments.setColumnWidth(2, 180)
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

    def get_cos_cell_information(self):
        current_row = self.cos_appointments.currentRow()
        current_column = self.cos_appointments.currentColumn()
        time = self.cos_appointments.verticalHeaderItem(current_row).text()
        date = self.cos_new_date.text()
        self.cos_time.setText(time)
        self.cos_date.setText(date)
        if self.cos_appointments.item(current_row, current_column):
            QMessageBox.information(self, "დრო დაკავებულია", "ეს დრო დაკავებულია, აირჩიეთ სხვა დრო.")
        else:
            print("empty")

    def make_an_appointment_cos(self):
        conn = db.connect()
        first_name = self.cos_fname.text()
        last_name = self.cos_lname.text()
        phone = self.cos_phone.text()
        zone = self.cos_zone.currentText()
        doctor = self.cos_doctor.currentText()
        date = self.cos_date.text()
        time = self.cos_time.text()
        if self.cos_time.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        else:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cosmetology_appointments (procedure_name, fname, lname, phone, doctor, date, time) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)", (zone, first_name, last_name, phone, doctor, date, time))
            self.cos_fname.clear()
            self.cos_lname.clear()
            self.cos_phone.clear()
            self.cos_doctor.clear()
            for doctor_cos in self.settings["კოსმეტოლოგია"]["ექიმები"]:
                self.cos_doctor.addItem(doctor_cos)
            for zone_cos in self.settings["კოსმეტოლოგია"]["პროცედურები"]:
                self.cos_zone.addItem(zone_cos)
            conn.commit()

            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                "VALUES (?, ?, ?)", (first_name, last_name, phone))
                conn.commit()
            else:
                client_phones = [client[3] for client in cursor2]
                if phone not in client_phones:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                    "VALUES (?, ?, ?)", (first_name, last_name, phone))
                    conn.commit()
            conn.close()

            QMessageBox.information(self, 'პაციენტი ჩაიწერა',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}")
            self.load_data()

    # ლაზერი
    def change_date_las(self):
        global today
        today = self.las_new_date.text()
        self.current_date.clear()
        self.las_current_date.setText(today)
        self.las_appointments.clearContents()
        self.load_data()

    def laser(self):
        db = Database()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `laser_appointments` WHERE date=%s", (today,))
        times = load_times()
        self.las_date.setText(self.las_new_date.text())

        self.las_patients.setText(str(cursor.rowcount))
        self.las_current_day.setText(datetime.now().strftime("%A"))
        self.las_current_date.setText(datetime.now().date().strftime("%d.%m.%Y"))

        self.las_appointments.setColumnWidth(0, 160)
        self.las_appointments.setColumnWidth(1, 170)
        self.las_appointments.setColumnWidth(2, 120)
        self.las_appointments.setColumnWidth(3, 180)
        self.las_appointments.setColumnWidth(4, 120)
        self.las_appointments.setColumnWidth(5, 190)

        row = 0
        for las in cursor:
            self.las_appointments.setItem(int(times[las[8]]), 0, QTableWidgetItem(las[1]))
            self.las_appointments.setItem(int(times[las[8]]), 1, QTableWidgetItem(las[2]))
            self.las_appointments.setItem(int(times[las[8]]), 2, QTableWidgetItem(las[3]))
            self.las_appointments.setItem(int(times[las[8]]), 3, QTableWidgetItem(las[4]))
            self.las_appointments.setItem(int(times[las[8]]), 4, QTableWidgetItem(las[5]))
            self.las_appointments.setItem(int(times[las[8]]), 5, QTableWidgetItem(las[6]))

            row += 1

    def get_las_cell_information(self):
        current_row = self.las_appointments.currentRow()
        current_column = self.las_appointments.currentColumn()
        time = self.las_appointments.verticalHeaderItem(current_row).text()
        date = self.las_new_date.text()
        self.las_time.setText(time)
        self.las_date.setText(date)
        if self.las_appointments.item(current_row, current_column):
            QMessageBox.information(self, "დრო დაკავებულია", "ეს დრო დაკავებულია, აირჩიეთ სხვა დრო.")
        else:
            print("empty")

    def make_an_appointment_las(self):
        conn = db.connect()
        first_name = self.las_fname.text()
        last_name = self.las_lname.text()
        phone = self.las_phone.text()
        laser_type = self.las_type.currentText()
        zone = self.las_zone.currentText()
        doctor = self.las_doctor.currentText()
        date = self.las_date.text()
        time = self.las_time.text()

        if self.las_time.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO laser_appointments (laser_type, zone, fname, lname, phone, doctor, date, time) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (laser_type, zone, first_name, last_name, phone, doctor, date, time))
            self.las_fname.clear()
            self.las_lname.clear()
            self.las_phone.clear()
            for doctor_las in self.settings["ლაზერი"]["ექიმები"]:
                self.las_doctor.addItem(doctor_las)
            for type_las in self.settings["ლაზერი"]["ლაზერის ტიპები"]:
                self.las_type.addItem(type_las)
            for zone_las in self.settings["ლაზერი"]["ზონები"]:
                self.las_zone.addItem(zone_las)

            conn.commit()
            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                "VALUES (?, ?, ?)", (first_name, last_name, phone))
                conn.commit()
            else:
                client_phones = [client[3] for client in cursor2]
                if phone not in client_phones:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                    "VALUES (?, ?, ?)", (first_name, last_name, phone))
                    conn.commit()
            conn.close()

            QMessageBox.information(self, 'პაციენტი ჩაიწერა',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}")
            self.load_data()

    # სოლარიუმი 1
    def change_date_sol_1(self):
        global today
        today = self.sol_1_new_date.text()
        self.sol_1_current_date.clear()
        self.sol_1_current_date.setText(today)
        self.sol_1_appointments.clearContents()
        self.load_data()

    def solarium_1(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `solarium_1_appointments` WHERE date=%s", (today,))
        times = load_times()
        self.sol_1_date.setText(self.sol_1_new_date.text())

        self.sol_1_patients.setText(str(cursor.rowcount))
        self.sol_1_current_day.setText(datetime.now().strftime("%A"))
        self.sol_1_current_date.setText(datetime.now().date().strftime("%d.%m.%Y"))

        self.sol_1_appointments.setColumnWidth(0, 230)
        self.sol_1_appointments.setColumnWidth(1, 230)
        self.sol_1_appointments.setColumnWidth(2, 230)
        self.sol_1_appointments.setColumnWidth(3, 230)

        row = 0
        for sol_1 in cursor:
            self.sol_1_appointments.setItem(int(times[sol_1[6]]), 0, QTableWidgetItem(sol_1[1]))
            self.sol_1_appointments.setItem(int(times[sol_1[6]]), 1, QTableWidgetItem(sol_1[2]))
            self.sol_1_appointments.setItem(int(times[sol_1[6]]), 2, QTableWidgetItem(sol_1[3]))
            self.sol_1_appointments.setItem(int(times[sol_1[6]]), 3, QTableWidgetItem(str(sol_1[4])))

            row += 1

    def get_sol_1_cell_information(self):
        current_row = self.sol_1_appointments.currentRow()
        current_column = self.sol_1_appointments.currentColumn()
        time = self.sol_1_appointments.verticalHeaderItem(current_row).text()
        date = self.sol_1_new_date.text()
        self.sol_1_time.setText(time)
        self.sol_1_date.setText(date)
        if self.sol_1_appointments.item(current_row, current_column):
            QMessageBox.information(self, "დრო დაკავებულია", "ეს დრო დაკავებულია, აირჩიეთ სხვა დრო.")
        else:
            print("empty")

    def make_an_appointment_sol_1(self):
        conn = db.connect()
        first_name = self.sol_1_fname.text()
        last_name = self.sol_1_lname.text()
        phone = self.sol_1_phone.text()
        minutes = self.sol_1_minutes.text()
        date = self.sol_1_date.text()
        time = self.sol_1_time.text()
        if self.sol_1_time.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO solarium_1_appointments (fname, lname, phone, minutes, date, time) "
                           "VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, minutes, date, time))
            self.sol_1_fname.clear()
            self.sol_1_lname.clear()
            self.sol_1_phone.clear()
            self.sol_1_minutes.clear()

            conn.commit()
            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                "VALUES (?, ?, ?)", (first_name, last_name, phone))
                conn.commit()
            else:
                client_phones = [client[3] for client in cursor2]
                if phone not in client_phones:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                    "VALUES (?, ?, ?)", (first_name, last_name, phone))
                    conn.commit()
            conn.close()
            QMessageBox.information(self, 'პაციენტი ჩაიწერა',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}"
                                    f"\nწუთები: {minutes}")
            self.load_data()

    def sol_1_buy_subscription(self):
        subs = Subscription()
        subs.buy_subscription()

    # სოლარიუმი 2
    def change_date_sol_2(self):
        global today

        today = self.sol_2_new_date.text()
        self.sol_2_current_date.clear()
        self.sol_2_current_date.setText(today)
        self.sol_2_appointments.clearContents()
        self.load_data()

    def solarium_2(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `solarium_2_appointments` WHERE date=%s", (today,))
        times = load_times()
        self.sol_2_date.setText(self.sol_2_new_date.text())

        self.sol_2_patients.setText(str(cursor.rowcount))
        self.sol_2_current_day.setText(datetime.now().strftime("%A"))
        self.sol_2_current_date.setText(datetime.now().date().strftime("%d.%m.%Y"))

        self.sol_2_appointments.setColumnWidth(0, 230)
        self.sol_2_appointments.setColumnWidth(1, 230)
        self.sol_2_appointments.setColumnWidth(2, 230)
        self.sol_2_appointments.setColumnWidth(3, 230)

        row = 0
        for sol_2 in cursor:
            self.sol_2_appointments.setItem(int(times[sol_2[6]]), 0, QTableWidgetItem(sol_2[1]))
            self.sol_2_appointments.setItem(int(times[sol_2[6]]), 1, QTableWidgetItem(sol_2[2]))
            self.sol_2_appointments.setItem(int(times[sol_2[6]]), 2, QTableWidgetItem(sol_2[3]))
            self.sol_2_appointments.setItem(int(times[sol_2[6]]), 3, QTableWidgetItem(str(sol_2[4])))

            row += 1

    def get_sol_2_cell_information(self):
        current_row = self.sol_2_appointments.currentRow()
        current_column = self.sol_2_appointments.currentColumn()
        time = self.sol_2_appointments.verticalHeaderItem(current_row).text()
        date = self.sol_2_new_date.text()
        self.sol_2_time.setText(time)
        self.sol_2_date.setText(date)
        if self.sol_2_appointments.item(current_row, current_column):
            QMessageBox.information(self, "დრო დაკავებულია", "ეს დრო დაკავებულია, აირჩიეთ სხვა დრო.")
        else:
            print("empty")

    def make_an_appointment_sol_2(self):
        conn = db.connect()
        first_name = self.sol_2_fname.text()
        last_name = self.sol_2_lname.text()
        phone = self.sol_2_phone.text()
        minutes = self.sol_2_minutes.text()
        date = self.sol_2_date.text()
        time = self.sol_2_time.text()
        if self.sol_2_time.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO solarium_2_appointments (fname, lname, phone, minutes, date, time) "
                           "VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, minutes, date, time))
            self.sol_2_fname.clear()
            self.sol_2_lname.clear()
            self.sol_2_phone.clear()
            self.sol_2_minutes.clear()
            conn.commit()

            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                "VALUES (?, ?, ?)", (first_name, last_name, phone))
                conn.commit()
            else:
                client_phones = [client[3] for client in cursor2]
                if phone not in client_phones:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                    "VALUES (?, ?, ?)", (first_name, last_name, phone))
                    conn.commit()
            conn.close()

            QMessageBox.information(self, 'პაციენტი ჩაიწერა',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}"
                                    f"\nწუთები: {minutes}")
            self.load_data()

    def sol_2_buy_subscription(self):
        subs = Subscription()

