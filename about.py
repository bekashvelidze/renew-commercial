from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi


class About(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/about.ui", self)