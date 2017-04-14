from PyQt5.QtWidgets import QMenuBar, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from presentation.Translate import Translate as TR
from structure.enums.ObjectType import ObjectType


class MainMenu(QMenuBar):
    """
    Class for creating main menu on window
    """

    templates_menu_signal = QtCore.pyqtSignal(ObjectType)


    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        """
        Init basic UI
        :return:
        """
        exit_action = QAction(QIcon('resources/icons/exit.png'), TR().tr('Menu_exit'),
                              self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        open_action = QAction(QIcon('resources/icons/open.png'), TR().tr('Menu_open'),
                              self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open file')

        save_action = QAction(QIcon('resources/icons/save.png'), TR().tr('Menu_save'),
                              self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save file')

        file_menu = self.addMenu(TR().tr('Menu_file'))
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        self.init_player_ui()

        about_action = QAction(TR().tr('Menu_about'), self)
        help_menu = self.addMenu(TR().tr('Menu_help'))
        help_menu.addAction(about_action)


    def init_player_ui(self):
        spell_templates = QAction(QIcon(ObjectType.SPELL.icon()), TR().tr('Menu.spell'), self)
        ability_templates = QAction(QIcon(ObjectType.ABILITY.icon()), TR().tr('Menu.ability'), self)
        item_templates = QAction(QIcon(ObjectType.ITEM.icon()), TR().tr('Menu.item'), self)
        modifier_templates = QAction(QIcon(ObjectType.MODIFIER.icon()), TR().tr('Menu.modifier'),
                                     self)
        effect_templates = QAction(QIcon(ObjectType.EFFECT.icon()), TR().tr('Menu.effect'), self)
        character_templates = QAction(QIcon(ObjectType.CHARACTER.icon()), TR().tr('Menu.character'),
                                      self)

        monster_templates = QAction(QIcon(ObjectType.MONSTER.icon()), TR().tr('Menu.monster'),
                                    self)

        ability_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.ABILITY))
        spell_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.SPELL))
        item_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.ITEM))
        modifier_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.MODIFIER))
        effect_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.EFFECT))
        character_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.CHARACTER))
        monster_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.MONSTER))

        file_menu = self.addMenu(TR().tr('Menu.templates'))
        file_menu.addAction(spell_templates)
        file_menu.addAction(ability_templates)
        file_menu.addAction(item_templates)
        file_menu.addAction(modifier_templates)
        file_menu.addAction(effect_templates)
        file_menu.addAction(character_templates)
        file_menu.addSeparator()
        file_menu.addAction(monster_templates)
