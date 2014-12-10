import unittest
import logging
from bitstring import *
from DLX_Register import *
from DLX_ALU import *
from DLX_Pipeline import *

class TestCasesPipe_EX(unittest.TestCase):

     @classmethod
     def setUpClass(cls):
        #create logger
        mylogger = logging.getLogger("Pipeline")
        mylogger.info("----------Unit Test Pipeline SetUp----------")
        cls.valueA = BitArray(int=8, length=32)
        cls.regb = DLX_Reg_Bank()
        cls.storage = 0
        cls.alu = DLX_ALU()
        cls.pipe = DLX_Pipeline(cls.storage, cls.alu, cls.regb)
        return super().setUpClass()

     def test_doEX_ADD(self):
        mylogger.info("TestCase: test_doEX_ADD START")
        self.ins = BitArray(hex='0x00000000')
        self.imm = BitArray(hex='0x20')
        self.valueB = BitArray(int=8, length=32)
        self.pipe.insFIFO[2] =    self.ins    
        self.pipe.A.setVal(self.valueA)
        self.pipe.B.setVal(self.valueB)
        self.pipe.Imm.setVal(self.imm)
        self.pipe.doEX()
        self.assertEqual(self.pipe.AO.getVal().int, 16 , "Wrong Value in AO")
        mylogger.info("TestCase: test_doEX_ADD SUCCESSFUL")

     def test_doEX_ADDU(self):
        mylogger.info("TestCase: test_doEX_ADDU START")
        self.ins = BitArray(hex='0x00000000')
        self.imm = BitArray(hex='0x21')
        self.valueB = BitArray(int=8, length=32)
        self.pipe.insFIFO[2] =    self.ins    
        self.pipe.A.setVal(self.valueA)
        self.pipe.B.setVal(self.valueB)
        self.pipe.Imm.setVal(self.imm)
        self.pipe.doEX()
        self.assertEqual(self.pipe.AO.getVal().int, 16 , "Wrong Value in AO")
        mylogger.info("TestCase: test_doEX_ADDU SUCCESSFUL")

     def test_doEX_ADDI(self):
        mylogger.info("TestCase: test_doEX_ADDI START")
        self.ins = BitArray(hex='0x20000000')
        self.imm = BitArray(int=8, length=32)
        self.pipe.insFIFO[2] =    self.ins    
        self.pipe.A.setVal(self.valueA)
        self.pipe.Imm.setVal(self.imm)
        self.pipe.doEX()
        self.assertEqual(self.pipe.AO.getVal().int, 16 , "Wrong Value in AO")
        mylogger.info("TestCase: test_doEX_ADDI SUCCESSFUL")

     def test_doEX_ADDUI(self):
        mylogger.info("TestCase: test_doEX_ADDUI START")
        self.ins = BitArray(hex='0x24000000')
        self.imm = BitArray(int=8, length=32)
        self.pipe.insFIFO[2] =    self.ins    
        self.pipe.A.setVal(self.valueA)
        self.pipe.Imm.setVal(self.imm)
        self.pipe.doEX()
        self.assertEqual(self.pipe.AO.getVal().int, 16 , "Wrong Value in AO")
        mylogger.info("TestCase: test_doEX_ADDUI SUCCESSFUL")

     def test_doEX_SNEU1(self):
        mylogger.info("TestCase: test_doEX_SNEU1 START")
        self.ins = BitArray(hex='0x00000000')
        self.imm = BitArray(hex='0x11')
        self.valueB = BitArray(int=15, length=32)
        self.pipe.insFIFO[2] =    self.ins    
        self.pipe.A.setVal(self.valueA)
        self.pipe.B.setVal(self.valueB)
        self.pipe.Imm.setVal(self.imm)
        self.pipe.doEX()
        self.assertEqual(self.pipe.AO.getVal().int, 1, "Wrong Value in AO")
        mylogger.info("TestCase: test_doEX_SNEU1 SUCCESSFUL")

     def test_doEX_SNEU2(self):
        mylogger.info("TestCase: test_doEX_SNEU2 START")
        self.ins = BitArray(hex='0x00000000')
        self.imm = BitArray(hex='0x11')
        self.valueB = BitArray(int=8, length=32)
        self.pipe.insFIFO[2] =    self.ins    
        self.pipe.A.setVal(self.valueA)
        self.pipe.B.setVal(self.valueB)
        self.pipe.Imm.setVal(self.imm)
        self.pipe.doEX()
        self.assertEqual(self.pipe.AO.getVal().int, 0, "Wrong Value in AO")
        mylogger.info("TestCase: test_doEX_SNEU2 SUCCESSFUL")

     @classmethod
     def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        del cls.regb
        return super().tearDownClass()