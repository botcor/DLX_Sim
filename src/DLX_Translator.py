#!/usr/bin/env python
#
# translator.py
# Name: DLX Translator
# Author: Cornelius Bott
# Date: 13.10.2014
# Brief: Translate the DLX instructions   String <-> Opcode
# 
# History:
#
import logging
from bitstring import BitArray

#create logger
mylogger = logging.getLogger("Pipeline")

class DLX_Translator:

	# TODO: add all missing possible Values.
    l_instruction =	[ 'LHI', 'LW', 'LBU', 'LB', 'LHU', 'LH', 'SW', 'SH', 'SB', 'ADDI', 'ADDUI', 'SUBI', 'SUBUI', 'ANDI', 'ORI', 'XORI', 'SLLI', 'SRAI', 'SRLI', 'SEQUI', 'SNEUI', 'SLTUI', 'SGTUI', 'SLEUI', 'SGEUI', 'SEQI', 'SNEI', 'SLTI', 'SGTI', 'SLEI', 'SGEI', 'BEQZ', 'BNEZ', 'JR', 'JALR', 'J', 'JAL', 'TRAP' ]
    l_opcode =	[ 0x0F, 0x23, 0x24, 0x20, 0x25, 0x21, 0x2B, 0x29, 0x28, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x14, 0x17, 0x16, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x04, 0x05, 0x12, 0x13, 0x02, 0x03, 0x11 ]
    l_funcins = [ 'ADD', 'ADDU', 'SUB', 'SUBU', 'AND', 'OR', 'XOR', 'SLL', 'SRA', 'SRL', 'SEQU', 'SNEU', 'SLTU', 'SGTU', 'SLEU', 'SGEU', 'SEQ', 'SNE', 'SLT', 'SGT', 'SLE', 'SGE' ]
    l_funcopc = [ 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x04, 0x07, 0x06, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D ]

	# Translate the instruction name (string) into the opcode (integer).
    def instoop(self, ins):
        #TODO: get the func thingy working right.
        i = self.l_instruction.count(ins)
        if i == 1:	
            i = self.l_instruction.index(ins)
            return self.l_opcode[i]
        elif i>1:
            mylogger.debug("ERR: Found Instruction " + ins + " more than one time.")
        elif i<1:
            mylogger.debug("ERR: Instruction " + ins + " not found.")
        return "BAD"

	# Translate the opcode (integer) into the instruction name (string).
    def optoins(self, op, func):
        mylogger.debug("op " + repr(op) + "   func " + repr(func))		
        if func is not 0:
            i = self.l_funcopc.count(func)
            if i == 1:
                i = self.l_funcopc.index(func)
                return self.l_funcins[i]
        else:
            i = self.l_opcode.count(op)
            if i == 1:
                i = self.l_opcode.index(op)
                return self.l_instruction[i]
        if i > 1:
            mylogger.debug("ERR: Opcode " + repr(op) + " found more then one time.")
        elif i<1:
            mylogger.debug("ERR: Opcode " + repr(op) + " not found.")
        return "BAD"


class DLX_Disassembly(DLX_Translator):
    # Determine the Register Name from the Address
    def __Reg(self, Address):
        if Address > 31 or Address < 0:
            mylogger.debug("ERR: Bad Register address "+ repr(Address) +".")
            return "BAD"
        return "r" + repr(Address)
	
	# Format J:
	# | op | dist |
	# get the dist value
    def __JtoAsm(self, Operation):
        dist = (Operation & 0x03FFFFFF)
        return repr(dist)

    # Format I:
    # | op | rs1 | rd | imm |
    # get the Registers rs1 and rd as well as the immediate value
    def __ItoAsm(self, Operation):
        rs1 = (Operation & 0x03FFFFFF) >> (5+16)
        rs1 = self.__Reg(rs1)
        rd = (Operation & 0x001FFFFF) >> (16)
        rd = self.__Reg(rd)
        imm = (Operation & 0x0000FFFF)
        return rd +", "+ rs1 +", "+ repr(imm)
	
	# Format R:
	# | op | rs1 | rs2 | rd | func |
	# get the Registers rs1, rs2 and rd
    def __RtoAsm(self, Operation):
        rs1 = (Operation & 0x03FFFFFF) >> (5+16)
        rs1 = self.__Reg(rs1)
        rs2 = (Operation & 0x001FFFFF) >> (16)
        rs2 = self.__Reg(rs2)
        rd = (Operation & 0x0000FFFF) >> (32-6-5-5-5)
        rd = self.__Reg(rd)
        return rd +", "+ rs1 +", "+ rs2

	# Translate an Operation to readable Asembler
    def OperationToAsm(self, Operation):
        opcode = Operation[0:6].uint
        func = 0
        if opcode == 0x00:
            func = (Operation.uint & 0x000007FF)
            result = self.__RtoAsm(Operation.uint)
        elif opcode < 0x03:
            result = self.__JtoAsm(Operation.uint)
        else:
            result = self.__ItoAsm(Operation.uint)
        opcode = self.optoins(opcode,func)
        return opcode + " " + result
