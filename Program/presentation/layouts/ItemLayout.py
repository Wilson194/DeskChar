# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.AbilityManager import AbilityManager
from presentation.Translate import Translate as TR
from structure.abilities.Ability import Ability
from structure.enums.Races import Races
from structure.spells.Spell import Spell
from business.managers.SpellManager import SpellManager
from structure.enums.Classes import Classes
from presentation.layouts.Layout import Layout


class AbilityLayout(Layout):
    """
    Layout for editing spell templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.ability_manager = AbilityManager()
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

        # Class
        class_label = QtWidgets.QLabel(TR().tr('Class') + ':')
        self.input_grid.addWidget(class_label, 1, 0)
        self.class_input = QtWidgets.QComboBox()
        self.class_input.setObjectName("Class_input")
        self.class_input.currentIndexChanged.connect(self.data_changed)
        self.synchronize(self.class_input)
        self.input_grid.addWidget(self.class_input, 1, 1)
        self.class_input.addItem(TR().tr('Select_value'))
        for drd_class in Classes:
            data = {'value': drd_class}
            self.class_input.addItem(TR().tr(str(drd_class)), QtCore.QVariant(data))

        # Race
        race_label = QtWidgets.QLabel(TR().tr('Race') + ':')
        self.input_grid.addWidget(race_label, 2, 0)
        self.race_input = QtWidgets.QComboBox()
        self.race_input.setObjectName("Race_input")
        self.race_input.currentIndexChanged.connect(self.data_changed)
        self.synchronize(self.race_input)
        self.input_grid.addWidget(self.race_input, 2, 1)
        self.race_input.addItem(TR().tr('Select_value'))
        for drd_race in Races:
            data = {'value': drd_race}
            self.race_input.addItem(TR().tr(str(drd_race)), QtCore.QVariant(data))

        # Description
        self.description_label = QtWidgets.QLabel()
        self.description_label.setText(TR().tr('Description') + ':')
        self.input_grid.addWidget(self.description_label, 3, 0, 1, 1)
        self.description_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.description_input, 3, 1, 1, 1)
        self.description_input.textChanged.connect(self.data_changed)

        # Chance
        self.chance_label = QtWidgets.QLabel()
        self.chance_label.setText(TR().tr('Chance') + ':')
        self.input_grid.addWidget(self.chance_label, 4, 0, 1, 1)
        self.chance_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.chance_input, 4, 1, 1, 1)
        self.chance_input.textChanged.connect(self.data_changed)

        self.addLayout(self.input_grid)


    def map_data(self, ability: Ability):
        """
        Mapa data from object to inputs in layout
        :param ability: Ability object
        """
        self.object = ability
        self.header.setText(ability.name)
        self.name_input.setPlainText(ability.name)
        self.description_input.setPlainText(ability.description)
        self.chance_input.setPlainText(ability.chance)
        class_index = ability.drd_class - 2 if ability.drd_class is not None else 0
        race_index = ability.drd_race - 2 if ability.drd_race is not None else 0

        self.class_input.setCurrentIndex(class_index)
        self.race_input.setCurrentIndex(race_index)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()
        self.object.chance = self.chance_input.toPlainText()
        class_index = self.class_input.currentIndex()
        race_index = self.race_input.currentIndex()
        self.object.drd_class = class_index + 2 if class_index > 0 else None
        self.object.drd_race = race_index + 2 if race_index > 0 else None

        self.ability_manager.update_ability(self.object)
