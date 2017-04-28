from PyQt5.QtWidgets import QMenuBar, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets

from data.drdFile.drdFile import DrdFile
from presentation.Translate import Translate as TR
from presentation.dialogs.Settings import Settings
from presentation.dialogs.TextDialog import TextDialog
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
        open_action.triggered.connect(self.open_slot)

        save_action = QAction(QIcon('resources/icons/save.png'), TR().tr('Menu_save'),
                              self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save file')
        save_action.triggered.connect(self.save_slot)

        settings_action = QAction(QIcon('resources/icons/settings.png'), TR().tr('Menu_settings'),
                                  self)
        settings_action.setShortcut('Ctrl+T')
        settings_action.setStatusTip('Settings')
        settings_action.triggered.connect(self.settings_slot)

        file_menu = self.addMenu(TR().tr('Menu_file'))
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(settings_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        self.init_player_ui()

        about_action = QAction(TR().tr('Menu_about'), self)
        help_menu = self.addMenu(TR().tr('Menu_help'))
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.about_action)


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
        scenario_templates = QAction(QIcon(ObjectType.SCENARIO.icon()), TR().tr('Menu.scenario'),
                                     self)
        location_templates = QAction(QIcon(ObjectType.LOCATION.icon()), TR().tr('Menu.location'),
                                     self)
        map_templates = QAction(QIcon(ObjectType.MAP.icon()), TR().tr('Menu.map'),
                                self)

        context_templates = QAction(QIcon(ObjectType.ABILITY_CONTEXT.icon()),
                                    TR().tr('Menu.ability_context'), self)

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
        scenario_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.SCENARIO)
        )
        location_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.LOCATION)
        )
        context_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.ABILITY_CONTEXT)
        )
        map_templates.triggered.connect(
            lambda: self.templates_menu_signal.emit(ObjectType.MAP)
        )

        file_menu = self.addMenu(TR().tr('Menu.templates'))
        file_menu.addAction(spell_templates)
        file_menu.addAction(item_templates)

        file_menu.addAction(ability_templates)
        file_menu.addAction(context_templates)

        file_menu.addAction(effect_templates)
        file_menu.addAction(modifier_templates)

        file_menu.addSeparator()
        file_menu.addAction(character_templates)
        file_menu.addSeparator()
        file_menu.addAction(monster_templates)
        file_menu.addAction(scenario_templates)
        file_menu.addAction(location_templates)
        file_menu.addAction(map_templates)


    def settings_slot(self):
        Settings.get_data()


    def about_action(self):
        # TextDialog(TR().tr('About_text'))
        QtWidgets.QMessageBox.about(self, "About Image Viewer",
                                    "<p>The <b>Image Viewer</b> example shows how to combine "
                                    "QLabel and QScrollArea to display an image. QLabel is "
                                    "typically used for displaying text, but it can also display "
                                    "an image. QScrollArea provides a scrolling view around "
                                    "another widget. If the child widget exceeds the size of the "
                                    "frame, QScrollArea automatically provides scroll bars.</p>"
                                    "<p>The example demonstrates how QLabel's ability to scale "
                                    "its contents (QLabel.scaledContents), and QScrollArea's "
                                    "ability to automatically resize its contents "
                                    "(QScrollArea.widgetResizable), can be used to implement "
                                    "zooming and scaling features.</p>"
                                    "<p>In addition the example shows how to use QPainter to "
                                    "print an image.</p>")


    def open_slot(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        types = "DrD Files (*.drd)"
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, TR().tr("File_select_open"),
                                                            "", types, options=options)

        if fileName:
            DrdFile().open(fileName)
            self.templates_menu_signal.emit(ObjectType.SCENARIO)


    def save_slot(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        types = "DrD Files (*.drd)"
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, TR().tr("File_select_target"),
                                                            "", types, options=options)

        if fileName:
            DrdFile().create(fileName)
            TextDialog('File saved')
