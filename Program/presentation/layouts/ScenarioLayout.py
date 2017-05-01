# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.MonsterManager import MonsterManager
from business.managers.ScenarioManager import ScenarioManager
from structure.enums.Alignment import Alignment
from presentation.layouts.Layout import Layout
from structure.enums.MonsterRace import MonsterRace
from structure.enums.MonsterSize import MonsterSize
from structure.monster.Monster import Monster
from structure.scenario.Scenario import Scenario
from structure.tree.NodeObject import NodeObject


class ScenarioLayout(Layout):
    """
    Layout for editing scenario templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.manager = ScenarioManager()
        self.object = None


    def init_ui(self):
        """
        Init basic UI
        """
        self.setObjectName('Scenario layout')

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

        self.dateInput = self.date_box(self.input_grid, 'Date', 0, 2, True)

        self.addLayout(self.input_grid)


    def map_data(self, scenario: Scenario, treeNode: NodeObject = None) -> None:
        """
        Mapa data from object to inputs in layout
        :param scenario: Scenario object
        :param treeNode: node in tree widget, if its need to get whole object
        """
        self.object = scenario
        self.nameInput.setPlainText(self.object.name)
        self.descriptionInput.setPlainText(self.object.description)

        if self.object.date:
            d = self.object.date
            date = QtCore.QDate(d.year, d.month, d.day)
        else:
            date = QtCore.QDate(100, 1, 1)

        self.dateInput.setDate(date)


    def save_data(self) -> None:
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.nameInput.toPlainText()
        self.object.description = self.descriptionInput.toPlainText()

        self.object.date = self.dateInput.date().toPyDate()
        # print(self.dateInput.date().toPyDate().strftime('%Y/%m/%d'))

        self.manager.update_scenario(self.object)
