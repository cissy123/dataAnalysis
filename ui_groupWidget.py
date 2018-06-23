# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\dataAnalysis_py\groupWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_groupWidget(object):
    def setupUi(self, groupWidget):
        groupWidget.setObjectName("groupWidget")
        groupWidget.resize(400, 332)
        self.buttonBox = QtWidgets.QDialogButtonBox(groupWidget)
        self.buttonBox.setGeometry(QtCore.QRect(30, 270, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(groupWidget)
        self.widget.setGeometry(QtCore.QRect(10, 0, 321, 251))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tw_same = QtWidgets.QTreeWidget(self.widget)
        self.tw_same.setObjectName("tw_same")
        self.horizontalLayout.addWidget(self.tw_same)
        self.tw_diff = QtWidgets.QTreeWidget(self.widget)
        self.tw_diff.setObjectName("tw_diff")
        self.horizontalLayout.addWidget(self.tw_diff)

        self.retranslateUi(groupWidget)
        self.buttonBox.accepted.connect(groupWidget.accept)
        self.buttonBox.rejected.connect(groupWidget.reject)
        QtCore.QMetaObject.connectSlotsByName(groupWidget)

    def retranslateUi(self, groupWidget):
        _translate = QtCore.QCoreApplication.translate
        groupWidget.setWindowTitle(_translate("groupWidget", "Dialog"))
        self.tw_same.headerItem().setText(0, _translate("groupWidget", "sameGroup"))
        self.tw_diff.headerItem().setText(0, _translate("groupWidget", "differentGroup"))

