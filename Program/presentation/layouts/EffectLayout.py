# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.ModifierManager import ModifierManager
from presentation.layouts.Layout import Layout
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


        self.addLayout(self.inputGrid)




    def map_data(self, modifier: Modifier):
        """
        Mapa data from object to inputs in layout
        :param modifier: Spell object
        """
        # self.object = modifier
        # self.header.setText(modifier.name)
        # self.nameInput.setText(modifier.name)
        #
        # targetTypeIndex = modifier.targetType.value
        # targetAttributeIndex = modifier.valueTargetAttribute.value
        # valueTypeIndex = modifier.valueType.value
        # value = modifier.value
        # self.targetTypeInput.setCurrentIndex(targetTypeIndex)
        # self.targetAttributeInput.setCurrentIndex(targetAttributeIndex)
        # self.valueTypeInput.setCurrentIndex(valueTypeIndex)
        # self.valueInput.setValue(value)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        # valid, data = self.completed()
        # if valid:
        #     self.object.name = self.nameInput.text()
        #     self.object.targetType = data[0]
        #     self.object.valueTargetAttribute = data[1]
        #     self.object.valueType = data[2]
        #     self.object.value = data[3]
        #
        #     self.modifier_manager.update(self.object)
