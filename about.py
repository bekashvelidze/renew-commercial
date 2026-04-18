import os
from datetime import datetime

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from helpers_functions import get_version, BASE_DIR, resource_path


class About(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path('icons/renew.ico')))
        loadUi(os.path.join(BASE_DIR, 'ui', 'about.ui'), self)
        production_year = 2023
        current_year = datetime.now().year
        if datetime.now().year == production_year:
            self.years.setText(str(production_year))
        else:
            self.years.setText(f"{str(production_year)} - {str(current_year)}")

        self.version.setText(get_version())

