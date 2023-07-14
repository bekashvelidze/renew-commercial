import json
import datetime
from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from connection import Database
from load_data import LoadData




class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)
        self.clients = [{"name": "სახელი", "lname": "გვარი", "phone": "599999999", "zone": "ზონა", "doctor": "ექიმი",
                    "price": "100", "time": "11:45"},
                   {"name": "სახელი2", "lname": "გვარი2", "phone": "577777777", "zone": "ზონა2", "doctor": "ექიმი2",
                    "price": "120", "time": "12:00"}]
        self.load_data(self.services[self.tabWidget.tabText(self.tabWidget.currentIndex())])
        self.cos_make_an_appointment_button.clicked.connect(self.make_an_appointment_cos)
        self.cos_buy_subscription_button.clicked.connect(self.buy_subscription)
        self.cos_appointments.cellClicked.connect(self.get_cell_information)


    def get_cell_information(self):
        service = self.cos_appointments
        current_row = service.currentRow()
        current_column = service.currentColumn()
        time = service.verticalHeaderItem(current_row).text()
        date = datetime.now().date().strftime("%d.%m.%Y")
        self.cos_time.setText(time)
        self.cos_date.setText(date)
        if service.item(current_row, current_column):
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
        #TODO 1: გროვდება ინფორმაცია ჩაწერის ველებიდან და ასევე 'time' და 'date' ველებიდან, იხნსნება მომსახურების
        # ცხრილი ბაზაში და იწერება შებამისი ინფორმაცია 'INSERT'-ით
        # იხურება ფანჯარა და ახლდება ინფორმაცია ინტერფეისის ცხრილში
        QMessageBox.information(self, 'პაციენტი ჩაიწერა',
                                f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                f"\nდრო: {time}")

    def buy_subscription(self):
        #TODO 2: ახალი ფანჯარა, სახელი, გვარი, წუთების რაოდენობა
        # იხსნება ცხრილი 'clients', მოწმდება კლიენტის ნომრის მიხედვით წუთების რაოდენობა, ემატება და კეთდება 'UPDATE"
        # იხურება ფანჯარა და ბრუნდება ძირითად ფანჯარაში
        QMessageBox.information(self, 'აბონემენტის შეძება',
                                f"აბონემენტი დარეგისტრირებულია:\nსახელი, გვარი: {self.clients[0]['name']} {self.clients[0]['lname']}"
                                f"\nწუთი: 50")