# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

from data.DAO.LangDAO import LangDAO
from data.DAO.SettingsDAO import SettingsDAO
from presentation.dialogs.NewLangTab import NewLangTab
from structure.enums.NodeType import NodeType
from presentation.Translate import Translate as TR


class Settings(QtWidgets.QDialog):
    """
    Dialog for creating new item in tree widget
    """


    def __init__(self, parent=None):
        super().__init__(parent)

        self.DAO = SettingsDAO()
        self.langDAO = LangDAO()

        self.init_data()
        self.init_ui()


    def init_data(self):
        langId = self.DAO.get_value('language', int)
        self.lang = self.langDAO.get_lang(langId) if langId else self.langDAO.get_lang(1)


    def init_ui(self):
        """
        Init basic layout
        """
        self.setWindowIcon(QtGui.QIcon('resources/icons/char.png'))
        self.setWindowTitle('Settings')
        self.layout = QtWidgets.QGridLayout(self)

        self.langLabel = QtWidgets.QLabel('Default language:', self)
        buttonText = '{} ({})'.format(self.lang.name, self.lang.code)
        self.langButton = QtWidgets.QPushButton(buttonText, self)
        self.langButton.clicked.connect(self.lang_button_slot)

        self.layout.addWidget(self.langLabel, 1, 0)
        self.layout.addWidget(self.langButton, 1, 1)

        self.layout.addWidget(QHLine(), 2, 0, 1, 2)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.save_slot)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.layout.addWidget(self.buttonBox, 3, 0, 1, 2, QtCore.Qt.AlignHCenter)


    def lang_button_slot(self):
        data, result = NewLangTab.get_data()
        if result:
            self.lang = self.langDAO.get_lang(data['id'])
            buttonText = '{} ({})'.format(self.lang.name, self.lang.code)
            self.langButton.setText(buttonText)


    def save_slot(self):
        self.DAO.set_value('language', self.lang.id)
        self.DAO.set_value('language', self.lang.code)
        self.accept()


    @staticmethod
    def get_data(parent=None):
        dialog = Settings(parent)
        dialog.exec_()


class QHLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
