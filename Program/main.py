#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from presentation.main import *
from data.database.DatabaseTables import *
import sys


if __name__ == '__main__':
    DatabaseTables().create_tables()
    app = QApplication([])

    main_window = MainWindow()


    sys.exit(app.exec_())
