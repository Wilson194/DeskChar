# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.AbilityManager import AbilityManager
from structure.abilities.Ability import Ability
from structure.enums.Races import Races
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

        self.name_input = self.text_box(self.input_grid, 'Name', 0, 0)
        self.class_input = self.combo_box(self.input_grid, 'Class', Classes, 0, 1, True)
        self.race_input = self.combo_box(self.input_grid, 'Race', Races, 0, 2, True)
        self.description_input = self.text_box(self.input_grid, 'Description', 0, 3)
        self.chance_input = self.text_box(self.input_grid, 'Chance', 0, 4)

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
        class_index = ability.drd_class if ability.drd_class is not None else 0
        race_index = ability.drd_race if ability.drd_race is not None else 0

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
        self.object.drd_class = class_index if class_index > 0 else None
        self.object.drd_race = race_index if race_index > 0 else None

        self.ability_manager.update_ability(self.object)
