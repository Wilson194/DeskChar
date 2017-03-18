# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.ModifierManager import ModifierManager
from business.managers.SpellManager import SpellManager
from structure.enums.Attributes import Attributes
from structure.enums.Classes import Classes
from presentation.layouts.Layout import Layout
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType
from structure.spells.Spell import Spell


class ModifierLayout(Layout):
    """
    Layout for editing spell templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.modifier_manager = ModifierManager()
        self.object = None


    def init_ui(self):
        """
        Init basic UI
        """
        self.setObjectName('Modifier layout')

        self.header = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(15)
        self.header.setFont(font)
        self.header.setAlignment(QtCore.Qt.AlignCenter)

        self.addWidget(self.header)

        self.input_grid = QtWidgets.QGridLayout()
        self.input_grid.setSpacing(20)
        self.input_grid.setObjectName("Input grid")

        self.targetObject = self.combo_box(self.input_grid, 'Target object', ObjectType, 0, 0, True)
        self.targetAttribute = self.combo_box(self.input_grid, 'Target attribute', Attributes, 0, 1,
                                              True)
        self.value = self.spin_box(self.input_grid, 'Value', 0, 2, True)
        self.valueType = self.combo_box(self.input_grid, 'Value type', ModifierValueTypes, 0, 3, True)


        self.addLayout(self.input_grid)


    def map_data(self, spell: Spell):
        """
        Mapa data from object to inputs in layout
        :param spell: Spell object
        """
        # self.object = spell
        # self.header.setText(spell.name)
        # self.name_input.setPlainText(spell.name)
        # self.description_input.setPlainText(spell.description)
        # self.mana_cost_initial_input.setPlainText(spell.mana_cost_initial)
        # self.mana_cost_continual_input.setPlainText(spell.mana_cost_continual)
        # self.range_input.setPlainText(spell.range)
        # self.scope_input.setPlainText(spell.scope)
        # self.cast_time_input.setValue(spell.cast_time)
        # self.duration_input.setPlainText(spell.duration)
        #
        # class_index = spell.drd_class if spell.drd_class is not None else 0
        # self.class_input.setCurrentIndex(class_index)
        #
        # self.class_input.setCurrentIndex(spell.drd_class)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        # self.object.name = self.name_input.toPlainText()
        # self.object.description = self.description_input.toPlainText()
        # self.object.mana_cost_initial = self.mana_cost_initial_input.toPlainText()
        # self.object.mana_cost_continual = self.mana_cost_continual_input.toPlainText()
        # self.object.range = self.range_input.toPlainText()
        # self.object.scope = self.scope_input.toPlainText()
        # self.object.cast_time = self.cast_time_input.value()
        # self.object.duration = self.duration_input.toPlainText()
        #
        # class_index = self.class_input.currentIndex()
        # self.object.drd_class = class_index if class_index > 0 else None
        #
        # self.spell_manager.update_spell(self.object)
