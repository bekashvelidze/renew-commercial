import json
import datetime
from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem
from PyQt6.uic import loadUi

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)
        self.clients = [{"name": "სახელი", "lname": "გვარი", "phone": "599999999", "zone": "ზონა", "doctor": "ექიმი",
                    "price": "100", "time": "11:45"},
                   {"name": "სახელი2", "lname": "გვარი2", "phone": "577777777", "zone": "ზონა2", "doctor": "ექიმი2",
                    "price": "120", "time": "12:00"}]
        self.load_data()
        self.make_an_appointment_button.clicked.connect(self.make_an_appointment)
        self.buy_subscription_button.clicked.connect(self.buy_subscription)
        self.appointments.cellClicked.connect(self.get_cell_information)

    def load_data(self):
        with open("times.json", "r") as file:
            times = json.load(file)
        row = 0
        self.appointments.setColumnWidth(0, 120)
        self.appointments.setColumnWidth(1, 180)
        self.appointments.setColumnWidth(2, 120)
        self.appointments.setColumnWidth(3, 120)
        self.appointments.setColumnWidth(4, 160)
        self.appointments.setColumnWidth(5, 120)

        for person in self.clients:
            self.appointments.setItem(int(times[person["time"]]), 0, QTableWidgetItem(person["name"]))
            self.appointments.setItem(int(times[person["time"]]), 1, QTableWidgetItem(person["lname"]))
            self.appointments.setItem(int(times[person["time"]]), 2, QTableWidgetItem(person["phone"]))
            self.appointments.setItem(int(times[person["time"]]), 3, QTableWidgetItem(person["zone"]))
            self.appointments.setItem(int(times[person["time"]]), 4, QTableWidgetItem(person["doctor"]))
            self.appointments.setItem(int(times[person["time"]]), 5, QTableWidgetItem(person["price"]))
            row += 1

    def get_cell_information(self):
        current_row = self.appointments.currentRow()
        current_column = self.appointments.currentColumn()
        time = self.appointments.verticalHeaderItem(current_row).text()
        date = datetime.now().date().strftime("%d.%m.%Y")
        self.time.setText(time)
        self.date.setText(date)
        if self.appointments.item(current_row, current_column):
            QMessageBox.information(self, "დრო დაკავებულია", "ეს დრო დაკავებულია, აირჩიეთ სხვა დრო.")
        else:
            print("empty")
    def make_an_appointment(self):
        #TODO 1: გროვდება ინფორმაცია ჩაწერის ველებიდან და ასევე 'time' და 'date' ველებიდან, იხნსნება მომსახურების
        # ცხრილი ბაზაში და იწერება შებამისი ინფორმაცია 'INSERT'-ით
        # იხურება ფანჯარა და ახლდება ინფორმაცია ინტერფეისის ცხრილში
        QMessageBox.information(self, 'პაციენტი ჩაიწერა',
                                f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {self.clients[0]['name']} {self.clients[0]['lname']}"
                                f"\nდრო: {self.clients[0]['time']}")

    def buy_subscription(self):
        #TODO 2: ახალი ფანჯარა, სახელი, გვარი, წუთების რაოდენობა
        # იხსნება ცხრილი 'clients', მოწმდება კლიენტის ნომრის მიხედვით წუთების რაოდენობა, ემატება და კეთდება 'UPDATE"
        # იხურება ფანჯარა და ბრუნდება ძირითად ფანჯარაში
        QMessageBox.information(self, 'აბონემენტის შეძება',
                                f"აბონემენტი დარეგისტრირებულია:\nსახელი, გვარი: {self.clients[0]['name']} {self.clients[0]['lname']}"
                                f"\nწუთი: 50")