from PyQt5 import QtWidgets, QtGui


class TextDialog:
    def __init__(self, text, icon=None):
        msg = QtWidgets.QMessageBox()
        if icon:
            msg.setIcon(icon)
        else:
            msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setWindowTitle("MessageBox")

        msg.setWindowIcon(QtGui.QIcon('resources/icons/char.png'))

        msg.setText(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
