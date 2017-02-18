import sys, random
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QLabel
from PyQt5 import QtCore

from presentation.MainMenu import MainMenu
from presentation.StatusBar import StatusBar
from presentation.TreeWidget import TreeWidget
from presentation.MainFrame import MainFrame


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        MainMenu(self.menuBar())
        StatusBar(self.statusBar())

        central_frame = MainFrame(self)
        self.setCentralWidget(central_frame)
        TreeWidget(self.centralWidget())

        self.show()
