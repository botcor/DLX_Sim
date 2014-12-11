#!/usr/bin/python

import sys
from PySide import QtCore, QtGui

class ProgramView():
    def __init__(self):    
        self.view = QtGui.QListView()
        self.view.setObjectName("Program View")
        self.view.setGeometry(QtCore.QRect(0, 10, 401, 291))
        self.view.setUniformItemSizes(True)
        self.view.setSelectionRectVisible(True)
        self.model = QtGui.QStandardItemModel(self.view)
        self.view.setModel(self.model)

    def setProgram(self):
        # create an item with a caption
        item1 = QtGui.QStandardItem("Item in the Model. 1")
        # Add the item to the model
        self.model.appendRow(item1)
        # create an item with a caption
        item2 = QtGui.QStandardItem("Item in the Model. 2")
        # Add the item to the model
        self.model.appendRow(item2)
        # create an item with a caption
        item3 = QtGui.QStandardItem("Item in the Model. 3")
        # Add the item to the model
        self.model.appendRow(item3)
        # create an item with a caption
        item4 = QtGui.QStandardItem("Item in the Model. 4")
        # Add the item to the model
        self.model.appendRow(item4)

def showPipeline():
    mySW.ui.DW1 = QtGui.QDockWidget(mySW)
    mySW.ui.DW1.setObjectName("DW1")
    mySW.ui.DW1.setWidget(mySW.ui.ProgramView)

def showMemory():
    mySW.ui.DW1 = QtGui.QDockWidget(mySW)
    mySW.ui.DW1.setObjectName("DW1")
    mySW.ui.DW1.setWidget(mySW.ui.ProgramView)

def showRegisters():
    mySW.ui.DW1 = QtGui.QDockWidget(mySW)
    mySW.ui.DW1.setObjectName("DW1")
    mySW.ui.DW1.setWidget(mySW.ui.ProgramView)

def showStatistics():
    mySW.ui.DW1 = QtGui.QDockWidget(mySW)
    mySW.ui.DW1.setObjectName("DW1")
    mySW.ui.DW1.setWidget(mySW.ui.ProgramView)

