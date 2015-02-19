import unittest
import logging
from bitstring import *
from DLX_Register import *
from DLX_Speicher import *
from DLX_Pipeline import *


class TestCasesPipe_ID(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create logger
        mylogger = logging.getLogger("Pipeline")
        mylogger.info("----------Unit Test Pipeline SetUp----------")
        cls.a = BitArray(int=25, length=32)
        cls.b = BitArray(int=8, length=32)
        cls.c = BitArray(int=1, length=32)
        cls.regb = DLX_Reg_Bank()
        cls.regb.Bank[31].setVal(cls.a)
        cls.regb.Bank[3].setVal(cls.b)
        cls.regb.Bank[2].setVal(cls.c)
        cls.storage = 0
        cls.alu = 0
        cls.pipe = DLX_Pipeline(cls.storage, cls.alu, cls.regb)
        return super().setUpClass()

    def test_doID_I1(self):
        mylogger.info("TestCase: test_doID_I1 START")
        #ADDI r15, r3, 255
        self.ins = BitArray(hex='0x206F00FF')
        self.pipe.IR.setVal(self.ins)
        self.pipe.doID()
        self.assertEqual(self.pipe.Imm.getVal().int, 255 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 8 , "Wrong Value in A")
        mylogger.info("TestCase: test_doID_I1 SUCCESSFUL")

    def test_doID_I2(self):
        mylogger.info("TestCase: test_doID_I2 START")
        #ADDI r15, r3, -255
        self.ins = BitArray(hex='0x206FFF01')
        self.pipe.IR.setVal(self.ins)
        self.pipe.doID()
        self.assertEqual(self.pipe.Imm.getVal().int, -255 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 8 , "Wrong Value in A")
        mylogger.info("TestCase: test_doID_I2 SUCCESSFUL")

    def test_doID_I3(self):
        mylogger.info("TestCase: test_doID_I3 START")
        #ADDUI r15, r3, -255
        self.ins = BitArray(hex='0x2460FF01')
        self.pipe.IR.setVal(self.ins)
        self.pipe.doID()
        self.assertEqual(self.pipe.Imm.getVal().int, 65281 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 8 , "Wrong Value in A")
        mylogger.info("TestCase: test_doID_I3 SUCCESSFUL")

    def test_doID_I4(self):
        mylogger.info("TestCase: test_doID_I4 START")
        #ADDUI r15, r3, 255
        self.ins = BitArray(hex='0x246000FF')
        self.pipe.IR.setVal(self.ins)
        self.pipe.doID()
        self.assertEqual(self.pipe.Imm.getVal().int, 255 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 8 , "Wrong Value in A")
        mylogger.info("TestCase: test_doID_I4 SUCCESSFUL")

    def test_doID_R1(self):
        mylogger.info("TestCase: test_doID_R1 START")
        #SRL r15, r3, r2
        self.ins = BitArray(hex='0x00627806')
        self.pipe.IR.setVal(self.ins)
        self.pipe.doID()
        self.assertEqual(self.pipe.Imm.getVal().int, 6 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 8 , "Wrong Value in A")
        self.assertEqual(self.pipe.B.getVal().int, 1 , "Wrong Value in B")
        mylogger.info("TestCase: test_doID_R1 SUCCESSFUL")

    def test_doID_R2(self):
        mylogger.info("TestCase: test_doID_R2 START")
        #SRL r15, r31, r2
        self.ins = BitArray(hex='0x03E27806')
        self.pipe.IR.setVal(self.ins)
        self.pipe.doID()
        self.assertEqual(self.pipe.Imm.getVal().int, 6 , "Wrong Value in Imm")
        self.assertEqual(self.pipe.A.getVal().int, 25, "Wrong Value in A")
        self.assertEqual(self.pipe.B.getVal().int, 1 , "Wrong Value in B")
        mylogger.info("TestCase: test_doID_R2 SUCCESSFUL")

    def test_doID_J1(self):
        mylogger.info("TestCase: test_doID_J1 START")
        #J 8
        self.ins = BitArray(hex='0x08000008')
        self.pipe.IR.setVal(self.ins)
        self.pipe.doID()
        self.assertEqual(self.pipe.Imm.getVal().int, 8 , "Wrong Value in Imm")
        mylogger.info("TestCase: test_doID_J1 SUCCESSFUL")

    def test_doID_J2(self):
        mylogger.info("TestCase: test_doID_J2 START")
        #J 8
        self.ins = BitArray(hex='0x0BFFFFF8')
        self.pipe.IR.setVal(self.ins)
        self.pipe.doID()
        self.assertEqual(self.pipe.Imm.getVal().int, -8 , "Wrong Value in Imm")
        mylogger.info("TestCase: test_doID_J2 SUCCESSFUL")


    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        del cls.regb
        del cls.storage
        del cls.alu
        del cls.pipe
        return super().tearDownClass()
