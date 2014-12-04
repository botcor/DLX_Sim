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
        cls.regb.setRegByID(31,cls.a)
        cls.regb.setRegByID(8,cls.b)
        cls.regb.setRegByID(1,cls.c)
        cls.storage = 0
        cls.alu = 0
        cls.pipe = DLX_Pipeline(cls.storage, cls.alu, cls.regb)
        return super().setUpClass()

    def test_doID_I1(self):
        mylogger.info("TestCase: test_doID_I1 START")
        #ADDI r15, r3, 255
        self.pipe.IR = '0x206F00FF'
        self.assertEqual(self.pipe.Imm.int, 255 , "")
        self.assertEqual(self.pipe.A.int, 8 , "")
        mylogger.info("TestCase: test_doID_I1 SUCCESSFUL")

    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        del cls.regb
        return super().tearDownClass()
