# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Dec  9 13:27:37 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuDLX_Sim_MainWindow = QtGui.QMenu(self.menubar)
        self.menuDLX_Sim_MainWindow.setObjectName("menuDLX_Sim_MainWindow")
        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuSimulator = QtGui.QMenu(self.menubar)
        self.menuSimulator.setObjectName("menuSimulator")
        self.menuPipeline = QtGui.QMenu(self.menubar)
        self.menuPipeline.setObjectName("menuPipeline")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.DW1 = QtGui.QDockWidget(MainWindow)
        self.DW1.setObjectName("DW1")
        self.DW1_Contents = QtGui.QListView(self.DW1)
        self.DW1_Contents.setGeometry(QtCore.QRect(0, 10, 401, 291))
        self.DW1_Contents.setGridSize(QtCore.QSize(0, 0))
        self.DW1_Contents.setUniformItemSizes(True)
        self.DW1_Contents.setSelectionRectVisible(True)
        self.DW1_Contents.setObjectName("listView")
        self.DW1.setWidget(self.DW1_Contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.DW1)

        self.actionProgramm_laden = QtGui.QAction(MainWindow)
        self.actionProgramm_laden.setObjectName("actionProgramm_laden")
        
        self.actionReset_DLX = QtGui.QAction(MainWindow)
        self.actionReset_DLX.setObjectName("actionReset_DLX")
        self.actionProgram = QtGui.QAction(MainWindow)
        self.actionProgram.setCheckable(True)
        self.actionProgram.setChecked(True)
        self.actionProgram.setObjectName("actionProgram")
        self.actionPipeline = QtGui.QAction(MainWindow)
        self.actionPipeline.setCheckable(True)
        self.actionPipeline.setChecked(True)
        self.actionPipeline.setObjectName("actionPipeline")
        self.actionMemory = QtGui.QAction(MainWindow)
        self.actionMemory.setCheckable(True)
        self.actionMemory.setObjectName("actionMemory")
        self.actionRegisters = QtGui.QAction(MainWindow)
        self.actionRegisters.setCheckable(True)
        self.actionRegisters.setChecked(True)
        self.actionRegisters.setObjectName("actionRegisters")
        self.actionNext_Step = QtGui.QAction(MainWindow)
        self.actionNext_Step.setObjectName("actionNext_Step")
        self.actionMore_Steps = QtGui.QAction(MainWindow)
        self.actionMore_Steps.setObjectName("actionMore_Steps")
        self.actionRun = QtGui.QAction(MainWindow)
        self.actionRun.setObjectName("actionRun")
        self.actionForwarding = QtGui.QAction(MainWindow)
        self.actionForwarding.setCheckable(True)
        self.actionForwarding.setObjectName("actionForwarding")
        self.actionMemory_Size = QtGui.QAction(MainWindow)
        self.actionMemory_Size.setObjectName("actionMemory_Size")
        self.actionStatistics = QtGui.QAction(MainWindow)
        self.actionStatistics.setCheckable(True)
        self.actionStatistics.setObjectName("actionStatistics")
        self.menuDLX_Sim_MainWindow.addAction(self.actionProgramm_laden)
        self.menuDLX_Sim_MainWindow.addAction(self.actionReset_DLX)
        self.menuWindow.addAction(self.actionProgram)
        self.menuWindow.addAction(self.actionPipeline)
        self.menuWindow.addAction(self.actionMemory)
        self.menuWindow.addAction(self.actionRegisters)
        self.menuWindow.addAction(self.actionStatistics)
        self.menuSimulator.addAction(self.actionNext_Step)
        self.menuSimulator.addAction(self.actionMore_Steps)
        self.menuSimulator.addAction(self.actionRun)
        self.menuPipeline.addAction(self.actionForwarding)
        self.menuPipeline.addAction(self.actionMemory_Size)
        self.menubar.addAction(self.menuDLX_Sim_MainWindow.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuSimulator.menuAction())
        self.menubar.addAction(self.menuPipeline.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDLX_Sim_MainWindow.setTitle(QtGui.QApplication.translate("MainWindow", "DLX_Sim", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Window", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSimulator.setTitle(QtGui.QApplication.translate("MainWindow", "Simulator", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPipeline.setTitle(QtGui.QApplication.translate("MainWindow", "DLX", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProgramm_laden.setText(QtGui.QApplication.translate("MainWindow", "Load Program", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset_DLX.setText(QtGui.QApplication.translate("MainWindow", "Reset DLX", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProgram.setText(QtGui.QApplication.translate("MainWindow", "Program", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPipeline.setText(QtGui.QApplication.translate("MainWindow", "Pipeline", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMemory.setText(QtGui.QApplication.translate("MainWindow", "Memory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRegisters.setText(QtGui.QApplication.translate("MainWindow", "Registers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNext_Step.setText(QtGui.QApplication.translate("MainWindow", "Next Step", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMore_Steps.setText(QtGui.QApplication.translate("MainWindow", "More Steps", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.actionForwarding.setText(QtGui.QApplication.translate("MainWindow", "Forwarding", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMemory_Size.setText(QtGui.QApplication.translate("MainWindow", "Memory Size", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStatistics.setText(QtGui.QApplication.translate("MainWindow", "Statistics", None, QtGui.QApplication.UnicodeUTF8))

    def setOpenFileName(self, parent):   
        filters = "All Files (*);;CSV (*.csv *.CSV)" # Only allow these file ext to be opened
        title = "Load a Program"
        open_at = "/home/"
        fileName = QtGui.QFileDialog.getOpenFileName(parent, title, open_at, filters)
        print(fileName)
