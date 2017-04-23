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
        elif isinstance(input, QtWidgets.QCheckBox):
            input.stateChanged.connect(lambda: self.save_synchronize_data_slot(input))


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
            elif isinstance(one, QtWidgets.QCheckBox):
                one.setChecked(obj.checkState())


    def text_line(self, grid: object, name: str, xposition: int, yposition: int,
                  synchronize: bool = False, xspan: int = 1,
                  yspan: int = 1) -> QtWidgets.QLabel:
        """
        Widget for text line input
        :param grid: parent grid
        :param name: Name of label
        :param xposition: grid position x
        :param yposition:  grid position y
        :param synchronize: bool, if true, value is synchronized trough all languages
        :return: input object
        """
        label = QtWidgets.QLabel()
        label.setText(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition, 1, 1)
        input = QtWidgets.QLineEdit()
        input.setObjectName(name)
        grid.addWidget(input, yposition, xposition + 1, yspan, xspan)
        input.textChanged.connect(self.data_changed)
        if synchronize:
            self.synchronize(input)

        return input


    def text_box(self, grid: object, name: str, xposition: int, yposition: int,
                 synchronize: bool = False, xspan: int = 1,
                 yspan: int = 1) -> QtWidgets.QPlainTextEdit:
        """
        Widget for text box
        :param grid: parent grid
        :param name: Name of label
        :param xposition: grid position x
        :param yposition: grid position y
        :param synchronize: bool, if true, value is synchronized trough all languages
        :return: input object
        """
        label = QtWidgets.QLabel()
        label.setText(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition, 1, 1)
        input = QtWidgets.QPlainTextEdit()
        input.setObjectName(name)
        grid.addWidget(input, yposition, xposition + 1, yspan, xspan)
        input.textChanged.connect(self.data_changed)
        if synchronize:
            self.synchronize(input)

        return input


    def combo_box(self, grid: object, name: str, data: object, xposition: int, yposition: int,
                  synchronize: bool = False, xspan: int = 1,
                  yspan: int = 1) -> QtWidgets.QComboBox:
        """
        Widget for combobox
        :param grid: parent grid
        :param name: Name of label
        :param data: List of data for combobox (enum)
        :param xposition: grid position x
        :param yposition: grid position y
        :param synchronize: bool, if true, value is synchronized trough all languages
        :return: input object
        """
        label = QtWidgets.QLabel(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition, yspan, xspan)
        input = QtWidgets.QComboBox()
        input.setObjectName(name + "_input")
        input.currentIndexChanged.connect(self.data_changed)
        if synchronize:
            self.synchronize(input)
        grid.addWidget(input, yposition, xposition + 1, yspan, xspan)
        input.addItem(TR().tr('Select_value'))
        for value in data:
            Qdata = {'value': value}
            input.addItem(TR().tr(str(value)), QtCore.QVariant(Qdata))

        return input


    def spin_box(self, grid: object, name: str, xposition: int, yposition: int,
                 synchronize: bool = False, xspan: int = 1, yspan: int = 1) -> QtWidgets.QSpinBox:
        """
        Widget for numbers, limit (-20,10000)         
        :param grid: parent grid
        :param name: Name of label
        :param xposition: grid position x
        :param yposition: grid position y
        :param synchronize: bool, if true, value is synchronized trough all languages
        :param yspan: 
        :param xspan:
        :return: input object
        """
        label = QtWidgets.QLabel()
        label.setText(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition, yspan, xspan)
        input = QtWidgets.QSpinBox()
        input.setMaximum(100000)
        input.setMinimum(-10000)
        input.setObjectName(name)
        if synchronize:
            self.synchronize(input)
        grid.addWidget(input, yposition, xposition + 1, yspan, xspan)
        input.valueChanged.connect(self.data_changed)

        return input


    def date_box(self, grid: object, name: str, xposition: int, yposition: int,
                 synchronize: bool = False, xspan: int = 1,
                 yspan: int = 1) -> QtWidgets.QDateEdit:
        label = QtWidgets.QLabel()
        label.setText(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition, 1, 1)

        input = QtWidgets.QDateEdit()
        input.setMinimumDate(QtCore.QDate(100, 1, 1))
        input.setObjectName(name)
        if synchronize:
            self.synchronize(input)
        grid.addWidget(input, yposition, xposition + 1, yspan, xspan)
        input.dateChanged.connect(self.data_changed)

        return input


    def check_box(self, grid: object, name: str, xposition: int, yposition: int,
                  synchronize: bool = False, xspan: int = 1,
                  yspan: int = 1) -> QtWidgets.QCheckBox:
        label = QtWidgets.QLabel()
        label.setText(TR().tr(name) + ':')
        grid.addWidget(label, yposition, xposition, 1, 1)

        input = QtWidgets.QCheckBox()
        input.setObjectName(name)
        if synchronize:
            self.synchronize(input)
        grid.addWidget(input, yposition, xposition + 1, yspan, xspan)
        input.stateChanged.connect(self.data_changed)

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
