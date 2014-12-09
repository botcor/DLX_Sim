#!/usr/bin/env python
#
# translator.py
# Name: DLX Pipeline
# Author: Cornelius Bott
# Date: 19.10.2014
# Brief: Contains the entire DLX-Pipeline Registers and Functions
# 
# History:
#   18.11.2014  -   add Registers, stage functions IF and ID
#   20.11.2014  -   add __extend and __0extend, __insFIFO
#                   change the __op stuff in doID()
#   21.11.2014  -   add the right extension of Imm for the different opcodes
#   22.11.2014  -   add functionality of EX including ALU calls and Condition checking
import sys
sys.path.append('./src')
import logging
import inspect
from DLX_Register import *


class DLX_Pipeline:
    def __init__(self, storage, alu, regbank):        
        self.stages = ['IF','ID','EX','MEM','WB']
        self.piperegs = ['PC','NPC','IR','A','B','Imm','Cond','AO','LMD']
        mylogger.info("Pipeline Stages: %s",self.stages)
        mylogger.info("Pipeline Registers: %s",self.piperegs)
        self.__insFIFO = [BitArray(uint=0, length=32), BitArray(uint=0, length=32), BitArray(uint=0, length=32), BitArray(uint=0, length=32), BitArray(uint=0, length=32)]
        self.storage = storage
        self.alu = alu
        self.regbank = regbank
        self.PC = DLX_Register(name="PC")
        self.NPC = DLX_Register()
        self.IR = DLX_Register()
        self.A = DLX_Register()
        self.B = DLX_Register()
        self.Imm = DLX_Register()
        self.Cond = DLX_Register()
        self.AO = DLX_Register()
        self.LMD = DLX_Register()
        forwarding = 'true'

    def __shiftFIFO(self, n):
        self.__insFIFO[:n] + self.__insFIFO[n:]
        self.__insFIFO[0] = 0

    def __extend(self, value):
        return BitArray(int=value.int, length=32)

    def __extend0(self, value):
        return BitArray(uint=value.uint, length=32)

    def doIF(self):
        # get the next word from storage (indicated by PC) and store it to the IR Register
        self.IR.setVal( BitArray( uint=( self.storage.getW( self.PC.getVal().uint )), length=32 ) )
        # store the Instruction to insFIFO as well
        self.__insFIFO[0] = self.IR.getVal()
        # increase the PC by 4 (bytes) and store in NPC
        self.NPC.setVal( BitArray( uint=( self.PC.getVal().uint + 4 ), length=32 ) )
        
    def doID(self):
        # save the opcode aside (not DLX specified)
        __OP = BitArray( self.IR.getVal()[0:6], length=6 )
        # determine the Instruction Format
        # and dependent on that
            # get the registers from regbank
        if ( __OP.uint == 0x00 ):
            # R-Type
            # get rs1   which is @                                   v
            self.A.setVal( self.regbank.getRegByID( self.IR.getVal()[6:11].uint ).getVal() )
            # get rs2   which is @                                   v
            self.B.setVal( self.regbank.getRegByID( self.IR.getVal()[11:16].uint ).getVal() )
            # get func  whitch is @                                    v
            self.Imm.setVal( self.regbank.getRegByID( self.IR.getVal()[16:32].uint ).getVal() )
        elif ( __OP.uint <= 0x03 ):
            # J-Type
            # get dist  which is @                                     v
            self.Imm.setVal( self.regbank.getRegByID( self.IR.getVal()[6:32].uint ).getVal() )
        else:
            # I-Type
            # get rs1   which is @                                   v
            self.A.setVal( self.regbank.getRegByID( self.IR.getVal()[6:11].uint ).getVal() )
            # get immediate   which is @                               v
            self.Imm.setVal( self.regbank.getRegByID( self.IR.getVal()[16:32].uint ).getVal() )

        # determine the kind of extension and extend the Imm value
        if ( __OP.uint == 0x08 | __OP.uint == 0x0A | (__OP.uint >= 0x18 & __OP.uint <= 0x1D) |
                __OP.uint == 0x02 | __OP.uint == 0x03 | __OP.uint == 0x04 | __OP.uint == 0x05):
            # for ADDI,        SUBI,       SEQI, SNEI, SLTI, SGTI, SLEI, SGEI,          J, JAL,  BEQZ, BNEZ
            self.Imm.setVal( self.__extend(self.Imm.getVal() ) )
        elif ( __OP.uint == 0x0F | __OP.uint == 0x23 | __OP.uint == 0x20 | __OP.uint == 0x21 |
                __OP.uint == 0x2B | __OP.uint == 0x29 | __OP.uint == 0x28 ):
            # for LHI, LW, LB, LH, SW, SH, SB
            self.Imm.setVal( self.__extend(self.Imm.getVal() ) )
        elif not( __OP.uint == 0x14 | __OP.uint == 0x17 | __OP.uint == 0x16 | __OP.uint == 0x00 ):
            # excluding SLLI, SRAI, SRLI along with all R-Type Instructions
            # -->    for ADDUI, SUBUI, ANDI, ORI, XORI,    SEQUI, SNEUI, SLTUI, SGTUI, SLEUI, SGEUI,   LBU, LHU
            self.Imm.setVal( self.__extend0( self.Imm.getVal() ) )

        # get the registers from the regbank
        #

    def doEX(self):
        # save the opcode aside (not DLX specified)
        __IR = self.__insFIFO[2]
        __OP = BitArray( __IR[0:6], length=6 )
        # determine Task by the rules:
        # dependent on Type load B or Imm
            # dependent on opcode do
                # condition checking
                # alu calling
                
                # dependent on opcode do extension of Imm and call the ALU
        if ( __OP.uint == 0x00 ):
            # R-Type
            # func is stored in the Register Imm
            if (self.Imm.getVal().uint == 0x20):
                #ADD
                self.AO.setVal( self.alu.ADD(self.A.getVal(), self.B.getVal() ) )
            elif (self.Imm.getVal().uint == 0x21):
                #ADDU
                self.AO.setVal( self.alu.ADDU(self.A.getVal(), self.B.getVal() ) )
            elif (self.Imm.getVal().uint == 0x22):
                #SUB
                self.AO.setVal( self.alu.SUB(self.A.getVal(), self.B.getVal() ) )
            elif (self.Imm.getVal().uint == 0x23):
                #SUBU
                self.AO.setVal( self.alu.SUBU(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x24):
                #AND
                self.AO.setVal( self.alu.AND(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x25):
                #OR
                self.AO.setVal( self.alu.OR(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x26):
                #XOR
                self.AO.setVal( self.alu.XOR(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x04):
                #SLL
                self.AO.setVal( self.alu.SLL(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x04):
                #SLL
                self.AO.setVal( self.alu.SLL(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x07):
                #SRA
                self.AO.setVal( self.alu.SRA(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x06):
                #SRL
                self.AO.setVal( self.alu.SRL(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x10):
                #SEQU
                self.AO.setVal( self.alu.SEQU(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x11):
                #SNEU
                self.AO.setVal( self.alu.SNEU(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x12):
                #SLTU
                self.AO.setVal( self.alu.SLTU(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x13):
                #SGTU
                self.AO.setVal( self.alu.SGTU(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x14):
                #SLEU
                self.AO.setVal( self.alu.SLEU(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x15):
                #SGEU
                self.AO.setVal( self.alu.SGEU(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x28):
                #SEQ
                self.AO.setVal( self.alu.SEQ(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x29):
                #SNE
                self.AO.setVal( self.alu.SRL(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x2A):
                #SLT
                self.AO.setVal( self.alu.SLT(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x2B):
                #SGT
                self.AO.setVal( self.alu.SGT(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x2C):
                #SLE
                self.AO.setVal( self.alu.SLE(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x2D):
                #SGE
                self.AO.setVal( self.alu.SGE(self.A.getVal(), self.B.getVal()) )
            else:
                print("Fehler")

        elif ( __OP.uint <= 0x03 ):
            # J-Type
            if ( __OP.uint == 0x02 ):
                self.AO.setVal( self.alu.J(self.Imm.getVal()) )
            elif (self.Imm.getVal().uint == 0x03):
                #SRL
                self.AO.setVal( self.alu.JAL(self.A.getVal(), self.B.getVal()) )
        else:
            # I-Type
            # Branches
            if (__OP.uint == 0x04):
                #BEQZ
                if(self.A.getVal().uint == 0x00):
                    self.Cond.setVal(BitArray(hex='0xAAAA'))
                    self.AO.setVal( self.alu.ADD( self.NPC.getVal() ), self.Imm.getVal() )
                else:
                    self.Cond.setVal(BitArray(hex='0x5555'))
            elif (__OP.uint == 0x05):
                #BNEZ
                if(self.A.getVal().uint != 0x00):
                    self.Cond.setVal(BitArray(hex='0xAAAA'))
                else:
                    self.Cond.setVal(BitArray(hex='0x5555'))
                #self.AO.setVal( self.alu.ADD(self.PC ) )
            elif (__OP.uint == 0x12):
                #JR do nothing here
                thumbs = 'twiddle'
            elif (__OP.uint == 0x13):
                #JALR do nothing here
                thumbs = 'twiddle'
            elif (__OP.uint == 0x08):
                #ADDI
                self.AO.setVal( self.alu.ADD(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x09):
                #ADDUI
                self.AO.setVal( self.alu.ADDU(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x0A):
                #SUBI
                self.AO.setVal( self.alu.SUB(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x0B):
                #SUBUI
                self.AO.setVal( self.alu.SUBU(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x0C):
                #ANDI
                self.AO.setVal( self.alu.AND(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x0D):
                #ORI
                self.AO.setVal( self.alu.OR(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x0E):
                #XORI
                self.AO.setVal( self.alu.XOR(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x14):
                #SLLI
                self.AO.setVal( self.alu.SLL(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x17):
                #SRAI
                self.AO.setVal( self.alu.SRA(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x16):
                #SRLI
                self.AO.setVal( self.alu.SRL(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x30):
                #SEQUI
                self.AO.setVal( self.alu.SEQU(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x31):
                #SNEUI
                self.AO.setVal( self.alu.SNEU(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x32):
                #SLTUI
                self.AO.setVal( self.alu.SLTU(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x33):
                #SGTUI
                self.AO.setVal( self.alu.SGTU(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x34):
                #SLEUI
                self.AO.setVal( self.alu.SLEU(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x35):
                #SGEUI
                self.AO.setVal( self.alu.SGEU(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x18):
                #SEQI
                self.AO.setVal( self.alu.SEQ(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x19):
                #SNEI
                self.AO.setVal( self.alu.SRL(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x1A):
                #SLTI
                self.AO.setVal( self.alu.SLT(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x1B):
                #SGTI
                self.AO.setVal( self.alu.SGT(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x1C):
                #SLEI
                self.AO.setVal( self.alu.SLE(self.A.getVal(), self.Imm.getVal()) )
            elif (__OP.uint == 0x1D):
                #SGEI
                self.AO.setVal( self.alu.SGE(self.A.getVal(), self.Imm.getVal()) )
            else:
                print("Fehler")

        return 0

    def doMEM(self):
        # save the opcode aside (not DLX specified)
        __IR = self.__insFIFO[3]
        __OP = BitArray( __IR[0:6], length=6 )
        # get reference to rs1
        __rs1 = self.regbank.getRegByID( self.IR.getVal()[6:11].uint )

        # dependent on opcode do
        #   get the data from storage and store to LMD
        #   pass through AO
        if ( __OP.uint == '0x0F' ):
            # for LHI
            self.LMD.setVal( BitArray( uint=self.Imm.getVal().uint << 16, length=32 ) )
        elif ( __OP.uint == '0x23' ):
            # for LW
            self.LMD.setVal( self.__extend( self.storage.getW( self.regbank.getRegByID(__rs1).getVal().int + self.Imm.getVal().int ) ) )
        elif (  __OP.uint == '0x20' ):
            # for LB
            self.LMD.setVal( self.__extend( self.storage.getB( self.regbank.getRegByID(__rs1).getVal().int + self.Imm.getVal().int ) ) )
        elif ( __OP.uint == '0x21' ):
            # for LH
            self.LMD.setVal( self.__extend( self.storage.getH( self.regbank.getRegByID(__rs1).getVal().int + self.Imm.getVal().int ) ) )
        elif ( __OP.uint == '0x24' ):
            # for LBU
            self.LMD.setVal( self.__extend0( self.storage.getB( self.regbank.getRegByID(__rs1).getVal().int + self.Imm.getVal().int ) ) )
        elif ( __OP.uint == '0x25' ):
            # for LHU
            self.LMD.setVal( self.__extend0( self.storage.getH( self.regbank.getRegByID(__rs1).getVal().int + self.Imm.getVal().int ) ) )
        else:
            self.LMD.setVal( self.AO.getVal )

    def doWB(self):
        # save the opcode aside (not DLX specified)
        __IR = self.__insFIFO(4)
        __OP = BitArray( __IR[0:6], length=6 )
        # get reference to rs1
        __rs1 = self.regbank.getRegByID( self.IR.getVal()[6:11].uint )
        # get reference to rd
        if ( __OP.uint == 0x00 ):
            # R-Type
            __rd = self.regbank.getRegByID( self.IR.getVal()[16:21].uint )
        elif ( __OP.uint <= 0x03 ):
            # J-Type
            __rd = 0
        else:
            # I-Type
            __rd = self.regbank.getRegByID( self.IR.getVal()[11:16].uint )
            
        # dependent on opcode do
        #   write value to storage @ rs1 + ...
        #   write value to register rd
        if( __OP.uint == '0x2B' ):
            # SW
            self.storage.setW( self.LMD.getVal, __rs1.getVal.int + self.Imm.getVal().int )
        elif ( __OP.uint == '0x29' ):
            # SH
            self.storage.setH( self.LMD.getVal, __rs1.getVal.int + self.Imm.getVal().int )
        elif ( __OP.uint == '0x28' ):
            # SB
            self.storage.setB( self.LMD.getVal, __rs1.getVal.int + self.Imm.getVal().int )
        else:
            self.regbank.getRegByID(__rd).setVal( self.LMD.getVal() )

    def doPipeNext(self):
        mylogger.debug("Function: %s",(inspect.stack()[0][3]))
        mylogger.debug("PC:       %d",self.PC.getVal().uint)
        mylogger.debug("Instruction FIFO: [0] %d, [1] %d, [2] %d, [3] %d, [4] %d", self.insFIFO[0], self.insFIFO[1], self.insFIFO[2], self.insFIFO[3], self.insFIFO[4])
        self.WB()
        self.doMEM()
        self.doEX()
        self.doID()
        self.doIF()

        self.__shiftFIFO(1)

    def getRegsByName(self):
        return 0
