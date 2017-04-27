# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from business.managers.ModifierManager import ModifierManager
from presentation.layouts.Layout import Layout
from structure.effects.Modifier import Modifier
from structure.enums.ArmorSize import ArmorSize
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.Handling import Handling
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.WeaponWeight import WeaponWeight
from presentation.Translate import Translate as TR


class ModifierLayout(Layout):
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

        self.inputGrid = QtWidgets.QGridLayout()
        self.inputGrid.setSpacing(20)
        self.inputGrid.setObjectName("Input grid")

        self.nameInput = self.text_line(self.inputGrid, 'Name', 0, 0)

        # Target Type Input -> Character / Item - Armor, money, weapon, ...
        self.targetTypeInput = self.combo_box(self.inputGrid, 'Target_type',
                                              ModifierTargetTypes, 0, 1, True)
        self.targetTypeInput.currentIndexChanged.connect(self.targetTypeChangedSlot)

        # Target attribute input -> charisma, strength, handling, ...
        self.targetAttributeInput = self.combo_box(self.inputGrid, 'Target_attribute_type',
                                                   [], 0, 2, True)
        self.targetAttributeInput.setDisabled(True)

        # Target value type -> % / full / ..
        self.valueTypeInput = self.combo_box(self.inputGrid, 'Value_type', [], 0, 3, True)
        self.valueTypeInput.setDisabled(True)

        # Value -> number
        self.valueInput = self.spin_box(self.inputGrid, 'Value', 0, 4, True)
        self.valueInput.setDisabled(True)

        self.valueComboInput = self.combo_box(self.inputGrid, 'Value', [], 0, 4, True)
        self.valueComboInput.hide()
        self.valueComboInput.setDisabled(True)

        self.addLayout(self.inputGrid)


    def targetTypeChangedSlot(self, index):
        """
        Slot that is called when target type is changed
        :param index: index of target type input combobox
        """
        try:
            self.targetAttributeInput.currentIndexChanged.disconnect(
                self.attributeTargetChangedSlot)
        except:
            pass

        self.targetAttributeInput.setCurrentIndex(0)
        self.targetAttributeInput.clear()

        if index == 0:
            self.targetAttributeInput.setDisabled(True)
            self.valueTypeInput.setDisabled(True)
            self.valueInput.setDisabled(True)
            self.valueComboInput.setDisabled(True)

        elif ModifierTargetTypes(index) is ModifierTargetTypes.CHARACTER:
            data = CharacterAttributes
            self.targetAttributeInput.addItem(TR().tr('Select_value'))
            for value in data:
                Qdata = {'value': value}
                self.targetAttributeInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
            self.targetAttributeInput.setDisabled(False)
            self.targetAttributeInput.currentIndexChanged.connect(self.attributeTargetChangedSlot)

        else:
            data = ItemsAttributes
            self.targetAttributeInput.addItem(TR().tr('Select_value'))
            for value in data:
                Qdata = {'value': value}
                self.targetAttributeInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
            self.targetAttributeInput.setDisabled(False)
            self.targetAttributeInput.currentIndexChanged.connect(self.attributeTargetChangedSlot)


    def attributeTargetChangedSlot(self, index):
        """
        Slot that is called when target attributes is changed
        :param index: index of target attribute combobox
        :return:
        """
        try:
            self.valueTypeInput.currentIndexChanged.disconnect(self.valueTypeChangedSlot)
        except:
            pass

        self.valueTypeInput.setDisabled(False)
        self.valueInput.setDisabled(True)
        self.valueComboInput.setDisabled(True)

        if index == 0:
            self.valueTypeInput.setDisabled(True)

        elif ModifierTargetTypes(self.targetTypeInput.currentIndex()) is ModifierTargetTypes.CHARACTER:
            self.valueTypeInput.clear()
            self.valueTypeInput.addItem(TR().tr('Select_value'))
            for value in [ModifierValueTypes.FROM_BASE, ModifierValueTypes.FROM_TOTAL, ModifierValueTypes.TO_TOTAL]:
                Qdata = {'value': value}
                self.valueTypeInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
            self.valueTypeInput.currentIndexChanged.connect(self.valueTypeChangedSlot)

        else:
            self.valueComboInput.clear()
            self.valueComboInput.addItem(TR().tr('Select_value'))
            self.valueTypeInput.clear()
            if ItemsAttributes(index) is ItemsAttributes.WEAPON_MELEE_HANDLING:
                self.valueTypeInput.addItem(TR().tr('Select_value'))
                for value in ModifierValueTypes:
                    Qdata = {'value': value}
                    self.valueTypeInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
                self.valueTypeInput.currentIndexChanged.connect(self.valueSetTypeSlot)
                self.valueTypeInput.setCurrentIndex(ModifierValueTypes.TYPE_WEAPON_HANDLING.value)
                self.valueTypeInput.setDisabled(True)
                self.valueComboInput.show()
                self.valueInput.hide()
                self.valueComboInput.setDisabled(False)
                for one in Handling:
                    self.valueComboInput.addItem(TR().tr(one))

            elif ItemsAttributes(index) is ItemsAttributes.WEAPON_WEIGHT:
                self.valueTypeInput.addItem(TR().tr('Select_value'))
                for value in ModifierValueTypes:
                    Qdata = {'value': value}
                    self.valueTypeInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
                self.valueTypeInput.currentIndexChanged.connect(self.valueSetTypeSlot)
                self.valueTypeInput.setCurrentIndex(ModifierValueTypes.TYPE_WEAPON_WEIGHT.value)
                self.valueTypeInput.setDisabled(True)
                self.valueComboInput.show()
                self.valueInput.hide()
                self.valueComboInput.setDisabled(False)
                for one in WeaponWeight:
                    self.valueComboInput.addItem(TR().tr(one))

            elif ItemsAttributes(index) is ItemsAttributes.ARMOR_SIZE:
                self.valueTypeInput.addItem(TR().tr('Select_value'))
                for value in ModifierValueTypes:
                    Qdata = {'value': value}
                    self.valueTypeInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
                self.valueTypeInput.currentIndexChanged.connect(self.valueSetTypeSlot)
                self.valueTypeInput.setCurrentIndex(ModifierValueTypes.TYPE_ARMOR_SIZE.value)
                self.valueTypeInput.setDisabled(True)
                self.valueComboInput.show()
                self.valueInput.hide()
                self.valueComboInput.setDisabled(False)
                for one in ArmorSize:
                    self.valueComboInput.addItem(TR().tr(one))

            else:
                self.valueTypeInput.addItem(TR().tr('Select_value'))
                for value in [ModifierValueTypes.FROM_BASE, ModifierValueTypes.FROM_TOTAL, ModifierValueTypes.TO_TOTAL]:
                    Qdata = {'value': value}
                    self.valueTypeInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
                self.valueTypeInput.currentIndexChanged.connect(self.valueTypeChangedSlot)

                self.valueComboInput.hide()
                self.valueInput.show()


    def valueTypeChangedSlot(self, index):
        """

        :param index:
        :return:
        """
        valuesType = ModifierValueTypes(self.valueTypeInput.currentIndex()) if self.valueTypeInput.currentIndex() > 0 else None

        self.valueComboInput.clear()
        self.valueComboInput.addItem(TR().tr('Select_value'))

        if valuesType is ModifierValueTypes.TYPE_ARMOR_SIZE:
            for value in ArmorSize:
                Qdata = {'value': value}
                self.valueComboInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
            self.valueComboInput.show()
            self.valueInput.hide()
            self.valueComboInput.setDisabled(False)
        elif valuesType is ModifierValueTypes.TYPE_WEAPON_WEIGHT:
            for value in WeaponWeight:
                Qdata = {'value': value}
                self.valueComboInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
            self.valueComboInput.show()
            self.valueInput.hide()
            self.valueComboInput.setDisabled(False)
        elif valuesType is ModifierValueTypes.TYPE_WEAPON_HANDLING:
            for value in Handling:
                Qdata = {'value': value}
                self.valueComboInput.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))
            self.valueComboInput.show()
            self.valueInput.hide()
            self.valueComboInput.setDisabled(False)
        else:
            self.valueInput.show()
            self.valueInput.setDisabled(False)


    def valueSetTypeSlot(self, index):
        """

        :param index:
        :return:
        """
        self.valueInput.setValue(index)


    def completed(self) -> tuple:
        """
        Function that chcecked if all important inputs are filled.
         return True only if inputs are valid modifier
        :return: (bool, [targetType, attributeType, valueType, value])
        """
        try:
            targetType = ModifierTargetTypes(self.targetTypeInput.currentIndex())
            if targetType is ModifierTargetTypes.CHARACTER:
                attributeType = CharacterAttributes(self.targetAttributeInput.currentIndex())
            else:
                attributeType = ItemsAttributes(self.targetAttributeInput.currentIndex())

            if attributeType is ItemsAttributes.WEAPON_MELEE_HANDLING:
                valueType = ModifierValueTypes(self.valueTypeInput.currentIndex())
                value = Handling(self.valueComboInput.currentIndex())
            elif attributeType is ItemsAttributes.WEAPON_WEIGHT:
                valueType = ModifierValueTypes(self.valueTypeInput.currentIndex())
                value = WeaponWeight(self.valueTypeInput.currentIndex())
            elif attributeType is ItemsAttributes.ARMOR_SIZE:
                valueType = ModifierValueTypes(self.valueTypeInput.currentIndex())
                value = ArmorSize(self.valueComboInput.currentIndex())
            else:
                valueType = ModifierValueTypes(self.valueTypeInput.currentIndex())
                value = self.valueInput.value()
            return True, [targetType, attributeType, valueType, value]
        except:
            return False, []


    def map_data(self, modifier: Modifier):
        """
        Mapa data from object to inputs in layout
        :param modifier: Spell object
        """
        self.object = modifier
        self.header.setText(modifier.name)
        self.nameInput.setText(modifier.name)

        targetTypeIndex = modifier.targetType.value if modifier.targetType else 0
        if modifier.targetType is ModifierTargetTypes.CHARACTER:
            targetAttributeIndex = modifier.characterTargetAttribute.value if modifier.characterTargetAttribute else 0
        else:
            targetAttributeIndex = modifier.itemTargetAttribute.value if modifier.itemTargetAttribute else 0

        valueTypeIndex = modifier.valueType.value if modifier.valueType else 0
        value = modifier.value if modifier.value else 0
        self.targetTypeInput.setCurrentIndex(targetTypeIndex)
        self.targetAttributeInput.setCurrentIndex(targetAttributeIndex)
        self.valueTypeInput.setCurrentIndex(valueTypeIndex)
        self.valueInput.setValue(value)
        self.valueComboInput.setCurrentIndex(value)


    def save_data(self):
        """
        Update data in object from inputs and update in manager
        """
        valid, data = self.completed()
        if valid:
            self.object.name = self.nameInput.text()
            self.object.targetType = data[0]
            if self.object.targetType is ModifierTargetTypes.CHARACTER:
                self.object.characterTargetAttribute = data[1]
            else:
                self.object.itemTargetAttribute = data[1]
            self.object.valueType = data[2]
            self.object.value = data[3]

            self.modifier_manager.update(self.object)
