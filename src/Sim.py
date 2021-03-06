import logging
from bitstring import *
from DLX_Speicher import *
from DLX_ALU import *
from DLX_Register import *
from DLX_Pipeline import *
from DLX_Translator import *


#create logger
mylogger = logging.getLogger("Simulator")

class Simulator:

    def __init__(self):
        mylogger.debug("Simulator wurde angelegt") 
        self.storage = DLX_Speicher()
        self.alu = DLX_ALU()
        self.regb = DLX_Reg_Bank()
        self.pipe = DLX_Pipeline(self.storage, self.alu, self.regb)
        self.state = [0,0,0,0,0]
        self.command = [0]
        self.programView = []
        self.cnt = 0
        self.cycle = 0
        self.fStall = False
        self.disassambly = DLX_Disassembly()
        self.newPC = 4096
        self.oldPC = 0
        

    def reset(self):
        self.pipe.reset()
        self.storage.reset()
        self.state = [0,0,0,0,0]
        self.command = [0]
        self.programView = []
        self.cnt = 0
        self.cycle = 0
        self.fStall = False
        self.newPC = 4096
        self.oldPC = 0

    def collectData(self, filename):
    
        p0 = BitArray(uint=0, length=32)
        p1 = BitArray(uint=0, length=32)
        p2 = BitArray(uint=0, length=32)
        p3 = BitArray(uint=0, length=32)
        datei = open(filename, "r")
        list = []
        x = 0
        adr=0
        for zeile in datei:
            list.append(zeile[:-1])
            x = x + 1

        for i in range(0,x):
            y = list[i]
        
            if y[0:8].isdigit():
                p0[0:8] = BitArray(hex=y[10:13])
                p0[8:16] = BitArray(hex=y[13:16])
                p0[16:24] = BitArray(hex=y[16:19])
                p0[24:32] = BitArray(hex=y[19:22])
                p1[0:8] = BitArray(hex=y[22:25])
                p1[8:16] = BitArray(hex= y[25:28])
                p1[16:24] = BitArray(hex=y[28:31])
                p1[24:32] = BitArray(hex=y[31:34])
                p2[0:8] = BitArray(hex=y[34:37])
                p2[8:16] = BitArray(hex=y[37:40])
                p2[16:24] = BitArray(hex=y[40:43])
                p2[24:32] = BitArray(hex=y[43:46])
                p3[0:8] = BitArray(hex=y[46:49])
                p3[8:16] = BitArray(hex=y[49:52])
                p3[16:24] = BitArray(hex=y[52:55])
                p3[24:32] = BitArray(hex=y[55:57])
   
                self.storage.setW((adr),p0)
                self.programView.append(self.disassambly.OperationToAsm(p0))
                adr = adr+4
                self.storage.setW(((adr)),p1)
                self.programView.append(self.disassambly.OperationToAsm(p1))
                adr = adr+4
                self.storage.setW(((adr)),p2)
                self.programView.append(self.disassambly.OperationToAsm(p2))
                adr = adr+4
                self.storage.setW(((adr)),p3)
                self.programView.append(self.disassambly.OperationToAsm(p3))
                adr = adr+4

        mylogger.debug("Funktion %s  Datei: %s wurde in den Speicher geschrieben", (inspect.stack()[0][3]), filename)

    def doPipe(self):
            self.pipe.doPipeNext()
            self.oldPC = self.newPC
            self.newPC = self.pipe.PC.getVal()
            if ((self.oldPC != self.newPC) & (((self.disassambly.OperationToAsm(self.pipe.insFIFO[0]))[0:3]) != "BAD")):
                self.command.append(self.disassambly.OperationToAsm(self.pipe.insFIFO[0]))
                if(len(self.command) == 2):
                    self.fStall = False
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[0]))[0:3]) == "BAD") | (self.pipe.insFIFO[0] == 0)):
                        self.state[0] = 0
                    else:
                        self.state[0] = (len(self.command) - 1)
                    self.cycle += 1
                elif(len(self.command) == 3):
                    self.fStall = False
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[0]))[0:3]) == "BAD") | (self.pipe.insFIFO[0] == 0)):
                        self.state[0] = 0
                    else:
                        self.state[0] = (len(self.command) - 1)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[1]))[0:3]) == "BAD") | (self.pipe.insFIFO[1] == 0)):
                        self.state[1] = 0
                    else:
                        self.state[1] = (len(self.command) - 2)
                    self.cycle += 1
                elif(len(self.command) == 4):
                    self.fStall = False
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[0]))[0:3]) == "BAD") | (self.pipe.insFIFO[0] == 0)):
                        self.state[0] = 0
                    else:
                        self.state[0] = (len(self.command) - 1)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[1]))[0:3]) == "BAD") | (self.pipe.insFIFO[1] == 0)):
                        self.state[1] = 0
                    else:
                        self.state[1] = (len(self.command) - 2)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[2]))[0:3]) == "BAD") | (self.pipe.insFIFO[2] == 0)):
                        self.state[2] = 0
                    else:
                        self.state[2] = (len(self.command) - 3)
                    self.cycle += 1
                elif(len(self.command) == 5):
                    self.fStall = False
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[0]))[0:3]) == "BAD") | (self.pipe.insFIFO[0] == 0)):
                        self.state[0] = 0
                    else:
                        self.state[0] = (len(self.command) - 1)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[1]))[0:3]) == "BAD") | (self.pipe.insFIFO[1] == 0)):
                        self.state[1] = 0
                    else:
                        self.state[1] = (len(self.command) - 2)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[2]))[0:3]) == "BAD") | (self.pipe.insFIFO[2] == 0)):
                        self.state[2] = 0
                    else:
                        self.state[2] = (len(self.command) - 3)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[3]))[0:3]) == "BAD") | (self.pipe.insFIFO[3] == 0)):
                        self.state[3] = 0
                    else:
                        self.state[3] = (len(self.command) - 4)
                    self.cycle += 1
                else:
                    self.fStall = False
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[0]))[0:3]) == "BAD") | (self.pipe.insFIFO[0] == 0)):
                        self.state[0] = 0
                    else:
                        self.state[0] = (len(self.command) - 1)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[1]))[0:3]) == "BAD") | (self.pipe.insFIFO[1] == 0)):
                        self.state[1] = 0
                    else:
                        self.state[1] = (len(self.command) - 2)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[2]))[0:3]) == "BAD") | (self.pipe.insFIFO[2] == 0)):
                        self.state[2] = 0
                    else:
                        self.state[2] = (len(self.command) - 3)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[3]))[0:3]) == "BAD") | (self.pipe.insFIFO[3] == 0)):
                        self.state[3] = 0
                    else:
                        self.state[3] = (len(self.command) - 4)
                    if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[4]))[0:3]) == "BAD") | (self.pipe.insFIFO[4] == 0)):
                        self.state[4] = 0
                    else:
                        self.state[4] = (len(self.command) - 5)
                    self.cycle += 1
            else:
                if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[0]))[0:3]) == "BAD") | (self.pipe.insFIFO[0] == 0)):
                        self.state[0] = 0
                else:
                        self.state[0] = (len(self.command) - 1)
                if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[1]))[0:3]) == "BAD") | (self.pipe.insFIFO[1] == 0)):
                        self.state[1] = 0
                else:
                        self.state[1] = (len(self.command) - 2)
                if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[2]))[0:3]) == "BAD") | (self.pipe.insFIFO[2] == 0)):
                        self.state[2] = 0
                else:
                        self.state[2] = (len(self.command) - 3)
                if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[3]))[0:3]) == "BAD") | (self.pipe.insFIFO[3] == 0)):
                        self.state[3] = 0
                else:
                        self.state[3] = (len(self.command) - 4)
                if ((((self.disassambly.OperationToAsm(self.pipe.insFIFO[4]))[0:3]) == "BAD") | (self.pipe.insFIFO[4] == 0)):
                        self.state[4] = 0
                else:
                        self.state[4] = (len(self.command) - 5)
                self.cycle += 1


