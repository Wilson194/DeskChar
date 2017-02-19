from PyQt5.QtWidgets import QFrame
from PyQt5 import QtWidgets, QtGui, QtCore
from presentation.Translate import Translate as TR


class SpellLayout(QtWidgets.QVBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()


    def init_ui(self):
        self.setObjectName('Spell layout')

        self.header = QtWidgets.QLabel()
        self.header.setText('Kouzlo - Ohnivá koule')
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
        name_input = QtWidgets.QLineEdit()
        self.input_grid.addWidget(name_input, 0, 1, 1, 1)

        # Description
        self.description_label = QtWidgets.QLabel()
        self.description_label.setText(TR().tr('Description') + ':')
        self.input_grid.addWidget(self.description_label, 1, 0, 1, 1)
        self.description_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.description_input, 1, 1, 1, 1)

        # Mana cost initial
        self.mana_cost_initial_label = QtWidgets.QLabel()
        self.mana_cost_initial_label.setText(TR().tr('Mana_cost_initial') + ':')
        self.input_grid.addWidget(self.mana_cost_initial_label, 2, 0, 1, 1)
        self.mana_cost_initial_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.mana_cost_initial_input, 2, 1, 1, 1)

        # Mana cost continual
        self.mana_cost_continual_label = QtWidgets.QLabel()
        self.mana_cost_continual_label.setText(
            TR().tr('Mana_cost_continual') + ':')
        self.input_grid.addWidget(self.mana_cost_continual_label, 3, 0, 1, 1)
        self.mana_cost_continual_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.mana_cost_continual_input, 3, 1, 1, 1)

        # Range
        self.range_label = QtWidgets.QLabel()
        self.range_label.setText(TR().tr('Range') + ':')
        self.input_grid.addWidget(self.range_label, 4, 0, 1, 1)
        self.range_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.range_input, 4, 1, 1, 1)

        # Scope
        self.scope_label = QtWidgets.QLabel()
        self.scope_label.setText(TR().tr('Scope') + ':')
        self.input_grid.addWidget(self.scope_label, 5, 0, 1, 1)
        self.scope_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.scope_input, 5, 1, 1, 1)

        # Cast time
        self.cast_time_label = QtWidgets.QLabel()
        self.cast_time_label.setText(TR().tr('Cast_time') + ':')
        self.input_grid.addWidget(self.cast_time_label, 6, 0, 1, 1)
        self.cast_time_input = QtWidgets.QSpinBox()
        self.input_grid.addWidget(self.cast_time_input, 6, 1, 1, 1)

        # Duration
        self.duration_label = QtWidgets.QLabel()
        self.duration_label.setText(TR().tr('Duration') + ':')
        self.input_grid.addWidget(self.duration_label, 7, 0, 1, 1)
        self.duration_input = QtWidgets.QPlainTextEdit()
        self.input_grid.addWidget(self.duration_input, 7, 1, 1, 1)



        self.addLayout(self.input_grid)
