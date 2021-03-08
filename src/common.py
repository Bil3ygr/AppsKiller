# coding: utf-8

import json
import os
import time
import traceback

from PyQt5 import QtGui, QtCore


g_ConfigData = {}
g_Runner = None


def getRunningOnStart():
    return g_ConfigData.get('AutoRun', False)


def setRunningOnStart(enable):
    g_ConfigData['AutoRun'] = enable
    writeJson()


def setAppInfos(apps):
    g_ConfigData['Apps'] = apps
    writeJson()


def getAppInfos():
    return g_ConfigData.get('Apps', [])


def getIcon():
    return QtGui.QIcon(':/icon/killer.png')


def readJson():
    global g_ConfigData
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            g_ConfigData = json.load(f)


def writeJson():
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(g_ConfigData, f, ensure_ascii=False, indent=4)


readJson()


def killApp(name):
    print('kill', name)


class Runner(QtCore.QObject):

    state_change_signal = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimeout)

        self.isRunning = False
        self.timeRecord = {}

    def onTimeout(self):
        current = time.time()
        for name, interval in getAppInfos():
            if interval:
                try:
                    _interval = int(interval)
                except:
                    traceback.print_exc()
                else:
                    if _interval:
                        if current - self.timeRecord[name] >= _interval:
                            killApp(name)
                            self.timeRecord[name] = current
                    else:
                        killApp(name)
            else:
                killApp(name)

    def start(self):
        if self.isRunning:
            return

        self.isRunning = True
        self.refreshInfos()
        self.timer.start()
        self.state_change_signal.emit(True)

    def stop(self):
        if not self.isRunning:
            return

        self.isRunning = False
        self.timeRecord = {}
        self.timer.stop()
        self.state_change_signal.emit(False)

    def refreshInfos(self):
        for name, _ in getAppInfos():
            if name not in self.timeRecord:
                self.timeRecord[name] = time.time()


def connectSignal(widget):
    global g_Runner
    if not g_Runner:
        g_Runner = Runner()
    g_Runner.state_change_signal.connect(widget.onRunningStateChanged)


def run():
    if g_Runner:
        g_Runner.start()


def stop():
    if g_Runner:
        g_Runner.stop()


def refreshTimerInfos():
    if g_Runner:
        g_Runner.refreshInfos()


def isRunning():
    if g_Runner:
        return g_Runner.isRunning
    else:
        return False
