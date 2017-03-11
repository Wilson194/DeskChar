from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from presentation.MainMenu import MainMenu
from presentation.StatusBar import StatusBar
from structure.enums.ObjectType import ObjectType
from presentation.widgets.TreeWidget import TreeWidget
from presentation.widgets.TabWidget import TabWidget
from presentation.Toolbar import ToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabWidget = None
        self.splitter = None
        self.grid_layout = None
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('DeskChar')
        self.setWindowIcon(QtGui.QIcon('resources/icons/char.png'))

        self.setMenuWidget(MainMenu())
        self.setStatusBar(StatusBar())
        self.toolBar = ToolBar(parent=self)

        self.setObjectName('MainWindow')

        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName('central widget')

        self.grid_layout = QGridLayout(self.centralWidget)
        self.grid_layout.setObjectName('Grid layout')

        self.menuWidget().templates_menu_signal.connect(self.redraw_central_widget)
        self.toolBar.templates_tool_signal.connect(self.redraw_central_widget)

        self.setCentralWidget(self.centralWidget)
        self.setGeometry(200, 50, 800, 800)
        # self.showMaximized()
        self.show()


    def redraw_central_widget(self, object_type: ObjectType):
        for i in range(self.centralWidget.layout().count()):
            self.tabWidget.destroy()
            self.centralWidget.layout().takeAt(i).widget().setHidden(True)

        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setHandleWidth(15)

        tree = TreeWidget(self.splitter, object_type)
        self.tabWidget = TabWidget(self.splitter, None, object_type)
        tree.item_doubleclick_signal.connect(self.tabWidget.tree_item_clicked)

        self.tabWidget.setObjectName("tabWidget")

        self.grid_layout.addWidget(self.splitter, 0, 0, 1, 1)
        self.splitter.setSizes([200, 600])

        self.show()
