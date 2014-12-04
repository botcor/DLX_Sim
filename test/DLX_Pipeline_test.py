#!/usr/bin/env python
#
# translator.py
# Name: DLX Pipeline
# Author: Cornelius Bott
# Date: 19.10.2014
# Brief: Contains the entire DLX-Pipeline Registers and Functions
# 
# History:
#
import sys
sys.path.append('../src')

from bitstring import *
from DLX_Pipeline import DLX_Pipeline
from DLX_Speicher import DLX_Speicher
from DLX_Register import *

instruction1 = BitArray(bin='0b00100110111100101001110000011100')
instruction2 = BitArray(bin='0b00100011111000001111100001001000')
instruction3 = BitArray(bin='0b00001011110001001001100001100010')
storage = DLX_Speicher()
storage.setW(0, instruction1)
storage.setW(4, instruction2)
storage.setW(8, instruction3)

alu = 0
regbank = DLX_Reg_Bank()
pipe = DLX_Pipeline(storage,alu,regbank)

pipe.doPipeNext()

print(pipe.extend0( BitArray(uint=0x3F, length=6) ))

