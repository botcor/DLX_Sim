import unittest
import sys
import logging.config
from bitstring import *
from DLX_Register import *


class TestCasesReg(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create logger
        mylogger = logging.getLogger("Register")
        mylogger.info("----------Unit Test Register SetUp----------")
        cls.a = BitArray(int=255, length=32)
        cls.regb = DLX_Reg_Bank()
        return super().setUpClass()


    def test_regb(self):
        mylogger.info("TestCase: test_regb START")
        for i in range(1,32):
            self.regb.setRegByID(i,self.a)
        for i in range(1,32):
            self.assertEqual(self.regb.getRegByID(i).int, 255 , "Register has incorrect value")
        mylogger.info("TestCase: test_regb SUCCESSFUL")

    def test_reg0(self):
        mylogger.info("TestCase: test_reg0 START")
        self.regb.setRegByID(0,self.a)
        self.assertEqual(self.regb.getRegByID(0).int, 0 , "Register0 ist not 0")
        mylogger.info("TestCase: test_reg0 SUCCSESSFUL")      



    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Register TearDown----------\n")
        del cls.regb
        return super().tearDownClass()
