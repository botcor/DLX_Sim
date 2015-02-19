import logging
from bitstring import *

#create logger
mylogger = logging.getLogger("Speicher")

class DLX_Speicher:
    storage = []
    size = 2048
    def __init__(self, size=2048):
        mylogger.debug("DLX_Speicher wurde angelegt")
        x =  BitArray(uint=0, length=8)
        for i in range(0, size):
            self.storage.append(x)
            
    def reset(self):
        mylogger.debug("Speicher wurde zurueckgesetzt")
        for i in range(0, self.size):
            self.storage[i] = BitArray(uint=0, length=8)
                
    def setB(self, adr, value):
        self.storage[adr] = value

    def setHW(self, adr, value):
        if adr % 2 == 0:
            self.storage[adr] = value[0:8]
            self.storage[adr +1] = value[8:16]

    def setW(self, adr, value):
        if adr % 4 == 0:
            self.storage[adr] = value[0:8]
            self.storage[adr +1] = value[8:16]
            self.storage[adr +2] = value[16:24]
            self.storage[adr +3] = value[24:32]

    def getB(self, adr):
        return self.storage[adr]

    def getHW(self,adr):
        if adr % 2 == 0:
            x = BitArray(uint=0, length=16)
            x[0:8] = self.storage[adr]
            x[8:16] = self.storage[adr +1]
            return x

    def getW(self, adr):
        if adr % 4 == 0:
            x = BitArray(uint=0, length=32)
            x[0:8] = self.storage[adr]
            x[8:16] = self.storage[adr +1]
            x[16:24] = self.storage[adr +2]
            x[24:32] = self.storage[adr +3]
            return x
