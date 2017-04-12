from PyQt5 import QtCore
from PyQt5 import QtWidgets
from business.managers.LangManager import LangManager
from business.managers.PlayerTreeManager import PlayerTreeManager
from presentation.dialogs.NewLangTab import NewLangTab
from business.managers.TabWidgetManager import TabWidgetManager
from presentation.layouts.Layout import Layout
from structure.enums.ObjectType import ObjectType
from presentation.Synchronizer import Synchronizer as Sync


class TabWidget(QtWidgets.QFrame):
    """
    Custom tab widget with function for editing templates
    """


    def __init__(self, parent, target_id: int, target_type: ObjectType):
        super().__init__(parent)

        self.layouts_changed = []

        self.lang_manager = LangManager()
        self.tab_manager = TabWidgetManager()

        self.target_id = target_id
        self.target_type = target_type

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

        self.init_data()

        self.new_tab = QtWidgets.QWidget()


    def init_data(self):
        """
        Init data, create language tabs
        """
        if self.target_id:
            data = self.tab_manager.get_data(self.target_id, self.target_type)
            for one in data:
                tab = QtWidgets.QWidget()
                lang = self.lang_manager.get_lang_by_code(one.lang)
                tab_text = lang.name + ' (' + lang.code + ')'
                layout = one.layout()(tab)
                layout.map_data(one)
                tab.setLayout(layout)
                self.tab_widget.insertTab(self.tab_bar.count(), tab, tab_text)
                layout.data_changed_signal.connect(self.data_changed_slot)

            self.new_tab = QtWidgets.QWidget()

            self.tab_widget.insertTab(self.tab_bar.count(), self.new_tab, '+')


    def change_object(self, target_id: int, target_type: ObjectType):
        """
        change object that mapped on tabs
        :param target_id: id of object
        :param target_type: type object
        """
        self.tab_widget.clear()
        self.target_id = target_id
        self.target_type = target_type
        self.init_data()


    def tree_item_clicked(self, item):
        """
        Function for mapping tree item click
        :param item: tree item in tree widget, has data
        """

        for layout in self.layouts_changed:
            layout.save_data()
        self.layouts_changed.clear()
        Sync().delete_data('Input_synchronize')
        item = item.data(0, 11)
        self.change_object(item.id, ObjectType(item.object_type))


    def data_changed_slot(self, layout: Layout):
        """
        Function slot for add layout changes
        :param layout: changed layout
        """
        if layout not in self.layouts_changed:
            self.layouts_changed.append(layout)


    def tab_clicked(self, i: int):
        """
        Action when click on tab
        :param i: num of tab you click on
        """
        num_tabs = self.tab_bar.count()

        if num_tabs == i + 1:
            data, choice = NewLangTab.get_data()
            if choice:
                lang = self.lang_manager.get_lang(data['id'])
                for tab_index in range(num_tabs - 1):
                    tab = self.tab_widget.widget(tab_index)
                    exist_lang = tab.layout().object.lang
                    if lang.code == exist_lang:
                        return
                new_tab = QtWidgets.QWidget()
                self.tab_widget.insertTab(i, new_tab, lang.name + ' (' + lang.code + ')')
                self.tab_widget.setCurrentIndex(i)
                # obj = self.tab_manager.get_empty_object(self.target_type, self.target_id, lang.code)
                # id = self.target_type.instance()().DAO()().create(
                #     self.target_type.instance()(None, lang.code))
                obj = self.target_type.instance()().DAO()().get(self.target_id, lang.code)

                new_tab.setLayout(obj.layout()(new_tab))
                new_tab.layout().object = obj
                new_tab.layout().data_changed_signal.connect(self.data_changed_slot)
        else:
            pass


    def tab_right_clicked(self, i: int):
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
