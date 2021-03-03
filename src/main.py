# coding: utf-8

import sys

from PyQt5 import QtCore, QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.quitAction = QtCore.QAction(
            "&Quit", self, triggered=QtWidgets.QApplication.instance().quit)

        self.trayIconMenu = QtWidgets.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        icon = QtGui.QIcon('res/icons8-close-sign-100.ico')

        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(icon)
        self.trayIcon.show()

        self.setWindowIcon(icon)


def main():
    app = QtWidgets.QApplication(sys.argv)

    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)

    mainwindow = QtWidgets.QMainWindow()
    mainwindow.show()

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
