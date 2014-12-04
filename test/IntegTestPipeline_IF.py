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
        #fill data storgae with testvalues: 0xDEADBEEF, 0xFACEBAFF, 0x0BADCEDE 0xAAAAAAAA
        cls.ins1 = BitArray(hex='0xdeadbeef')
        cls.ins2 = BitArray(hex='0xFACEBAFF')
        cls.ins3 = BitArray(hex='0x0BADCEDE')
        cls.ins4 = BitArray(hex='0xAAAAAAAA')
        cls.storage.setW(0, cls.ins1.hex)
        cls.storage.setW(4, cls.ins2.hex)
        cls.storage.setW(8, cls.ins3.hex)
        cls.storage.setW(12, cls.ins4.hex)
        cls.alu = 0
        cls.pipe = DLX_Pipeline(cls.storage, cls.alu, cls.regb)
        return super().setUpClass()

    def test_doIF(self):
        mylogger.info("TestCase: test_doIF START")
        self.pipe.doIF()
        self.assertEqual(self.pipe.IR.hex, '0xDEADBEEF' , "")
        self.assertEqual(self.pipe.NPC, self.pipe.PC + 4 , "")
        self.assertEqual(self.pipe.__insFIFO[0], self.pipe.IR , "")
        mylogger.info("TestCase: test_doIF SUCCESSFUL")

    def test_doIF2x(self):
        mylogger.info("TestCase: test_doIF2x START")
        self.pipe.doIF()
        self.pipe.doIF()
        self.assertEqual(self.pipe.IR.hex, '0xDEADBEEF' , "")
        self.assertEqual(self.pipe.NPC, self.pipe.PC + 4 , "")
        self.assertEqual(self.pipe.__insFIFO[0], self.pipe.IR , "")
        mylogger.info("TestCase: test_doIF2x SUCCESSFUL")

    def test_doIF2x(self):
        mylogger.info("TestCase: test_doIF2x START")
        self.pipe.doIF()
        self.pipe.PC = self.pipe.PC +4
        self.pipe.doIF()
        self.assertEqual(self.pipe.IR.hex, '0xFACEBAFF' , "")
        self.assertEqual(self.pipe.NPC, self.pipe.PC + 4 + 4, "")
        self.assertEqual(self.pipe.__insFIFO[0], self.pipe.IR , "")
        mylogger.info("TestCase: test_doIF2x SUCCESSFUL")

    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        del cls.regb
        return super().tearDownClass()
