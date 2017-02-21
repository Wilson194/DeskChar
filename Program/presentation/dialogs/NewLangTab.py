# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

from structure.enums.NodeType import NodeType
from presentation.Translate import Translate as TR
from business.managers.LangManager import LangManager


class NewLangTab(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lang_manager = LangManager()
        self.init_ui()


    def init_ui(self):
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setSpacing(25)

        self.radio_select = QtWidgets.QRadioButton('Select lang', self)
        self.radio_select.setChecked(True)
        self.radio_new = QtWidgets.QRadioButton('Create new lang', self)

        self.lang_combo = QtWidgets.QComboBox(self)
        self.name_label = QtWidgets.QLabel('Name', self)
        self.name_input = QtWidgets.QLineEdit(self)
        self.code_label = QtWidgets.QLabel('Code', self)
        self.code_input = QtWidgets.QLineEdit(self)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)

        langs = self.lang_manager.get_all_langs()
        for lang in langs:
            text = lang.name + ' (' + lang.code + ')'
            self.lang_combo.addItem(text)

        self.layout.addWidget(self.radio_select, 0, 0)
        self.layout.addWidget(self.lang_combo, 0, 1, 1, 2)
        self.layout.addWidget(self.line, 1, 0, 1, 3)
        self.layout.addWidget(self.radio_new, 2, 0, 2, 1)

        self.layout.addWidget(self.name_label, 2, 1)
        self.layout.addWidget(self.name_input, 2, 2)
        self.layout.addWidget(self.code_label, 3, 1)
        self.layout.addWidget(self.code_input, 3, 2)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.accept_click)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.layout.addWidget(self.buttonBox, 4, 0, 1, 3, QtCore.Qt.AlignHCenter)


    def accept_click(self):
        if self.radio_new.isChecked():
            if self.lang_manager.lang_exists(self.code_input.text()):
                label = QtWidgets.QLabel('Existuju', self)
                self.layout.addWidget(label, 5, 0)
            else:
                self.lang_manager.create_lang(self.name_input.text(), self.code_input.text())
                self.accept()
        elif self.radio_select.isChecked():
            self.accept()


    def get_inputs(self):
        data = {
            'type': self.lang_combo.currentIndex() + 1
        }
        return data


    @staticmethod
    def get_data(parent=None):
        dialog = NewLangTab(parent)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return (data, result == QtWidgets.QDialog.Accepted)
