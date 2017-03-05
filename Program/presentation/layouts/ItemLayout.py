# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.AbilityManager import AbilityManager
from presentation.Translate import Translate as TR
from structure.abilities.Ability import Ability
from structure.enums.Races import Races
from structure.items.Item import Item
from structure.spells.Spell import Spell
from business.managers.SpellManager import SpellManager
from structure.enums.Classes import Classes
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

        # Name
        name_label = QtWidgets.QLabel()
        name_label.setText(TR().tr('Name') + ':')
        self.input_grid.addWidget(name_label, 0, 0, 1, 1)
        self.name_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.name_input, 0, 1, 1, 1)
        self.name_input.textChanged.connect(self.data_changed)

        # Description
        self.description_label = QtWidgets.QLabel()
        self.description_label.setText(TR().tr('Description') + ':')
        self.input_grid.addWidget(self.description_label, 1, 0, 1, 1)
        self.description_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.description_input, 1, 1, 1, 1)
        self.description_input.textChanged.connect(self.data_changed)

        # Weight
        self.weight_label = QtWidgets.QLabel()
        self.weight_label.setText(TR().tr('Weight') + ':')
        self.input_grid.addWidget(self.weight_label, 2, 0, 1, 1)
        self.weight_input = QtWidgets.QSpinBox()
        self.synchronize(self.weight_input)
        self.input_grid.addWidget(self.weight_input, 2, 1, 1, 1)
        self.weight_input.valueChanged.connect(self.data_changed)

        # Price
        self.price_label = QtWidgets.QLabel()
        self.price_label.setText(TR().tr('Cast_time') + ':')
        self.input_grid.addWidget(self.price_label, 3, 0, 1, 1)
        self.price_input = QtWidgets.QSpinBox()
        self.synchronize(self.price_input)
        self.input_grid.addWidget(self.price_input, 3, 1, 1, 1)
        self.price_input.valueChanged.connect(self.data_changed)

        self.addLayout(self.input_grid)


    def map_data(self, item: Item):
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


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()
        self.object.weight = self.weight_input.value()
        self.object.price = self.price_input.value()

        self.ability_manager.update_ability(self.object)
