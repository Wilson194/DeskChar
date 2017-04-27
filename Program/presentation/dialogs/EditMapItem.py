# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

from structure.enums.NodeType import NodeType
from presentation.Translate import Translate as TR
from structure.enums.ObjectType import ObjectType
from structure.map.MapItem import MapItem


class EditMapItem(QtWidgets.QDialog):
    """
    Dialog for creating new item in tree widget
    """


    def __init__(self, parent=None, mapItem: MapItem = None):
        super().__init__(parent)

        self.mapItem = mapItem
        self.init_ui()


    def init_ui(self):
        """
        Init basic layout
        """
        self.setWindowIcon(QtGui.QIcon('resources/icons/char.png'))
        self.setWindowTitle(TR().tr('Edit_information'))
        self.layout = QtWidgets.QGridLayout(self)

        self.name_label = QtWidgets.QLabel(TR().tr('name') + ' :', self)
        self.layout.addWidget(self.name_label, 0, 0)

        self.name_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.name_input, 0, 1)
        self.name_input.setText(self.mapItem.name)

        self.description_label = QtWidgets.QLabel(TR().tr('description') + ':', self)
        self.layout.addWidget(self.description_label, 1, 0)

        self.description_input = QtWidgets.QPlainTextEdit(self)
        self.layout.addWidget(self.description_input, 1, 1)
        self.description_input.setPlainText(self.mapItem.description)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.layout.addWidget(self.buttonBox, 2, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.name_input.setFocus()


    def get_inputs(self) -> dict:
        """
        Get inputs from dialog
        :return: dictionary of data (name,value)
        """

        data = {
            'name'       : self.name_input.text(),
            'description': self.description_input.toPlainText(),
        }
        return data


    @staticmethod
    def get_data(parent=None, mapItem: MapItem= None) -> tuple:
        """
        Create new dialog and return data from dialog (name,type)
        :param objects: List of object that can be created
        :objects list of object to create
        :param parent: parent object for creating dialog
        :return: tuple of data and result by buttons(true,false)
        """
        dialog = EditMapItem(parent, mapItem)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return data, result == QtWidgets.QDialog.Accepted
