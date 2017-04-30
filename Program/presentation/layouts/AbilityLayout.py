# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.AbilityManager import AbilityManager
from data.DAO.AbilityDAO import AbilityDAO
from structure.abilities.Ability import Ability
from structure.enums.Races import Races
from structure.enums.Classes import Classes
from presentation.layouts.Layout import Layout
from presentation.Translate import Translate as TR


class AbilityLayout(Layout):
    """
    Layout for editing spell templates
    """


    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent

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
        self.level_input = self.spin_box(self.input_grid, 'Level', 0, 3, True)
        self.description_input = self.text_box(self.input_grid, 'Description', 0, 4)
        self.chance_input = self.text_box(self.input_grid, 'Chance', 0, 5)

        self.table = QtWidgets.QTableWidget(self.__parent)
        self.input_grid.addWidget(self.table, 6, 0, 1, 2)

        self.addLayout(self.input_grid)


    def map_data(self, ability: Ability, treeNode=None):
        """
        Mapa data from object to inputs in layout
        :param ability: Ability object
        """
        self.object = ability
        self.header.setText(ability.name)
        self.name_input.setPlainText(ability.name)
        self.description_input.setPlainText(ability.description)
        self.chance_input.setPlainText(ability.chance)
        self.level_input.setValue(ability.level if ability.level else 1)
        class_index = ability.drd_class.value if ability.drd_class is not None else 0
        race_index = ability.drd_race.value if ability.drd_race is not None else 0

        self.__set_table_data(treeNode)

        self.class_input.setCurrentIndex(class_index)
        self.race_input.setCurrentIndex(race_index)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.name_input.toPlainText()
        self.object.description = self.description_input.toPlainText()
        self.object.chance = self.chance_input.toPlainText()
        self.object.level = self.level_input.value()
        class_index = self.class_input.currentIndex()
        race_index = self.race_input.currentIndex()
        self.object.drd_class = Classes(class_index) if class_index > 0 else None
        self.object.drd_race = Races(race_index) if race_index > 0 else None

        self.ability_manager.update_ability(self.object)


    def __set_table_data(self, treeNode):
        self.table.setColumnCount(4)

        heades = [TR().tr('Name'), TR().tr('Target_attribute_type'), TR().tr('Value_type'), TR().tr('Value')]
        self.table.setHorizontalHeaderLabels(heades)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)

        # print(treeNode)
        ability = AbilityDAO().get(self.object.id, self.object.lang, treeNode.id, treeNode.context)

        self.table.setRowCount(len(ability.contexts))

        for i, context in enumerate(ability.contexts):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(context.name))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(TR().tr((context.targetAttribute))))

            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(TR().tr((context.valueType))))

            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(context.value)))
