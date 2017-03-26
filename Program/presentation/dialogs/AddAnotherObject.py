# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

from business.managers.PlayerTreeManager import PlayerTreeManager
from structure.enums.NodeType import NodeType
from presentation.Translate import Translate as TR
from structure.enums.ObjectType import ObjectType
from structure.tree.Folder import Folder
from structure.tree.Node import Node


class AddAnotherObject(QtWidgets.QDialog):
    """
    Dialog for import object of another type to tree
    """


    def __init__(self, node: Node, parent=None):
        super().__init__(parent)
        self.setWindowTitle(TR().tr('Add_object'))
        # self.setWindowIcon('resources/icons/char.png')
        self.treeManager = PlayerTreeManager()
        self.__selected = {}

        self.__node = node
        self.__parent = parent
        self.init_ui()


    def init_ui(self):
        """
        Init basic layout
        """
        self.layout = QtWidgets.QGridLayout(self)

        self.tabWidget = QtWidgets.QTabWidget(self.__parent)
        self.layout.addWidget(self.tabWidget, 0, 0)
        for child in self.__node.object.treeChildren:
            tab = QtWidgets.QWidget()
            self.__selected[child] = []
            self.tabWidget.addTab(tab, TR().tr(child))
            self.create_tree(tab, child)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.layout.addWidget(self.buttonBox, 2, 0, 1, 2, QtCore.Qt.AlignHCenter)

        self.setLayout(self.layout)


    def create_tree(self, tab, objectType: ObjectType):
        """
        Create tree on current tab
        :param tab: TabWidget tab
        :param objectType: type of object
        """
        layout = QtWidgets.QVBoxLayout(tab)
        treeWidget = QtWidgets.QTreeWidget(tab)
        layout.addWidget(treeWidget)
        treeWidget.header().close()
        treeWidget.itemClicked.connect(self.item_check_slot)

        searchBox = QtWidgets.QLineEdit(tab)
        layout.addWidget(searchBox)

        searchBox.textChanged.connect(
            lambda: self.search_box_change_slot(objectType, searchBox, treeWidget))
        items = self.treeManager.get_tree(objectType)
        self.set_items(items, treeWidget)


    def set_items(self, items: list, treeWidget: QtWidgets, parent=None):
        """
        Create item tree in widget
        :param treeWidget: Tree widget, where items will be crated
        :param items: object items
        :param parent: id of parent item (recursion)
        """
        if parent is None:
            parent = treeWidget
        for item in items:
            tree_item = QtWidgets.QTreeWidgetItem(parent)
            tree_item.setText(0, item.name)
            tree_item.setData(0, 5, QtCore.QVariant(item.id))

            if isinstance(item, Folder):
                folder_icon = QtGui.QIcon()
                folder_icon.addPixmap(QtGui.QPixmap("resources/icons/open.png"),
                                      QtGui.QIcon.Normal, QtGui.QIcon.Off)
                tree_item.setIcon(0, folder_icon)
                tree_item.setFlags(
                    tree_item.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                self.set_items(item.children, tree_item)
                tree_item.setData(0, 6, QtCore.QVariant(NodeType.FOLDER.value))
            else:
                icon = item.object.DAO()().get(item.object.id).icon
                object_icon = QtGui.QIcon(icon)
                tree_item.setIcon(0, object_icon)
                tree_item.setFlags(
                    tree_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                tree_item.setData(0, 6, QtCore.QVariant(NodeType.OBJECT.value))

            if item.id in self.__selected[self.selected_tab()]:
                tree_item.setCheckState(0, QtCore.Qt.Checked)
            else:
                tree_item.setCheckState(0, QtCore.Qt.Unchecked)


    def item_check_slot(self, item):
        """
        Slot for handling check items, because of searching, need store checked items in list
        :param item: current clicked item
        """
        if item.checkState(0) == QtCore.Qt.Unchecked:
            node = self.treeManager.get_node(item.data(0, 5))
            if isinstance(node, Folder):
                for i in range(item.childCount()):
                    self.item_check_slot(item.child(i))
            else:
                if item.data(0, 5) in self.__selected[self.selected_tab()]:
                    self.__selected[self.selected_tab()].remove(item.data(0, 5))
        else:
            node = self.treeManager.get_node(item.data(0, 5))
            if isinstance(node, Folder):
                for i in range(item.childCount()):
                    self.item_check_slot(item.child(i))
            else:
                if item.data(0, 5) not in self.__selected[self.selected_tab()]:
                    self.__selected[self.selected_tab()].append(item.data(0, 5))


    def search_box_change_slot(self, objectType: ObjectType, searchBox: QtWidgets,
                               treeWidget: QtWidgets):
        """
        Slot, that redraw tree widget base on search box
        :param objectType: type of object
        :param searchBox: search box widget
        :param treeWidget: tree Widget
        """
        treeWidget.clear()

        text = searchBox.text()
        items = self.treeManager.search_tree_nodes(objectType, text)
        self.set_items(items, treeWidget)


    def selected_tab(self) -> ObjectType:
        """
        Find currently selected tab and return ObjectType of that tab
        :return: Object type of tab
        """
        return self.__node.object.treeChildren[self.tabWidget.currentIndex()]


    def get_inputs(self) -> dict:
        """
        Get inputs from dialog
        :return: dictionary of data (name,value)
        """
        return self.__selected


    @staticmethod
    def get_data(node: Node, parent=None) -> tuple:
        dialog = AddAnotherObject(node, parent)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return data, result == QtWidgets.QDialog.Accepted
