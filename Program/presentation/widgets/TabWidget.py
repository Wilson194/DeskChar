from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from business.managers.LangManager import LangManager
from presentation.dialogs.NewLangTab import NewLangTab


class TabWidget(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.lang_manager = LangManager()

        self.init_ui()


    def init_ui(self):
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.frame_layout = QtWidgets.QVBoxLayout(self)
        self.frame_layout.setObjectName("Frame layout")

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.frame_layout.addWidget(self.tab_widget)

        self.tab_bar = TabBar()
        self.tab_widget.setTabBar(self.tab_bar)

        self.tab_bar.clicked.connect(self.tab_clicked)

        self.new_tab = QtWidgets.QWidget()

        self.tab_widget.addTab(self.new_tab, '+')


    def tab_clicked(self, i):
        num_tabs = self.tab_bar.count()

        if num_tabs == i + 1:
            data, choice = NewLangTab.get_data()
            lang = self.lang_manager.get_lang(data['type'])
            new_tab = QtWidgets.QWidget()
            self.tab_widget.insertTab(i, new_tab, lang.name + ' (' + lang.code + ')')
            self.tab_widget.setCurrentIndex(i)


class TabBar(QtWidgets.QTabBar):
    clicked = QtCore.pyqtSignal(int)


    def __init__(self):
        super().__init__()
        self.previousMiddleIndex = -1


    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == QtCore.Qt.LeftButton:
            self.previousIndex = self.tabAt(mouseEvent.pos())
        QtWidgets.QTabBar.mousePressEvent(self, mouseEvent)


    def mouseReleaseEvent(self, mouseEvent):
        if mouseEvent.button() == QtCore.Qt.LeftButton and \
                        self.previousIndex == self.tabAt(mouseEvent.pos()):
            self.clicked.emit(self.previousIndex)
        self.previousIndex = -1
        QtWidgets.QTabBar.mouseReleaseEvent(self, mouseEvent)
