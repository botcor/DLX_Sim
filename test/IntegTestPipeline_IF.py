import unittest
import sys
import logging.config
from bitstring import *
from DLX_Register import *
from DLX_Speicher import *
from DLX_Pipeline import *


class TestCasesPipe_IF(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create logger
        mylogger = logging.getLogger("Pipeline")
        mylogger.info("----------Unit Test Pipeline SetUp----------")
        cls.a = BitArray(int=255, length=32)
        cls.regb = DLX_Reg_Bank()
        cls.storage = DLX_Speicher()
        #fill data storage with testvalues: 0xDEADBEEF, 0xFACEBAFF
        cls.ins1 = BitArray(hex='0xdeadbeef')
        cls.ins2 = BitArray(hex='0xFACEBAFF')
        cls.ins3 = BitArray(hex='0xABCDE000')
        cls.storage.setW(0, cls.ins1)
        cls.storage.setW(4, cls.ins2)
        cls.storage.setW(8, cls.ins3)
        cls.alu = 0
        cls.pipe = DLX_Pipeline(cls.storage, cls.alu, cls.regb)
        return super().setUpClass()


    def test_doIF(self):
        mylogger.info("TestCase: test_doIF START")
        self.pipe.doIF()
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0xDEADBEEF').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint + 4, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        mylogger.info("TestCase: test_doIF SUCCESSFUL")

    def test_doIF2x(self):
        mylogger.info("TestCase: test_doIF2x START")
        self.pipe.doIF()
        self.pipe.doIF()
        self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0xABCDE000').hex , "Wrong Value in IR")
        self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint + 4, "Wrong Value in NPC")
        self.assertEqual(self.pipe.insFIFO[0], self.pipe.IR.getVal() , "")
        mylogger.info("TestCase: test_doIF2x SUCCESSFUL")

    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        del cls.regb
        del cls.storage
        del cls.alu
        del cls.pipe
        return super().tearDownClass()
