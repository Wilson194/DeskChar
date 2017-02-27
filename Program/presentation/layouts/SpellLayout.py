# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from presentation.Translate import Translate as TR
from structure.spells.Spell import Spell
from business.managers.SpellManager import SpellManager
from structure.enums.Classes import Classes
from presentation.layouts.Layout import Layout


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
        for drd_class in Classes:
            data = {'value': drd_class}
            self.class_input.addItem(TR().tr(str(drd_class)), QtCore.QVariant(data))

        # Description
        self.description_label = QtWidgets.QLabel()
        self.description_label.setText(TR().tr('Description') + ':')
        self.input_grid.addWidget(self.description_label, 2, 0, 1, 1)
        self.description_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.description_input, 2, 1, 1, 1)
        self.description_input.textChanged.connect(self.data_changed)

        # Mana cost initial
        self.mana_cost_initial_label = QtWidgets.QLabel()
        self.mana_cost_initial_label.setText(TR().tr('Mana_cost_initial') + ':')
        self.input_grid.addWidget(self.mana_cost_initial_label, 3, 0, 1, 1)
        self.mana_cost_initial_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.mana_cost_initial_input, 3, 1, 1, 1)
        self.mana_cost_initial_input.textChanged.connect(self.data_changed)

        # Mana cost continual
        self.mana_cost_continual_label = QtWidgets.QLabel()
        self.mana_cost_continual_label.setText(
            TR().tr('Mana_cost_continual') + ':')
        self.input_grid.addWidget(self.mana_cost_continual_label, 4, 0, 1, 1)
        self.mana_cost_continual_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.mana_cost_continual_input, 4, 1, 1, 1)
        self.mana_cost_continual_input.textChanged.connect(self.data_changed)

        # Range
        self.range_label = QtWidgets.QLabel()
        self.range_label.setText(TR().tr('Range') + ':')
        self.input_grid.addWidget(self.range_label, 5, 0, 1, 1)
        self.range_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.range_input, 5, 1, 1, 1)
        self.range_input.textChanged.connect(self.data_changed)

        # Scope
        self.scope_label = QtWidgets.QLabel()
        self.scope_label.setText(TR().tr('Scope') + ':')
        self.input_grid.addWidget(self.scope_label, 6, 0, 1, 1)
        self.scope_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.scope_input, 6, 1, 1, 1)
        self.scope_input.textChanged.connect(self.data_changed)

        # Cast time
        self.cast_time_label = QtWidgets.QLabel()
        self.cast_time_label.setText(TR().tr('Cast_time') + ':')
        self.input_grid.addWidget(self.cast_time_label, 7, 0, 1, 1)
        self.cast_time_input = QtWidgets.QSpinBox()
        self.synchronize(self.cast_time_input)
        self.input_grid.addWidget(self.cast_time_input, 7, 1, 1, 1)
        self.cast_time_input.valueChanged.connect(self.data_changed)

        # Duration
        self.duration_label = QtWidgets.QLabel()
        self.duration_label.setText(TR().tr('Duration') + ':')
        self.input_grid.addWidget(self.duration_label, 8, 0, 1, 1)
        self.duration_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.duration_input, 8, 1, 1, 1)
        self.duration_input.textChanged.connect(self.data_changed)

        self.addLayout(self.input_grid)


    def map_data(self, spell: Spell):
        """
        Mapa data from object to inputs in layout
        :param spell: Spell object
        """
        self.object = spell
        self.header.setText(spell.name)
        self.name_input.setPlainText(spell.name)
        self.description_input.setPlainText(spell.description)
        self.mana_cost_initial_input.setPlainText(spell.mana_cost_initial)
        self.mana_cost_continual_input.setPlainText(spell.mana_cost_continual)
        self.range_input.setPlainText(spell.range)
        self.scope_input.setPlainText(spell.scope)
        self.cast_time_input.setValue(spell.cast_time)
        self.duration_input.setPlainText(spell.duration)
        self.class_input.setCurrentIndex(spell.drd_class - 1)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText().encode('utf-8').decode('utf-8')
        self.object.description = self.description_input.toPlainText().encode('utf-8').decode('utf-8')
        self.object.mana_cost_initial = self.mana_cost_initial_input.toPlainText().encode('utf-8').decode('utf-8')
        self.object.mana_cost_continual = self.mana_cost_continual_input.toPlainText().encode('utf-8').decode('utf-8')
        self.object.range = self.range_input.toPlainText().encode('utf-8').decode('utf-8')
        self.object.scope = self.scope_input.toPlainText().encode('utf-8').decode('utf-8')
        self.object.cast_time = self.cast_time_input.value()
        self.object.duration = self.duration_input.toPlainText().encode('utf-8').decode('utf-8')
        self.object.drd_class = self.class_input.currentIndex() + 1

        self.spell_manager.update_spell(self.object)
