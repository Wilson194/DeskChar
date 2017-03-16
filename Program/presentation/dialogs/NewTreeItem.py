# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

from structure.enums.NodeType import NodeType
from presentation.Translate import Translate as TR


class NewTreeItem(QtWidgets.QDialog):
    """
    Dialog for creating new item in tree widget
    """


    def __init__(self, objects: list, parent=None):
        super().__init__(parent)

        self.__objects = objects
        self.init_ui()


    def init_ui(self):
        """
        Init basic layout
        """
        self.layout = QtWidgets.QGridLayout(self)

        self.type_label = QtWidgets.QLabel(self)
        self.type_label.setText(TR().tr('Type') + ' :')
        self.layout.addWidget(self.type_label, 0, 0)
        self.type_input = QtWidgets.QComboBox(self)
        self.layout.addWidget(self.type_input, 0, 1)

        data = {'NodeType': NodeType.FOLDER}
        self.type_input.addItem(TR().tr(NodeType.FOLDER), QtCore.QVariant(data))

        for obj in self.__objects:
            data = {'NodeType': NodeType.OBJECT, 'Object': obj}
            self.type_input.addItem(str(obj().__name__()[-1]), QtCore.QVariant(data))

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


    def get_inputs(self) -> dict:
        """
        Get inputs from dialog
        :return: dictionary of data (name,value)
        """

        current = self.type_input.currentData()
        data = {
            'name'    : self.name_input.text(),
            'NodeType': current['NodeType'] if 'NodeType' in current else None,
            'Object'  : current['Object'] if 'Object' in current else None
        }
        return data


    @staticmethod
    def get_data(objects: list, parent=None) -> tuple:
        """
        Create new dialog and return data from dialog (name,type)
        :param objects: List of object that can be created
        :objects list of object to create
        :param parent: parent object for creating dialog
        :return: tuple of data and result by buttons(true,false)
        """
        dialog = NewTreeItem(objects, parent)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return data, result == QtWidgets.QDialog.Accepted
