# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.ItemManager import ItemManager
from presentation.layouts.Layout import Layout
from structure.items.Money import Money


class MoneyLayout(Layout):
    """
    Layout for editing spell templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.item_manager = ItemManager()
        self.object = None


    def init_ui(self):
        """
        Init basic UI
        """
        self.setObjectName('Money layout')

        self.header = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(15)
        self.header.setFont(font)
        self.header.setAlignment(QtCore.Qt.AlignCenter)

        self.addWidget(self.header)

        self.input_grid = QtWidgets.QGridLayout()
        self.input_grid.setSpacing(20)
        self.input_grid.setObjectName("Input grid")

        self.name_input = self.text_box(self.input_grid, 'Name', 0, 0)
        self.description_input = self.text_box(self.input_grid, 'Description', 0, 1)
        self.copper_input = self.spin_box(self.input_grid, 'Copper', 0, 2, True)
        self.silver_input = self.spin_box(self.input_grid, 'Silver', 0, 3, True)
        self.gold_input = self.spin_box(self.input_grid, 'Gold', 0, 4, True)
        self.amount_input = self.spin_box(self.input_grid, 'Amount', 0, 5, True)

        self.addLayout(self.input_grid)


    def map_data(self, item: Money, treeNode=None):
        """
        Mapa data from object to inputs in layout
        :param item: Item object
        """
        self.object = item
        self.header.setText(item.name)
        self.name_input.setPlainText(item.name)
        self.description_input.setPlainText(item.description)
        self.copper_input.setValue(item.copper if item.copper else 0)
        self.silver_input.setValue(item.silver if item.silver else 0)
        self.gold_input.setValue(item.gold if item.gold else 0)
        self.amount_input.setValue(item.amount)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()

        self.object.copper = self.copper_input.value()
        self.object.silver = self.silver_input.value()
        self.object.gold = self.gold_input.value()
        self.object.amount = self.amount_input.value()

        self.item_manager.update(self.object)
