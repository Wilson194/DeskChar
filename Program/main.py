#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This is a Tetris game clone.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from presentation.main import *


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()

    translator = QtCore.QTranslator()
    translator.load("resources/translate/main_CS.qm")
    app.installTranslator(translator)

    print('Localization loaded: '
          , translator.load('main_CS.qm',
                            'resources/translate'))  # name, dir

    print(app.tr('Apple'))

    sys.exit(app.exec_())
