#!/usr/bin/env python
#
# DLX_Register.py
# Name: DLX Pipeline
# Author: Cornelius Bott
# Date: 29.10.2014
# Brief: Contains the entire DLX-Pipeline Registers and Functions
# 
# Disclaimer:
#
import sys
sys.path.append("./src")
from DLX_Register import *

RegBank = DLX_Reg_Bank()

for i in range(0,32):
    print(RegBank.Bank[i].getName())
    print(RegBank.getRegByID(i))

for i in range(0,32):
    RegBank.Bank[i].setVal(BitArray(uint=123, length=32))

for i in range(0,32):
    print(RegBank.Bank[i].getName())
    print(RegBank.getRegByID(i))
