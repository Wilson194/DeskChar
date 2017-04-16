# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.CharacterManager import CharacterManager
from business.managers.SpellManager import SpellManager
from structure.character.Character import Character
from structure.enums.Alignment import Alignment
from structure.enums.Classes import Classes
from presentation.layouts.Layout import Layout
from structure.enums.Races import Races
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

        self.name_input = self.text_box(self.input_grid, 'Name', 0, 0, False, 3, 1)
        self.description_input = self.text_box(self.input_grid, 'Description', 0, 1, False, 3, 1)

        self.class_input = self.combo_box(self.input_grid, 'Class', Classes, 0, 2, True, 3, 1)
        self.race_input = self.combo_box(self.input_grid, 'Race', Races, 0, 3, True, 3, 1)
        self.alignment_input = self.combo_box(self.input_grid, 'Alignment', Alignment, 0, 4, True,
                                              3, 1)

        self.agility_input = self.spin_box(self.input_grid, 'Agility', 0, 5, True, 3, 1)
        self.charisma_input = self.spin_box(self.input_grid, 'Charisma', 0, 6, True, 3, 1)
        self.intelligence_input = self.spin_box(self.input_grid, 'Intelligence', 0, 7, True, 3, 1)
        self.mobility_input = self.spin_box(self.input_grid, 'Mobility', 0, 8, True, 3, 1)
        self.strength_input = self.spin_box(self.input_grid, 'Strength', 0, 9, True, 3, 1)
        self.toughness_input = self.spin_box(self.input_grid, 'Toughness', 0, 10, True, 3, 1)

        self.age_input = self.spin_box(self.input_grid, 'Age', 0, 11, True, 3, 1)
        self.height_input = self.spin_box(self.input_grid, 'Height', 0, 12, True, 3, 1)
        self.weight_input = self.spin_box(self.input_grid, 'Weight', 0, 13, True, 3, 1)
        self.level_input = self.spin_box(self.input_grid, 'Level', 0, 14, True, 3, 1)
        self.xp_input = self.spin_box(self.input_grid, 'Xp', 0, 15, True, 3, 1)
        self.maxHealth_input = self.spin_box(self.input_grid, 'MaxHealth', 0, 16, True)
        self.maxMana_input = self.spin_box(self.input_grid, 'MaxMana', 0, 17, True)

        self.currentHealth_input = self.spin_box(self.input_grid, 'CurrentHealth', 2, 16, True)
        self.currentMana_input = self.spin_box(self.input_grid, 'CurrentMana', 2, 17, True)

        self.addLayout(self.input_grid)


    def map_data(self, character: Character):
        """
        Mapa data from object to inputs in layout
        :param character: character object
        """
        self.object = character
        self.name_input.setPlainText(self.object.name)
        self.description_input.setPlainText(self.object.description)

        self.agility_input.setValue(self.object.agility if self.object.agility else 0)
        self.charisma_input.setValue(self.object.charisma if self.object.charisma else 0)
        self.intelligence_input.setValue(
            self.object.intelligence if self.object.intelligence else 0)
        self.mobility_input.setValue(self.object.mobility if self.object.mobility else 0)
        self.strength_input.setValue(self.object.strength if self.object.strength else 0)
        self.toughness_input.setValue(self.object.toughness if self.object.toughness else 0)

        self.age_input.setValue(self.object.age if self.object.age else 0)
        self.height_input.setValue(self.object.height if self.object.height else 0)
        self.weight_input.setValue(self.object.weight if self.object.weight else 0)
        self.level_input.setValue(self.object.level if self.object.level else 0)
        self.xp_input.setValue(self.object.xp if self.object.xp else 0)
        self.maxHealth_input.setValue(self.object.maxHealth if self.object.maxHealth else 0)
        self.maxMana_input.setValue(self.object.maxMana if self.object.maxMana else 0)
        self.currentHealth_input.setValue(
            self.object.currentHealth if self.object.currentHealth else 0)
        self.currentMana_input.setValue(self.object.currentMana if self.object.currentMana else 0)

        raceIndex = self.object.drdRace.value if self.object.drdRace is not None else 0
        classIndex = self.object.drdClass.value if self.object.drdClass is not None else 0
        alignmentIndex = self.object.alignment.value if self.object.alignment is not None else 0

        self.race_input.setCurrentIndex(raceIndex)
        self.class_input.setCurrentIndex(classIndex)
        self.alignment_input.setCurrentIndex(alignmentIndex)


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
        self.object.currentHealth = self.currentHealth_input.value()
        self.object.currentMana = self.currentMana_input.value()

        alIndex = self.alignment_input.currentIndex()
        clIndex = self.class_input.currentIndex()
        rcIndex = self.race_input.currentIndex()

        self.object.alignment = Alignment(alIndex) if alIndex != 0 else None
        self.object.drdClass = Classes(clIndex) if clIndex != 0 else None
        self.object.drdRace = Races(rcIndex) if rcIndex != 0 else None

        self.manager.update_character(self.object)
