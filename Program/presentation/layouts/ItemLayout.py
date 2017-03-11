# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.AbilityManager import AbilityManager
from presentation.Translate import Translate as TR
from structure.items.Item import Item
from presentation.layouts.Layout import Layout


class ItemLayout(Layout):
    """
    Layout for editing spell templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.item_manager = AbilityManager()
        self.object = None


    def init_ui(self):
        """
        Init basic UI
        """
        self.setObjectName('Spell layout')

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
        self.name_input = self.text_box(self.input_grid, 'Description', 0, 1)
        self.weight_input = self.spin_box(self.input_grid, 'Weight', 0, 2, True)
        self.price_input = self.spin_box(self.input_grid, 'Weight', 0, 3, True)

        self.addLayout(self.input_grid)


    def map_data(self, item: Item):
        """
        Mapa data from object to inputs in layout
        :param item: Item object
        """
        # self.object = item
        # self.header.setText(item.name)
        # self.name_input.setPlainText(item.name)
        # self.description_input.setPlainText(item.description)
        # self.weight_input.setValue(item.weight)
        # self.price_input.setValue(item.price)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        # self.object.name = self.name_input.toPlainText()
        # self.object.description = self.description_input.toPlainText()
        # self.object.weight = self.weight_input.value()
        # self.object.price = self.price_input.value()
        #
        # self.ability_manager.update(self.object)
