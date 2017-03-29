# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.ModifierManager import ModifierManager
from presentation.layouts.Layout import Layout
from structure.effects.Effect import Effect
from structure.effects.Modifier import Modifier
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.Handling import Handling
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.WeaponWeight import WeaponWeight
from presentation.Translate import Translate as TR


class EffectLayout(Layout):
    """
    Layout for editing spell templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.modifier_manager = ModifierManager()
        self.object = None
        self.__parent = parent


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

        self.inputGrid = QtWidgets.QGridLayout()
        self.inputGrid.setSpacing(20)
        self.inputGrid.setObjectName("Input grid")

        self.nameInput = self.text_box(self.inputGrid, 'Name', 0, 0)
        self.descriptionInput = self.text_box(self.inputGrid, 'Description', 0, 1)
        self.targetInput = self.combo_box(self.inputGrid, 'Modifier_target', ModifierTargetTypes, 0,
                                          2, True)


        table = QtWidgets.QTableWidget(self.__parent)
        table.setRowCount(4)


        self.addLayout(self.inputGrid)


    def map_data(self, effect: Effect):
        """
        Mapa data from object to inputs in layout
        :param effect: Spell object
        """
        self.object = effect
        self.header.setText(effect.name)
        self.nameInput.setPlainText(effect.name)
        self.descriptionInput.setPlainText(effect.description)

        targetTypeIndex = effect.targetType.value
        self.targetInput.setCurrentIndex(targetTypeIndex)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """

        self.object.name = self.nameInput.toPlainText()
        self.object.description = self.descriptionInput.toPlainText()

        targetIndex = self.targetInput.currentIndex()
        self.object.targetType = targetIndex if targetIndex > 0 else None

        self.modifier_manager.update(self.object)
