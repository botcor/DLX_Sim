import unittest
import logging
from bitstring import *
from DLX_Pipeline import *
from Sim import *

class TestCasesPipe(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create logger
        mylogger = logging.getLogger("Pipeline")
        mylogger.info("----------Unit Test Pipeline SetUp----------")
        cls.regb = DLX_Reg_Bank()
        cls.storage = DLX_Speicher()
        cls.a = BitArray(int=8, length=32) #r3
        #fill data storage with testvalues: 
        cls.ins1 = BitArray(hex='0x206F00FF') #ADDI r15, r3, 255
        cls.ins2 = BitArray(hex='0x00627825') #OR r15, r3, r2
        cls.ins3 = BitArray(hex='0x10A00020') #BEQZ r5,32
        cls.ins4 = BitArray(hex='0x0C000018') #JAL 24
        cls.ins5 = BitArray(hex='0x8C410004') #LW r1, 4(r2)
        cls.ins6 = BitArray(hex='0x90410004') #LBU r1, 4(r2)          
        cls.regb.Bank[3].setVal(cls.a)
        cls.alu = DLX_ALU()
        cls.pipe = DLX_Pipeline(cls.storage, cls.alu, cls.regb)
        return super().setUpClass()

    def setUp(self):
        self.pipe.ResetPipeline()
        return super().setUp()


    def test_doPipe_ADDI(self):
        mylogger.info("TestCase: test_doPipe_ADDI START")
        self.storage.setW(0, self.ins1)
        self.pipe.doPipeNext() #IF
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0x206F00FF').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        self.pipe.doPipeNext() #ID
        self.assertEqual(self.pipe.Imm.getVal().int, 255 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 8 , "Wrong Value in A")
        self.pipe.doPipeNext() #EX
        self.assertEqual(self.pipe.AO.getVal().int, 263 , "Wrong Value in AO")
        self.pipe.doPipeNext() #MEM
        self.assertEqual(self.pipe.LMD.getVal().int, 263 , "Wrong Value in LMD")
        self.pipe.doPipeNext() #WB
        self.assertEqual(self.regb.getRegByID(15).getVal().int, 263 , "Wrong Value in RD")
        mylogger.info("TestCase: test_doPipe_ADDI SUCCESSFUL")

    def test_doPipe_OR(self):
        mylogger.info("TestCase: test_doPipe_OR START")
        self.storage.setW(0, self.ins2)
        self.r2 = BitArray(int=246, length=32) #r2
        self.regb.Bank[2].setVal(self.r2)
        self.pipe.doPipeNext() #IF
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0x00627825').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        self.pipe.doPipeNext() #ID
        self.assertEqual(self.pipe.A.getVal().int, 8 , "Wrong Value in A")
        self.assertEqual(self.pipe.B.getVal().int, 246 , "Wrong Value in B")
        self.pipe.doPipeNext() #EX
        self.assertEqual(self.pipe.AO.getVal().int, 254 , "Wrong Value in AO")
        self.pipe.doPipeNext() #MEM
        self.assertEqual(self.pipe.LMD.getVal().int, 254 , "Wrong Value in LMD")
        self.pipe.doPipeNext() #WB
        self.assertEqual(self.regb.getRegByID(15).getVal().int, 254 , "Wrong Value in RD")
        mylogger.info("TestCase: test_doPipe_OR SUCCESSFUL")


    def test_doPipe_BEQZ0(self):
        mylogger.info("TestCase: test_doPipe_BEQZ0 START")
        self.storage.setW(0, self.ins3)
        self.branch = BitArray(int=0, length=32) #r5
        self.regb.Bank[5].setVal(self.branch)
        self.pipe.doPipeNext() #IF
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0x10A00020').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        self.pipe.doPipeNext() #ID
        self.assertEqual(self.pipe.Imm.getVal().int, 32 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 0, "Wrong Value in A")
        self.pipe.doPipeNext() #EX
        self.assertEqual(self.pipe.Cond.getVal().int, 1 , "Wrong Value in Cond")
        self.assertEqual(self.pipe.AO.getVal().int, 36 , "Wrong Value in AO")
        self.pipe.doPipeNext() #MEM
        self.assertEqual(self.pipe.PC.getVal().uint, 36, "Wrong Value in PC")
        self.pipe.doPipeNext() #WB
        mylogger.info("TestCase: test_doPipe_BEQZ0 SUCCESSFUL")

    def test_doPipe_BEQZ1(self):
        mylogger.info("TestCase: test_doPipe_BEQZ1 START")
        self.storage.setW(0, self.ins3)
        self.branch = BitArray(int=1, length=32) #r5
        self.regb.Bank[5].setVal(self.branch)
        self.pipe.doPipeNext() #IF
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0x10A00020').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        self.pipe.doPipeNext() #ID
        self.assertEqual(self.pipe.Imm.getVal().int, 32 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 1, "Wrong Value in A")
        self.pipe.doPipeNext() #EX
        self.assertEqual(self.pipe.Cond.getVal().int, 0 , "Wrong Value in Cond")
        self.pipe.doPipeNext() #MEM
        self.assertEqual(self.pipe.PC.getVal().uint, 16, "Wrong Value in PC")
        self.pipe.doPipeNext() #WB
        mylogger.info("TestCase: test_doPipe_BEQZ1 SUCCESSFUL")

    def test_doPipe_JAL(self):
        mylogger.info("TestCase: test_doPipe_JAL START")
        self.storage.setW(0, self.ins4)
        self.pipe.doPipeNext() #IF
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0x0C000018').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        self.pipe.doPipeNext() #ID
        self.assertEqual(self.pipe.Imm.getVal().int, 24 , "Wrong Value in Imm")
        self.pipe.doPipeNext() #EX
        self.assertEqual(self.pipe.AO.getVal().int, 24 , "Wrong Value in AO")
        self.assertEqual(self.regb.getRegByID(31).getVal().int, 4 , "Wrong Value in R31")
        self.pipe.doPipeNext() #MEM
        self.assertEqual(self.pipe.PC.getVal().uint, 24, "Wrong Value in PC")
        self.pipe.doPipeNext() #WB
        mylogger.info("TestCase: test_doPipe_JAL SUCCESSFUL")

    def test_doPipe_LW(self):
        mylogger.info("TestCase: test_doPipe_LW START")
        self.insTest = BitArray(hex='0xFFFFFFFF')
        self.storage.setW(0, self.ins5)
        self.storage.setW(256, self.insTest)
        self.r2 = BitArray(int=252, length=32) #r2
        self.regb.Bank[2].setVal(self.r2)
        self.pipe.doPipeNext() #IF
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0x8C410004').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        self.pipe.doPipeNext() #ID
        self.assertEqual(self.pipe.Imm.getVal().int, 4 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 252 , "Wrong Value in A")
        self.pipe.doPipeNext() #EX
        self.assertEqual(self.pipe.AO.getVal().int, 256 , "Wrong Value in AO")
        self.pipe.doPipeNext() #MEM
        self.assertEqual(self.pipe.LMD.getVal().int, BitArray(hex='0xFFFFFFFF').int , "Wrong Value in LMD")
        self.pipe.doPipeNext() #WB
        self.assertEqual(self.regb.getRegByID(1).getVal().int, BitArray(hex='0xFFFFFFFF').int , "Wrong Value in RD")
        mylogger.info("TestCase: test_doPipe_LW SUCCESSFUL")

    def test_doPipe_LBU(self):
        mylogger.info("TestCase: test_doPipe_LBU START")
        self.insTest = BitArray(hex='0xFFFFFFF4')
        self.storage.setW(0, self.ins6)
        self.storage.setW(256, self.insTest)
        self.r2 = BitArray(int=255, length=32) #r2
        self.regb.Bank[2].setVal(self.r2)
        self.pipe.doPipeNext() #IF
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0x90410004').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        self.pipe.doPipeNext() #ID
        self.assertEqual(self.pipe.Imm.getVal().int, 4 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 255 , "Wrong Value in A")
        self.pipe.doPipeNext() #EX
        self.assertEqual(self.pipe.AO.getVal().int, 259 , "Wrong Value in AO")
        self.pipe.doPipeNext() #MEM
        self.assertEqual(self.pipe.LMD.getVal().int, 244 , "Wrong Value in LMD")
        self.pipe.doPipeNext() #WB
        self.assertEqual(self.regb.getRegByID(1).getVal().int, 244 , "Wrong Value in RD")
        mylogger.info("TestCase: test_doPipe_LBU SUCCESSFUL")


    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        del cls.regb
        del cls.storage
        del cls.alu
        del cls.pipe
        return super().tearDownClass()