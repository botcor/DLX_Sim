#!/usr/bin/env python
# 
# DLX_ALU.py
# Name: DLX ALU
# Author: Marco Klingseisen
# Date: 03.11.2014
# Brief: Contains the Implementation of all Arithmetic, Logical, Shift and Conditional Integer DLX Instructions  
# 
# History:
# 03.11.2014 - Creation
# 22.11.2014 - Added Overflow-Flag

import logging
import inspect
from bitstring import *

#create logger
mylogger = logging.getLogger("ALU")

class DLX_ALU:

    overfl = 0 #overflow flag
    #underfl = 0 #TODO underflow flag and detection

    def __init__(self): 
        pass
    
    #ARITHMETIC and LOGIC

    #SIGNED ADDITION
    def ADD(self, a, b):
        self.overfl = 0 #reset overflow flag
        erg = BitArray(int=(a.int + b.int), length=33)
        self.overfl = erg[0]
        erg = erg[1:33]
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg.hex)
        mylogger.debug("Function: %s  Overflow: %s",(inspect.stack()[0][3]), self.overfl)
        return erg

    #UNSIGNED ADDITION
    def ADDU(self, a, b):
        self.overfl = 0 #reset overflow flag
        erg = BitArray(uint=(a.uint + b.uint), length=33)
        self.overfl = erg[0]
        erg = erg[1:33]
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.uint,a.hex, b.uint,b.hex,  erg.uint,erg.hex)
        mylogger.debug("Function: %s  Overflow: %s",(inspect.stack()[0][3]), self.overfl)
        return erg

    #SIGNED SUBTRACTION
    def SUB(self, a, b):
        self.overfl = 0 #reset overflow flag
        erg = BitArray(int=(a.int - b.int), length=33)
        #self.overfl = erg[0]
        erg = erg[1:33]
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg.hex)
        #mylogger.debug("Function: %s  Overflow: %s",(inspect.stack()[0][3]), overfl)
        return erg

    #UNSIGNED SUBTRACTION
    def SUBU(self, a, b):
        self.overfl = 0 #reset overflow flag
        erg = BitArray(uint=(a.uint - b.uint), length=33)
        self.overfl = erg[0]
        erg = erg[1:33]
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.uint,a.hex, b.uint,b.hex,  erg.uint,erg.hex)
        mylogger.debug("Function: %s  Overflow: %s",(inspect.stack()[0][3]), self.overfl)
        return erg

    #LOGICAL AND BITS
    def AND(self, a, b):
        erg = BitArray(int=(a.int & b.int), length=32)
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg.hex)
        return erg

    #LOGICAL OR BITS
    def OR(self, a, b):
        erg = BitArray(int=(a.int | b.int), length=32)
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg.hex)
        return erg

    #LOGICAL EXCLUSIVE OR BITS
    def XOR(self, a, b):
        erg = BitArray(int=(a.int ^ b.int), length=32)
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg.hex)
        return erg


    #SHIFTS

    #SHIFT LEFT LOGICAL
    def SLL(self, a, b):        
        erg = BitArray(int = a.int, length=32)
        erg <<= b.int
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg.hex)
        return erg

    #SHIFT RIGHT ARITHMETIC
    def SRA(self, a, b):
        erg = BitArray(int=(a.int >> b.int), length=32)
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg.hex)
        return erg

    #SHIFT RIGHT LOGICAL
    def SRL(self, a, b):
        erg = BitArray(int = a.int, length=32)
        erg >>= b.int
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg.hex)
        return erg


    #CONDITIONAL

    #SET EQUAL UNSIGNED
    def SEQU(self, a, b):
        erg = BitArray(uint = 0, length=32)
        if(a.uint == b.uint):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.uint,a.hex, b.uint,b.hex,  erg.uint,erg[31])
        return erg

    #SET NOT EQUAL UNSIGNED
    def SNEU(self, a, b):
        erg = BitArray(uint = 0, length=32)
        if(a.uint != b.uint):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.uint,a.hex, b.uint,b.hex,  erg.uint,erg[31])
        return erg

    #SET LESS THAN UNSIGNED
    def SLTU(self, a, b):
        erg = BitArray(uint = 0, length=32)
        if(a.uint < b.uint):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.uint,a.hex, b.uint,b.hex,  erg.uint,erg[31])
        return erg  
    
    #SET GREATER THAN UNSIGNED
    def SGTU(self, a, b):
        erg = BitArray(uint = 0, length=32)
        if(a.uint > b.uint):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.uint,a.hex, b.uint,b.hex,  erg.uint,erg[31])
        return erg

    #SET LESS EQUAL UNSIGNED
    def SLEU(self, a, b):
        erg = BitArray(uint = 0, length=32)
        if(a.uint <= b.uint):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.uint,a.hex, b.uint,b.hex,  erg.uint,erg[31])
        return erg

    #SET GREATER EQUAL UNSIGNED
    def SGEU(self, a, b):
        erg = BitArray(uint = 0, length=32)
        if(a.uint >= b.uint):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.uint,a.hex, b.uint,b.hex,  erg.uint,erg[31])
        return erg  
    
    #SET EQUAL
    def SEQ(self, a, b):
        erg = BitArray(int = 0, length=32)
        if(a.int == b.int):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg[31])
        return erg 
  
    #SET NOT EQUAL
    def SNE(self, a, b):
        erg = BitArray(int = 0, length=32)
        if(a.int != b.int):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg[31])
        return erg

    #SET LESS THAN
    def SLT(self, a, b):
        erg = BitArray(int = 0, length=32)
        if(a.int < b.int):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg[31])
        return erg

    #SET GREATER THAN
    def SGT(self, a, b):
        erg = BitArray(int = 0, length=32)
        if(a.int > b.int):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg[31])
        return erg

    #SET LESS EQUAL
    def SLE(self, a, b):
        erg = BitArray(int = 0, length=32)
        if(a.int <= b.int):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg[31])
        return erg

    #SET GREATER EQUAL
    def SGE(self, a, b):
        erg = BitArray(int = 0, length=32)
        if(a.int >= b.int):
            erg[31] = 1
        mylogger.debug("Function: %s, Value a: %d(%s), Value b: %d(%s), Result : %d(%s)",(inspect.stack()[0][3]), a.int,a.hex, b.int,b.hex,  erg.int,erg[31])
        return erg

