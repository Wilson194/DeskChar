
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from presentation.Translate import Translate as TR
from business.managers.LangManager import LangManager


class NewLangTab(QtWidgets.QDialog):
    """
    Dialog for select language for new tab or create new tab
    """


    def __init__(self, parent=None):
        super().__init__(parent)

        self.new_lang = None
        self.lang_manager = LangManager()
        self.init_ui()


    def init_ui(self):
        """
        Init basic UI
        """
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setSpacing(25)

        self.radio_select = QtWidgets.QRadioButton(TR().tr('Select_lang'), self)
        self.radio_select.setChecked(True)
        self.radio_new = QtWidgets.QRadioButton(TR().tr('Create_new_lang'), self)

        self.lang_combo = QtWidgets.QComboBox(self)
        self.name_label = QtWidgets.QLabel(TR().tr('Name'), self)
        self.name_input = QtWidgets.QLineEdit(self)
        self.code_label = QtWidgets.QLabel(TR().tr('Code'), self)
        self.code_input = QtWidgets.QLineEdit(self)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)

        langs = self.lang_manager.get_all_langs()
        for lang in langs:
            text = lang.name + ' (' + lang.code + ')'
            data = {'id': lang.id}

            self.lang_combo.addItem(text, QtCore.QVariant(data))

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
        """
        Action when click on accept button
        """
        if self.radio_new.isChecked():
            if self.lang_manager.lang_exists(self.code_input.text()):
                label = QtWidgets.QLabel('Existuju', self)
                self.layout.addWidget(label, 5, 0)
            else:
                self.new_lang = self.lang_manager.create_lang(self.name_input.text(),
                                                              self.code_input.text())
                self.accept()
        elif self.radio_select.isChecked():
            self.accept()


    def get_inputs(self):
        """
        Get data from inputs
        """
        if self.radio_select.isChecked():
            data = {
                'id': self.lang_combo.currentData()['id']
            }
        else:
            data = {
                'id': self.new_lang.id if self.new_lang else None
            }

        return data


    @staticmethod
    def get_data(parent=None):
        """
        Static method for create dialog
        :param parent:
        :return: (data,result) data -> input data, result -> True/False
        """
        dialog = NewLangTab(parent)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return (data, result == QtWidgets.QDialog.Accepted)
