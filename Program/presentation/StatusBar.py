from PyQt5 import QtWidgets


class StatusBar(QtWidgets.QStatusBar):
    """
    Class for status bar in window. 
    Some actions and tooltip is displayed there
    """


    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        pass
