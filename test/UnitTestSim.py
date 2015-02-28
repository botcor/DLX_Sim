import unittest
import sys
import logging.config
from bitstring import *
from DLX_Speicher import *
from Sim import *


class TestCasesSim(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create logger
        mylogger = logging.getLogger("Simulator")        
        mylogger.info("----------Unit Test Simulator SetUp----------")
        cls.sim = Simulator()
        return super().setUpClass()

    def test_read(self):
        mylogger.info("TestCase: test_read START")
        self.sim.collectData("test.dlx")

        self.assertEqual(self.sim.storage.getW(0).hex, '00000007' , "Storage has incorrect value")
        self.assertEqual(self.sim.storage.getW(4).hex, '00000003' , "Storage has incorrect value")
        self.assertEqual(self.sim.storage.getW(8).hex, '8c010000' , "Storage has incorrect value")
        self.assertEqual(self.sim.storage.getW(12).hex, 'ac010004' , "Storage has incorrect value")
        self.assertEqual(self.sim.storage.getW(16).hex, '44000000' , "Storage has incorrect value")
        mylogger.info("TestCase: test_read SUCCESSFUL")


    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Simulator TearDown----------\n")
        del cls.sim
        return super().tearDownClass()