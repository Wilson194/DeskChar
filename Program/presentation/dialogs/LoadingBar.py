# from PyQt5 import QtWidgets
# from PyQt5 import QtCore
# import sys
# from PyQt5.QtCore import QThread
#
#
#
# class LoadigDialog(QtWidgets.QDialog):
#     def __init__(self,parent=None):
#         super().__init__(parent)
#         self.resize(50, 50)
#         self.Button = QtWidgets.QPushButton(self)
#         self.Button.clicked.connect(self.Run_Something)
#         self.Button.setText("Run")
#
#     def Run_Something(self):
#         self.progress = QtWidgets.QProgressDialog("Running","Cancel",0,0,self)
#         self.progress.setWindowTitle('Please wait...')
#         self.progress.setWindowModality(QtCore.Qt.WindowModal)
#         self.progress.canceled.connect(self.progress.close)
#         self.progress.setValue(1)
#         self.progress.show()
#
#         self.TT = Test_Thread()
#         self.TT.finished.connect(self.TT_Finished)
#         self.progress.canceled.connect(self.progress.close)
#         self.progress.setValue(1)
#         self.progress.show()
#         self.TT.start()
#
#     def TT_Finished(self):
#         self.progress.setLabelText("Analysis finished")
#         self.progress.setRange(0,1)
#         self.progress.setValue(1)
#         self.progress.setCancelButtonText("Close")
#         self.progress.canceled.connect(self.progress.close)
#
# class Test_Thread(QtCore.QThread):
#     finished = QtCore.pyqtSignal()
#
#     def __init__(self):
#         QtCore.QThread.__init__(self)
#
#     def run(self):
#         end = 10**20
#         start = 0
#
#         while start < end:
#             start += 1
#
#
#         self.finished.emit()
#         # self.terminate()
#
# if __name__=='__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     Test = TestDialog()
#     Test.show()
#     sys.exit(app.exec_())
#
