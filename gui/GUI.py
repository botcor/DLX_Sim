#!/usr/bin/python

# Import PySide classes
import sys
sys.path.append('./src')
sys.path.append('./test')
import logging
from PySide.QtCore import *
from PySide.QtGui import *
from MainWindow import *
from Models import *
from Sim import *

#create logger
mylogger = logging.getLogger("Pipeline")

class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        self.count = 0

def OpenFile():
    parent = myMW
    filters = "DLX (*.dlx)" # Only allow these file ext to be opened
    title = "Load a Program"
    open_at = "/home/"
    fileName = QtGui.QFileDialog.getOpenFileName(parent, title, open_at, filters)
    mySIM.collectData(fileName[0])
    memmod.updateContent()
    progmod.setContentInitial()

def goNext():
    mySIM.doPipe(1)
    pipemod.updateContent()
    regmod.updateContent()
    progmod.updateContent()

def goMore():
    num_steps = QtGui.QInputDialog.getInt( myMW, "Prompt", "Please insert a Number:", 2)
    for i in range (0,num_steps[0]):
        mySIM.doPipe(1)
        pipemod.updateContent()
        regmod.updateContent()
        progmod.updateContent()

def Run():
    #myStubSIM.NextStep(True)
    pipemod.updateContent()

def changeMemSize():
    new_size = QtGui.QInputDialog.getInt( myMW, "Prompt", "Please insert the new memory size:", mySIM.pipe.storage.size)
    #mySIM.pipeline.storage.size = new_size

def switchFWD(checked):
    reset()
    if(checked == True):
        mySIM.pipe.fForwarding = True
    else:
        mySIM.pipe.fForwarding = False
    mylogger.debug("Forwarding is %s", mySIM.pipe.fForwarding)

def reset():
    dialog = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Question", "Do you really want to reset the DLX?", QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel, myMW, 0)
    answer = dialog.exec()
    print(answer)
    if(answer == 1024):
        # actually reset the DLX
        mySIM.pipe.reset()
        mySIM.storage.reset()
        # construct and connect the models to the views
        progmod = ProgramModel(myMW.ui.programview, mySIM)
        pipemod = PipelineModel(myMW.ui.pipeview, mySIM)
        regmod = RegisterModel(myMW.ui.registerview, mySIM)
        memmod = MemoryModel(myMW.ui.memoryview, mySIM)
        # setup the initial content of the models
        pipemod.setContentInitial()
        regmod.setContentInitial()
        memmod.setContentInitial()

def quitApp():
    app.quit()

if __name__ == "__main__":
    # general stuff
    app = QtGui.QApplication(sys.argv)
    myMW = ControlMainWindow()
    myMW.show()
    mySIM = Simulator()
    # construct and connect the models to the views
    progmod = ProgramModel(myMW.ui.programview, mySIM)
    pipemod = PipelineModel(myMW.ui.pipeview, mySIM)
    regmod = RegisterModel(myMW.ui.registerview, mySIM)
    memmod = MemoryModel(myMW.ui.memoryview, mySIM)
    # setup the initial content of the models
    pipemod.setContentInitial()
    regmod.setContentInitial()
    memmod.setContentInitial()
    # connect the menu actions to the custom functions
    myMW.ui.action_LoadProgram.triggered.connect(OpenFile)
    myMW.ui.action_ResetDLX.triggered.connect(reset)
    myMW.ui.action_NextStep.triggered.connect(goNext)
    myMW.ui.action_MoreSteps.triggered.connect(goMore)
    myMW.ui.action_Run.triggered.connect(Run)
    myMW.ui.action_Forwarding.toggled.connect(switchFWD)
    myMW.ui.action_MemorySize.triggered.connect(changeMemSize)
    sys.exit(app.exec_())

