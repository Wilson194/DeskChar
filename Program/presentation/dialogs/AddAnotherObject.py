# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

from business.managers.PlayerTreeManager import PlayerTreeManager
from structure.enums.NodeType import NodeType
from presentation.Translate import Translate as TR
from structure.tree.Folder import Folder
from structure.tree.Node import Node


class AddAnotherObject(QtWidgets.QDialog):
    """
    Dialog for creating new item in tree widget
    """


    def __init__(self, node: Node, parent=None):
        super().__init__(parent)
        self.setWindowTitle(TR().tr('Add_object'))
        self.treeManager = PlayerTreeManager()

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


    def create_tree(self, tab, objectType):
        treeWdiget = QtWidgets.QTreeWidget(tab)

        items = self.treeManager.get_tree(objectType)
        self.set_items(items, treeWdiget)


    def set_items(self, items: list, treeWidget: QtWidgets, parent=None):
        """
        Create item tree in widget
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
                icon = self.__data_type.instance().DAO()().get(item.object.id).icon
                object_icon = QtGui.QIcon(icon)
                tree_item.setIcon(0, object_icon)
                tree_item.setFlags(
                    tree_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                tree_item.setData(0, 6, QtCore.QVariant(NodeType.OBJECT.value))

            # if self.checking:
            #     tree_item.setCheckState(0, QtCore.Qt.Unchecked)


    def get_inputs(self) -> dict:
        """
        Get inputs from dialog
        :return: dictionary of data (name,value)
        """
        data = {}
        return data


    @staticmethod
    def get_data(node: Node, parent=None) -> tuple:
        dialog = AddAnotherObject(node, parent)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return data, result == QtWidgets.QDialog.Accepted
