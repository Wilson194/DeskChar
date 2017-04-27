from PyQt5 import QtWidgets, QtGui
from presentation.Translate import Translate as TR


class TextDialog:
    def __init__(self, text, icon=None):
        msg = QtWidgets.QMessageBox()
        if icon:
            msg.setIcon(icon)
        else:
            msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setWindowTitle(TR().tr('About'))

        msg.setWindowIcon(QtGui.QIcon('resources/icons/char.png'))

        msg.setText(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
