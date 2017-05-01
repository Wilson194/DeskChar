# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.ItemManager import ItemManager
from structure.enums.Handling import Handling
from structure.enums.Races import Races
from structure.enums.WeaponWeight import WeaponWeight
from presentation.layouts.Layout import Layout
from structure.items.MeleeWeapon import MeleeWeapon
from structure.tree.NodeObject import NodeObject


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
        self.initiative_input = self.spin_box(self.input_grid, 'Initiative', 0, 8, True)
        self.weapon_weight_input = self.combo_box(self.input_grid, 'WeaponWeight', WeaponWeight, 0, 9, True, haveNone=False)
        self.handling_input = self.combo_box(self.input_grid, 'Handling', Handling, 0, 10, True, haveNone=False)
        self.racial_input = self.combo_box(self.input_grid, 'Racial', Races, 0, 11, True)
        self.amount_input = self.spin_box(self.input_grid, 'Amount', 0, 12, True)

        self.addLayout(self.input_grid)


    def map_data(self, item: MeleeWeapon, treeNode: NodeObject = None) -> None:
        """
        Mapa data from object to inputs in layout
        :param item: MeleeWeapon object
        :param treeNode: node in tree widget, if its need to get whole object
        """
        self.object = item
        self.header.setText(item.name)
        self.name_input.setPlainText(item.name)
        self.description_input.setPlainText(item.description)
        self.weight_input.setValue(item.weight if item.weight else 0)
        self.price_input.setValue(item.price if item.price else 0)
        self.strength_input.setValue(item.strength if item.strength else 0)
        self.rampancy_input.setValue(item.rampancy if item.rampancy else 0)
        self.defence_input.setValue(item.defence if item.length else 0)
        self.length_input.setValue(item.length if item.length else 0)
        self.amount_input.setValue(item.amount)
        self.initiative_input.setValue(item.initiative if item.initiative else 0)

        handling_index = item.handling.value if item.handling is not None else 1
        weapon_weight_index = item.weaponWeight.value if item.weaponWeight is not None else 1
        racial_index = item.racial.value if item.racial is not None else 0

        self.handling_input.setCurrentIndex(handling_index - 1)
        self.weapon_weight_input.setCurrentIndex(weapon_weight_index - 1)
        self.racial_input.setCurrentIndex(racial_index)


    def save_data(self) -> None:
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
        self.object.amount = self.amount_input.value()
        self.object.initiative = self.initiative_input.value()

        handling_index = self.handling_input.currentIndex()
        weapon_weight_index = self.weapon_weight_input.currentIndex()
        racial_index = self.racial_input.currentIndex()

        self.object.handling = Handling(handling_index + 1)
        self.object.weaponWeight = WeaponWeight(weapon_weight_index + 1)
        self.object.racial = Races(racial_index) if racial_index > 0 else None

        self.item_manager.update(self.object)
