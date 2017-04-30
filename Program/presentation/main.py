from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from presentation.MainMenu import MainMenu
from presentation.StatusBar import StatusBar
from presentation.widgets.MapWidget import MapWidget
from structure.enums.ObjectType import ObjectType
from presentation.widgets.TreeWidget import TreeWidget
from presentation.widgets.TabWidget import TabWidget
from presentation.Toolbar import ToolBar
from presentation.Translate import Translate as TR


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabWidget = None
        self.splitter = None
        self.grid_layout = None
        self.mapWidget = None

        self.tree = None

        self.init_ui()


    def closeEvent(self, event):

        quit_msg = TR().tr('Quit_text')
        reply = QtWidgets.QMessageBox.question(self, TR().tr('Sure_quit'),
                                               quit_msg,
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Save)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        elif reply == QtWidgets.QMessageBox.Save:
            response = self.menuWidget().save_slot()
            if response:
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()


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
        if self.tabWidget:
            self.tabWidget.tree_item_clicked(None)
        if self.mapWidget:
            self.mapWidget.tree_item_doubleclick_action(None)
        for i in range(self.centralWidget.layout().count()):
            if self.tabWidget:
                self.tabWidget.destroy()
            if self.mapWidget:
                self.mapWidget.destroy()

            self.centralWidget.layout().takeAt(i).widget().setHidden(True)
            bars = self.findChildren(QtWidgets.QToolBar, 'MapToolbar')
            for bar in bars:
                self.removeToolBar(bar)

        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setHandleWidth(15)

        self.tree = TreeWidget(self.splitter, object_type, self)
        # self.tree.show()

        if object_type is ObjectType.MAP:
            self.tabWidget = None
            self.mapWidget = MapWidget(self.splitter, self)
            self.mapWidget.setObjectName('mapWidget')
            self.tree.item_doubleclick_signal.connect(self.mapWidget.tree_item_doubleclick_action)
        else:
            self.mapWidget = None
            self.tabWidget = TabWidget(self.splitter, None, object_type, self)
            self.tabWidget.setObjectName("tabWidget")
            self.tree.item_doubleclick_signal.connect(self.tabWidget.tree_item_clicked)

        self.grid_layout.addWidget(self.splitter, 0, 0, 1, 1)

        self.splitter.setSizes([200, 600])

        self.show()


    def redraw_context_widget(self, object_type: ObjectType, item):
        if object_type is ObjectType.MAP:
            self.tabWidget.hide()
            bars = self.findChildren(QtWidgets.QToolBar, 'MapToolbar')
            for bar in bars:
                bar.show()

            if self.mapWidget:
                self.mapWidget.show()
                if item:
                    self.mapWidget.tree_item_doubleclick_action(item)
            else:
                self.mapWidget = MapWidget(self.splitter, self)
                self.mapWidget.setObjectName('mapWidget')
                self.tree.item_doubleclick_signal.connect(self.mapWidget.tree_item_doubleclick_action)
                if item:
                    self.mapWidget.tree_item_doubleclick_action(item)
        elif object_type is None:
            if self.mapWidget:
                self.mapWidget.hide()
            if self.tabWidget:
                self.tabWidget.hide()

        else:
            if self.mapWidget:
                self.mapWidget.hide()

            bars = self.findChildren(QtWidgets.QToolBar, 'MapToolbar')
            for bar in bars:
                bar.hide()

            if self.tabWidget:
                self.tabWidget.show()
                if item:
                    self.tabWidget.tree_item_clicked(item)
            else:
                self.tabWidget = TabWidget(self.splitter, None, object_type, self)
                self.tabWidget.setObjectName("tabWidget")
                self.tree.item_doubleclick_signal.connect(self.tabWidget.tree_item_clicked)
                if item:
                    self.tabWidget.tree_item_clicked(item)
