# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.ItemManager import ItemManager
from presentation.layouts.Layout import Layout
from structure.items.RangeWeapon import RangeWeapon


class RangeWeaponLayout(Layout):
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
        self.setObjectName('Range weapon layout')

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
        self.weight_input = self.spin_box(self.input_grid, 'Weight', 0, 2, True)
        self.price_input = self.spin_box(self.input_grid, 'Price', 0, 3, True)
        self.initiative_input = self.spin_box(self.input_grid, 'Initiative', 0, 4, True)
        self.strength_input = self.spin_box(self.input_grid, 'Strength', 0, 5, True)
        self.rampancy_input = self.spin_box(self.input_grid, 'Rampancy', 0, 6, True)
        self.rangeLow_input = self.spin_box(self.input_grid, 'RangeLow', 0, 7, True)
        self.rangeMedium_input = self.spin_box(self.input_grid, 'RangeMedium', 0, 8, True)
        self.rangeHigh_input = self.spin_box(self.input_grid, 'RangeHigh', 0, 9, True)

        self.addLayout(self.input_grid)


    def map_data(self, item: RangeWeapon):
        """
        Mapa data from object to inputs in layout
        :param item: Item object
        """
        self.object = item
        self.header.setText(item.name)
        self.name_input.setPlainText(item.name)
        self.description_input.setPlainText(item.description)
        self.weight_input.setValue(item.weight)
        self.price_input.setValue(item.price)
        self.initiative_input.setValue(item.initiative)
        self.strength_input.setValue(item.strength)
        self.rampancy_input.setValue(item.rampancy)
        self.rangeLow_input.setValue(item.rangeLow)
        self.rangeMedium_input.setValue(item.rangeMedium)
        self.rangeHigh_input.setValue(item.rangeHigh)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()
        self.object.weight = self.weight_input.value()
        self.object.price = self.price_input.value()
        self.object.initiative = self.initiative_input.value()
        self.object.strength = self.strength_input.value()
        self.object.rampancy = self.rampancy_input.value()
        self.object.rangeLow = self.rangeLow_input.value()
        self.object.rangeMedium = self.rangeMedium_input.value()
        self.object.rangeHigh = self.rangeHigh_input.value()

        self.item_manager.update(self.object)