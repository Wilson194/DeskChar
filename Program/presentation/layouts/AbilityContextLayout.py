# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.AbilityContextManager import AbilityContextManager
from business.managers.ModifierManager import ModifierManager
from data.DAO.AbilityContextDAO import AbilityContextDAO
from presentation.layouts.Layout import Layout
from structure.effects.AbilityContext import AbilityContext
from structure.effects.Modifier import Modifier
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.Handling import Handling
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.WeaponWeight import WeaponWeight
from presentation.Translate import Translate as TR


class AbilityContextLayout(Layout):
    """
    Layout for editing spell templates
    """


    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

        self.contextManager = AbilityContextManager()
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

        self.inputGrid = QtWidgets.QGridLayout()
        self.inputGrid.setSpacing(20)
        self.inputGrid.setObjectName("Input grid")

        self.nameInput = self.text_line(self.inputGrid, 'Name', 0, 0)

        self.targetAttributeInput = self.combo_box(self.inputGrid, 'Target_attribute_type',
                                                   CharacterAttributes, 0, 2, True)

        self.valueTypeInput = self.combo_box(self.inputGrid, 'Value_type',
                                             [ModifierValueTypes.TO_TOTAL, ModifierValueTypes.FROM_BASE,
                                              ModifierValueTypes.FROM_TOTAL], 0, 3, True)

        self.valueInput = self.spin_box(self.inputGrid, 'Value', 0, 4, True)

        self.addLayout(self.inputGrid)


    def map_data(self, context: AbilityContext, treeNode=None):
        """
        Mapa data from object to inputs in layout
        :param context: Spell object
        """
        self.object = context
        self.header.setText(context.name)
        self.nameInput.setText(context.name)

        targetAttributeIndex = self.object.targetAttribute.value if self.object.targetAttribute else 0
        valueTypeIndex = self.object.valueType.value if self.object.valueType else 0
        value = self.object.value if self.object.value else 0

        self.targetAttributeInput.setCurrentIndex(targetAttributeIndex)
        self.valueTypeInput.setCurrentIndex(valueTypeIndex)
        self.valueInput.setValue(value)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """

        self.object.name = self.nameInput.text()
        targetAttributeIndex = self.targetAttributeInput.currentIndex()
        valueTypeIndex = self.valueTypeInput.currentIndex()

        self.object.targetAttribute = CharacterAttributes(targetAttributeIndex) if targetAttributeIndex != 0 else None
        self.object.valueType = ModifierValueTypes(valueTypeIndex) if valueTypeIndex != 0 else None
        self.object.value = self.valueInput.value()

        self.contextManager.update(self.object)


