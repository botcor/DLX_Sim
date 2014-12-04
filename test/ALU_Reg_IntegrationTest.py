#!/usr/bin/env python
#
# ALU_Reg_IntegrationTest.py
# Name: Integration Test DLX-Registers and ALU
# Author: Marco Klingseisen
# Date: 08.11.2014
# Brief: Integration Test for DLX-Registers and ALU
# 
# History:
# 08.11.2014 - Creation
#

import logging
import logging.config
import logging.handlers
import sys
sys.path.append("./src")
from DLX_Register import *
from DLX_ALU import *
from bitstring import *

#configure logger
logging.config.fileConfig("logging.conf")

#test values
a = BitArray(int=8, length=32)
b = BitArray(int=8, length=32)

o1 = BitArray(uint=4294967295, length=32)
o2 = BitArray(uint=1, length=32)

#ALU anlegen
alu = DLX_ALU()

#Registerbank anlegen
regb = DLX_Reg_Bank()

regb.setRegByID(1,a)
regb.setRegByID(4,a)
regb.getRegByID(2)

#SEQU r2, r1, r0 - object-oriented Version 
regb.setRegByID(2, (alu.SEQU(regb.getRegByID(1),regb.getRegByID(0) )))

#SEQU r3, r1, r4 - object-oriented Version 
regb.setRegByID(2, (alu.SEQU(regb.getRegByID(1),regb.getRegByID(4) )))

#SNEU r3, r1, r0 - direct Version
regb.Bank[3].setVal( alu.SNE(regb.Bank[1].getVal(), regb.Bank[0].getVal() ) )

#Overflow Test: 
regb.setRegByID(8,o1)
regb.setRegByID(9,o2)
#no overflow yet: ADDU r10, r8, r0
regb.setRegByID(10, (alu.ADDU(regb.getRegByID(8),regb.getRegByID(0) )))

#producing overflow: ADDU r10, r8, r9
regb.setRegByID(10, (alu.ADDU(regb.getRegByID(8),regb.getRegByID(9) )))
