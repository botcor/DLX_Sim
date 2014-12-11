#!/usr/bin/python     

# Import PySide classes
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from MainWindow import *
from Views import *

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
    pv.setProgram()
    return fileName

def goNext():
    LocalItem = pv.model.item(mySW.count)
    LocalItem.setBackground(QBrush(Qt.blue,Qt.FDiagPattern))
    pv.model.setItem(mySW.count, LocalItem)
    mySW.count += 1

def quitApp():
    app.quit()

def showProgram():
    mySW.ui.DW1 = QtGui.QDockWidget(mySW)
    mySW.ui.DW1.setObjectName("DW1")
    mySW.ui.DW1.setWidget(pv.view)
    mySW.addDockWidget(QtCore.Qt.DockWidgetArea(1), mySW.ui.DW1)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    pv = ProgramView()
    mySW.ui.action_LoadProgram.triggered.connect(setOpenFileName)
    mySW.ui.action_NextStep.triggered.connect(goNext)
    mySW.ui.action_ProgramView.triggered.connect(showProgram)
    sys.exit(app.exec_())

