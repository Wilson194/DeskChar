# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore

from business.managers.EffectManager import EffectManager
from business.managers.ModifierManager import ModifierManager
from data.DAO.EffectDAO import EffectDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
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

        self.effect_manager = EffectManager()
        self.object = None
        self.__parent = parent

        self.init_ui()


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
        self.targetInput = self.combo_box(self.inputGrid, 'Effect_target', ModifierTargetTypes, 0, 2, True)
        self.activeInput = self.check_box(self.inputGrid, 'Active', 0, 3, True)

        self.table = QtWidgets.QTableWidget(self.__parent)

        self.inputGrid.addWidget(self.table, 4, 0, 1, 2)

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
        self.activeInput.setChecked(effect.active)
        self.__set_table_data()

        targetTypeIndex = effect.targetType.value
        self.targetInput.setCurrentIndex(targetTypeIndex)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """

        self.object.name = self.nameInput.toPlainText()
        self.object.description = self.descriptionInput.toPlainText()

        targetIndex = self.targetInput.currentIndex()
        self.object.targetType = ModifierTargetTypes(targetIndex) if targetIndex != 0 else None

        self.object.active = self.activeInput.checkState()

        self.effect_manager.update_effect(self.object)


    def __set_table_data(self):
        self.table.setColumnCount(5)
        self.table.setRowCount(len(self.object.modifiers))

        heades = [TR().tr('Name'), TR().tr('Target_type'), TR().tr('Target_attribute_type'),
                  TR().tr('Value_type'), TR().tr('Value')]
        self.table.setHorizontalHeaderLabels(heades)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)

        # effectNode = PlayerTreeDAO().get_node_by_object(self.object)
        # EffectDAO().get(self.object.id,self.object.lang,effectNode.id, effectNode)

        for i, modifier in enumerate(self.object.modifiers):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(modifier.name))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(TR().tr((modifier.targetType))))
            if modifier.itemTargetAttribute is not None:
                self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(
                    TR().tr((modifier.itemTargetAttribute))))
            else:
                self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(
                    TR().tr((modifier.characterTargetAttribute))))

            if modifier.itemTargetAttribute in (
                    ItemsAttributes.WEAPON_MELEE_HANDLING, ItemsAttributes.WEAPON_WEIGHT):
                self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(TR().tr((modifier.valueType))))
            else:
                self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(TR().tr((modifier.valueType))))
                self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(modifier.value)))
