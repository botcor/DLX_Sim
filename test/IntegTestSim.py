import unittest
import sys
import logging.config
from bitstring import *
from Sim import *

#create logger
mylogger = logging.getLogger("Simulator")

class TestCasesSim(unittest.TestCase):

    @classmethod
    def setUpClass(cls):        
        mylogger.info("----------Unit Test Simulator SetUp----------")
        cls.sim = Simulator()
        return super().setUpClass()

    def test_sim(self):
        mylogger.info("TestCase: test_sim START")
        self.sim.collectData("simtest.dlx")
        self.sim.doPipe(20)
        mylogger.info("TestCase: test_sim SUCCESSFUL")

    def test_sim_haz(self):
        mylogger.info("TestCase: test_sim START")
        self.sim.collectData("simtest2.dlx")
        self.sim.doPipe(20)
        mylogger.info("TestCase: test_sim SUCCESSFUL")



    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Simulator TearDown----------\n")
        cls.sim.storage.reset()
        del cls.sim
        return super().tearDownClass()