# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.ItemManager import ItemManager
from structure.enums.Handling import Handling
from structure.enums.WeaponWeight import WeaponWeight
from presentation.layouts.Layout import Layout
from structure.items.MeleeWeapon import MeleeWeapon


class MeleeWeaponLayout(Layout):
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
        self.setObjectName('Melee weapon layout')

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
        self.strength_input = self.spin_box(self.input_grid, 'Strength', 0, 4, True)
        self.rampancy_input = self.spin_box(self.input_grid, 'Rampancy', 0, 5, True)
        self.defence_input = self.spin_box(self.input_grid, 'Defence', 0, 6, True)
        self.length_input = self.spin_box(self.input_grid, 'Length', 0, 7, True)
        self.weapon_weight_input = self.combo_box(self.input_grid, 'WeaponWeight', WeaponWeight, 0,
                                                  8, True)
        self.handling_input = self.combo_box(self.input_grid, 'Handling', Handling, 0,
                                             9, True)

        self.addLayout(self.input_grid)


    def map_data(self, item: MeleeWeapon):
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
        self.strength_input.setValue(item.strength)
        self.rampancy_input.setValue(item.rampancy)
        self.defence_input.setValue(item.defence)
        self.length_input.setValue(item.length)

        handling_index = item.handling.value if item.handling is not None else 0
        weapon_weight_index = item.weaponWeight.value if item.weaponWeight is not None else 0

        self.handling_input.setCurrentIndex(handling_index)
        self.weapon_weight_input.setCurrentIndex(weapon_weight_index)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()
        self.object.weight = self.weight_input.value()
        self.object.price = self.price_input.value()
        self.object.strength = self.strength_input.value()
        self.object.rampancy = self.rampancy_input.value()
        self.object.defence = self.defence_input.value()
        self.object.length = self.length_input.value()

        handling_index = self.handling_input.currentIndex()
        weapon_weight_index = self.weapon_weight_input.currentIndex()

        self.object.handling = Handling(handling_index) if handling_index > 0 else None
        self.object.weaponWeight = WeaponWeight(
            weapon_weight_index) if weapon_weight_index > 0 else None

        self.item_manager.update(self.object)