# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.CharacterManager import CharacterManager
from business.managers.SpellManager import SpellManager
from structure.character.Character import Character
from structure.enums.Classes import Classes
from presentation.layouts.Layout import Layout
from structure.spells.Spell import Spell


class CharacterLayout(Layout):
    """
    Layout for editing character templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.manager = CharacterManager()
        self.object = None


    def init_ui(self):
        """
        Init basic UI
        """
        self.setObjectName('Character layout')

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

        self.agility_input = self.spin_box(self.input_grid, 'Agility', 0, 2, True)
        self.charisma_input = self.spin_box(self.input_grid, 'Charisma', 0, 3, True)
        self.intelligence_input = self.spin_box(self.input_grid, 'Intelligence', 0, 4, True)
        self.mobility_input = self.spin_box(self.input_grid, 'Mobility', 0, 5, True)
        self.strength_input = self.spin_box(self.input_grid, 'Strength', 0, 6, True)
        self.toughness_input = self.spin_box(self.input_grid, 'Toughness', 0, 7, True)

        self.age_input = self.spin_box(self.input_grid, 'Age', 0, 8, True)
        self.height_input = self.spin_box(self.input_grid, 'Height', 0, 9, True)
        self.weight_input = self.spin_box(self.input_grid, 'Weight', 0, 10, True)
        self.level_input = self.spin_box(self.input_grid, 'Level', 0, 11, True)
        self.xp_input = self.spin_box(self.input_grid, 'Xp', 0, 12, True)
        self.maxHealth_input = self.spin_box(self.input_grid, 'MaxHealth', 0, 13, True)
        self.maxMana_input = self.spin_box(self.input_grid, 'MaxMana', 0, 14, True)

        # self.class_input = self.combo_box(self.input_grid, 'Class', Classes, 0, 1, True)


        self.addLayout(self.input_grid)


    def map_data(self, character: Character):
        """
        Mapa data from object to inputs in layout
        :param character: character object
        """
        self.object = character
        self.name_input.setPlainText(self.object.name)
        self.description_input.setPlainText(self.object.description)

        self.agility_input.setValue(self.object.agility)
        self.charisma_input.setValue(self.object.charisma)
        self.intelligence_input.setValue(self.object.intelligence)
        self.mobility_input.setValue(self.object.mobility)
        self.strength_input.setValue(self.object.strength)
        self.toughness_input.setValue(self.object.toughness)

        self.age_input.setValue(self.object.age)
        self.height_input.setValue(self.object.height)
        self.weight_input.setValue(self.object.weight)
        self.level_input.setValue(self.object.level)
        self.xp_input.setValue(self.object.xp)
        self.maxHealth_input.setValue(self.object.maxHealth)
        self.maxMana_input.setValue(self.object.maxMana)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()

        self.object.agility = self.agility_input.value()
        self.object.charisma = self.charisma_input.value()
        self.object.intelligence = self.intelligence_input.value()
        self.object.mobility = self.mobility_input.value()
        self.object.strength = self.strength_input.value()
        self.object.toughness = self.toughness_input.value()

        self.object.age = self.age_input.value()
        self.object.height = self.height_input.value()
        self.object.weight = self.weight_input.value()
        self.object.level = self.level_input.value()
        self.object.xp = self.xp_input.value()
        self.object.maxHealth = self.maxHealth_input.value()
        self.object.maxMana = self.maxMana_input.value()

        self.manager.update_character(self.object)