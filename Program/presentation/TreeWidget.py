from PyQt5 import QtCore
from PyQt5 import QtWidgets


class TreeWidget:
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.init_ui()


    def init_ui(self):
        tree_widget = QtWidgets.QTreeWidget(self.parent_widget)
        tree_widget.headerItem().setText(0, 'test')
        tree_widget.headerItem().setTextAligment(0, QtCore.Qt.AlignHCenter)
