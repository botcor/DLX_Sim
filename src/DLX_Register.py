#!/usr/bin/env python
#
# DLX_Register.py
# Name: DLX Pipeline
# Author: Cornelius Bott
# Date: 29.10.2014
# Brief: Contains the DLX-Registers and Functions to read and write them.
#        The Registers are organised in a Bank. With one Zero-Register and any number of normal Registers.
# 
# History:
# 29.10.2014 - Creation
# 08.11.2014 - Adding Logger
#
import logging
from bitstring import *

#create logger
mylogger = logging.getLogger("Register")

class DLX_Register:
    __name = 0
    __value = 0

    def __init__(self, regsize=32, name='rXX', value=0):
        self.__name = name
        self.__value = BitArray(uint=value, length=regsize)
        mylogger.debug("Register %s wurde angelegt.", self.__name)

    def setVal(self, value):
        self.__value.bin = value.bin
        mylogger.debug("Register %s wurde der Wert %s zugewiesen.", self.__name, value.bin)

    def getVal(self):
        mylogger.debug("Register %s hat momentan den Wert %s.", self.__name, self.__value.bin)
        return self.__value
        

    def getName(self):
        return self.__name


class DLX_Register0(DLX_Register):
    def __init__(self, regsize=32, name='r0', value=0):
        self.__name = name
        self.__value = BitArray(uint=0, length=regsize)
        mylogger.debug("Register %s wurde angelegt.", self.__name)

    def setVal(self, value=0):
        self.__value = BitArray(uint=0, length=32)

    def getVal(self):
        return self.__value

    def getName(self):
        return self.__name


class DLX_Reg_Bank:
    Bank = []
    def __init__(self, number=32, regsize=32):
        self.Bank.append( DLX_Register0() )
        for i in range(1, number):
            self.Bank.append( DLX_Register( regsize=32, name='r' + str(i), value=0) )

    def getRegByID(self, index):
        return self.Bank[index]

    def getRegByName(self, name):
        return 0
