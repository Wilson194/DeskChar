import sys, random
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QLabel
from PyQt5 import QtCore

from presentation.MainMenu import MainMenu
from presentation.StatusBar import StatusBar
from presentation.TreeWidget import TreeWidget
from presentation.MainFrame import MainFrame
from data.DAO.SpellDAO import SpellDAO


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        MainMenu(self.menuBar())
        StatusBar(self.statusBar())

        central_frame = MainFrame(self)
        self.setCentralWidget(central_frame)

        tree = TreeWidget(self.centralWidget())
        tree2 = TreeWidget(self.centralWidget())


        central_frame.grid.addWidget(tree, 1, 1)
        central_frame.grid.addWidget(tree2, 1, 2)

        self.show()
