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
    memmod.updateContent()
    return fileName

def goNext():
    mySIM.doPipe(1)
    pipemod.updateContent()
    regmod.updateContent()

def goMore():
    num_steps = QtGui.QInputDialog.getInt( mySW, "Prompt", "Please insert a Number:", 2)
    for i in range (1,num_steps[0]):
        mySIM.doPipe(1)
        pipemod.updateContent()
        regmod.updateContent()

def Run():
    #myStubSIM.NextStep(True)
    pipemod.updateContent()

def quitApp():
    app.quit()

def changeMemSize():
    new_size = QtGui.QInputDialog.getInt( mySW, "Prompt", "Please insert the new memory size:", mySIM.pipe.storage.size)
    #mySIM.pipeline.storage.size = new_size

def switchFWD(checked):
    dialog = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Info", "The DLX will be reset", QtGui.QMessageBox.Ok, mySW, 0)
    answer = dialog.exec()
    print(answer)
    if(checked == True):
        mySIM.pipe.fForwarding = True
    else:
        mySIM.pipe.fForwarding = False
    print(mySIM.pipe.fForwarding)

def Reset():
    dialog = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Question", "Do you really want to reset the DLX?", QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel, mySW, 0)
    answer = dialog.exec()
    print(answer)
    if(answer == 1024):
        # actually reset the DLX
        mySIM.pipe.ResetPipeline()
        mySIM.storage.reset()
        # construct and connect the models to the views
        progmod = ProgramModel(mySW.ui.programview, mySIM)
        pipemod = PipelineModel(mySW.ui.pipeview, mySIM)
        regmod = RegisterModel(mySW.ui.registerview, mySIM)
        memmod = MemoryModel(mySW.ui.memoryview, mySIM)
        # setup the initial content of the models
        pipemod.setContentInitial()
        regmod.setContentInitial()
        memmod.setContentInitial()

if __name__ == "__main__":
    # general stuff
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySIM = Simulator()
    # construct and connect the models to the views
    progmod = ProgramModel(mySW.ui.programview, mySIM)
    pipemod = PipelineModel(mySW.ui.pipeview, mySIM)
    regmod = RegisterModel(mySW.ui.registerview, mySIM)
    memmod = MemoryModel(mySW.ui.memoryview, mySIM)
    # setup the initial content of the models
    pipemod.setContentInitial()
    regmod.setContentInitial()
    memmod.setContentInitial()
    # connect the menu actions to the custom functions
    mySW.ui.action_LoadProgram.triggered.connect(setOpenFileName)
    mySW.ui.action_ResetDLX.triggered.connect(Reset)
    mySW.ui.action_NextStep.triggered.connect(goNext)
    mySW.ui.action_MoreSteps.triggered.connect(goMore)
    mySW.ui.action_Run.triggered.connect(Run)
    mySW.ui.action_Forwarding.toggled.connect(switchFWD)
    mySW.ui.action_MemorySize.triggered.connect(changeMemSize)
    sys.exit(app.exec_())

