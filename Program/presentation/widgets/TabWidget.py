from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from business.managers.LangManager import LangManager
from presentation.dialogs.NewLangTab import NewLangTab
from presentation.layouts.SpellLayout import SpellLayout


class TabWidget(QtWidgets.QFrame):
    """
    Custom tab widget with function for editing templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.lang_manager = LangManager()

        self.init_ui()


    def init_ui(self):
        """
        Init basic UI for widget
        """
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.frame_layout = QtWidgets.QVBoxLayout(self)
        self.frame_layout.setObjectName("Frame layout")

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.frame_layout.addWidget(self.tab_widget)

        self.tab_bar = TabBar()
        self.tab_widget.setTabBar(self.tab_bar)

        self.tab_bar.clicked.connect(self.tab_clicked)
        self.tab_bar.right_clicked.connect(self.tab_right_clicked)

        self.new_tab = QtWidgets.QWidget()

        self.tab_widget.addTab(self.new_tab, '+')


    def tab_clicked(self, i):
        """
        Action when click on tab
        :param i: num of tab you click on
        """
        num_tabs = self.tab_bar.count()

        if num_tabs == i + 1:
            data, choice = NewLangTab.get_data()
            if choice:
                lang = self.lang_manager.get_lang(data['id'])
                new_tab = QtWidgets.QWidget()
                self.tab_widget.insertTab(i, new_tab, lang.name + ' (' + lang.code + ')')
                self.tab_widget.setCurrentIndex(i)
                new_tab.setLayout(SpellLayout(new_tab))


    def tab_right_clicked(self, i):
        print('right', i)


class TabBar(QtWidgets.QTabBar):
    """
    Custom tab bar for tab widget
    """
    clicked = QtCore.pyqtSignal(int)
    right_clicked = QtCore.pyqtSignal(int)


    def __init__(self):
        super().__init__()
        self.previousMiddleIndex = -1


    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() in (QtCore.Qt.LeftButton, QtCore.Qt.RightButton):
            self.previousIndex = self.tabAt(mouseEvent.pos())
        QtWidgets.QTabBar.mousePressEvent(self, mouseEvent)


    def mouseReleaseEvent(self, mouseEvent):
        if self.previousIndex == self.tabAt(mouseEvent.pos()):
            if mouseEvent.button() == QtCore.Qt.LeftButton:
                self.clicked.emit(self.previousIndex)
            elif mouseEvent.button() == QtCore.Qt.RightButton:
                self.right_clicked.emit(self.previousIndex)
        self.previousIndex = -1
        QtWidgets.QTabBar.mouseReleaseEvent(self, mouseEvent)
