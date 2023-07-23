import sys
import json
import datetime
import webbrowser
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon
from connection import Database
from settings import Settings
from subscription import Subscription
from funds import Funds
from about import About


today = datetime.now().date().strftime("%d.%m.%Y")
db = Database()


def open_documentation():
    webbrowser.open('https://nextcloud.org.ge/renew_documentation')


def check_integer(number):
    try:
        if int(number):
            return True
    except ValueError:
        return False


def load_procedures():
    conn = db.connect()
    cursor_procedures = conn.cursor()
    cursor_procedures.execute("SELECT * FROM procedures")

    return cursor_procedures


def load_doctors(category):
    conn = db.connect()
    cursor_doctors = conn.cursor()
    cursor_doctors.execute("SELECT * FROM doctors WHERE category=%s", (category,))

    return cursor_doctors


def load_zones():
    conn = db.connect()
    cursor_zones = conn.cursor()
    cursor_zones.execute("SELECT * FROM zones")

    return cursor_zones


def load_types():
    conn = db.connect()
    cursor_types = conn.cursor()
    cursor_types.execute("SELECT * FROM types")

    return cursor_types


def load_times():
    with open("times.json", "r", encoding="utf-8") as file:
        times = json.load(file)

    return times


def load_days():
    with open("days.json", "r", encoding="utf-8") as file:
        days = json.load(file)

    return days


