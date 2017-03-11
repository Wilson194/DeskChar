# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from abc import abstractmethod
from presentation.Synchronizer import Synchronizer as Sync
from presentation.Translate import Translate as TR


class Layout(QtWidgets.QVBoxLayout):
    """
    Parent class for templates layouts
    """
    data_changed_signal = QtCore.pyqtSignal(object)


    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent
        self.__synchronize_data = []


    def data_changed(self):
        """
        function that emit data_change_signal
        """
        self.data_changed_signal.emit(self)


    def synchronize(self, input: object):
        """
        Create synchronization of this input through lang tabs
         Dont forget delete data when changed object!
        :param input: Input widget
        """
        synchronize_data = Sync().get_data('Input_synchronize')
        if synchronize_data is None:
            Sync().save_data('Input_synchronize', {input.objectName(): [input]})
        elif input.objectName() not in synchronize_data:
            synchronize_data[input.objectName()] = [input]
        else:
            synchronize_data[input.objectName()].append(input)

        if isinstance(input, QtWidgets.QComboBox):
            input.currentIndexChanged.connect(lambda: self.save_synchronize_data_slot(input))
        elif isinstance(input, QtWidgets.QSpinBox):
            input.valueChanged.connect(lambda: self.save_synchronize_data_slot(input))


    def save_synchronize_data_slot(self, obj):
        """
        Slot for synchronize data when data is changed
        :param obj: object with changed input
        """
        synchronize_data = Sync().get_data('Input_synchronize')
        for one in synchronize_data[obj.objectName()]:
            if isinstance(one, QtWidgets.QComboBox):
                one.setCurrentIndex(obj.currentIndex())
            elif isinstance(one, QtWidgets.QSpinBox):
                one.setValue(obj.value())


    def text_box(self, grid, name, xposition, yposition, synchonize=False):
        label = QtWidgets.QLabel()
        label.setText(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition, 1, 1)
        input = QtWidgets.QPlainTextEdit()
        grid.addWidget(input, yposition, xposition + 1, 1, 1)
        input.textChanged.connect(self.data_changed)
        if synchonize:
            self.synchronize(input)

        return input


    def combo_box(self, grid, name, data, xposition, yposition, synchonize=False):
        label = QtWidgets.QLabel(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition)
        input = QtWidgets.QComboBox()
        input.setObjectName(name + "_input")
        input.currentIndexChanged.connect(self.data_changed)
        if synchonize:
            self.synchronize(input)
        grid.addWidget(input, yposition, xposition + 1)
        input.addItem(TR().tr('Select_value'))
        for value in data:
            Qdata = {'value': value}
            input.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))

        return input


    def spin_box(self, grid, name, xposition, yposition, synchronize=False):
        label = QtWidgets.QLabel()
        label.setText(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition, 1, 1)
        input = QtWidgets.QSpinBox()
        if synchronize:
            self.synchronize(input)
        grid.addWidget(input, yposition, xposition+1, 1, 1)
        input.valueChanged.connect(self.data_changed)

        return input


    @abstractmethod
    def map_data(self, obj: object):
        """
        Map data from object to layout
        :param obj: object with data
        """
        pass


    @abstractmethod
    def save_data(self):
        """
        Save data from input to database, use manager
        """
        pass
