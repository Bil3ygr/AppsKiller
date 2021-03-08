# coding: utf-8

from PyQt5 import QtCore, QtGui, QtWidgets

import common
from settings import SettingsDialog


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.trayIconMenu = QtWidgets.QMenu(self)
        self.settingsDialog = None

        self.addTrayAction()
        self.addTrayIcon()

    def addTrayAction(self):
        self.startAction = QtWidgets.QAction(
            "Run", self, triggered=self.runKiller)
        self.stopAction = QtWidgets.QAction(
            "Stop", self, triggered=self.stopKiller)
        self.settingAction = QtWidgets.QAction(
            "Settings", self, triggered=self.showSettingsDialog)
        self.quitAction = QtWidgets.QAction(
            "Quit", self, triggered=QtWidgets.QApplication.instance().quit)

    def refreshTrayMenu(self):
        self.trayIconMenu.clear()

        if common.isRunning():
            self.trayIconMenu.addAction(self.stopAction)
        else:
            self.trayIconMenu.addAction(self.startAction)
        self.trayIconMenu.addAction(self.settingAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

    def addTrayIcon(self):
        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(common.getIcon())
        self.trayIcon.show()

    def runKiller(self):
        common.run()
        self.refreshTrayMenu()

    def stopKiller(self):
        common.stop()
        self.refreshTrayMenu()

    def showSettingsDialog(self):
        if self.settingsDialog:
            return

        self.settingsDialog = SettingsDialog()
        self.settingsDialog.finished.connect(self.onSettingsDialogFinished)
        self.settingsDialog.show()

    def onSettingsDialogFinished(self, result):
        self.settingsDialog = None

    def onRunningStateChanged(self):
        self.refreshTrayMenu()
