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
#   20.11.2014  -   add __extend and __0extend, insFIFO
#                   change the __op stuff in doID()
#   21.11.2014  -   add the right extension of Imm for the different opcodes
#   22.11.2014  -   add functionality of EX including ALU calls and Condition checking
import sys
sys.path.append('./src')
import logging
import inspect
from DLX_Register import *

#create logger
mylogger = logging.getLogger("Pipeline")

class DLX_Pipeline:
    dInstruction =	{ "LHI" : 0x0F, "LW" : 0x23, "LBU" : 0x24 , "LB" : 0x20, "LHU" : 0x25, "LH" : 0x21, "SW" : 0x2B, "SH" : 0x29, "SB" : 0x28, "ADDI" : 0x08, "ADDUI" : 0x09, "SUBI" : 0x0A, "SUBUI" : 0x0B, "ANDI" : 0x0C, "ORI" : 0x0D, "XORI" : 0x0E, "SLLI" : 0x14, "SRAI" : 0x17, "SRLI" : 0x16, "SEQUI" : 0x30, "SNEUI" : 0x31, "SLTUI" : 0x32, "SGTUI" : 0x33, "SLEUI" : 0x34, "SGEUI" : 0x35, "SEQI" : 0x18, "SNEI" : 0x19, "SLTI" : 0x1A, "SGTI" : 0x1B, "SLEI" : 0x1C, "SGEI" : 0x1D, "BEQZ" : 0x04, "BNEZ" : 0x05, "JR" : 0x12, "JALR" : 0x13, "J" : 0x02, "JAL" : 0x03, "TRAP" :0x11 }

    dFuncIns = { "ADD" : 0x20, "ADDU" : 0x21, "SUB" : 0x22, "SUBU" : 0x23, "AND" : 0x24, "OR" : 0x25, "XOR" : 0x26, "SLL" : 0x04, "SRA" : 0x07, "SRL" : 0x06, "SEQU" : 0x10, "SNEU" : 0x11, "SLTU" : 0x12, "SGTU" : 0x13, "SLEU" : 0x14, "SGEU" : 0x15, "SEQ" : 0x28, "SNE" : 0x29, "SLT" : 0x2A, "SGT" : 0x2B, "SLE" : 0x2C, "SGE" : 0x2D }

    def __init__(self, storage, alu, regbank):        
        self.stages = ['IF','ID','EX','MEM','WB']
        self.piperegs = ['PC','NPC','IR','A','B','Imm','Cond','AO','DO','LMD']
        mylogger.info("Pipeline Stages: %s",self.stages)
        mylogger.info("Pipeline Registers: %s",self.piperegs)
        self.insFIFO = [BitArray(uint=0, length=32), BitArray(uint=0, length=32), BitArray(uint=0, length=32), BitArray(uint=0, length=32), BitArray(uint=0, length=32)]
        self.storage = storage
        self.alu = alu
        self.regbank = regbank
        # define the Pipeline Registers
        self.PC = DLX_Register(name="PC")
        self.NPC = DLX_Register(name="NPC")
        self.NPC_2 = DLX_Register(name="NPC_2")
        self.IR = DLX_Register(name="IR")
        self.A = DLX_Register(name="A")
        self.B = DLX_Register(name="B")
        self.Imm = DLX_Register(name="Imm")
        self.Cond = DLX_Register(name="Cond")
        self.AO = DLX_Register(name="AO")
        self.DO = DLX_Register(name="DO")
        self.LMD = DLX_Register(name="LMD")
        # define the Flags and Options
        self.fJump = 'false'
        self.fForwarding = 'true'
        self.fDataHazard = 'false'
        self.fCtrlHazard = 'false'
        self.cStallCnt = 0

    def __shiftFIFO(self, n):
        self.insFIFO[:n] + self.insFIFO[n:]
        self.insFIFO[0] = 0

    def __extend(self, value):
        return BitArray(int=value.int, length=32)

    def __extend0(self, value):
        return BitArray(uint=value.uint, length=32)

    def doIF(self):
        mylogger.debug("do Function: %s",(inspect.stack()[0][3]) )
        # get the next word from storage (indicated by PC) and store it to the IR Register
        self.IR.setVal( BitArray( uint=( self.storage.getW( self.PC.getVal().uint ).uint), length=32 ) )
        # store the Instruction to insFIFO as well
        self.insFIFO[0] = self.IR.getVal()
        # 
        if not(self.StallCnt > 0):
            # determin the next Program Counter
            self.NPC.setVal( BitArray( uint=( self.PC.getVal().uint + 4 ), length=32 ) )
            if (self.fJump == True):
                self.PC.setVal( self.AO.getVal() )
            else:
                self.PC.getVal( self.NPC.setVal() )
        else:
            self.StallCnt -= 1
        
        
    def doID(self):
        mylogger.debug("do Function: %s",(inspect.stack()[0][3]) )
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
            # get func  whitch is @           v
            self.Imm.setVal( self.IR.getVal()[21:32] )
        elif ( __OP.uint <= 0x03 ):
            # J-Type
            # get dist  which is @            v
            self.Imm.setVal( self.IR.getVal()[6:32] )
        else:
            # I-Type
            # get rs1   which is @                                   v
            self.A.setVal( self.regbank.getRegByID( self.IR.getVal()[6:11].uint ).getVal() )
            # get rd used for the store commands
            self.B.setVal( self.regbank.getRegByID( self.IR.getVal()[11:16].uint ).getVal() )
            # get immediate   which is @      v
            self.Imm.setVal( self.IR.getVal()[16:32] )

        # determine the kind of extension and extend the Imm value
        if ( __OP.uint == 0x08 | __OP.uint == 0x0A | ( __OP.uint >= 0x18 & __OP.uint <= 0x1D) |
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

        # forward the NPC Register to the EX stage
        self.NPC_2.setVal( self.NPC.getVal() )
        return 0

    def doEX(self):
        mylogger.debug("do Function: %s",(inspect.stack()[0][3]) )
        # save the opcode aside (not DLX specified)
        __IR = self.insFIFO[2]
        __OP = BitArray( __IR[0:6], length=6 )
        # determine Task by the rules:
        # dependent on Type load B or Imm
            # dependent on the opcode do
                # condition checking
                # alu calling
        if ( __OP.uint == 0x00 ):
            # R-Type
            # func is stored in the Register Imm
            if (self.Imm.getVal().uint == 0x20):
                #ADD
                self.AO.setVal( self.alu.ADD(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x21):
                #ADDU
                self.AO.setVal( self.alu.ADDU(self.A.getVal(), self.B.getVal()) )
            elif (self.Imm.getVal().uint == 0x22):
                #SUB
                self.AO.setVal( self.alu.SUB(self.A.getVal(), self.B.getVal()) )
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
                mylogger.debug("Fehler in doEX R-Type")

        elif ( __OP.uint <= 0x03 ):
            # J-Type
            if ( __OP.uint == 0x02 ):
                # increase the Imm by 4 (bytes) and store in NPC
                self.AO.setVal( BitArray( uint=( self.Imm.getVal().uint + 4 ), length=32 ) )
            elif (self.Imm.getVal().uint == 0x03):
                #JAL
                # store current PC to R31 increased by 4, increase the PC by Imm and store in NPC
                self.regbank.getRegByID(31).setVal( BitArray( uint=( self.PC.getVal().uint + 4 ), length=32 ) )
                self.AO.setVal( BitArray( uint=( self.PC.getVal().uint + self.Imm.getVal().uint ), length=32 ) )
        else:
            # I-Type
            # Branches
            if (__OP.uint == 0x04):
                #BEQZ
                if(self.A.getVal().uint == 0x00):
                    self.Cond.setVal(BitArray(hex='0xAAAA'))
                    self.AO.setVal( self.alu.ADD( self.NPC_2.getVal() ), self.Imm.getVal() )
                else:
                    self.Cond.setVal(BitArray(hex='0x5555'))
            elif (__OP.uint == 0x05):
                #BNEZ
                if(self.A.getVal().uint != 0x00):
                    self.Cond.setVal(BitArray(hex='0xAAAA'))
                    self.AO.setVal( self.alu.ADD( self.NPC_2.getVal() ), self.Imm.getVal() )
                else:
                    self.Cond.setVal(BitArray(hex='0x5555'))
            elif not( __OP.uint == 0x04 | __OP.uint == 0x05 ):
                self.Cond.setVal( hex='0x5555' )
            elif (__OP.uint == 0x12):
                #JR
                self.AO.setVal( BitArray( uint=( self.A.getVal().uint ) ) )
            elif (__OP.uint == 0x13):
                #JALR
                self.regbank.getRegByID(31).setVal( BitArray( uint=( self.PC.getVal().uint + 4 ), length=32 ) )
                self.AO.setVal( BitArray( uint=( self.A.getVal().uint) ) )
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
            elif ( __OP.uint == 0x0F ):
                #LHI
                self.AO.setVal( self.alu.SLL(self.A.getVal(), BitArray(uint=16, length=32)) )
            elif ( __OP.uint == 0x20 | __OP.uint == 0x21 | __OP.uint == 0x23 | __OP.uint == 0x24 | __OP.uint == 0x25):
                #LB LH LW LBU LHU
                self.AO.setVal( self.alu.ADDU(self.A.getVal(), self.Imm.getVal()) )
            elif ( __OP.uint == 0x2B | __OP.uint == 0x29 | __OP.uint == 0x28):
                #SW SH SB
                self.AO.setVal( self.alu.ADDU(self.A.getVal(), self.Imm.getVal()) )
                self.DO.setVal( self.B.getVal() )
            else:
                mylogger.debug("Fehler in doEX R-Type")
        return 0

    def doMEM(self):
        mylogger.debug("do Function: %s",(inspect.stack()[0][3]) )
        # save the opcode aside (not DLX specified)
        __IR = self.insFIFO[3]
        mylogger.debug("insFIFO[3]: %s",self.insFIFO[3] )
        __OP = BitArray( __IR[0:6], length=6 )
        mylogger.debug("__OP: %s",__OP )
        mylogger.debug("__OP.uint: %s",__OP.uint )
        # get reference to rs1
        __rs1 = self.regbank.getRegByID( self.IR.getVal()[6:11].uint )

        # if a load/store
        #   get the data from storage and store to LMD
        # else proceed the jump or forward AO
        #
        if ( __OP.uint == 0x23 ):
            # LW
            self.LMD.setVal( self.storage.getW( self.AO.getVal().uint ) )
        elif ( __OP.uint == 0x20 ):
            # LB
            self.LMD.setVal( self.__extend( self.storage.getB( self.AO.getVal().uint ) ) )
        elif ( __OP.uint == 0x21 ):
            # LH
            self.LMD.setVal( self.__extend( self.storage.getH( self.AO.getVal().uint ) ) )
        elif ( __OP.uint == 0x24 ):
            # LBU
            self.LMD.setVal( self.__extend0( self.storage.getB( self.AO.getVal().uint ) ) )
        elif ( __OP.uint == 0x25 ):
            # LHU
            self.LMD.setVal( self.__extend0( self.storage.getH( self.AO.getVal().uint ) ) )
        elif ( __OP.uint == 0x2B ):
            # SW
            self.storage.setW( self.DO.getVal(), self.AO.getVal().uint )
        elif ( __OP.uint == 0x29 ):
            # SH
            self.storage.setH( self.DO.getVal(), self.AO.getVal().uint )
        elif ( __OP.uint == 0x28 ):
            # SB
            self.storage.setB( self.DO.getVal(), self.AO.getVal().uint )
        elif ( __OP.uint == 0x12 | __OP.uint == 0x13 | __OP.uint == 0x02 | __OP.uint == 0x03 ):
                 # JR                    JALR                J                     JAL
            self.fJump = True
        elif ( __OP.uint == 0x04 | __OP.uint == 0x05 ):
            #  BEQZ                BNEZ  
            if (self.Cond.getVal().hex == '0x5555'):
                self.fJump = True
            else:
                self.fJump = False
        elif not( __OP.uint == 0x04 | __OP.uint == 0x05 | __OP.uint == 0x12 | __OP.uint == 0x13 | __OP.uint == 0x02 | __OP.uint == 0x03):
            self.fJump = False
        else:
            self.LMD.setVal( self.AO.getVal() )
        return 0

    def doWB(self):
        mylogger.debug("do Function: %s",(inspect.stack()[0][3]) )
        # save the opcode aside (not DLX specified)
        __IR = self.insFIFO[4]
        __OP = BitArray( __IR[0:6], length=6 )

        if not( __OP.uint == 0x2B | __OP.uint == 0x29 | __OP.uint == 0x28 ):
            self.regbank.getRegById(  ).setVal( self.LMD.getVal() )
        return 0

    def detectDataHazard():
        __OP_mem = self.insFIFO[3][0:6]
        __OP_id = self.insFIFO[1][0:6]
        __OP_ex = self.insFIFO[2][0:6]
        
        # determine the affected registers in MEM, ID and EX
        if ( __OP_mem.uint == 0x00 ):
            # R-Type
            __rd_mem = self.insFIFO[3][16:20].uint
        elif ( __OP_mem.uint <= 0x03 ):
            # J-Type
            __rd_mem = 0
        else:
            # I-Type
            __rd_mem = self.self.insFIFO[3][11:16].uint

        if ( __OP_id.uint == 0x00 ):
            # R-Type
            __rs1_id = self.insFIFO[1][6:11].uint
            __rs2_id = self.insFIFO[1][11:16].uint
        elif ( __OP_id.uint <= 0x03 ):
            # J-Type
            __rs1_id = 0xFF
            __rs2_id = 0xFF
        else:
            # I-Type
            __rs1_id = self.insFIFO[1][6:11].uint
            __rs2_id = 0xFF

        if ( __OP_ex.uint == 0x00 ):
            # R-Type
            __rd_ex = self.insFIFO[1][0:6].uint
        elif ( __OP_ex.uint <= 0x03 ):
            # J-Type
            __rd_ex = 0xFF
        else:
            # I-Type
            __rd_ex = self.insFIFO[1][0:6].uint
        
        # checking for hazards
        if( __rd_mem ==  __rs1_id ):
            # Hazard between ID and MEM forward to A
            self.fDataHazard = True
            if(fForwarding == True):
                # forward LMD to A
                mylogger.debug("FWD: LMD -> A")
            else:
                # do two stalls
                self.StallCnt = 2
            mylogger.debug("DataHazard: MEM -> ID(A)")
        elif ( __rd_mem == __rs2_id ):
            # Hazard between ID and MEM forward to B
            self.fDataHazard = True
            if(fForwarding == True):
                # forward LMD to B
                mylogger.debug("FWD: LMD -> B")
            else:
                # do two stalls
                self.StallCnt = 2
            mylogger.debug("DataHazard: MEM -> ID(B)")
        elif( __rd_ex == __rs1_id ):
            # Hazard between ID and EX forward to A
            self.fDataHazard = True
            mylogger.debug("DataHazard: EX -> ID(A)")
        elif( __rd_ex == __rs2_id ):
            # Hazard between ID and EX forward to B
            self.fDataHazard = True
            mylogger.debug("DataHazard: EX -> ID(A)")
        else:
            self.fDataHazard = False
        

    def doPipeNext(self):
        mylogger.debug("do Function: %s", (inspect.stack()[0][3]))
        mylogger.debug("PC:       %d", self.PC.getVal().uint)
        mylogger.debug("Instruction FIFO: [0] %s, [1] %s, [2] %s, [3] %s, [4] %s", self.insFIFO[0], self.insFIFO[1], self.insFIFO[2], self.insFIFO[3], self.insFIFO[4])
        self.DataHazard = self.detectDataHazard()
        self.doWB()
        self.doMEM()
        self.doEX()
        self.doID()
        self.doIF()

        self.__shiftFIFO(1)

    def getPipeRegByName(self, name):
        if name == 'PC':
            return self.PC
        elif name == 'IR':
            return self.IR
        elif name == 'A':
            return self.A
        elif name == 'B':
            return self.B
        elif name == 'Imm':
            return self.Imm
        elif name == 'Cond':
            return self.Cond
        elif name == 'AO':
            return self.AO
        elif name == 'DO':
            return self.DO
        elif name == 'LMD':
            return self.LMD
        else:
            return 0

