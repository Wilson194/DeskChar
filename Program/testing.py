# !/usr/bin/python3
# -*- coding: utf-8 -*-

# from PIL import Image
# from os import mkdir
#
# sheet = Image.open("resources/icons/image-tango-feet.png")
# count = 0
#
# for x in range(26):
#     for y in range(10):
#         a = ((x + 1) * 30) + 48
#         b = ((y + 1) * 30) + 424
#         icon = sheet.crop((a - 25, b - 25, a, b))  # Problem here
#         icon.save("resources/icons/{}.png".format(count))
#         count += 1


# from structure.enums.Classes import Classes
#
# print(Classes.ALCHEMIST)



"""
ZetCode PyQt5 tutorial

In this example, we receive data from
a QInputDialog dialog.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys
import sip
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QTextEdit,
                             QInputDialog, QApplication)

from PyQt5 import QtCore

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        QtCore.
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QTextEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()


    def showDialog(self):
        sip.setapi('QString', 2)
        self.le.insertPlainText('pppppéčpppp')

        print(type(self.le.toPlainText()))


if __name__ == '__main__':
    sip.setapi('QString',2)
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())