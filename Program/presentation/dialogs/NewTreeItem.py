# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

from structure.enums.NodeType import NodeType
from presentation.Translate import Translate as TR


class NewTreeItem(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()


    def init_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.type_label = QtWidgets.QLabel(self)
        self.type_label.setText(TR().tr('Type') + ' :')
        self.layout.addWidget(self.type_label, 0, 0)
        self.type_input = QtWidgets.QComboBox(self)
        self.layout.addWidget(self.type_input, 0, 1)

        for item in NodeType:
            self.type_input.addItem(TR().tr(item), QtCore.QVariant(item.value))

        self.name_label = QtWidgets.QLabel(self)
        self.name_label.setText(TR().tr('Name') + ' :')
        self.layout.addWidget(self.name_label, 1, 0)
        self.name_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.name_input, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.layout.addWidget(self.buttonBox, 2, 0, 1, 2, QtCore.Qt.AlignHCenter)


    def get_inputs(self):
        data = {
            'name': self.name_input.text(),
            'type': self.type_input.currentIndex()+1
        }
        return data


    @staticmethod
    def get_data(parent=None):
        dialog = NewTreeItem(parent)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return (data, result == QtWidgets.QDialog.Accepted)
