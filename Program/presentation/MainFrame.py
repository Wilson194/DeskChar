from PyQt5.QtWidgets import QFrame, QGridLayout


class MainFrame(QFrame):
    """
    Class for main frame of main Window
    """


    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid = QGridLayout()

        self.init_ui()


    def init_ui(self):
        self.setLayout(self.grid)
