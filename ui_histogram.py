# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\lixinshui\Desktop\histogram.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_histogram(object):
    def setupUi(self, histogram):
        histogram.setObjectName("histogram")
        histogram.resize(400, 300)
        histogram.setMinimumSize(QtCore.QSize(0, 0))

        self.retranslateUi(histogram)
        QtCore.QMetaObject.connectSlotsByName(histogram)

    def retranslateUi(self, histogram):
        _translate = QtCore.QCoreApplication.translate
        histogram.setWindowTitle(_translate("histogram", "Dialog"))

