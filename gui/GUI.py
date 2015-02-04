#!/usr/bin/python

# Import PySide classes
import sys
sys.path.append('./src')
from PySide.QtCore import *
from PySide.QtGui import *
from MainWindow1 import *
from Models import *
from Sim import *

class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        self.count = 0

def setOpenFileName():
    parent = None
    filters = "All Files (*);;CSV (*.csv *.CSV)" # Only allow these file ext to be opened
    title = "Load a Program"
    open_at = "/home/"
    fileName = QtGui.QFileDialog.getOpenFileName(parent, title, open_at, filters)
    mySIM.collectData(fileName[0])
    return fileName

def goNext():
    LocalItem = progview.model.item(mySW.count)
    LocalItem.setBackground(QBrush(Qt.blue,Qt.FDiagPattern))
    progview.model.setItem(mySW.count, LocalItem)
    mySW.count += 1

def quitApp():
    app.quit()

def showProgram(checked):
    if(checked):    
        progmod.setContent()

def showRegisters(checked):
    if(checked):
        regmod.setContent()

def showMemory(checked):
    if(checked):
        memmod.setContent(mySIM.storage)

def showPipeline(checked):
    if(checked):
        pipemod.setContent()


if __name__ == "__main__":
    # general stuff
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySIM = Simulator()
    # construct and connect the models to the views
    progmod = ProgramModel(mySW.ui.programview)
    pipemod = PipelineModel(mySW.ui.pipeview)
    regmod = RegisterModel(mySW.ui.registerview)
    memmod = MemoryModel(mySW.ui.memoryview)
    # setup the initial content of the models
    progmod.setContentInitial()
    # connect the menu actions to the custom functions
    mySW.ui.action_LoadProgram.triggered.connect(setOpenFileName)
    mySW.ui.action_NextStep.triggered.connect(goNext)
    mySW.ui.action_ProgramView.toggled.connect(showProgram)
    mySW.ui.action_RegisterView.toggled.connect(showRegisters)
    mySW.ui.action_MemoryView.toggled.connect(showMemory)
    mySW.ui.action_PipelineView.toggled.connect(showPipeline)
    mySW.ui.action_ProgramView.setChecked(True)
    sys.exit(app.exec_())

