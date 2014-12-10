# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'program.ui'
#
# Created: Tue Dec  9 22:05:53 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Program(object):
    def setupUi(self, Program):
        Program.setObjectName("Program")
        Program.resize(400, 300)
        self.listView = QtGui.QListView(Program)
        self.listView.setGeometry(QtCore.QRect(0, 10, 401, 291))
        self.listView.setGridSize(QtCore.QSize(0, 0))
        self.listView.setUniformItemSizes(True)
        self.listView.setSelectionRectVisible(True)
        self.listView.setObjectName("listView")

        self.retranslateUi(Program)
        QtCore.QMetaObject.connectSlotsByName(Program)

    def retranslateUi(self, Program):
        Program.setWindowTitle(QtGui.QApplication.translate("Program", "Form", None, QtGui.QApplication.UnicodeUTF8))

