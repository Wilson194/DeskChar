from PyQt5 import QtCore
from PyQt5 import QtWidgets


class TreeWidget(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()


    def init_ui(self):


        grid = QtWidgets.QGridLayout(self)

        tree = QtWidgets.QTreeWidget()

        grid.addWidget(tree)



        # def set_items(self, items: list):
        #     for item in items:
        #         tree_item = QtWidgets.QTreeWidgetItem(self)
        #         tree_item.setText(0, item.name)
