import datetime
import os
from helpers_functions import critical_error, close_main_application, db, get_version, check_integer, open_documentation, load_days, load_times, load_types, load_doctors, load_procedures, load_zones, BASE_DIR
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QPushButton
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon, QColor


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(os.path.join(BASE_DIR, 'ui', 'main_window.ui'), self)

        self.today = datetime.now().date().strftime("%Y-%m-%d")
        self.statusBar().showMessage(f"ვერსია: {get_version()}")
        self.load_data()
        self.tabWidget.currentChanged.connect(self.load_data)

        self.search_date = None

        self.init_cosmetics_tab()
        self.init_laser_tab()
        self.init_solarium_tabs()

        self.connect_signals()

    def init_cosmetics_tab(self):
        self.cos_new_date.setDate(datetime.strptime(self.today, "%Y-%m-%d"))
        self.cos_new_date.dateChanged.connect(self.change_date_cos)

        for doctor_cos in load_doctors("კოსმეტოლოგია"):
            self.cos_doctor.addItem(doctor_cos[1])
        for zone_cos in load_procedures():
            self.cos_zone.addItem(zone_cos[1])

        self.cos_zone.setCurrentText("აირჩიეთ პროცედურა")
        self.cos_doctor.setCurrentText("აირჩიეთ ექიმი")

    def init_laser_tab(self):
        self.las_new_date.setDate(datetime.strptime(self.today, "%Y-%m-%d"))
        self.las_new_date.dateChanged.connect(self.change_date_las)

        for doctor_las in load_doctors("ლაზერი"):
            self.las_doctor.addItem(doctor_las[1])
        for type_las in load_types():
            self.las_type.addItem(type_las[1])
        for zone_las in load_zones():
            self.las_zone.addItem(zone_las[1])

        self.las_type.setCurrentText("აირჩიეთ ლაზერის ტიპი")
        self.las_zone.setCurrentText("აირჩიეთ ზონა")
        self.las_doctor.setCurrentText("აირჩიეთ ექიმი")

    def init_solarium_tabs(self):
        self.sol_1_new_date.setDate(datetime.strptime(self.today, "%Y-%m-%d"))
        self.sol_2_new_date.setDate(datetime.strptime(self.today, "%Y-%m-%d"))
        self.sol_1_new_date.dateChanged.connect(self.change_date_sol_1)
        self.sol_2_new_date.dateChanged.connect(self.change_date_sol_2)

    def connect_signals(self):
        # Appointment buttons
        self.cos_make_an_appointment_button.clicked.connect(self.make_an_appointment_cos)
        self.las_make_an_appointment_button.clicked.connect(self.make_an_appointment_las)
        self.sol_1_make_an_appointment_button.clicked.connect(self.make_an_appointment_sol_1)
        self.sol_2_make_an_appointment_button.clicked.connect(self.make_an_appointment_sol_2)

        # Pay buttons
        self.cos_pay_button.clicked.connect(self.funds)
        self.las_pay_button.clicked.connect(self.funds)
        self.sol_1_pay_button.clicked.connect(self.funds)
        self.sol_2_pay_button.clicked.connect(self.funds)

        # Search buttons
        self.search_button_cos.clicked.connect(self.search_client_cos)
        self.search_button_las.clicked.connect(self.search_client_las)
        self.search_button_sol_1.clicked.connect(self.search_client_sol_1)
        self.search_button_sol_2.clicked.connect(self.search_client_sol_2)

        # Menu items
        self.close_application.triggered.connect(close_main_application)
        self.patient_history.triggered.connect(self.patient_history_window)
        self.change_settings.triggered.connect(self.settings_window)
        self.documentation.triggered.connect(open_documentation)
        self.about_menu.triggered.connect(self.about_window)
        self.patients_list_menu.triggered.connect(self.patients_list_window)
        self.patient_edit.triggered.connect(self.patients_edit_window)

        # Cell click events
        self.cos_appointments.cellClicked.connect(self.get_cos_cell_information)
        self.las_appointments.cellClicked.connect(self.get_las_cell_information)
        self.sol_1_appointments.cellClicked.connect(self.get_sol_1_cell_information)
        self.sol_2_appointments.cellClicked.connect(self.get_sol_2_cell_information)

    def patient_history_window(self):
        if not hasattr(self, 'history_win'):
            from history import PatientHistory
            self.history_win = PatientHistory()
        self.history_win.setWindowTitle("პაციენტის ისტორია")
        self.history_win.setWindowIcon(QIcon("ui/renew.ico"))
        self.history_win.show()

    def patients_list_window(self):
        if not hasattr(self, 'patients_list_win'):
            from patients_list import PatientsList
            self.patients_list_win = PatientsList()
        self.patients_list_win.setFixedWidth(550)
        self.patients_list_win.setFixedHeight(600)
        x = (self.patients_list_win.screen().availableGeometry().width() // 2) - (self.patients_list_win.width() // 2)
        y = (self.patients_list_win.screen().availableGeometry().height() // 2) - (self.patients_list_win.height() // 2)
        self.patients_list_win.move(x, y)
        self.patients_list_win.setWindowTitle("პაციენტების სია")
        self.patients_list_win.setWindowIcon(QIcon("ui/renew.ico"))
        self.patients_list_win.show()

    def patients_edit_window(self):
        if not hasattr(self, 'patient_edit_win'):
            from patient_edit import PatientsEdit
            self.patient_edit_win = PatientsEdit()
        self.patient_edit_win.setFixedWidth(500)
        self.patient_edit_win.setFixedHeight(380)
        x = (self.patient_edit_win.screen().availableGeometry().width() // 2) - (
                    self.patient_edit_win.width() // 2)
        y = (self.patient_edit_win.screen().availableGeometry().height() // 2) - (
                    self.patient_edit_win.height() // 2)
        self.patient_edit_win.move(x, y)
        self.patient_edit_win.setWindowTitle("პაციენტის რედაქტირება")
        self.patient_edit_win.setWindowIcon(QIcon("ui/renew.ico"))
        self.patient_edit_win.show()


    def load_data(self):
        index = self.tabWidget.currentIndex()
        service = self.tabWidget.tabText(index)

        if service == "კოსმეტოლოგია":
            self.cos_fname.clear()
            self.cos_lname.clear()
            self.cos_phone.clear()
            self.cos_new_date.setDate(datetime.strptime(self.today, "%Y-%m-%d"))
            self.cosmetology()
        elif service == "ლაზერი":
            self.las_fname.clear()
            self.las_lname.clear()
            self.las_phone.clear()
            self.las_new_date.setDate(datetime.strptime(self.today, "%Y-%m-%d"))
            self.laser()
        elif service == "სოლარიუმი 1":
            self.sol_1_fname.clear()
            self.sol_1_lname.clear()
            self.sol_1_phone.clear()
            self.sol_1_new_date.setDate(datetime.strptime(self.today, "%Y-%m-%d"))
            self.solarium_1()
        elif service == "სოლარიუმი 2":
            self.sol_2_fname.clear()
            self.sol_2_lname.clear()
            self.sol_2_phone.clear()
            self.sol_2_new_date.setDate(datetime.strptime(self.today, "%Y-%m-%d"))
            self.solarium_2()

    # კოსმეტოლოგია
    def change_date_cos(self):
        new_date = self.cos_new_date.text()
        self.current_date.clear()
        self.current_date.setText(new_date)
        self.cosmetology(new_date)

    def cosmetology(self, *args):
        self.cos_appointments.clearContents()
        self.cos_appointments.setRowCount(44)
        conn = db.connect()
        if args:
            self.search_date = args[0]
        else:
            self.search_date = self.today
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `cosmetology_appointments` WHERE date=%s", (self.search_date,))
            times = load_times()

            self.cos_date.setText(self.cos_new_date.text())
            self.cos_patients.setText(str(cursor.rowcount))
            self.cos_current_day.setText(load_days()[datetime.now().strftime("%A")])
            self.current_date.setText(datetime.now().date().strftime("%d.%m.%Y"))

            self.cos_appointments.setColumnWidth(0, 50)
            self.cos_appointments.setColumnWidth(1, 225)
            self.cos_appointments.setColumnWidth(2, 120)
            self.cos_appointments.setColumnWidth(3, 140)
            self.cos_appointments.setColumnWidth(4, 140)
            self.cos_appointments.setColumnWidth(5, 215)
            self.cos_appointments.setColumnWidth(6, 20)

            for cos in cursor:
                row_id = int(times.get(cos[7], 0))
                btn = QPushButton("X")
                btn.setStyleSheet("color: red; font-weight: bold;")
                btn.pressed.connect(self.cancel_cos)
                self.cos_appointments.setItem(row_id, 0, QTableWidgetItem(str(cos[0])))
                self.cos_appointments.setItem(row_id, 1, QTableWidgetItem(cos[1]))
                self.cos_appointments.setItem(row_id, 2, QTableWidgetItem(cos[2]))
                self.cos_appointments.setItem(row_id, 3, QTableWidgetItem(cos[3]))
                self.cos_appointments.setItem(row_id, 4, QTableWidgetItem(cos[4]))
                self.cos_appointments.setItem(row_id, 5, QTableWidgetItem(cos[5]))
                self.cos_appointments.setCellWidget(row_id, 6, btn)
                if cos[8] == "paid":
                    self.cos_appointments.item(row_id, 0).setBackground(QColor(142, 172, 80))
                    self.cos_appointments.item(row_id, 1).setBackground(QColor(142, 172, 80))
                    self.cos_appointments.item(row_id, 2).setBackground(QColor(142, 172, 80))
                    self.cos_appointments.item(row_id, 3).setBackground(QColor(142, 172, 80))
                    self.cos_appointments.item(row_id, 4).setBackground(QColor(142, 172, 80))
                    self.cos_appointments.item(row_id, 5).setBackground(QColor(142, 172, 80))
        except Exception as e:
            critical_error("დაკავშირების პრობლემა!")
        finally:
                conn.close()

    def get_cos_cell_information(self):
        current_row = self.cos_appointments.currentRow()
        current_column = self.cos_appointments.currentColumn()
        time = self.cos_appointments.verticalHeaderItem(current_row).text()
        date = self.cos_new_date.text()
        self.cos_time.setText(time)
        self.cos_date.setText(date)
        if self.cos_appointments.item(current_row, current_column):
            try:
                appo_id = str(self.cos_appointments.item(current_row, 0).text())
                fname = str(self.cos_appointments.item(current_row, 2).text())
                lname = str(self.cos_appointments.item(current_row, 3).text())
                phone = str(self.cos_appointments.item(current_row, 4).text())
                category = "კოსმეტოლოგია"
                self.funds(appo_id, fname, lname, phone, category)
            except AttributeError:
                pass

    def make_an_appointment_cos(self):
        conn = db.connect()
        first_name = self.cos_fname.text()
        last_name = self.cos_lname.text()
        phone = self.cos_phone.text()
        zone = self.cos_zone.currentText()
        doctor = self.cos_doctor.currentText()
        date = self.cos_date.text()
        time = self.cos_time.text()
        status = "unpaid"
        category = "კოსმეტოლოგია"

        if not time:
            return QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        if not all([first_name, last_name, phone]):
            return QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        if not check_integer(phone):
            return QMessageBox.warning(self, 'შეცდომა', "ტელეფონის ველში მხოლოდ ციფრებია დაშვებული!")
        if zone == "აირჩიეთ პროცედურა" or doctor == "აირჩიეღ ექიმი":
            return QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ პროცედურა და ექიმი.")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO cosmetology_appointments (procedure_name, fname, lname, phone, doctor, date, time, status) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (zone, first_name, last_name, phone, doctor, date, time, status))

            time_now = datetime.now().time().strftime("%H:%M")
            cursor.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                             "VALUES (?, ?, ?, ?, ?, ?)",
                             (f"{first_name} {last_name}", category, date, time_now, phone,
                              f"განყოფილება: ჩაწერა | პროცედურა: {zone}, ექიმი: {doctor}"))
            cursor.execute("SELECT 1 FROM clients WHERE phone = ? LIMIT 1", (phone,))
            if not cursor.fetchone():
                balance = 0
                init_minutes = 0
                cursor.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes)
                               )
            conn.commit()

            self.cos_fname.clear()
            self.cos_lname.clear()
            self.cos_phone.clear()
            self.cos_time.setText("")
            self.cos_zone.setCurrentText("აირჩიეთ პროცედურა")
            self.cos_doctor.setCurrentText("აირჩიეთ ექიმი")

            QMessageBox.information(self, 'პაციენტი ჩაწერილია',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}")
            self.cosmetology(self.search_date)
        except Exception as e:
            critical_error("მონაცემთა ბაზასთან კავშირის პრობლემა")
        finally:
            conn.close()

    # ლაზერი
    def change_date_las(self):
        new_date = self.las_new_date.text()
        self.current_date.clear()
        self.las_current_date.setText(new_date)
        self.laser(new_date)

    def laser(self, *args):
        self.las_appointments.clearContents()
        self.cos_appointments.setRowCount(44)
        conn = db.connect()
        if args:
            self.search_date = args[0]
        else:
            self.search_date = self.today
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `laser_appointments` WHERE date=%s", (self.search_date,))
            times = load_times()

            self.las_date.setText(self.las_new_date.text())
            self.las_patients.setText(str(cursor.rowcount))
            self.las_current_day.setText(load_days()[datetime.now().strftime("%A")])
            self.las_current_date.setText(datetime.now().date().strftime("%d.%m.%Y"))

            self.las_appointments.setColumnWidth(0, 50)
            self.las_appointments.setColumnWidth(1, 120)
            self.las_appointments.setColumnWidth(2, 170)
            self.las_appointments.setColumnWidth(3, 110)
            self.las_appointments.setColumnWidth(4, 170)
            self.las_appointments.setColumnWidth(5, 110)
            self.las_appointments.setColumnWidth(6, 160)
            self.las_appointments.setColumnWidth(7, 20)


            for las in cursor:
                row_id = int(times.get(las[8], 0))
                btn = QPushButton("X")
                btn.setStyleSheet("color: red; font-weight: bold;")
                btn.pressed.connect(self.cancel_las)
                self.las_appointments.setItem(row_id, 0, QTableWidgetItem(str(las[0])))
                self.las_appointments.setItem(row_id, 1, QTableWidgetItem(las[1]))
                self.las_appointments.setItem(row_id, 2, QTableWidgetItem(las[2]))
                self.las_appointments.setItem(row_id, 3, QTableWidgetItem(las[3]))
                self.las_appointments.setItem(row_id, 4, QTableWidgetItem(las[4]))
                self.las_appointments.setItem(row_id, 5, QTableWidgetItem(las[5]))
                self.las_appointments.setItem(row_id, 6, QTableWidgetItem(las[6]))
                self.las_appointments.setCellWidget(row_id, 7, btn)
                if las[9] == "paid":
                    self.las_appointments.item(row_id, 0).setBackground(QColor(142, 172, 80))
                    self.las_appointments.item(row_id, 1).setBackground(QColor(142, 172, 80))
                    self.las_appointments.item(row_id, 2).setBackground(QColor(142, 172, 80))
                    self.las_appointments.item(row_id, 3).setBackground(QColor(142, 172, 80))
                    self.las_appointments.item(row_id, 4).setBackground(QColor(142, 172, 80))
                    self.las_appointments.item(row_id, 5).setBackground(QColor(142, 172, 80))
                    self.las_appointments.item(row_id, 6).setBackground(QColor(142, 172, 80))

        except Exception as e:
            critical_error(f"დაკავშირების პრობლემა! {e}")
        finally:
            conn.close()

    def get_las_cell_information(self):
        current_row = self.las_appointments.currentRow()
        current_column = self.las_appointments.currentColumn()
        time = self.las_appointments.verticalHeaderItem(current_row).text()
        date = self.las_new_date.text()
        self.las_time.setText(time)
        self.las_date.setText(date)
        if self.las_appointments.item(current_row, current_column):
            try:
                appo_id = str(self.las_appointments.item(current_row, 0).text())
                zone = self.las_appointments.item(current_row, 2).text()
                fname = str(self.las_appointments.item(current_row, 3).text())
                lname = str(self.las_appointments.item(current_row, 4).text())
                phone = str(self.las_appointments.item(current_row, 5).text())
                category = "ლაზერი"
                self.funds(appo_id, fname, lname, phone, category, zone)
            except AttributeError:
                pass

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
        status = "unpaid"
        category = "ლაზერი"

        if not time:
            return QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        if not all([first_name, last_name, phone]):
            return QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        if not check_integer(phone):
            return QMessageBox.warning(self, 'შეცდომა', "ტელეფონის ველში მხოლოდ ციფრებია დაშვებული!")
        if type == "აირჩიეთ ლაზერის ტიპი" or zone == "აირჩიეთ ზონა" or doctor == "აირჩიეთ ექიმი.":
            return QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ ლაზერის ტიპი, ზონა და ექიმი.")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO laser_appointments (laser_type, zone, fname, lname, phone, doctor, date, time, status) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (laser_type, zone, first_name, last_name, phone, doctor, date, time, status)
            )
            time_now = datetime.now().time().strftime("%H:%M")
            cursor.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                             "VALUES (?, ?, ?, ?, ?, ?)",
                             (f"{first_name} {last_name}", category, date, time_now, phone,
                              f"განყოფილება: ჩაწერა | ლაზერის ტიპი: {laser_type}, ზონა: {zone}, ექიმი: {doctor}")
                           )
            cursor.execute("SELECT 1 FROM clients WHERE phone = ? LIMIT 1", (phone,))
            if not cursor.fetchone():
                balance = 0
                init_minutes = 0
                cursor.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes)
                                )
            conn.commit()

            self.las_fname.clear()
            self.las_lname.clear()
            self.las_phone.clear()
            self.las_type.setCurrentText("აირჩიეთ ლაზერის ტიპი")
            self.las_zone.setCurrentText("აირჩიეთ ზონა")
            self.las_doctor.setCurrentText("აირჩიეთ ექიმი")
            self.las_time.setText("")

            QMessageBox.information(self, 'პაციენტი ჩაწერილია',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}")
            self.laser(self.search_date)
        except Exception as e:
            critical_error(f"მონაცემთა ბაზასთან კავშირის პრობლემა - {e}")
        finally:
            conn.close()

    # სოლარიუმი 1
    def change_date_sol_1(self):
        new_date = self.sol_1_new_date.text()
        self.sol_1_current_date.clear()
        self.sol_1_current_date.setText(new_date)
        self.solarium_1(new_date)

    def solarium_1(self, *args):
        self.sol_1_appointments.clearContents()
        self.sol_1_appointments.setRowCount(44)
        conn = db.connect()
        if args:
            self.search_date = args[0]
        else:
            self.search_date = self.today
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM `solarium_1_appointments` WHERE date=%s", (self.search_date,))
            times = load_times()

            self.sol_1_date.setText(self.sol_1_new_date.text())
            self.sol_1_patients.setText(str(cursor.rowcount))
            self.sol_1_current_day.setText(load_days()[datetime.now().strftime("%A")])
            self.sol_1_current_date.setText(datetime.now().date().strftime("%d.%m.%Y"))

            self.sol_1_appointments.setColumnWidth(0, 50)
            self.sol_1_appointments.setColumnWidth(1, 190)
            self.sol_1_appointments.setColumnWidth(2, 230)
            self.sol_1_appointments.setColumnWidth(3, 230)
            self.sol_1_appointments.setColumnWidth(4, 190)
            self.sol_1_appointments.setColumnWidth(5, 20)

            for sol_1 in cursor:
                row_id = int(times[sol_1[6]])
                btn = QPushButton("X")
                btn.setStyleSheet("color: red; font-weight: bold;")
                btn.pressed.connect(self.cancel_sol_1)
                self.sol_1_appointments.setItem(row_id, 0, QTableWidgetItem(str(sol_1[0])))
                self.sol_1_appointments.setItem(row_id, 1, QTableWidgetItem(sol_1[1]))
                self.sol_1_appointments.setItem(row_id, 2, QTableWidgetItem(sol_1[2]))
                self.sol_1_appointments.setItem(row_id, 3, QTableWidgetItem(sol_1[3]))
                self.sol_1_appointments.setItem(row_id, 4, QTableWidgetItem(str(sol_1[4])))
                self.sol_1_appointments.setCellWidget(row_id, 5, btn)
                if sol_1[7] == "paid":
                    self.sol_1_appointments.item(row_id, 0).setBackground(QColor(142, 172, 80))
                    self.sol_1_appointments.item(row_id, 1).setBackground(QColor(142, 172, 80))
                    self.sol_1_appointments.item(row_id, 2).setBackground(QColor(142, 172, 80))
                    self.sol_1_appointments.item(row_id, 3).setBackground(QColor(142, 172, 80))
                    self.sol_1_appointments.item(row_id, 4).setBackground(QColor(142, 172, 80))
        except Exception as e:
            critical_error(f"დაკავშირების პრობლემა! {e}")
        finally:
            conn.close()

    def get_sol_1_cell_information(self):
        current_row = self.sol_1_appointments.currentRow()
        current_column = self.sol_1_appointments.currentColumn()
        time = self.sol_1_appointments.verticalHeaderItem(current_row).text()
        date = self.sol_1_new_date.text()
        self.sol_1_time.setText(time)
        self.sol_1_date.setText(date)
        if self.sol_1_appointments.item(current_row, current_column):
            try:
                appo_id = str(self.sol_1_appointments.item(current_row, 0).text())
                fname = str(self.sol_1_appointments.item(current_row, 1).text())
                lname = str(self.sol_1_appointments.item(current_row, 2).text())
                phone = str(self.sol_1_appointments.item(current_row, 3).text())
                category = "სოლარიუმი 1"
                self.funds(appo_id, fname, lname, phone, category)
            except AttributeError:
                pass

    def make_an_appointment_sol_1(self):
        conn = db.connect()
        first_name = self.sol_1_fname.text()
        last_name = self.sol_1_lname.text()
        phone = self.sol_1_phone.text()
        minutes = self.sol_1_minutes.text()
        date = self.sol_1_date.text()
        time = self.sol_1_time.text()
        status = "unpaid"
        category = "სოლარიუმი 1"

        if not time:
            return QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        if not all([first_name, last_name, phone, minutes]):
            return QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        if not check_integer(phone) or not check_integer(minutes):
            return QMessageBox.warning(self, 'შეცდომა', "ამ ველში მხოლოდ ციფრებია დაშვებული!")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO solarium_1_appointments (fname, lname, phone, minutes, date, time, status) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, minutes, date, time, status)
                           )
            time_now = datetime.now().time().strftime("%H:%M")
            cursor.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                             "VALUES (?, ?, ?, ?, ?, ?)",
                             (f"{first_name} {last_name}", category, date, time_now, phone,
                              f"განყოფილება: ჩაწერა | წუთი: {minutes}"))
            cursor.execute("SELECT 1 FROM clients WHERE phone = ? LIMIT 1", (phone,))
            if not cursor.fetchone():
                balance = 0
                init_minutes = 0
                cursor.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes)
                                )
            conn.commit()

            self.sol_1_fname.clear()
            self.sol_1_lname.clear()
            self.sol_1_phone.clear()
            self.sol_1_minutes.clear()
            self.sol_1_time.setText("")

            QMessageBox.information(self, 'პაციენტი ჩაწერილია',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}"
                                    f"\nწუთები: {minutes}")

            self.solarium_1(self.search_date)

        except Exception as e:
            critical_error(f"მონაცემთა ბაზასთან კავშირის პრობლემა - {e}")
        finally:
            conn.close()

    # სოლარიუმი 2
    def change_date_sol_2(self):
        new_date = self.sol_2_new_date.text()
        self.sol_2_current_date.clear()
        self.sol_2_current_date.setText(new_date)
        self.solarium_2(new_date)

    def solarium_2(self, *args):
        self.sol_2_appointments.clearContents()
        self.sol_2_appointments.setRowCount(44)
        conn = db.connect()
        if args:
            self.search_date = args[0]
        else:
            self.search_date = self.today
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM `solarium_2_appointments` WHERE date=%s", (self.search_date,))
            times = load_times()

            self.sol_2_date.setText(self.sol_2_new_date.text())
            self.sol_2_patients.setText(str(cursor.rowcount))
            self.sol_2_current_day.setText(load_days()[datetime.now().strftime("%A")])
            self.sol_2_current_date.setText(datetime.now().date().strftime("%d.%m.%Y"))

            self.sol_2_appointments.setColumnWidth(0, 50)
            self.sol_2_appointments.setColumnWidth(1, 190)
            self.sol_2_appointments.setColumnWidth(2, 230)
            self.sol_2_appointments.setColumnWidth(3, 230)
            self.sol_2_appointments.setColumnWidth(4, 190)
            self.sol_2_appointments.setColumnWidth(5, 20)

            for sol_2 in cursor:
                row_id = int(times[sol_2[6]])
                btn = QPushButton("X")
                btn.setStyleSheet("color: red; font-weight: bold;")
                btn.pressed.connect(self.cancel_sol_2)
                self.sol_2_appointments.setItem(row_id, 0, QTableWidgetItem(str(sol_2[0])))
                self.sol_2_appointments.setItem(row_id, 1, QTableWidgetItem(sol_2[1]))
                self.sol_2_appointments.setItem(row_id, 2, QTableWidgetItem(sol_2[2]))
                self.sol_2_appointments.setItem(row_id, 3, QTableWidgetItem(sol_2[3]))
                self.sol_2_appointments.setItem(row_id, 4, QTableWidgetItem(str(sol_2[4])))
                self.sol_2_appointments.setCellWidget(row_id, 5, btn)
                if sol_2[7] == "paid":
                    self.sol_2_appointments.item(row_id, 0).setBackground(QColor(142, 172, 80))
                    self.sol_2_appointments.item(row_id, 1).setBackground(QColor(142, 172, 80))
                    self.sol_2_appointments.item(row_id, 2).setBackground(QColor(142, 172, 80))
                    self.sol_2_appointments.item(row_id, 3).setBackground(QColor(142, 172, 80))
                    self.sol_2_appointments.item(row_id, 4).setBackground(QColor(142, 172, 80))

        except Exception as e:
            critical_error(f"დაკავშირების პრობლემა! {e}")
        finally:
            conn.close()

    def get_sol_2_cell_information(self):
        current_row = self.sol_2_appointments.currentRow()
        current_column = self.sol_2_appointments.currentColumn()
        time = self.sol_2_appointments.verticalHeaderItem(current_row).text()
        date = self.sol_2_new_date.text()
        self.sol_2_time.setText(time)
        self.sol_2_date.setText(date)
        if self.sol_2_appointments.item(current_row, current_column):
            try:
                appo_id = str(self.sol_2_appointments.item(current_row, 0).text())
                fname = str(self.sol_2_appointments.item(current_row, 1).text())
                lname = str(self.sol_2_appointments.item(current_row, 2).text())
                phone = str(self.sol_2_appointments.item(current_row, 3).text())
                category = "სოლარიუმი 2"
                self.funds(appo_id, fname, lname, phone, category)
            except AttributeError:
                pass

    def make_an_appointment_sol_2(self):
        conn = db.connect()
        first_name = self.sol_2_fname.text()
        last_name = self.sol_2_lname.text()
        phone = self.sol_2_phone.text()
        minutes = self.sol_2_minutes.text()
        date = self.sol_2_date.text()
        time = self.sol_2_time.text()
        status = "unpaid"
        category = "სოლარიუმი 2"

        if not time:
            return QMessageBox.warning(self, 'შეცდომა', "აირჩიეთ დრო ჩასაწერად.")
        if not all([first_name, last_name, phone, minutes]):
            return QMessageBox.warning(self, 'შეცდომა', "ყველა ველის შევსება სავალდებულოა!")
        if not check_integer(phone) or not check_integer(minutes):
            return QMessageBox.warning(self, 'შეცდომა', "ამ ველში მხოლოდ ციფრებია დაშვებული!")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO solarium_2_appointments (fname, lname, phone, minutes, date, time, status) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, minutes, date, time, status)
                           )
            time_now = datetime.now().time().strftime("%H:%M")
            cursor.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                             "VALUES (?, ?, ?, ?, ?, ?)",
                             (f"{first_name} {last_name}", category, date, time_now, phone,
                              f"განყოფილება: ჩაწერა | წუთი: {minutes}"))
            cursor.execute("SELECT 1 FROM clients WHERE phone = ? LIMIT 1", (phone,))
            if not cursor.fetchone():
                balance = 0
                init_minutes = 0
                cursor.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes)
                               )
            conn.commit()

            self.sol_2_fname.clear()
            self.sol_2_lname.clear()
            self.sol_2_phone.clear()
            self.sol_2_minutes.clear()
            self.sol_2_time.setText("")

            QMessageBox.information(self, 'პაციენტი ჩაწერილია',
                                    f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                    f"\nდრო: {time}"
                                    f"\nწუთები: {minutes}")
            self.solarium_2(self.search_date)
        except Exception as e:
            critical_error(f"მონაცემთა ბაზასთან კავშირის პრობლემა - {e}")
        finally:
            conn.close()

    def buy_subscription(self):
        self.subs_window.setWindowTitle("აბონემენტის შეძენა")
        self.subs_window.setWindowIcon(QIcon("ui/renew.ico"))
        self.subs_window.show()

    def funds(self, *args):
        from funds import Funds
        if not args[0]:
            self.funds_window = Funds()
        else:
            appo_id = args[0]
            fname = args[1]
            lname = args[2]
            phone = args[3]
            category = args[4]
            if len(args) == 6:
                zone = args[5]
                self.funds_window = Funds(appo_id, fname, lname, phone, category, zone)
                self.funds_window.search_client_2()
            else:
                self.funds_window = Funds(appo_id, fname, lname, phone, category)
                self.funds_window.search_client_2()
        self.funds_window.setWindowTitle("საფასურის გადახდა")
        self.funds_window.setWindowIcon(QIcon("ui/renew.ico"))
        self.funds_window.show()

    def settings_window(self):
        if not hasattr(self, "settings_window_open"):
            from settings import Settings
            self.settings_window_open = Settings()
        self.settings_window_open.setWindowTitle("პარამეტრები")
        self.settings_window_open.setWindowIcon(QIcon("ui/renew.ico"))
        self.settings_window_open.show()

    def about_window(self):
        if not hasattr(self, 'about_window_open'):
            from about import About
            self.about_window_open = About()
        self.about_window_open.setWindowTitle("პროგრამის შესახებ")
        self.about_window_open.setWindowIcon(QIcon("ui/renew.ico"))
        self.about_window_open.show()

    def search_client_cos(self):
        search = self.cos_phone.text()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE phone=%s", (search,))
        result_cos = cursor.fetchone()

        if not search:
            QMessageBox.warning(self, "შეცდომა","ამ ველის შევსება აუცილებელია")
        elif not result_cos:
            QMessageBox.warning(self, "შეცდომა",
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                f"პაციენტის ჩასაწერად.")
        if result_cos:
            self.cos_fname.setText(result_cos[1])
            self.cos_lname.setText(result_cos[2])
            conn.close()

    def search_client_las(self):
        conn = db.connect()
        search = self.las_phone.text()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE phone=%s", (search,))
        result_las = cursor.fetchone()

        if not search:
            QMessageBox.warning(self, "შეცდომა","ამ ველის შევსება აუცილებელია")
        elif not result_las:
            QMessageBox.warning(self, "შეცდომა",
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                f"პაციენტის ჩასაწერად.")
        if result_las:
            self.las_fname.setText(result_las[1])
            self.las_lname.setText(result_las[2])
            conn.close()

    def search_client_sol_1(self):
        search = self.sol_1_phone.text()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE phone=%s", (search,))
        result_sol_1 = cursor.fetchone()

        if not search:
            QMessageBox.warning(self, "შეცდომა","ამ ველის შევსება აუცილებელია")
        elif not result_sol_1:
            QMessageBox.warning(self, "შეცდომა",
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                f"პაციენტის ჩასაწერად.")
        if result_sol_1:
            self.sol_1_fname.setText(result_sol_1[1])
            self.sol_1_lname.setText(result_sol_1[2])
            conn.close()

    def search_client_sol_2(self):
        search = self.sol_2_phone.text()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE phone=%s", (search,))
        result_sol_2 = cursor.fetchone()

        if not search:
            QMessageBox.warning(self, "შეცდომა","ამ ველის შევსება აუცილებელია")
        elif not result_sol_2:
            QMessageBox.warning(self, "შეცდომა",
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                f"პაციენტის ჩასაწერად.")
        if result_sol_2:
            self.sol_2_fname.setText(result_sol_2[1])
            self.sol_2_lname.setText(result_sol_2[2])
            conn.close()

    def cancel_cos(self):
        conn = db.connect()
        current_row = self.cos_appointments.currentRow()
        if current_row == -1:
            return
        id_item = self.cos_appointments.item(current_row, 0)
        if not id_item:
            return

        num = id_item.text()
        first_name = self.cos_appointments.item(current_row, 2).text()
        last_name = self.cos_appointments.item(current_row, 3).text()

        msg = QMessageBox(parent=self)
        msg.setWindowTitle("ჩაწერის გაუქმება")
        msg.setText(f"დარწმუნებული ხართ, რომ გსურთ ჩაწერის გაუქმება პაციენტისთვის - {first_name} {last_name}? ")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        msg.button(QMessageBox.StandardButton.Yes).setText("დიახ")
        msg.button(QMessageBox.StandardButton.No).setText("არა")

        if msg.exec() == QMessageBox.StandardButton.Yes:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM cosmetology_appointments WHERE id=%s", (num,))
                result_check = cursor.fetchone()
                if result_check and result_check[8] == "paid":
                    QMessageBox.warning(self, "შეცდომა",
                                        "გადახდილი ჩაწერის წაშლა შეუძლებელია!")
                    return
                cursor.execute("DELETE FROM `cosmetology_appointments` WHERE id=%s", (num,))
                conn.commit()
                QMessageBox.information(self,
                                        "ჩაწერის გაუქმება",
                                        f"ჩაწერა გაუქმებულია პაციენტისთვის "
                                        f"{first_name} {last_name}.")
                self.cosmetology()
            except Exception as e:
                critical_error(f"ვერ მოხერხდა წაშლა - {e}")

    def cancel_las(self):
        conn = db.connect()
        current_row = self.las_appointments.currentRow()
        if current_row == -1:
            return
        id_item = self.las_appointments.item(current_row, 0)
        if not id_item:
            return

        num = id_item.text()
        first_name = self.las_appointments.item(current_row, 3).text()
        last_name = self.las_appointments.item(current_row, 4).text()

        msg = QMessageBox(parent=self)
        msg.setWindowTitle("ჩაწერის გაუქმება")
        msg.setText(f"დარწმუნებული ხართ, რომ გსურთ ჩაწერის გაუქმება პაციენტისთვის - {first_name} {last_name}? ")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        msg.button(QMessageBox.StandardButton.Yes).setText("დიახ")
        msg.button(QMessageBox.StandardButton.No).setText("არა")

        if msg.exec() == QMessageBox.StandardButton.Yes:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM laser_appointments WHERE id=%s", (num,))
                result_check = cursor.fetchone()
                if result_check and result_check[8] == "paid":
                    QMessageBox.warning(self, "შეცდომა",
                                        "გადახდილი ჩაწერის წაშლა შეუძლებელია!")
                    return
                cursor.execute("DELETE FROM `laser_appointments` WHERE id=%s", (num,))
                conn.commit()
                QMessageBox.information(self,
                                        "ჩაწერის გაუქმება",
                                        f"ჩაწერა გაუქმებულია პაციენტისთვის "
                                        f"{first_name} {last_name}.")
                self.laser()
            except Exception as e:
                critical_error(f"ვერ მოხერხდა წაშლა - {e}")

    def cancel_sol_1(self):
        conn = db.connect()
        current_row = self.sol_1_appointments.currentRow()
        if current_row == -1:
            return
        id_item = self.sol_1_appointments.item(current_row, 0)
        if not id_item:
            return

        num = id_item.text()
        first_name = self.sol_1_appointments.item(current_row, 1).text()
        last_name = self.sol_1_appointments.item(current_row, 2).text()

        msg = QMessageBox(parent=self)
        msg.setWindowTitle("ჩაწერის გაუქმება")
        msg.setText(f"დარწმუნებული ხართ, რომ გსურთ ჩაწერის გაუქმება პაციენტისთვის - {first_name} {last_name}? ")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        msg.button(QMessageBox.StandardButton.Yes).setText("დიახ")
        msg.button(QMessageBox.StandardButton.No).setText("არა")

        if msg.exec() == QMessageBox.StandardButton.Yes:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM solarium_1_appointments WHERE id=%s", (num,))
                result_check = cursor.fetchone()
                if result_check and result_check[8] == "paid":
                    QMessageBox.warning(self, "შეცდომა",
                                        "გადახდილი ჩაწერის წაშლა შეუძლებელია!")
                    return
                cursor.execute("DELETE FROM `solarium_1_appointments` WHERE id=%s", (num,))
                conn.commit()
                QMessageBox.information(self,
                                        "ჩაწერის გაუქმება",
                                        f"ჩაწერა გაუქმებულია პაციენტისთვის "
                                        f"{first_name} {last_name}.")
                self.solarium_1()
            except Exception as e:
                critical_error(f"ვერ მოხერხდა წაშლა - {e}")

    def cancel_sol_2(self):
        conn = db.connect()
        current_row = self.sol_2_appointments.currentRow()
        if current_row == -1:
            return
        id_item = self.sol_2_appointments.item(current_row, 0)
        if not id_item:
            return

        num = id_item.text()
        first_name = self.sol_2_appointments.item(current_row, 1).text()
        last_name = self.sol_2_appointments.item(current_row, 2).text()

        msg = QMessageBox(parent=self)
        msg.setWindowTitle("ჩაწერის გაუქმება")
        msg.setText(f"დარწმუნებული ხართ, რომ გსურთ ჩაწერის გაუქმება პაციენტისთვის - {first_name} {last_name}? ")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        msg.button(QMessageBox.StandardButton.Yes).setText("დიახ")
        msg.button(QMessageBox.StandardButton.No).setText("არა")

        if msg.exec() == QMessageBox.StandardButton.Yes:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM solarium_2_appointments WHERE id=%s", (num,))
                result_check = cursor.fetchone()
                if result_check and result_check[8] == "paid":
                    QMessageBox.warning(self, "შეცდომა",
                                        "გადახდილი ჩაწერის წაშლა შეუძლებელია!")
                    return
                cursor.execute("DELETE FROM `solarium_2_appointments` WHERE id=%s", (num,))
                conn.commit()
                QMessageBox.information(self,
                                        "ჩაწერის გაუქმება",
                                        f"ჩაწერა გაუქმებულია პაციენტისთვის "
                                        f"{first_name} {last_name}.")
                self.solarium_2()
            except Exception as e:
                critical_error(f"ვერ მოხერხდა წაშლა - {e}")

