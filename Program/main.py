#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from presentation.main import *
from database.DatabaseTables import *


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()

    DatabaseTables().create_tables()



    sys.exit(app.exec_())
