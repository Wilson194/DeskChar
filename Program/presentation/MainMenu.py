from PyQt5.QtWidgets import QMenuBar


class MainMenu:
    def __init__(self, menu_bar: QMenuBar):
        self.menu_bar = menu_bar

        self.init_ui()


    def init_ui(self):
        file_menu = self.menu_bar.addMenu('test')
