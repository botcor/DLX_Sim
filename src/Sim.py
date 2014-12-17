import logging
from bitstring import *
from DLX_Speicher import *
from DLX_ALU import *
from DLX_Register import *
from DLX_Pipeline import *
# DLX_Translator import *

#create logger
mylogger = logging.getLogger("Simulator")

class Simulator:

    def __init__(self):
        mylogger.debug("Simulator wurde angelegt") 
        self.storage = DLX_Speicher()
        #self.trans = DLX_Translator()
        self.alu = DLX_ALU()
        self.regb = DLX_Reg_Bank()
        self.pipe = DLX_Pipeline(self.storage, self.alu, self.regb)



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
                adr = adr+4
                self.storage.setW(((adr)),p1)
                adr = adr+4
                self.storage.setW(((adr)),p2)
                adr = adr+4
                self.storage.setW(((adr)),p3)
                adr = adr+4

        mylogger.debug("Funktion %s  Datei: %s wurde in den Speicher geschrieben", (inspect.stack()[0][3]), filename)
            
   


