# coding: utf-8


from PyQt5 import QtWidgets, QtCore, QtGui

import common


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowIcon(common.getIcon())
        self.resize(600, 300)

        self.vLayout = QtWidgets.QVBoxLayout()

        self.checkbox = QtWidgets.QCheckBox("Running on start")
        self.checkbox.setChecked(common.getRunningOnStart())
        self.checkbox.toggled.connect(self.onRunningOnStartChanged)
        self.vLayout.addWidget(self.checkbox)

        self.treeWidget = QtWidgets.QTreeWidget()
        header = self.treeWidget.headerItem()
        header.setText(0, 'Name')
        header.setText(1, 'Interval')
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setColumnWidth(0, 150)
        self.vLayout.addWidget(self.treeWidget)

        self.hLayout = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QToolButton()
        self.addButton.setIcon(QtGui.QIcon(':icon/add.png'))
        self.addButton.clicked.connect(self.onAddClicked)
        self.hLayout.addWidget(self.addButton)
        self.delButton = QtWidgets.QToolButton()
        self.delButton.setIcon(QtGui.QIcon(':icon/del.png'))
        self.delButton.clicked.connect(self.onDelClicked)
        self.hLayout.addWidget(self.delButton)
        self.hLayout.addStretch()
        self.runButton = QtWidgets.QToolButton()
        self.runButton.clicked.connect(self.onRunClicked)
        self.hLayout.addWidget(self.runButton)
        self.vLayout.addLayout(self.hLayout)
        self.setLayout(self.vLayout)

        self.initAppInfos()
        self.refreshRunButtonIcon()
        self.addEmptyItem()

        self.treeWidget.itemChanged.connect(self.onItemChanged)

        common.connectSignal(self)

    def initAppInfos(self):
        infos = common.getAppInfos()
        for name, interval in infos:
            widgetItem = self.addEmptyItem(True)
            widgetItem.setText(0, name)
            widgetItem.setText(1, interval)

        self.refreshDelButtonState()

    def refreshRunButtonIcon(self):
        if common.isRunning():
            self.runButton.setIcon(QtGui.QIcon(':icon/stop.png'))
        else:
            self.runButton.setIcon(QtGui.QIcon(':icon/play.png'))

    def addEmptyItem(self, selectable=False):
        widgetItem = QtWidgets.QTreeWidgetItem(self.treeWidget)
        flags = QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        if selectable:
            flags |= QtCore.Qt.ItemIsSelectable
        widgetItem.setFlags(flags)
        return widgetItem

    def itemSelectable(self, widgetItem):
        return widgetItem.flags() & QtCore.Qt.ItemIsSelectable

    def refreshDelButtonState(self):
        self.delButton.setEnabled(self.treeWidget.topLevelItemCount() > 1)

    def onRunningOnStartChanged(self, checked):
        common.setRunningOnStart(checked)

    def onItemChanged(self, widgetItem, column):
        appName = widgetItem.text(0)
        appName = appName.strip()
        if appName:
            if not self.itemSelectable(widgetItem):
                index = self.treeWidget.indexOfTopLevelItem(widgetItem)
                self.treeWidget.takeTopLevelItem(index)
                newWidgetItem = self.addEmptyItem(True)
                newWidgetItem.setText(0, widgetItem.text(0))
                newWidgetItem.setText(1, widgetItem.text(1))
                self.treeWidget.insertTopLevelItem(index, newWidgetItem)

            lastWidgetItem = self.treeWidget.topLevelItem(self.treeWidget.topLevelItemCount() - 1)
            if self.itemSelectable(lastWidgetItem):
                self.addEmptyItem()

            self.setAppInfos()
        else:
            index = self.treeWidget.indexOfTopLevelItem(widgetItem)
            if index != self.treeWidget.topLevelItemCount() - 1:
                self.treeWidget.takeTopLevelItem(index)
                self.setAppInfos()

        self.refreshDelButtonState()

    def onAddClicked(self):
        count = self.treeWidget.topLevelItemCount()
        widgetItem = self.treeWidget.topLevelItem(count - 1)
        self.treeWidget.editItem(widgetItem)

    def onDelClicked(self):
        widgetItem = self.treeWidget.currentItem()
        if widgetItem:
            index = self.treeWidget.indexOfTopLevelItem(widgetItem)
            self.treeWidget.takeTopLevelItem(index)
            self.setAppInfos()

    def setAppInfos(self):
        apps = []
        for index in range(self.treeWidget.topLevelItemCount() - 1):
            widgetItem = self.treeWidget.topLevelItem(index)
            apps.append((widgetItem.text(0), widgetItem.text(1)))

        common.setAppInfos(apps)

    def onRunClicked(self):
        if common.isRunning():
            common.stop()
        else:
            common.run()
        self.refreshRunButtonIcon()

    def onRunningStateChanged(self):
        self.refreshRunButtonIcon()
