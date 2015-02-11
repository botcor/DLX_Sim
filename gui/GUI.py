#!/usr/bin/python

# Import PySide classes
import sys
sys.path.append('./src')
sys.path.append('./test')
from Stubs import *
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

def Reset():
    # construct and connect the models to the views
    progmod = ProgramModel(mySW.ui.programview)
    pipemod = PipelineModel(mySW.ui.pipeview, myStubSIM)
    regmod = RegisterModel(mySW.ui.registerview)
    memmod = MemoryModel(mySW.ui.memoryview)
    # setup the initial content of the models
    pipemod.setContentInitial()
    # actually reset the DLX

def goNext():
    myStubSIM.NextStep(False)
    pipemod.setContent()

def goMore():
    num_steps = QtGui.QInputDialog.getInt( mySW, "Prompt", "Please insert a Number:", 2)

def Run():
    myStubSIM.NextStep(True)
    pipemod.setContent()

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

def changeMemSize():
    new_size = QtGui.QInputDialog.getInt( mySW, "Prompt", "Please insert the new size:", mySIM.pipeline.storage.size)
    #mySIM.pipeline.storage.size = ne_size

def switchFWD(checked):
    

if __name__ == "__main__":
    # general stuff
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySIM = Simulator()
    myStubSIM = StubSim()
    # construct and connect the models to the views
    progmod = ProgramModel(mySW.ui.programview)
    pipemod = PipelineModel(mySW.ui.pipeview, myStubSIM)
    regmod = RegisterModel(mySW.ui.registerview)
    memmod = MemoryModel(mySW.ui.memoryview)
    # setup the initial content of the models
    pipemod.setContentInitial()
    # connect the menu actions to the custom functions
    mySW.ui.action_LoadProgram.triggered.connect(setOpenFileName)
    mySW.ui.action_ResetDLX.triggered.connect(Reset)
    mySW.ui.action_NextStep.triggered.connect(goNext)
    mySW.ui.action_MoreSteps.triggered.connect(goMore)
    mySW.ui.action_Run.triggered.connect(Run)
    mySW.ui.action_ProgramView.toggled.connect(showProgram)
    mySW.ui.action_RegisterView.toggled.connect(showRegisters)
    mySW.ui.action_MemoryView.toggled.connect(showMemory)
    mySW.ui.action_PipelineView.toggled.connect(showPipeline)
    mySW.ui.action_ProgramView.setChecked(True)
    sys.exit(app.exec_())

