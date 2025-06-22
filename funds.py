import json
import calendar
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtGui import QColor
from connection import Database

db = Database()
today = datetime.now().date().strftime("%Y-%m-%d")
year = datetime.now().year
month_name = calendar.month_name[int(today.split("-")[1])]
month_number = int(today.split("-")[1])


def check_integer(number):
    try:
        if int(number):
            return True
    except ValueError:
        return False


def load_months():
    with open("months.json", "r", encoding="utf-8") as file:
        months = json.load(file)

    return months


def load_years():
    conn = db.connect()
    cursor_years = conn.cursor()
    cursor_years.execute("SELECT * FROM payments")
    years = [year_num[6].split("-")[0] for year_num in cursor_years]

    return years


def load_categories():
    conn = db.connect()
    cursor_cats = conn.cursor()
    cursor_cats.execute("SELECT * FROM categories")

    return cursor_cats


def load_payment_methods():
    conn = db.connect()
    cursor_methods = conn.cursor()
    cursor_methods.execute("SELECT * FROM payment_methods")

    return cursor_methods


class Funds(QWidget):

    def __init__(self, *args):
        super().__init__()
        loadUi("ui/pay.ui", self)
        self.category.setCurrentText("კატეგორია")
        self.years_combo.setCurrentText(str(year))
        self.appo_id = None
        self.zone_text_label = ''
        if args:
            args_list = [arg for arg in args]
            self.appo_id = str(args_list[0])
            self.fname.setText(str(args_list[1]))
            self.lname.setText(str(args_list[2]))
            self.phone.setText(str(args_list[3]))
            self.category.setCurrentText(str(args_list[4]))
            if len(args_list) == 6:
                self.zone_text.setText(f"ზონა: {str(args_list[5])}")
                self.zone_text_label = str(args_list[5])
        self.load_sub_types()
        self.conn = db.connect()
        self.search_button.clicked.connect(self.search_client)
        cursor_init = self.conn.cursor()
        cursor_init.execute("SELECT * from payments WHERE date=%s", (today,))
        self.load_payments_table(cursor_init)
        self.new_date.dateChanged.connect(self.change_date_daily)
        # Monthly report
        for key, value in load_months()[1].items():
            self.months_combo.addItem(value)
        years_num = sorted({year_num for year_num in load_years()})
        for year_num in years_num:
            self.years_combo.addItem(year_num)
        cursor_months = self.conn.cursor()
        cursor_months.execute("SELECT * FROM `payments` WHERE month(date)=%s AND year(date)=%s", (self.months_combo.currentText(), year,))
        self.load_payments_months(cursor_months, month_number, year)
        self.months_combo.currentTextChanged.connect(self.change_month)
        self.years_combo.currentTextChanged.connect(self.change_year)

        self.categories = load_categories()
        for category in self.categories:
            self.category.addItem(category[1])

        self.solarium_choose.currentTextChanged.connect(self.load_sub_types)

        self.payment_methods = load_payment_methods()
        for method in self.payment_methods:
            self.payment_method.addItem(method[1])
        self.payment_method.setCurrentText("გადახდის მეთოდი")

        self.pay_button.clicked.connect(self.pay)
        # Subscription
        for method in load_payment_methods():
            self.pay_method.addItem(method[1])
        self.pay_method.setCurrentText("გადახდის მეთოდი")
        self.search_button_sub.clicked.connect(self.search_client_sub)
        self.buy.clicked.connect(self.buy_subscription)

    def closeEvent(self, event):
        from main_window import MainWindow
        MainWindow().load_data()

    def load_current_date(self):
        global today
        today = datetime.now().date().strftime("%Y-%m-%d")
        self.change_month()
        self.months_combo.setCurrentText(month_name)
        self.years_combo.setCurrentText(str(year))

    def load_sub_types(self):
        solarium_name = self.solarium_choose.currentText()
        solariums = {
            "სოლარიუმი 1": "sub_types_sol_1",
            "სოლარიუმი 2": "sub_types_sol_2"
        }
        conn = db.connect()
        cursor_sub_types = conn.cursor()
        cursor_sub_types.execute(f"SELECT * FROM {solariums[solarium_name]}")
        self.minutes.clear()
        for sub_type in cursor_sub_types:
            self.minutes.addItem(sub_type[1])

    def change_date_daily(self):
        global today

        today = self.new_date.text()
        self.all_payments.clearContents()
        cursor23 = self.conn.cursor()
        cursor23.execute("SELECT * from payments WHERE date=%s", (today,))
        self.load_payments_table(cursor23)

    def change_month(self):
        global year, month_number

        month_number = self.months_combo.currentText()
        self.all_payments_mon.clearContents()
        cursor21 = self.conn.cursor()
        cursor21.execute("SELECT * FROM `payments` WHERE month(date)=%s AND year(date)=%s", (self.months_combo.currentText(), self.years_combo.currentText(),))
        self.load_payments_months(cursor21, month_number, year)

    def change_year(self):
        global year, month_number

        self.all_payments_mon.clearContents()
        cursor22 = self.conn.cursor()
        cursor22.execute("SELECT * FROM `payments` WHERE month(date)=%s AND year(date)=%s", (self.months_combo.currentText(), self.years_combo.currentText(),))
        year = self.years_combo.currentText()
        self.load_payments_months(cursor22, month_number, year)

    def clear_fields(self):
        self.conn.commit()
        self.fname.clear()
        self.lname.clear()
        self.phone.clear()
        self.amount.clear()
        self.search_by_phone.clear()
        self.balance.setText("0 წუთი")
        self.category.setCurrentText("კატეგორია")
        self.payment_method.setCurrentText("გადახდის მეთოდი")

    def load_clients(self):
        cursor10 = self.conn.cursor()
        cursor10.execute("SELECT * FROM clients")
        clients = [client for client in cursor10]
        return clients

    def search_client(self):
        search = self.search_by_phone.text()
        cursor11 = self.conn.cursor()
        cursor11.execute("SELECT * FROM clients WHERE phone=%s", (search,))

        if cursor11.rowcount == 0:
            QMessageBox.warning(self, "შეცდომა",
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                f"გადახდის დასაფიქსირებლად.")
        else:
            for client in cursor11:
                if search == client[3]:
                    self.fname.setText(client[1])
                    self.lname.setText(client[2])
                    self.phone.setText(client[3])
                    self.balance.setText(f"{client[5]} წუთი")

    def search_client_2(self):
        search = self.phone.text()
        cursor11 = self.conn.cursor()
        cursor11.execute("SELECT * FROM clients WHERE phone=%s", (search,))

        if cursor11.rowcount == 0:
            QMessageBox.warning(self, "შეცდომა",
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                f"გადახდის დასაფიქსირებლად.")
        else:
            for client in cursor11:
                if search == client[3]:
                    self.balance.setText(f"{client[5]} წუთი")

    def pay(self):
        categories = {
            "კოსმეტოლოგია": "cosmetology_appointments",
            "ლაზერი": "laser_appointments",
            "სოლარიუმი 1": "solarium_1_appointments",
            "სოლარიუმი 2": "solarium_2_appointments"
        }
        clients = self.load_clients()
        first_name = self.fname.text()
        last_name = self.lname.text()
        phone = self.phone.text()
        amount = self.amount.text()
        category = self.category.currentText()
        method = self.payment_method.currentText()
        status = "paid"
        time_now = datetime.now().time().strftime("%H:%M")

        if self.payment_method.currentText() == "გადახდის მეთოდი":
            QMessageBox.warning(self, "შეცდომა", "აირჩიეთ გადახდის მეთოდი")
        elif self.category.currentText() == "კატეგორია":
            QMessageBox.warning(self, "შეცდომა", "აირჩიეთ კატეგორია")
        elif method == "წუთები":
            cursor16 = self.conn.cursor()
            cursor16.execute("SELECT * FROM clients WHERE phone=%s", (phone,))
            if cursor16.rowcount == 0:
                QMessageBox.warning(self, "შეცდომა",
                                    f"პაციენტი ნომრით: {phone} არ მოიძებნა ბაზაში, გთხოვთ შეავსეთ შესაბამისი ველები "
                                    f"გადახდის დასაფიქსირებლად.")
            else:
                existing = [minute[5] for minute in cursor16]
                existing_minutes = sum(existing)
                if existing_minutes < int(amount):
                    QMessageBox.warning(self, "არასაკმარისი წუთები",
                                        f"აბონემენტი ნომრით: {phone} არ აქვს საკმარისი წუთები ბალანსზე,"
                                        f"\nბალანსი: {existing_minutes} წუთი.")
                    self.clear_fields()
                else:
                    cursor18 = self.conn.cursor()
                    cursor18.execute("INSERT INTO payments (fname, lname, phone, category, payment_method, date, "
                                     "minutes, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                               method, today, amount, 0))
                    self.conn.commit()
                    cursor80 = self.conn.cursor()
                    cursor80.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                                     "VALUES (?, ?, ?, ?, ?, ?)",
                                     (f"{first_name} {last_name}", category, today, time_now, phone,
                                      f"განყ.: გადახდა | წუთი: {amount}, გადახდის მეთოდი: {method}"))
                    self.conn.commit()
                    if self.appo_id is not None:
                        cursor44 = self.conn.cursor()
                        cursor44.execute(f"UPDATE {categories[category]} SET status=%s "
                                         f"WHERE id=%s", (status, self.appo_id))
                        self.conn.commit()
                    cursor20 = self.conn.cursor()
                    cursor20.execute("SELECT * from payments WHERE date=%s", (today,))
                    self.load_payments_table(cursor20)
                    updated_minutes = existing_minutes - int(amount)
                    cursor17 = self.conn.cursor()
                    cursor17.execute("UPDATE clients SET minutes=%s WHERE phone=%s", (updated_minutes, phone,))
                    self.conn.commit()
                    self.clear_fields()
                    QMessageBox.information(self, "წარმატებული გადახდა", "გადახდა წარმატებით განხორციელდა!")

        else:
            if first_name == "" or last_name == "" or phone == "" or amount == "":
                QMessageBox.information(self, "შეცდომა",
                                        f"ყველა ველის შევსება სავალდებულოა")
            else:
                cursor12 = self.conn.cursor()
                cursor12.execute("SELECT * FROM payments")

                client_phones = [client[3] for client in clients]
                if phone not in client_phones:
                    cursor13 = self.conn.cursor()
                    cursor13.execute("INSERT INTO payments (fname, lname, phone, category, payment_method, date, "
                                     "minutes, amount) VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                              method, today, 0, amount))
                    self.conn.commit()

                    if category == "ლაზერი":
                        cursor80 = self.conn.cursor()
                        cursor80.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                                             "VALUES (?, ?, ?, ?, ?, ?)",
                                             (f"{first_name} {last_name}", category, today, time_now, phone,
                                              f"განყ.: გადახდა | ზონა: {self.zone_text_label}, გადახდის მეთოდი: {method}, თანხა: {amount} ლარი"))
                        self.conn.commit()
                    else:
                        cursor80 = self.conn.cursor()
                        cursor80.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                                         "VALUES (?, ?, ?, ?, ?, ?)",
                                         (f"{first_name} {last_name}", category, today, time_now, phone,
                                          f"განყ.: გადახდა | გადახდის მეთოდი: {method}, თანხა: {amount} ლარი"))
                        self.conn.commit()
                    if self.appo_id is not  None:
                        cursor44 = self.conn.cursor()
                        cursor44.execute(f"UPDATE {categories[category]} SET status=%s "
                                         f"WHERE id=%s", (status, self.appo_id))
                        self.conn.commit()
                    cursor24 = self.conn.cursor()
                    cursor24.execute("SELECT * from payments WHERE date=%s", (today,))
                    self.load_payments_table(cursor24)
                    balance = 0
                    init_minutes = 0
                    cursor14 = self.conn.cursor()
                    cursor14.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                     "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, init_minutes))
                    self.conn.commit()
                    self.clear_fields()
                    cursor25 = self.conn.cursor()
                    cursor25.execute("SELECT * from payments WHERE date=%s", (today,))
                    self.load_payments_table(cursor25)

                else:
                    cursor15 = self.conn.cursor()
                    cursor15.execute("INSERT INTO payments (fname, lname, phone, category, payment_method, date, "
                                     "minutes, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                              method, today, 0, amount))
                    self.conn.commit()
                    if self.zone_text_label == '':
                        cursor80 = self.conn.cursor()
                        cursor80.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                                         "VALUES (?, ?, ?, ?, ?, ?)",
                                         (f"{first_name} {last_name}", category, today, time_now, phone,
                                          f"განყ.: გადახდა | გადახდის მეთოდი: {method}, თანხა: {amount} ლარი"))
                        self.conn.commit()
                    else:
                        cursor99 = self.conn.cursor()
                        cursor99.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                                             "VALUES (?, ?, ?, ?, ?, ?)",
                                             (f"{first_name} {last_name}", category, today, time_now, phone,
                                              f"განყ.: გადახდა | ზონა: {self.zone_text_label}, გადახდის მეთოდი: {method}, თანხა: {amount} ლარი"))
                        self.conn.commit()
                    if self.appo_id is not None:
                        cursor44 = self.conn.cursor()
                        cursor44.execute(f"UPDATE {categories[category]} SET status=%s "
                                         f"WHERE id=%s", (status, self.appo_id))
                        self.conn.commit()
                    cursor26 = self.conn.cursor()
                    cursor26.execute("SELECT * from payments WHERE date=%s", (today,))
                    QMessageBox.information(self, "წარმატებული გადახდა", "გადახდა წარმატებით განხორციელდა!")
                    self.clear_fields()
                    self.load_payments_table(cursor26)
        cursor_months = self.conn.cursor()
        cursor_months.execute("SELECT * FROM `payments` WHERE month(date)=%s AND year(date)=%s", (self.months_combo.currentText(), self.years_combo.currentText(),))
        self.load_payments_months(cursor_months, month_name, year)
        self.conn.close()

    def load_payments_table(self, data):
        self.all_payments.setRowCount(data.rowcount)
        self.all_payments.setColumnCount(8)

        self.all_payments.setColumnWidth(0, 120)
        self.all_payments.setColumnWidth(1, 200)
        self.all_payments.setColumnWidth(2, 100)
        self.all_payments.setColumnWidth(3, 150)
        self.all_payments.setColumnWidth(4, 160)
        self.all_payments.setColumnWidth(5, 90)
        self.all_payments.setColumnWidth(6, 60)
        self.all_payments.setColumnWidth(7, 60)

        self.all_payments.clearContents()
        payments = [payment for payment in data]
        total_cash = [pay[8] for pay in payments if pay[5] == "ნაღდი"]
        total_card = [pay[8] for pay in payments if pay[5] == "უნაღდო"]
        total_by_minutes = [pay[7] for pay in payments if pay[5] == "წუთები"]
        total_cos = [pay[8] for pay in payments if pay[4] == "კოსმეტოლოგია"]
        total_las = [pay[8] for pay in payments if pay[4] == "ლაზერი"]
        total_sol_1 = [pay[8] for pay in payments if pay[4] == "სოლარიუმი 1"]
        total_sol_2 = [pay[8] for pay in payments if pay[4] == "სოლარიუმი 2"]
        total_subs = [pay[8] for pay in payments if pay[4] == "აბონემენტი"]
        self.total_daily.setText(str(sum(total_cash) + sum(total_card)))
        self.cash.setText(str(sum(total_cash)))
        self.card.setText(str(sum(total_card)))
        self.cos_total.setText(str(sum(total_cos)))
        self.las_total.setText(str(sum(total_las)))
        self.sol_1_total.setText(str(sum(total_sol_1)))
        self.sol_2_total.setText(str(sum(total_sol_2)))
        self.subscriptions.setText(str(sum(total_subs)))
        self.new_date.setDate(datetime.strptime(today, "%Y-%m-%d"))
        self.pay_by_minutes.setText(str(sum(total_by_minutes)))
        self.all_payments.horizontalHeader().setVisible(True)
        self.all_payments.verticalHeader().setVisible(True)
        row = 0
        for item in payments:
            self.all_payments.setItem(row, 0, QTableWidgetItem(item[1]))
            self.all_payments.setItem(row, 1, QTableWidgetItem(item[2]))
            self.all_payments.setItem(row, 2, QTableWidgetItem(item[3]))
            self.all_payments.setItem(row, 3, QTableWidgetItem(item[4]))
            self.all_payments.setItem(row, 4, QTableWidgetItem(item[5]))
            self.all_payments.setItem(row, 5, QTableWidgetItem(item[6]))
            if item[8] == 0:
                self.all_payments.setItem(row, 6, QTableWidgetItem(f"-{str(item[7])}"))
            else:
                self.all_payments.setItem(row, 6, QTableWidgetItem(str(item[7])))
            self.all_payments.setItem(row, 7, QTableWidgetItem(str(item[8])))
            if item[5] == "ნაღდი":
                self.all_payments.item(row, 0).setBackground(QColor(255, 251, 193))
                self.all_payments.item(row, 1).setBackground(QColor(255, 251, 193))
                self.all_payments.item(row, 2).setBackground(QColor(255, 251, 193))
                self.all_payments.item(row, 3).setBackground(QColor(255, 251, 193))
                self.all_payments.item(row, 4).setBackground(QColor(255, 251, 193))
                self.all_payments.item(row, 5).setBackground(QColor(255, 251, 193))
                self.all_payments.item(row, 6).setBackground(QColor(255, 251, 193))
                self.all_payments.item(row, 7).setBackground(QColor(255, 251, 193))
            elif item[5] == "უნაღდო":
                self.all_payments.item(row, 0).setBackground(QColor(226, 246, 202))
                self.all_payments.item(row, 1).setBackground(QColor(226, 246, 202))
                self.all_payments.item(row, 2).setBackground(QColor(226, 246, 202))
                self.all_payments.item(row, 3).setBackground(QColor(226, 246, 202))
                self.all_payments.item(row, 4).setBackground(QColor(226, 246, 202))
                self.all_payments.item(row, 5).setBackground(QColor(226, 246, 202))
                self.all_payments.item(row, 6).setBackground(QColor(226, 246, 202))
                self.all_payments.item(row, 7).setBackground(QColor(226, 246, 202))
            elif item[5] == "წუთები":
                self.all_payments.item(row, 0).setBackground(QColor(184, 231, 225))
                self.all_payments.item(row, 1).setBackground(QColor(184, 231, 225))
                self.all_payments.item(row, 2).setBackground(QColor(184, 231, 225))
                self.all_payments.item(row, 3).setBackground(QColor(184, 231, 225))
                self.all_payments.item(row, 4).setBackground(QColor(184, 231, 225))
                self.all_payments.item(row, 5).setBackground(QColor(184, 231, 225))
                self.all_payments.item(row, 6).setBackground(QColor(184, 231, 225))
                self.all_payments.item(row, 7).setBackground(QColor(184, 231, 225))

            row += 1

    def load_payments_months(self, data, month, year_num):
        global month_number, year
        self.all_payments_mon.setRowCount(data.rowcount)
        self.all_payments_mon.setColumnCount(8)

        self.all_payments_mon.setColumnWidth(0, 120)
        self.all_payments_mon.setColumnWidth(1, 200)
        self.all_payments_mon.setColumnWidth(2, 100)
        self.all_payments_mon.setColumnWidth(3, 150)
        self.all_payments_mon.setColumnWidth(4, 160)
        self.all_payments_mon.setColumnWidth(5, 90)
        self.all_payments_mon.setColumnWidth(6, 60)
        self.all_payments_mon.setColumnWidth(7, 60)

        self.all_payments_mon.clearContents()
        payments = [payment for payment in data if (payment[6].split("-")[0] == str(year_num))]
        self.all_payments_mon.setRowCount(len(payments))
        total_cash = [pay[8] for pay in payments if pay[5] == "ნაღდი"]
        total_card = [pay[8] for pay in payments if pay[5] == "უნაღდო"]
        total_by_minutes = [pay[7] for pay in payments if pay[5] == "წუთები"]
        total_cos_m = [pay[8] for pay in payments if pay[4] == "კოსმეტოლოგია"]
        total_las_m = [pay[8] for pay in payments if pay[4] == "ლაზერი"]
        total_sol_1_m = [pay[8] for pay in payments if pay[4] == "სოლარიუმი 1"]
        total_sol_2_m = [pay[8] for pay in payments if pay[4] == "სოლარიუმი 2"]
        total_subs_m = [pay[8] for pay in payments if pay[4] == "აბონემენტი"]
        self.total_daily_mon.setText(str(sum(total_cash) + sum(total_card)))
        self.cash_mon.setText(str(sum(total_cash)))
        self.card_mon.setText(str(sum(total_card)))
        self.cos_total_m.setText(str(sum(total_cos_m)))
        self.las_total_m.setText(str(sum(total_las_m)))
        self.sol_1_total_m.setText(str(sum(total_sol_1_m)))
        self.sol_2_total_m.setText(str(sum(total_sol_2_m)))
        self.subscriptions_m.setText(str(sum(total_subs_m)))
        self.pay_by_minutes_mon.setText(str(sum(total_by_minutes)))
        self.months_combo.setCurrentText(str(month))
        self.years_combo.setCurrentText(str(year_num))
        self.all_payments_mon.horizontalHeader().setVisible(True)
        self.all_payments_mon.verticalHeader().setVisible(True)
        row = 0
        for item in payments:
            self.all_payments_mon.setItem(row, 0, QTableWidgetItem(item[1]))
            self.all_payments_mon.setItem(row, 1, QTableWidgetItem(item[2]))
            self.all_payments_mon.setItem(row, 2, QTableWidgetItem(item[3]))
            self.all_payments_mon.setItem(row, 3, QTableWidgetItem(item[4]))
            self.all_payments_mon.setItem(row, 4, QTableWidgetItem(item[5]))
            self.all_payments_mon.setItem(row, 5, QTableWidgetItem(item[6]))
            if item[8] == 0:
                self.all_payments_mon.setItem(row, 6, QTableWidgetItem(f"-{str(item[7])}"))
            else:
                self.all_payments_mon.setItem(row, 6, QTableWidgetItem(str(item[7])))
            self.all_payments_mon.setItem(row, 7, QTableWidgetItem(str(item[8])))
            if item[5] == "ნაღდი":
                self.all_payments_mon.item(row, 0).setBackground(QColor(255, 251, 193))
                self.all_payments_mon.item(row, 1).setBackground(QColor(255, 251, 193))
                self.all_payments_mon.item(row, 2).setBackground(QColor(255, 251, 193))
                self.all_payments_mon.item(row, 3).setBackground(QColor(255, 251, 193))
                self.all_payments_mon.item(row, 4).setBackground(QColor(255, 251, 193))
                self.all_payments_mon.item(row, 5).setBackground(QColor(255, 251, 193))
                self.all_payments_mon.item(row, 6).setBackground(QColor(255, 251, 193))
                self.all_payments_mon.item(row, 7).setBackground(QColor(255, 251, 193))
            elif item[5] == "უნაღდო":
                self.all_payments_mon.item(row, 0).setBackground(QColor(226, 246, 202))
                self.all_payments_mon.item(row, 1).setBackground(QColor(226, 246, 202))
                self.all_payments_mon.item(row, 2).setBackground(QColor(226, 246, 202))
                self.all_payments_mon.item(row, 3).setBackground(QColor(226, 246, 202))
                self.all_payments_mon.item(row, 4).setBackground(QColor(226, 246, 202))
                self.all_payments_mon.item(row, 5).setBackground(QColor(226, 246, 202))
                self.all_payments_mon.item(row, 6).setBackground(QColor(226, 246, 202))
                self.all_payments_mon.item(row, 7).setBackground(QColor(226, 246, 202))
            elif item[5] == "წუთები":
                self.all_payments_mon.item(row, 0).setBackground(QColor(184, 231, 225))
                self.all_payments_mon.item(row, 1).setBackground(QColor(184, 231, 225))
                self.all_payments_mon.item(row, 2).setBackground(QColor(184, 231, 225))
                self.all_payments_mon.item(row, 3).setBackground(QColor(184, 231, 225))
                self.all_payments_mon.item(row, 4).setBackground(QColor(184, 231, 225))
                self.all_payments_mon.item(row, 5).setBackground(QColor(184, 231, 225))
                self.all_payments_mon.item(row, 6).setBackground(QColor(184, 231, 225))
                self.all_payments_mon.item(row, 7).setBackground(QColor(184, 231, 225))
            row += 1

        month_name = calendar.month_name[int(today.split("-")[1])]

    def clear_fields_sub(self):
        self.conn.commit()
        self.fname_sub.clear()
        self.lname_sub.clear()
        self.phone_sub.clear()
        self.minutes.clear()
        self.cur_balance.setText("")
        self.pay_method.setCurrentText("გადახდის მეთოდი")
        self.search.clear()

    def load_clients_sub(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = [client for client in cursor]
        return clients

    def search_client_sub(self):
        search = self.search.text()
        cursor6 = self.conn.cursor()
        cursor6.execute("SELECT * FROM clients WHERE phone=%s", (search,))

        if cursor6.rowcount == 0:
            QMessageBox.warning(self, 'შეცდომა',
                                f"პაციენტი ნომრით: {search} არ მოიძებნა ბაზაში"
                                f"\nგთხოვთ შეავსეთ შესაბამისი ველები აბონემენტის დასარეგისტრირებლად.")
        else:
            for client in cursor6:
                if search == client[3]:
                    self.fname_sub.setText(client[1])
                    self.lname_sub.setText(client[2])
                    self.phone_sub.setText(client[3])
                    self.cur_balance.setText(f"{str(client[5])} წუთი")

    def buy_subscription(self):
        category = "აბონემენტი"
        clients = self.load_clients_sub()
        first_name = self.fname_sub.text()
        last_name = self.lname_sub.text()
        phone = self.phone_sub.text()
        minutes = self.minutes.currentText()
        solarium = self.solarium_choose.currentText()
        method = self.pay_method.currentText()
        time_now = datetime.now().time().strftime("%H:%M")

        solariums = {
            "სოლარიუმი 1": "sub_types_sol_1",
            "სოლარიუმი 2": "sub_types_sol_2"
        }

        checked_phone = check_integer(phone)
        checked_minutes = check_integer(minutes)

        if first_name == "" or last_name == "" or phone == "" or minutes == "":
            QMessageBox.warning(self, 'შეცდომა',
                                f'ყველა ველის შევსება სავალდებულოა')
        elif self.pay_method.currentText() == "გადახდის მეთოდი":
            QMessageBox.warning(self, 'შეცდომა',
                                f'აირჩიეთ გადახდის მეთოდი')
        elif not checked_phone:
            QMessageBox.warning(self, 'შეცდომა', "ტელეფონის ველში მხოლოდ ციფრებია დაშვებული!")
        elif not checked_minutes:
            QMessageBox.warning(self, 'შეცდომა', "წუთების ველში მხოლოდ ციფრებია დაშვებული!")
        else:
            cursor2 = self.conn.cursor()
            cursor2.execute("SELECT * FROM clients")
            balance = 0
            if cursor2.rowcount == 0:
                cursor3 = self.conn.cursor()
                cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, minutes))
                self.conn.commit()
                cursor50 = self.conn.cursor()
                cursor50.execute(f"SELECT * FROM {solariums[solarium]} WHERE sub_type=%s", (minutes,))
                money = [money[2] for money in cursor50]
                cursor_buy = self.conn.cursor()
                cursor_buy.execute("INSERT INTO payments (fname, lname, phone, category, payment_method, date, minutes,"
                                   "amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                               method, today, minutes, money[0]))
                self.conn.commit()
                cursor85 = self.conn.cursor()
                cursor85.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                                 "VALUES (?, ?, ?, ?, ?, ?)",
                                 (f"{first_name} {last_name}", category, today, time_now, phone,
                                  f"განყ.: აბონემენტი | წუთი: {minutes}, გადახდის მეთოდი: {method}"))
                self.conn.commit()

                cursor51 = self.conn.cursor()
                cursor51.execute(
                    "INSERT INTO subscriptions (fname, lname, phone, solarium, minutes, money, payment_method) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, solarium, minutes, money[0], method)
                )
                self.conn.commit()
                cursor30 = self.conn.cursor()
                cursor30.execute("SELECT * from payments WHERE date=%s", (today,))
                self.load_payments_table(cursor30)
            else:
                client_phones = [client[3] for client in clients]
                if phone not in client_phones:
                    cursor3 = self.conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone, balance, minutes) "
                                    "VALUES (?, ?, ?, ?, ?)", (first_name, last_name, phone, balance, minutes))
                    self.conn.commit()
                    cursor50 = self.conn.cursor()
                    cursor50.execute(f"SELECT * FROM {solariums[solarium]} WHERE sub_type=%s", (minutes,))
                    money = [money[2] for money in cursor50]
                    cursor_buy = self.conn.cursor()
                    cursor_buy.execute(
                        "INSERT INTO payments (fname, lname, phone, category, payment_method, date, minutes,"
                        "amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                    method, today, minutes, money[0]))
                    self.conn.commit()
                    cursor85 = self.conn.cursor()
                    cursor85.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                                     "VALUES (?, ?, ?, ?, ?, ?)",
                                     (f"{first_name} {last_name}", category, today, time_now,
                                      phone,
                                      f"განყ.: აბონემენტი | წუთი: {minutes}, გადახდის მეთოდი: {method}"))
                    self.conn.commit()
                    cursor50 = self.conn.cursor()
                    cursor50.execute(
                        "INSERT INTO subscriptions (fname, lname, phone, solarium, minutes, money, payment_method) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (first_name, last_name, phone, solarium, minutes, money[0], method)
                    )
                    self.conn.commit()
                    cursor31 = self.conn.cursor()
                    cursor31.execute("SELECT * from payments WHERE date=%s", (today,))
                    self.load_payments_table(cursor31)
                    QMessageBox.information(self, 'აბონემენტის შეძენა',
                                            f"აბონემენტი დარეგისტრირდა:\nსახელი, გვარი: {first_name} {last_name}"
                                            f"\nწუთი: {minutes}")
                    self.clear_fields_sub()
                else:
                    cursor4 = self.conn.cursor()
                    cursor4.execute("SELECT * FROM clients WHERE phone=%s", (phone,))
                    existing = [minute[5] for minute in cursor4]
                    existing_minutes = sum(existing)
                    updated_minutes = existing_minutes + int(minutes)
                    cursor5 = self.conn.cursor()
                    cursor5.execute("UPDATE clients SET minutes=%s WHERE phone=%s", (updated_minutes, phone,))
                    QMessageBox.information(self, 'აბონემენტის შეძენა',
                                            f"აბონემენტი დარეგისტრირდა:\nსახელი, გვარი: {first_name} {last_name}"
                                            f"\nწუთი: {minutes}")
                    self.clear_fields_sub()
                    self.conn.commit()
                    cursor50 = self.conn.cursor()
                    cursor50.execute(f"SELECT * FROM {solariums[solarium]} WHERE sub_type=%s", (minutes,))
                    money = [money[2] for money in cursor50]
                    cursor_buy = self.conn.cursor()
                    cursor_buy.execute(
                        "INSERT INTO payments (fname, lname, phone, category, payment_method, date, minutes,"
                        "amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, phone, category,
                                                                    method, today, minutes, money[0])
                    )
                    self.conn.commit()
                    cursor85 = self.conn.cursor()
                    cursor85.execute("INSERT INTO patient_history (fname_lname, category, date, time, phone, details)"
                                     "VALUES (?, ?, ?, ?, ?, ?)",
                                     (f"{first_name} {last_name}", category, today, time_now,
                                      phone,
                                      f"განყ.: აბონემენტი | წუთი: {minutes}, გადახდის მეთოდი: {method}"))
                    self.conn.commit()
                    cursor50 = self.conn.cursor()
                    cursor50.execute(
                        "INSERT INTO subscriptions (fname, lname, phone, solarium, minutes, money, payment_method) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (first_name, last_name, phone, solarium, minutes, money[0], method)
                    )
                    self.conn.commit()
                    cursor32 = self.conn.cursor()
                    cursor32.execute("SELECT * from payments WHERE date=%s", (today,))
                    self.load_payments_table(cursor32)