def close_main_application():
    sys.exit()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)
        self.procedures = load_procedures()
        self.load_data()
        self.tabWidget.currentChanged.connect(self.load_data)
        self.settings_window_open = Settings()
        self.subs_window = Subscription()
        self.funds_window = Funds()
        self.about = About()
        # Menu items
        self.close_application.triggered.connect(close_main_application)
        self.change_settings.triggered.connect(self.settings_window)
        self.documentation.triggered.connect(open_documentation)
        self.about_menu.triggered.connect(self.about_window)
        # Cosmetics
        self.cos_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.cos_new_date.dateChanged.connect(self.change_date_cos)
        self.doctors_cos = load_doctors("კოსმეტოლოგია")
        for doctor_cos in self.doctors_cos:
            self.cos_doctor.addItem(doctor_cos[1])
        self.procedures = load_procedures()
        for zone_cos in self.procedures:
            self.cos_zone.addItem(zone_cos[1])
        # Laser
        self.las_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.las_new_date.dateChanged.connect(self.change_date_las)
        self.doctors_las = load_doctors("ლაზერი")
        for doctor_las in self.doctors_las:
            self.las_doctor.addItem(doctor_las[1])
        self.laser_types = load_types()
        for type_las in self.laser_types:
            self.las_type.addItem(type_las[1])
        self.zones = load_zones()
        for zone_las in self.zones:
            self.las_zone.addItem(zone_las[1])
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
        self.sol_1_buy_subscription_button.clicked.connect(self.buy_subscription)
        self.sol_2_buy_subscription_button.clicked.connect(self.buy_subscription)
        self.cos_pay_button.clicked.connect(self.funds)
        self.las_pay_button.clicked.connect(self.funds)
        self.sol_1_pay_button.clicked.connect(self.funds)
        self.sol_2_pay_button.clicked.connect(self.funds)
        # Cell click events
        self.cos_appointments.cellClicked.connect(self.get_cos_cell_information)
        self.las_appointments.cellClicked.connect(self.get_las_cell_information)
        self.sol_1_appointments.cellClicked.connect(self.get_sol_1_cell_information)
        self.sol_2_appointments.cellClicked.connect(self.get_sol_2_cell_information)
        # Placeholder
        self.cos_zone.setCurrentText("აირჩიეთ პროცედურა")
        self.cos_doctor.setCurrentText("აირჩიეთ ექიმი")
        self.las_type.setCurrentText("აირჩიეთ ლაზერის ტიპი")
        self.las_zone.setCurrentText("აირჩიეთ ზონა")
        self.las_doctor.setCurrentText("აირჩიეთ ექიმი")

    def load_data(self):
        self.cos_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.las_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.sol_1_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
        self.sol_2_new_date.setDate(datetime.strptime(today, "%d.%m.%Y"))
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
        self.cosmetology()

    def cosmetology(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `cosmetology_appointments` WHERE date=%s", (today,))
        times = load_times()
        self.cos_date.setText(self.cos_new_date.text())

        self.cos_patients.setText(str(cursor.rowcount))
        self.cos_current_day.setText(load_days()[datetime.now().strftime("%A")])
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

    def make_an_appointment_cos(self):
        doctors = [doctor[1] for doctor in load_doctors("კოსმეტოლოგია")]
        procedures = [procedure[1] for procedure in load_procedures()]
        conn = db.connect()
        first_name = self.cos_fname.text()
        last_name = self.cos_lname.text()
        phone = self.cos_phone.text()
        zone = self.cos_zone.currentText()
        doctor = self.cos_doctor.currentText()
        date = self.cos_date.text()
        time = self.cos_time.text()

        checked = check_integer(phone)

        if self.cos_time.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        elif self.cos_fname.text() == "" or self.cos_lname.text() == "" or self.cos_phone.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        elif not checked:
            QMessageBox.warning(self, 'შეცდომა', "ტელეფონის ველში მხოლოდ ციფრებია დაშვებული!")
        elif self.cos_zone.currentText() == "აირჩიეთ პროცედურა":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ პროცედურა.")
        elif self.cos_doctor.currentText() == "აირჩიეთ ექიმი":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ ექიმი.")
        else:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cosmetology_appointments (procedure_name, fname, lname, phone, doctor, date, time) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)", (zone, first_name, last_name, phone, doctor, date, time))
            self.cos_fname.clear()
            self.cos_lname.clear()
            self.cos_phone.clear()
            self.cos_doctor.clear()
            self.cos_zone.clear()
            self.cos_time.setText("")
            for doctor_cos in doctors:
                self.cos_doctor.addItem(doctor_cos)
            for zone_cos in procedures:
                self.cos_zone.addItem(zone_cos)
            conn.commit()

            balance = 0
            init_minutes = 0

            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                conn.commit()
            else:
                client_phones = [client[3] for client in cursor2]
                if phone not in client_phones:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                    "VALUES (?, ?, ?, ?, ?)",
                                    (first_name, last_name, phone, balance, init_minutes))
                    conn.commit()
            conn.close()

            self.cos_zone.setCurrentText("აირჩიეთ პროცედურა")
            self.cos_doctor.setCurrentText("აირჩიეთ ექიმი")

            QMessageBox.information(self, 'პაციენტი ჩაწერილია',
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
        self.laser()

    def laser(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `laser_appointments` WHERE date=%s", (today,))
        times = load_times()
        self.las_date.setText(self.las_new_date.text())

        self.las_patients.setText(str(cursor.rowcount))
        self.las_current_day.setText(load_days()[datetime.now().strftime("%A")])
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

    def make_an_appointment_las(self):
        doctors = [doctor[1] for doctor in load_doctors("ლაზერი")]
        types = [las_type for las_type in load_types()]
        zones = [zone for zone in load_zones()]
        conn = db.connect()
        first_name = self.las_fname.text()
        last_name = self.las_lname.text()
        phone = self.las_phone.text()
        laser_type = self.las_type.currentText()
        zone = self.las_zone.currentText()
        doctor = self.las_doctor.currentText()
        date = self.las_date.text()
        time = self.las_time.text()

        checked = check_integer(phone)

        if self.las_time.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        elif self.las_fname.text() == "" or self.las_lname.text() == "" or self.las_phone.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        elif not checked:
            QMessageBox.warning(self, 'შეცდომა', "ტელეფონის ველში მხოლოდ ციფრებია დაშვებული!")
        elif self.las_type.currentText() == "აირჩიეთ ლაზერის ტიპი":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ ლაზერის ტიპი.")
        elif self.las_zone.currentText() == "აირჩიეთ ზონა":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ ზონა.")
        elif self.las_doctor.currentText() == "აირჩიეთ ექიმი":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ ექიმი.")
        else:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO laser_appointments (laser_type, zone, fname, lname, phone, doctor, date, time) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (laser_type, zone, first_name, last_name, phone, doctor, date, time)
            )
            self.las_fname.clear()
            self.las_lname.clear()
            self.las_phone.clear()
            self.las_type.clear()
            self.las_zone.clear()
            self.las_doctor.clear()
            self.las_time.setText("")
            for doctor_las in doctors:
                self.las_doctor.addItem(doctor_las)
            for type_las in types:
                self.las_type.addItem(type_las[1])
            for zone_las in zones:
                self.las_zone.addItem(zone_las[1])

            balance = 0
            init_minutes = 0

            conn.commit()
            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                conn.commit()
            else:
                client_phones = [client[3] for client in cursor2]
                if phone not in client_phones:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                    "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                    conn.commit()
            conn.close()

            self.las_type.setCurrentText("აირჩიეთ ლაზერის ტიპი")
            self.las_zone.setCurrentText("აირჩიეთ ზონა")
            self.las_doctor.setCurrentText("აირჩიეთ ექიმი")

            QMessageBox.information(self, 'პაციენტი ჩაწერილია',
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
        self.solarium_1()

    def solarium_1(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `solarium_1_appointments` WHERE date=%s", (today,))
        times = load_times()
        self.sol_1_date.setText(self.sol_1_new_date.text())

        self.sol_1_patients.setText(str(cursor.rowcount))
        self.sol_1_current_day.setText(load_days()[datetime.now().strftime("%A")])
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

    def make_an_appointment_sol_1(self):
        conn = db.connect()
        first_name = self.sol_1_fname.text()
        last_name = self.sol_1_lname.text()
        phone = self.sol_1_phone.text()
        minutes = self.sol_1_minutes.text()
        date = self.sol_1_date.text()
        time = self.sol_1_time.text()

        checked_phone = check_integer(phone)
        checked_minutes = check_integer(minutes)

        if self.sol_1_time.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        elif self.sol_1_fname.text() == "" or self.sol_1_lname.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        elif self.sol_1_phone.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        elif not checked_phone:
            QMessageBox.warning(self, 'შეცდომა', "ტელეფონის ველში მხოლოდ ციფრებია დაშვებული!")
        elif self.sol_1_minutes.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        elif not checked_minutes:
            QMessageBox.warning(self, 'შეცდომა', "წუთების ველში მხოლოდ ციფრებია დაშვებული!")
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO solarium_1_appointments (fname, lname, phone, minutes, date, time) "
                           "VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, minutes, date, time))
            self.sol_1_fname.clear()
            self.sol_1_lname.clear()
            self.sol_1_phone.clear()
            self.sol_1_minutes.clear()
            self.sol_1_time.setText("")

            balance = 0
            init_minutes = 0

            conn.commit()
            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                conn.commit()
            else:
                client_phones = [client[3] for client in cursor2]
                if phone not in client_phones:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                    "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                    conn.commit()
            conn.close()
            QMessageBox.information(self, 'პაციენტი ჩაწერილია',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}"
                                    f"\nწუთები: {minutes}")
            self.load_data()

    # სოლარიუმი 2
    def change_date_sol_2(self):
        global today

        today = self.sol_2_new_date.text()
        self.sol_2_current_date.clear()
        self.sol_2_current_date.setText(today)
        self.sol_2_appointments.clearContents()
        self.solarium_2()

    def solarium_2(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `solarium_2_appointments` WHERE date=%s", (today,))
        times = load_times()
        self.sol_2_date.setText(self.sol_2_new_date.text())

        self.sol_2_patients.setText(str(cursor.rowcount))
        self.sol_2_current_day.setText(load_days()[datetime.now().strftime("%A")])
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

    def make_an_appointment_sol_2(self):
        conn = db.connect()
        first_name = self.sol_2_fname.text()
        last_name = self.sol_2_lname.text()
        phone = self.sol_2_phone.text()
        minutes = self.sol_2_minutes.text()
        date = self.sol_2_date.text()
        time = self.sol_2_time.text()

        checked_phone = check_integer(phone)
        checked_minutes = check_integer(minutes)

        if self.sol_2_time.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        elif self.sol_2_fname.text() == "" or self.sol_2_lname.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        elif self.sol_2_phone.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        elif not checked_phone:
            QMessageBox.warning(self, 'შეცდომა', "ტელეფონის ველში მხოლოდ ციფრებია დაშვებული!")
        elif self.sol_2_minutes.text() == "":
            QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        elif not checked_minutes:
            QMessageBox.warning(self, 'შეცდომა', "წუთების ველში მხოლოდ ციფრებია დაშვებული!")
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO solarium_2_appointments (fname, lname, phone, minutes, date, time) "
                           "VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, minutes, date, time))
            self.sol_2_fname.clear()
            self.sol_2_lname.clear()
            self.sol_2_phone.clear()
            self.sol_2_minutes.clear()
            self.sol_2_time.setText("")
            conn.commit()

            balance = 0
            init_minutes = 0

            cursor2 = conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            if cursor2.rowcount == 0:
                cursor3 = conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                conn.commit()
            else:
                client_phones = [client[3] for client in cursor2]
                if phone not in client_phones:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                    "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                    conn.commit()
            conn.close()

            QMessageBox.information(self, 'პაციენტი ჩაწერილია',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}"
                                    f"\nწუთები: {minutes}")
            self.load_data()

    def buy_subscription(self):
        self.subs_window.setWindowTitle("აბონემენტის შეძენა")
        self.subs_window.setWindowIcon(QIcon("ui/renew.ico"))
        self.subs_window.show()

    def funds(self):
        self.funds_window.setWindowTitle("საფასურის გადახდა")
        self.funds_window.setWindowIcon(QIcon("ui/renew.ico"))
        self.funds_window.show()

    def settings_window(self):
        self.settings_window_open.setWindowTitle("პარამეტრები")
        self.settings_window_open.setWindowIcon(QIcon("ui/renew.ico"))
        self.settings_window_open.show()

    def about_window(self):
        self.about.setWindowTitle("პროგრამის შესახებ")
        self.about.setWindowIcon(QIcon("ui/renew.ico"))
        self.about.show()
