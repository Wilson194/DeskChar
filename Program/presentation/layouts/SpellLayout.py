# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.SpellManager import SpellManager
from structure.enums.Classes import Classes
from presentation.layouts.Layout import Layout
from structure.spells.Spell import Spell
from structure.tree.NodeObject import NodeObject


class SpellLayout(Layout):
    """
    Layout for editing spell templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.spell_manager = SpellManager()
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
        self.description_input = self.text_box(self.input_grid, 'Description', 0, 2)
        self.mana_cost_initial_input = self.text_box(self.input_grid, 'Mana_cost_initial', 0, 3)
        self.mana_cost_continual_input = self.text_box(self.input_grid, 'Mana_cost_continual', 0, 4)
        self.range_input = self.text_box(self.input_grid, 'Range', 0, 5)
        self.scope_input = self.text_box(self.input_grid, 'Scope', 0, 6)
        self.cast_time_input = self.spin_box(self.input_grid, 'Cast_time', 0, 7, True)
        self.duration_input = self.text_box(self.input_grid, 'Duration', 0, 8)

        self.addLayout(self.input_grid)


    def map_data(self, spell: Spell, treeNode: NodeObject = None) -> None:
        """
        Mapa data from object to inputs in layout
        :param spell: Spell object
        :param treeNode: node in tree widget, if its need to get whole object
        """
        self.object = spell
        self.header.setText(spell.name)
        self.name_input.setPlainText(spell.name)
        self.description_input.setPlainText(spell.description)
        self.mana_cost_initial_input.setPlainText(spell.mana_cost_initial)
        self.mana_cost_continual_input.setPlainText(spell.mana_cost_continual)
        self.range_input.setPlainText(spell.range)
        self.scope_input.setPlainText(spell.scope)
        self.cast_time_input.setValue(spell.cast_time if spell.cast_time else 0)
        self.duration_input.setPlainText(spell.duration)

        class_index = spell.drd_class.value if spell.drd_class is not None else 0
        self.class_input.setCurrentIndex(class_index)


    def save_data(self) -> None:
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()
        self.object.mana_cost_initial = self.mana_cost_initial_input.toPlainText()
        self.object.mana_cost_continual = self.mana_cost_continual_input.toPlainText()
        self.object.range = self.range_input.toPlainText()
        self.object.scope = self.scope_input.toPlainText()
        self.object.cast_time = self.cast_time_input.value()
        self.object.duration = self.duration_input.toPlainText()

        class_index = self.class_input.currentIndex()
        self.object.drd_class = Classes(class_index) if class_index > 0 else None

        self.spell_manager.update_spell(self.object)
