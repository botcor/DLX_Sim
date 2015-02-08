#!/usr/bin/python

# Import PySide classes
import sys
sys.path.append('./src')
from PySide.QtCore import *
from PySide.QtGui import *
from MainWindow1 import *
from Models import *
from Sim import *

class StubSim():
    Cycle = 0
    StallCnt = 0
    isStall = False
    CommandIndex = 0
    Commands = ["MOV A,B", "ADD R1,R2,R3", "SLL R1,1", "BLABLABLA", "Pause machen", "SUB R§,R$,R%", "NOP", "NOP", "NOP"]
    CommandState = ["IF","ID","EX","MEM","WB"]
    def NextStep(self,isStall):
        self.isStall = isStall
        if(self.isStall):
            self.Cycle += 1
            self.StallCnt += 1
        else:
            self.Cycle += 1
            self.CommandIndex += 1
    
