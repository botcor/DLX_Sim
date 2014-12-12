#!/usr/bin/python

import sys
from PySide import QtCore, QtGui

class View():
    def __init__(self):    
        self.view = QtGui.QListView()
        self.view.setGeometry(QtCore.QRect(0, 10, 401, 291))
        self.view.setUniformItemSizes(True)
        self.view.setSelectionRectVisible(True)
        self.model = QtGui.QStandardItemModel(self.view)
        self.view.setModel(self.model)

class ProgramView(View):
    def setContent(self):
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

class PipelineView(View):
    def setContent(self):
        # create an item with a caption
        item1 = QtGui.QStandardItem("Maybe show some rectangles")
        # Add the item to the model
        self.model.appendRow(item1)
        # create an item with a caption
        item2 = QtGui.QStandardItem("an the current instruction")
        # Add the item to the model
        self.model.appendRow(item2)
        # create an item with a caption
        item3 = QtGui.QStandardItem("in every single stage")
        # Add the item to the model
        self.model.appendRow(item3)
        # create an item with a caption
        item4 = QtGui.QStandardItem("if possible.")
        # Add the item to the model
        self.model.appendRow(item4)

class MemoryView(View):
    def setContent(self):
        # create an item with a caption
        item1 = QtGui.QStandardItem("adress, word")
        # Add the item to the model
        self.model.appendRow(item1)
        # create an item with a caption
        item2 = QtGui.QStandardItem("adress, word")
        # Add the item to the model
        self.model.appendRow(item2)
        # create an item with a caption
        item3 = QtGui.QStandardItem("adress, word")
        # Add the item to the model
        self.model.appendRow(item3)
        # create an item with a caption
        item4 = QtGui.QStandardItem("adress, word")
        # Add the item to the model
        self.model.appendRow(item4)

class RegisterView(View):
    def setContent(self):
        # create an item with a caption
        item1 = QtGui.QStandardItem("Some Registers")
        # Add the item to the model
        self.model.appendRow(item1)
        # create an item with a caption
        item2 = QtGui.QStandardItem("should be determined")
        # Add the item to the model
        self.model.appendRow(item2)
        # create an item with a caption
        item3 = QtGui.QStandardItem("by the Simulator")
        # Add the item to the model
        self.model.appendRow(item3)
        # create an item with a caption
        item4 = QtGui.QStandardItem("if possible.")
        # Add the item to the model
        self.model.appendRow(item4)

def showStatistics(View):
    def setContent(self):
        # create an item with a caption
        item1 = QtGui.QStandardItem("Show things like")
        # Add the item to the model
        self.model.appendRow(item1)
        # create an item with a caption
        item2 = QtGui.QStandardItem("MIPS")
        # Add the item to the model
        self.model.appendRow(item2)
        # create an item with a caption
        item3 = QtGui.QStandardItem("and amount of")
        # Add the item to the model
        self.model.appendRow(item3)
        # create an item with a caption
        item4 = QtGui.QStandardItem("load, store, alu instructions in %")
        # Add the item to the model
        self.model.appendRow(item4)

