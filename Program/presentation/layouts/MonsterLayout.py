# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.CharacterManager import CharacterManager
from business.managers.MonsterManager import MonsterManager
from business.managers.SpellManager import SpellManager
from structure.character.Character import Character
from structure.enums.Alignment import Alignment
from structure.enums.Classes import Classes
from presentation.layouts.Layout import Layout
from structure.enums.MonsterRace import MonsterRace
from structure.enums.MonsterSize import MonsterSize
from structure.monster.Monster import Monster
from structure.spells.Spell import Spell


class MonsterLayout(Layout):
    """
    Layout for editing character templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.manager = MonsterManager()
        self.object = None


    def init_ui(self):
        """
        Init basic UI
        """
        self.setObjectName('Monster layout')

        self.header = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(15)
        self.header.setFont(font)
        self.header.setAlignment(QtCore.Qt.AlignCenter)

        self.addWidget(self.header)

        self.input_grid = QtWidgets.QGridLayout()
        self.input_grid.setSpacing(20)
        self.input_grid.setObjectName("Input grid")

        self.nameInput = self.text_box(self.input_grid, 'Name', 0, 0)
        self.descriptionInput = self.text_box(self.input_grid, 'Description', 0, 1)

        self.viabilityInput = self.spin_box(self.input_grid, 'Viability', 0, 2, True)
        self.offenseInput = self.text_box(self.input_grid, 'Offense', 0, 3)
        self.defseInput = self.spin_box(self.input_grid, 'Defense', 0, 4, True)
        self.enduranceInput = self.spin_box(self.input_grid, 'Endurance', 0, 5, True)
        self.rampancyInput = self.spin_box(self.input_grid, 'Rampancy', 0, 6, True)
        self.mobilityInput = self.spin_box(self.input_grid, 'Mobility', 0, 7, True)
        self.perseveranceInput = self.spin_box(self.input_grid, 'Perseverance', 0, 8, True)
        self.intelligenceInput = self.spin_box(self.input_grid, 'Intelligence', 0, 9, True)
        self.charismaInput = self.spin_box(self.input_grid, 'Charisma', 0, 10, True)
        self.alignmentInput = self.combo_box(self.input_grid, 'Alignment', Alignment, 0, 11, True)
        self.experienceInput = self.spin_box(self.input_grid, 'Experience', 0, 12, True)
        self.hpInput = self.spin_box(self.input_grid, 'Hp', 0, 13, True)

        self.raceInput = self.combo_box(self.input_grid, 'Monster_race', MonsterRace, 0, 14, True)
        self.sizeInput = self.combo_box(self.input_grid, 'Monster_size', MonsterSize, 0, 15, True)

        self.addLayout(self.input_grid)


    def map_data(self, monster: Monster):
        """
        Mapa data from object to inputs in layout
        :param monster: Monster object
        """
        self.object = monster
        self.nameInput.setPlainText(self.object.name)
        self.descriptionInput.setPlainText(self.object.description)

        self.viabilityInput.setValue(self.object.viability if self.object.viability else 0)
        self.offenseInput.setPlainText(self.object.offense)
        self.defseInput.setValue(self.object.defense if self.object.defense else 0)
        self.enduranceInput.setValue(self.object.endurance if self.object.endurance else 0)
        self.rampancyInput.setValue(self.object.rampancy if self.object.rampancy else 0)
        self.mobilityInput.setValue(self.object.mobility if self.object.mobility else 0)
        self.perseveranceInput.setValue(self.object.perseverance if self.object.perseverance else 0)
        self.intelligenceInput.setValue(self.object.intelligence if self.object.intelligence else 0)
        self.charismaInput.setValue(self.object.charisma if self.object.charisma else 0)

        self.experienceInput.setValue(self.object.experience if self.object.experience else 0)
        self.hpInput.setValue(self.object.hp if self.object.hp else 0)

        raceIndex = self.object.monsterRace.value if self.object.monsterRace else 0
        sizeIndex = self.object.size.value if self.object.size else 0
        alignmentIndex = self.object.alignment.value if self.object.alignment else 0

        self.alignmentInput.setCurrentIndex(alignmentIndex)
        self.raceInput.setCurrentIndex(raceIndex)
        self.sizeInput.setCurrentIndex(sizeIndex)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.nameInput.toPlainText()
        self.object.description = self.descriptionInput.toPlainText()

        self.object.viability = self.viabilityInput.value()
        self.object.offense = self.offenseInput.toPlainText()
        self.object.defense = self.defseInput.value()
        self.object.endurance = self.enduranceInput.value()
        self.object.rampancy = self.rampancyInput.value()
        self.object.mobility = self.mobilityInput.value()
        self.object.perseverance = self.perseveranceInput.value()
        self.object.intelligence = self.intelligenceInput.value()
        self.object.charisma = self.charismaInput.value()

        self.object.experience = self.experienceInput.value()
        self.object.hp = self.hpInput.value()

        alignmentIndex = self.alignmentInput.currentIndex()
        raceIndex = self.raceInput.currentIndex()
        sizeIndex = self.sizeInput.currentIndex()
        self.object.monsterRace = MonsterRace(raceIndex) if raceIndex != 0 else None
        self.object.size = MonsterSize(sizeIndex) if sizeIndex != 0 else None
        self.object.alignment = Alignment(alignmentIndex) if alignmentIndex != 0 else None

        self.manager.update_monster(self.object)
