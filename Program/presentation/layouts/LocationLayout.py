# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.LocationManager import LocationManager
from business.managers.ScenarioManager import ScenarioManager
from presentation.layouts.Layout import Layout
from structure.monster.Monster import Monster


class LocationLayout(Layout):
    """
    Layout for editing scenario templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.manager = LocationManager()
        self.object = None


    def init_ui(self):
        """
        Init basic UI
        """
        self.setObjectName('Location layout')

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

        self.addLayout(self.input_grid)


    def map_data(self, monster: Monster):
        """
        Mapa data from object to inputs in layout
        :param monster: Monster object
        """
        self.object = monster
        self.nameInput.setPlainText(self.object.name)
        self.descriptionInput.setPlainText(self.object.description)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        self.object.name = self.nameInput.toPlainText()
        self.object.description = self.descriptionInput.toPlainText()

        self.manager.update_location(self.object)
