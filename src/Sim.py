import logging
from bitstring import *
from DLX_Speicher import *
from DLX_Translator import *

storage = DLX_Speicher()
trans = DLX_Translator
def collectData(filename):
    
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
    #print(list)
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
            print(p0)
            print(p1)
            print(p2)
            print(p3)
            storage.setW((adr*4),p0)
            storage.setW(((adr*4) + 4),p1)
            storage.setW(((adr*4) + 8),p2)
            storage.setW(((adr*4) + 12),p3)
            
   
collectData("Bubble.dlx")

