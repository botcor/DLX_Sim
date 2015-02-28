#!/usr/bin/python

import sys
from PySide import QtCore, QtGui
from bitstring import *

class Model():
    def __init__(self, model_of, pSim):    
        self.model = QtGui.QStandardItemModel(model_of)
        model_of.setModel(self.model)
        self.pSim = pSim
        self.items = []

class ProgramModel(Model):
    def setContentInitial(self):
        for instruction in self.pSim.programView:
            self.items.append(QtGui.QStandardItem(instruction))
        # Add the items to the model
        for i in range(0, len(self.items)-1):
            self.model.appendRow(self.items[i])
    def updateContent(self):
        self.items[int(self.pSim.oldPC.uint/4)].setBackground( QtGui.QBrush(QtGui.QColor(255,255,255), QtCore.Qt.SolidPattern) )
        self.items[int(self.pSim.newPC.uint/4)].setBackground( QtGui.QBrush(QtGui.QColor(255,255,0), QtCore.Qt.SolidPattern) )
        #update the model
        for i in range(0, len(self.items)-1):
            self.model.setItem(i ,self.items[i])
    def setBreakpoint(self, index):
        self.items[index].setBackground( QtGui.QBrush(QtGui.QColor(255,0,0), QtCore.Qt.SolidPattern) )
        self.model.setItem(index ,self.items[index])
        print('yes!')

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
        CurserX = 150 + self.Colm_Width * (self.pSim.cycle - 1)
        self.CommandIndex = (len(self.pSim.command) - 1)
        CurserY = 30 + self.Line_Height * self.CommandIndex
        gapCounter = 0
        # add the new content of the current turn
        # add the new command and number of the current clock cycle
        new_command = self.model.addText(str(self.pSim.command[self.CommandIndex]))
        new_command.setY(CurserY)
        new_num = self.model.addText(str(self.pSim.cycle),self.Font)
        new_num.setX(CurserX)
        # extend the two top lines
        self.model.addLine(CurserX + self.Colm_Width, 25, self.Colm_Width, 25, self.Pen)
        self.model.addLine(CurserX + self.Colm_Width, 0, self.Colm_Width, 0, self.Pen)
        # add the dotted clock cycle line
        self.model.addLine(CurserX + self.Colm_Width, 0, CurserX + self.Colm_Width, 400, self.Pen1)
        # add the rectangles

        if(self.pSim.state[0] != 0):
            idx = self.pSim.state[0]
            CurserY = 30 + self.Line_Height * (idx + gapCounter)
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush1)
            label = self.model.addText("IF")
            label.setX(CurserX)
            label.setY(CurserY)
        else:
            gapCounter += 1
        if(self.pSim.state[1] != 0):
            idx = self.pSim.state[1]
            CurserY = 30 + self.Line_Height * (idx + gapCounter)
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush2)
            label = self.model.addText("ID")
            label.setX(CurserX)
            label.setY(CurserY)
        else:
            gapCounter += 1
        if(self.pSim.state[2] != 0):
            idx = self.pSim.state[2]
            CurserY = 30 + self.Line_Height * (idx + gapCounter)
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush3)
            label = self.model.addText("EX")
            label.setX(CurserX)
            label.setY(CurserY)
        else:
            gapCounter += 1
        if(self.pSim.state[3] != 0):
            idx = self.pSim.state[3]
            CurserY = 30 + self.Line_Height * (idx + gapCounter)
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush4)
            label = self.model.addText("MEM")
            label.setX(CurserX)
            label.setY(CurserY)
        else:
            gapCounter += 1
        if(self.pSim.state[4] != 0):
            idx = self.pSim.state[4]
            CurserY = 30 + self.Line_Height * (idx + gapCounter)
            self.model.addRect(CurserX, CurserY, self.Colm_Width, self.Line_Height, self.Pen, self.Brush5)
            label = self.model.addText("WB")
            label.setX(CurserX)
            label.setY(CurserY)
        else:
            gapCounter += 1

class MemoryModel(Model):
    def setContentInitial(self):
        x = 0
        # Create the first line        
        self.items.append( QtGui.QStandardItem("Adress\tWord") )
        # Add the item to the model
        self.model.appendRow(self.items[x])
        while x < self.pSim.storage.size/4:
            # Get item from storage
            word = BitArray(self.pSim.storage.getW(x*4))
            # Create an item
            self.items.append( QtGui.QStandardItem( repr(x*4) +"\t"+ word.hex) )
            # Add the item to the model
            self.model.appendRow(self.items[x])
            x += 1
    def updateContent(self):
        self.items = []
        x = 0
        # Create the first line        
        self.items.append( QtGui.QStandardItem("Adress\tWord") )
        # Add the item to the model
        self.model.setItem(x, self.items[x])
        while x < self.pSim.storage.size/4:
            # Get item from storage
            word = BitArray(self.pSim.storage.getW(x*4))
            self.items.append( QtGui.QStandardItem( repr(x*4) +"\t"+ word.hex) )
            x += 1
        # Add the items to the model
        for i in range(1, len(self.items)-1):
            self.model.setItem(i, self.items[i])

class RegisterModel(Model):
    def setContentInitial(self):
        # Create the first line        
        self.items.append( QtGui.QStandardItem("Reg Name\tValue") )
        # Add all listed Registers
        for name in self.pSim.pipe.piperegs:
            self.items.append( QtGui.QStandardItem( name +"\t"+ repr(self.pSim.pipe.getPipeRegByName(name).getVal().int) ) )
        for i in range(0,31):
            self.items.append( QtGui.QStandardItem( self.pSim.pipe.regbank.getRegByID(i).getName() +"\t"+ repr(self.pSim.pipe.regbank.getRegByID(i).getVal().int) ) )
        # Add the items to the model
        for i in range(0, len(self.items)-1):
            self.model.appendRow(self.items[i])
    def updateContent(self):
        for name in self.pSim.pipe.piperegs:
            self.items[self.pSim.pipe.piperegs.index(name) +1] = QtGui.QStandardItem( name +"\t"+ repr(self.pSim.pipe.getPipeRegByName(name).getVal().int) )
        for i in range(0,31):
            self.items[len(self.pSim.pipe.piperegs)+i] = QtGui.QStandardItem( self.pSim.pipe.regbank.getRegByID(i).getName() +"\t"+ repr(self.pSim.pipe.regbank.getRegByID(i).getVal().int) )
        # Add the items to the model
        for i in range(1, len(self.items)-1):
            self.model.setItem(i, self.items[i])

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

