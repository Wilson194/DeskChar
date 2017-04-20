# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.ItemManager import ItemManager
from structure.items.Armor import Armor
from structure.items.Item import Item
from presentation.layouts.Layout import Layout


class ArmorLayout(Layout):
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
        self.setObjectName('Armor layout')

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
        self.price_input = self.spin_box(self.input_grid, 'Price', 0, 2, True)
        self.quality_input = self.spin_box(self.input_grid, 'Quality', 0, 3, True)
        self.weightA_input = self.spin_box(self.input_grid, 'WeightA', 0, 4, True)
        self.weightB_input = self.spin_box(self.input_grid, 'WeightB', 0, 5, True)
        self.weightC_input = self.spin_box(self.input_grid, 'WeightC', 0, 6, True)
        self.size_input = self.spin_box(self.input_grid, 'Size', 0, 7, True)
        self.amount_input = self.spin_box(self.input_grid, 'Amount', 0, 8, True)

        self.addLayout(self.input_grid)


    def map_data(self, item: Armor):
        """
        Mapa data from object to inputs in layout
        :param item: Item object
        """
        self.object = item

        self.header.setText(item.name)
        self.name_input.setPlainText(item.name)
        self.description_input.setPlainText(item.description)
        self.price_input.setValue(item.price if item.price else 0)
        self.quality_input.setValue(item.quality if item.quality else 0)
        self.weightA_input.setValue(item.weightA if item.weightA else 0)
        self.weightB_input.setValue(item.weightB if item.weightB else 0)
        self.weightC_input.setValue(item.weightC if item.weightC else 0)
        self.size_input.setValue(item.size if item.size else 0)
        self.amount_input.setValue(item.amount if item.amount else 1)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()
        self.object.price = self.price_input.value()
        self.object.quality = self.quality_input.value()
        self.object.weightA = self.weightB_input.value()
        self.object.weightB = self.weightB_input.value()
        self.object.weightC = self.weightC_input.value()
        self.object.size = self.size_input.value()
        self.object.amount = self.amount_input.value()

        self.item_manager.update(self.object)
