#!/usr/bin/python

import sys
from PySide import QtCore, QtGui
from bitstring import *

class Model():
    def __init__(self, model_of):    
        self.model = QtGui.QStandardItemModel(model_of)
        model_of.setModel(self.model)

class ProgramModel(Model):
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

class PipelineModel(Model):
    def __init__(self,model_of, pSim):
        self.model = QtGui.QGraphicsScene(model_of)
        model_of.setScene(self.model)
        self.Line_Height = 20
        self.Colm_Width = 40
        self.Pen = QtGui.QPen("black")
        self.Pen1 = QtGui.QPen(QtCore.Qt.DotLine)
        self.Font = QtGui.QFont("Helvetica")
        self.Font.setPointSize(11)
        self.Brush1 = QtGui.QBrush(QtGui.QColor(255,255,0), QtCore.Qt.SolidPattern)
        self.Brush2 = QtGui.QBrush(QtGui.QColor(255,174,0), QtCore.Qt.SolidPattern)
        self.Brush3 = QtGui.QBrush(QtGui.QColor(242,58,58), QtCore.Qt.SolidPattern)
        self.Brush4 = QtGui.QBrush(QtGui.QColor(82,69,255), QtCore.Qt.SolidPattern)
        self.Brush5 = QtGui.QBrush(QtGui.QColor(0,153,0), QtCore.Qt.SolidPattern)
        self.pSim = pSim
    def setContentInitial(self):
        self.model.addLine(0,0,0,400,self.Pen)
        self.model.addLine(150,0,150,400,self.Pen)
        self.model.addLine(0,0,190,0,self.Pen)
        self.model.addLine(0,25,190,25,self.Pen)
        self.model.addText("Command", self.Font)
    def updateContent(self):
        CurserX = 150 + self.Colm_Width * self.pSim.takt
        self.CommandIndex = (len(self.pSim.befehl) - 1)
        CurserY = 30 + self.Line_Height * self.CommandIndex
        # add the new content of the current turn
        # add the new command and number of the current clock cycle
        new_command = self.model.addText(self.pSim.befehl[self.CommandIndex])
        new_command.setY(CurserY)
        new_num = self.model.addText(str(self.pSim.takt),self.Font)
        new_num.setX(CurserX)
        # extend the two top lines
        self.model.addLine(CurserX + self.Colm_Width, 25, self.Colm_Width, 25, self.Pen)
        self.model.addLine(CurserX + self.Colm_Width, 0, self.Colm_Width, 0, self.Pen)
        # add the dotted clock cycle line
        self.model.addLine(CurserX + self.Colm_Width, 0, CurserX + self.Colm_Width, 400, self.Pen1)
        # add the rectangles

        if(self.pSim.zustand[0] != 0):
            idx = self.pSim.zustand[0]
            CurserY = 30 + self.Line_Height * idx
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush1)
            label = self.model.addText("IF")
            label.setX(CurserX)
            label.setY(CurserY)
        if(self.pSim.zustand[1] != 0):
            idx = self.pSim.zustand[1]
            CurserY = 30 + self.Line_Height * idx
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush2)
            label = self.model.addText("IF")
            label.setX(CurserX)
            label.setY(CurserY)
        if(self.pSim.zustand[2] != 0):
            idx = self.pSim.zustand[2]
            CurserY = 30 + self.Line_Height * idx
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush3)
            label = self.model.addText("IF")
            label.setX(CurserX)
            label.setY(CurserY)
        if(self.pSim.zustand[3] != 0):
            idx = self.pSim.zustand[3]
            CurserY = 30 + self.Line_Height * idx
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush4)
            label = self.model.addText("IF")
            label.setX(CurserX)
            label.setY(CurserY)
        if(pSim.zustand[4] != 0):
            idx = self.pSim.zustand[4]
            CurserY = 30 + self.Line_Height * idx
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush5)
            label = self.model.addText("IF")
            label.setX(CurserX)
            label.setY(CurserY)

class MemoryModel(Model):
    def setContent(self,storage):
        item = []
        x = 0
        # Create the first line        
        item.append( QtGui.QStandardItem("Adress\tWord") )
        # Add the item to the model
        self.model.appendRow(item[x])
        while x < storage.size/4:
            # Get item from storage
            word = BitArray(storage.getW(x*4))
            # Create an item
            item.append( QtGui.QStandardItem( repr(x*4) +"\t"+ word.hex) )
            # Add the item to the model
            self.model.appendRow(item[x])
            x += 1

class RegisterModel(Model):
    def setContentInitial(self,sim):
        self.item = []
        # Create the first line        
        self.item.append( QtGui.QStandardItem("Reg Name\tValue") )
        # Add all listed Registers
        for name in sim.pipe.piperegs:
            self.item.append( QtGui.QStandardItem( name +"\t"+ repr(sim.pipe.getPipeRegByName(name).getVal().int) ) )
        # Add the items to the model
        for i in range(0, len(self.item)-1):
            self.model.appendRow(self.item[i])
    def updateContent(self,sim):
        # Add the items to the model
        for i in range(1, self.item.length-1):
            self.model.setItem(i, self.item[i])

def StatisticsModel(Model):
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

