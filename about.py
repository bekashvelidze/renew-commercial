import json
from datetime import datetime
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi


def get_version():
    with open("version.json", "r") as file:
        version = json.load(file)

    return version["version"]


class About(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/about.ui", self)
        production_year = 2023
        current_year = datetime.now().year
        if datetime.now().year == production_year:
            self.years.setText(str(production_year))
        else:
            self.years.setText(f"{str(production_year)} - {str(current_year)}")

        self.version.setText(get_version())

