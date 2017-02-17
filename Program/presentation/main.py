import sys, random
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QLabel
from PyQt5 import QtCore

from presentation.MainMenu import MainMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print(self.tr('Apple'))
        self.init_ui()


    def init_ui(self):
        MainMenu(self.menuBar())

        self.show()
