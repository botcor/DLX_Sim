import unittest
import logging
from bitstring import *
from DLX_Register import *
from DLX_Speicher import *
from DLX_Pipeline import *


class TestCasesPipe_MEM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create logger
        mylogger = logging.getLogger("Pipeline")
        mylogger.info("----------Unit Test Pipeline SetUp----------")
        cls.storage = DLX_Speicher()
        #fill data storage with testvalues: 0xDEADBEEF, 0xFACEBAFF
        cls.ins1 = BitArray(hex='0xdeadbeef')
        cls.ins2 = BitArray(hex='0xFACEBAFF')
        cls.storage.setW(0, cls.ins1)
        cls.storage.setW(4, cls.ins2)
        cls.a = BitArray(hex='0x00000000')
        cls.regb = DLX_Reg_Bank()
        cls.regb.Bank[2].setVal(cls.a)       
        cls.alu = 0
        cls.pipe = DLX_Pipeline(cls.storage, cls.alu, cls.regb)
        return super().setUpClass()

    def test_doMEM_LHI(self):
        mylogger.info("TestCase: test_doMEM_LHI START")
        #LHI r1 8
        self.ins = BitArray(hex='0x3C010008')
        self.pipe.insFIFO[3] = self.ins 
        self.pipe.doMEM()
        self.assertEqual(self.pipe.LMD.getVal().int, 524288 , "Wrong Value in LMD")
        mylogger.info("TestCase: test_doMEM_LHI SUCCESSFUL")

    def test_doMEM_LW1(self):
        mylogger.info("TestCase: test_doMEM_LW1 START")
        #LW r1 4(r2)    r2 = 0
        self.ins = BitArray(hex='0x8C410004')
        self.pipe.insFIFO[3] = self.ins 
        self.pipe.doMEM()
        self.assertEqual(self.pipe.LMD.getVal().hex, BitArray(hex='0xFACEBAFF').hex , "Wrong Value in LMD")
        mylogger.info("TestCase: test_doMEM_LW1 SUCCESSFUL")

    def test_doMEM_LW2(self):
        mylogger.info("TestCase: test_doMEM_LW2 START")
        #LW r1 0(r2)    r2 = 4
        b = BitArray(hex='0x00000004')
        self.regb.Bank[2].setVal(b) 
        self.ins = BitArray(hex='0x8C410000')
        self.pipe.insFIFO[3] = self.ins 
        self.pipe.doMEM()
        self.assertEqual(self.pipe.LMD.getVal().hex, BitArray(hex='0xFACEBAFF').hex , "Wrong Value in LMD")
        mylogger.info("TestCase: test_doMEM_LW2 SUCCESSFUL")

    def test_doMEM_LBU(self):
        mylogger.info("TestCase: test_doMEM_LBU START")
        #LBU r1 4(r2)   r2 = 0
        b = BitArray(hex='0x00000004')
        self.regb.Bank[2].setVal(b) 
        self.ins = BitArray(hex='0x90410004')
        self.pipe.insFIFO[3] = self.ins 
        self.pipe.doMEM()
        self.assertEqual(self.pipe.LMD.getVal().hex, BitArray(hex='0x000000FA').hex , "Wrong Value in LMD")
        mylogger.info("TestCase: test_doMEM_LBU SUCCESSFUL")

    def test_doMEM_LB(self):
        mylogger.info("TestCase: test_doMEM_LB START")
        #LB r1 4(2)     r2 = 0
        b = BitArray(hex='0x00000004')
        self.regb.Bank[2].setVal(b) 
        self.ins = BitArray(hex='0x80410004')
        self.pipe.insFIFO[3] = self.ins 
        self.pipe.doMEM()
        # change r2 back to 0
        c = BitArray(hex='0x00000000')
        self.regb.Bank[2].setVal(c) 
        self.assertEqual(self.pipe.LMD.getVal().hex, BitArray(hex='0x000000FA').hex , "Wrong Value in LMD")
        mylogger.info("TestCase: test_doMEM_LB SUCCESSFUL")

    def test_doMEM_LHU1(self):
        mylogger.info("TestCase: test_doMEM_LHU1 START")
        #LHU r1 4(r2)   r2 = 0
        self.ins = BitArray(hex='0x94410004')
        self.pipe.insFIFO[3] = self.ins 
        self.pipe.doMEM()
        self.assertEqual(self.pipe.LMD.getVal().hex, BitArray(hex='0x0000FACE').hex , "Wrong Value in LMD")
        mylogger.info("TestCase: test_doMEM_LHU1 SUCCESSFUL")

    def test_doMEM_LHU2(self):
        mylogger.info("TestCase: test_doMEM_LHU2 START")
        #LHU r1 2(r2)   r2 = 0
        self.ins = BitArray(hex='0x94410002')
        self.pipe.insFIFO[3] = self.ins 
        self.pipe.doMEM()
        self.assertEqual(self.pipe.LMD.getVal().hex, BitArray(hex='0x0000BEEF').hex , "Wrong Value in LMD")
        mylogger.info("TestCase: test_doMEM_LHU2 SUCCESSFUL")

    def test_doMEM_LH(self):
        mylogger.info("TestCase: test_doMEM_LH START")
        #LHU r1 2(r2)   r2 = 0
        self.ins = BitArray(hex='0x84410004')
        self.pipe.insFIFO[3] = self.ins 
        self.pipe.doMEM()
        self.assertEqual(self.pipe.LMD.getVal().hex, BitArray(hex='0x0000FACE').hex , "Wrong Value in LMD")
        mylogger.info("TestCase: test_doMEM_LH SUCCESSFUL")




    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        del cls.regb
        return super().tearDownClass()