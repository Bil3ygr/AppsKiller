# coding: utf-8

import sys

from PyQt5 import QtCore, QtWidgets, QtGui

import common
import resources_rc
from mainwindow import MainWindow
from settings import SettingsDialog


def main():
    app = QtWidgets.QApplication(sys.argv)

    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)

    mainwindow = MainWindow()

    common.connectSignal(mainwindow)
    if common.getRunningOnStart():
        common.run()
    else:
        mainwindow.refreshTrayMenu()

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
