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
        cls.a = BitArray(int=25, length=32)
        cls.b = BitArray(int=8, length=32)
        cls.c = BitArray(int=1, length=32)
        #fill data storage with testvalues: 
        cls.ins1 = BitArray(hex='0x206F00FF') #ADDI r15, r3, 255
        cls.ins2 = BitArray(hex='0x11111111')
        cls.ins3 = BitArray(hex='0xABCDE000')
        cls.regb.Bank[31].setVal(cls.a)
        cls.regb.Bank[3].setVal(cls.b)
        cls.regb.Bank[2].setVal(cls.c)
        cls.storage.setW(0, cls.ins1)
        cls.storage.setW(4, cls.ins2)
        cls.storage.setW(8, cls.ins3)
        cls.alu = DLX_ALU()
        cls.pipe = DLX_Pipeline(cls.storage, cls.alu, cls.regb)
        return super().setUpClass()


    def test_doPipe(self):
        mylogger.info("TestCase: test_doPipe START")
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
        mylogger.info("TestCase: test_doPipe SUCCESSFUL")


    def test_insFIFO(self):
        mylogger.info("TestCase: test_insFIFO START")
        self.pipe.ResetPipeline()
        self.pipe.doPipeNext() #IF
        mylogger.debug("insFIFO after IF %s",self.pipe.insFIFO[0] )
        #self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        self.pipe.doPipeNext() #ID
        mylogger.debug("insFIFO after ID %s",self.pipe.insFIFO[1] )
        self.pipe.doPipeNext() #EX
        mylogger.debug("insFIFO after EX %s",self.pipe.insFIFO[2] )
        self.pipe.doPipeNext() #MEM
        mylogger.debug("insFIFO after MEM %s",self.pipe.insFIFO[3] )
        self.pipe.doPipeNext() #WB
        mylogger.debug("insFIFO after WB %s",self.pipe.insFIFO[4] )
        mylogger.info("TestCase: test_insFIFO SUCCESSFUL")

    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        del cls.regb
        del cls.storage
        del cls.alu
        del cls.pipe
        return super().tearDownClass()