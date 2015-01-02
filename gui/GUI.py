#!/usr/bin/python

# Import PySide classes
import sys
sys.path.append('./src')
from PySide.QtCore import *
from PySide.QtGui import *
from MainWindow import *
from Views import *
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
        progview.setContent()
        mySW.ui.DW1 = QtGui.QDockWidget(mySW)
        mySW.ui.DW1.setObjectName("DW1")
        mySW.ui.DW1.setWidget(progview.view)
        mySW.addDockWidget(QtCore.Qt.DockWidgetArea(1), mySW.ui.DW1)

def showRegisters(checked):
    if(checked):    
        regview.setContent()
        mySW.ui.DW2 = QtGui.QDockWidget(mySW)
        mySW.ui.DW2.setObjectName("DW2")
        mySW.ui.DW2.setWidget(regview.view)
        mySW.addDockWidget(QtCore.Qt.DockWidgetArea(2), mySW.ui.DW2)

def showMemory(checked):
    if(checked):
        memview.setContent(mySIM.storage)
        mySW.ui.DW3 = QtGui.QDockWidget(mySW)
        mySW.ui.DW3.setObjectName("DW3")
        mySW.ui.DW3.setWidget(memview.view)
        mySW.addDockWidget(QtCore.Qt.DockWidgetArea(1), mySW.ui.DW3)

def showPipeline(checked):
    if(checked):
        pipeview.setContent()
        mySW.ui.DW4 = QtGui.QDockWidget(mySW)
        mySW.ui.DW4.setObjectName("DW4")
        mySW.ui.DW4.setWidget(pipeview.view)
        mySW.addDockWidget(QtCore.Qt.DockWidgetArea(1), mySW.ui.DW4)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    mySIM = Simulator()
    progview = ProgramView()
    regview = RegisterView()
    memview = MemoryView()
    pipeview = PipelineView()
    mySW.ui.action_LoadProgram.triggered.connect(setOpenFileName)
    mySW.ui.action_NextStep.triggered.connect(goNext)
    mySW.ui.action_ProgramView.toggled.connect(showProgram)
    mySW.ui.action_RegisterView.toggled.connect(showRegisters)
    mySW.ui.action_MemoryView.toggled.connect(showMemory)
    mySW.ui.action_PipelineView.toggled.connect(showPipeline)
    mySW.ui.action_ProgramView.setChecked(True)
    sys.exit(app.exec_())

