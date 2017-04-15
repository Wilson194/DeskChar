#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication

from data.DAO.LangDAO import LangDAO
from presentation.main import MainWindow
from data.database.DatabaseTables import DatabaseTables
import sys

from structure.general.Lang import Lang


if __name__ == '__main__':
    DatabaseTables().create_tables()


    app = QApplication([])
    app.processEvents()

    main_window = MainWindow()

    sys.exit(app.exec_())
