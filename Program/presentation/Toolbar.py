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

        spell_action = QAction(QIcon(ObjectType.SPELL.icon()), 'Spells', self.__parent)
        toolbar.addAction(spell_action)

        ability_action = QAction(QIcon(ObjectType.ABILITY.icon()), 'Abilities', self.__parent)
        toolbar.addAction(ability_action)

        items_action = QAction(QIcon(ObjectType.ITEM.icon()), 'Items', self.__parent)
        toolbar.addAction(items_action)

        modifier_action = QAction(QIcon(ObjectType.MODIFIER.icon()), 'Modifiers', self.__parent)
        toolbar.addAction(modifier_action)

        effect_action = QAction(QIcon(ObjectType.EFFECT.icon()), 'Effect', self.__parent)
        toolbar.addAction(effect_action)

        character_action = QAction(QIcon(ObjectType.CHARACTER.icon()), 'Character', self.__parent)
        toolbar.addAction(character_action)

        context_action = QAction(QIcon(ObjectType.ABILITY_CONTEXT.icon()), 'AbilityContext', self.__parent)
        toolbar.addAction(context_action)



        spell_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.SPELL))

        ability_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.ABILITY))

        items_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.ITEM))

        modifier_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.MODIFIER))

        effect_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.EFFECT))

        character_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.CHARACTER))

        context_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.ABILITY_CONTEXT))

        toolbar.addSeparator()

        monster_action = QAction(QIcon(ObjectType.MONSTER.icon()), 'Monster', self.__parent)
        toolbar.addAction(monster_action)

        scenario_action = QAction(QIcon(ObjectType.SCENARIO.icon()), 'Scenario', self.__parent)
        toolbar.addAction(scenario_action)

        location_action = QAction(QIcon(ObjectType.LOCATION.icon()), 'Location', self.__parent)
        toolbar.addAction(location_action)

        monster_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.MONSTER))

        scenario_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.SCENARIO))

        location_action.triggered.connect(
            lambda: self.templates_tool_signal.emit(ObjectType.LOCATION))


