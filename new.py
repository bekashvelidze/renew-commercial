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
            for client in cursor2:
                if phone != client[3]:
                    cursor3 = conn.cursor()
                    cursor3.execute("INSERT INTO clients (fname, lname, phone) "
                                    "VALUES (?, ?, ?)", (first_name, last_name, phone))
                    conn.commit()
        conn.close()

        QMessageBox.information(self, 'პაციენტი ჩაიწერა',
                                f"პაციენტი ჩაწერილია:\nსახელი, გვარი: {first_name} {last_name}"
                                f"\nდრო: {time}")
        self.load_data()
