from PyQt5.QtWidgets import QAction, QToolBar
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from structure.enums.ObjectType import ObjectType


class ToolBar(QToolBar):
    templates_tool_signal = QtCore.pyqtSignal(ObjectType)


    def __init__(self, parent, *__args):
        super().__init__(*__args)
        self.__parent = parent

        self.init_ui()


    def init_ui(self):
        toolbar = self.__parent.addToolBar('TemplateToolBar')

        spell_action = QAction(QIcon('resources/icons/book.png'), 'Spells', self.__parent)
        toolbar.addAction(spell_action)

        ability_action = QAction(QIcon('resources/icons/map.png'), 'Abilities', self.__parent)
        toolbar.addAction(ability_action)

        items_action = QAction(QIcon('resources/icons/axe.png'), 'Items', self.__parent)
        toolbar.addAction(items_action)

        spell_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.SPELL))

        ability_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.ABILITY))

        items_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.ITEM))
