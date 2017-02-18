from PyQt5.QtWidgets import QFrame, QHBoxLayout, QGridLayout
from PyQt5.QtCore import *


class MainFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid = QGridLayout()

        self.init_ui()


    def init_ui(self):

        self.setLayout(self.grid)

