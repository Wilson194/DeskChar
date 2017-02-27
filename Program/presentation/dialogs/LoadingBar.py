from PyQt5 import QtWidgets
from PyQt5 import QtCore


class LoadingBar(QtWidgets.QDialog):
    signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.current = 0

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setRange(0, 100)

        layout.addWidget(self.progressBar)
        self.signal.connect(self.onProgress)


    def set_max(self, max):
        self.current = 0
        self.progressBar.setRange(0, max)


    def onProgress(self):
        print(self.current)
        self.current += 1
        self.progressBar.setValue(self.current)
