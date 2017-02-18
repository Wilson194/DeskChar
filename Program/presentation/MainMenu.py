from PyQt5.QtWidgets import QMenuBar, QAction, qApp
from PyQt5.QtGui import QIcon
from presentation.Translate import Translate as TR


class MainMenu:
    def __init__(self, menu_bar: QMenuBar):
        self.menu_bar = menu_bar

        self.init_ui()


    def init_ui(self):
        exit_action = QAction(QIcon('resources/icons/exit.png'), TR().tr('Menu_exit'),
                              self.menu_bar)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        open_action = QAction(QIcon('resources/icons/open.png'), TR().tr('Menu_open'),
                              self.menu_bar)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open file')

        save_action = QAction(QIcon('resources/icons/save.png'), TR().tr('Menu_save'),
                              self.menu_bar)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save file')

        file_menu = self.menu_bar.addMenu(TR().tr('Menu_file'))
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        about_action = QAction(TR().tr('Menu_about'), self.menu_bar)
        help_menu = self.menu_bar.addMenu(TR().tr('Menu_help'))
        help_menu.addAction(about_action)
