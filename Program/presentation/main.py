from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from presentation.MainMenu import MainMenu
from presentation.StatusBar import StatusBar
from presentation.layouts.SpellLayout import SpellLayout
from structure.enums.ObjectType import ObjectType
from widgets.TreeWidget import TreeWidget
from presentation.widgets.TabWidget import TabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        MainMenu(self.menuBar())
        StatusBar(self.statusBar())

        self.setObjectName('MainWindow')

        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName('central widget')

        self.grid_layout = QGridLayout(self.centralWidget)
        self.grid_layout.setObjectName('Grid layout')

        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setHandleWidth(15)

        tree = TreeWidget(self.splitter, ObjectType.SPELL)
        tree.item_doubleclick_signal.connect(self.test)
        # tree.set_items(PlayerTreeManager().get_spell_tree())

        self.tabWidget = TabWidget(self.splitter)
        # self.tabWidget.setObjectName("tabWidget")
        # self.tab = QtWidgets.QWidget()
        # self.tab.setObjectName("tab")
        # self.tabWidget.addTab(self.tab, "CS")

        # SpellLayout(self.tab)

        # self.tab_2 = QtWidgets.QWidget()
        # self.tab_2.setObjectName("tab_2")
        # self.tabWidget.addTab(self.tab_2, "EN")
        #
        # self.tab_2 = QtWidgets.QWidget()
        # self.tab_2.setObjectName("tab_2")
        # self.tabWidget.addTab(self.tab_2, "+")

        self.grid_layout.addWidget(self.splitter, 0, 0, 1, 1)
        self.setCentralWidget(self.centralWidget)

        self.splitter.setSizes([200, 600])
        self.setGeometry(2000, 50, 800, 800)
        self.show()


    def test(self, item):
        print(item)
