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
        cls.sim = Simulator()      
        cls.sim.collectData("test.dlx")
        return super().setUpClass()


    def test_doPipe(self):
        mylogger.info("TestCase: test_doPipe START")
        self.sim.pipe.doPipeNext()
        #self.assertEqual(self.pipe.IR.getVal().hex, BitArray(hex='0xDEADBEEF').hex , "Wrong Value in IR")
        #self.assertEqual(self.pipe.NPC.getVal().uint, self.pipe.PC.getVal().uint + 4 , "Wrong Value in NPC")
        mylogger.info("TestCase: test_doPipe SUCCESSFUL")

    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test Pipeline TearDown----------\n")
        return super().tearDownClass()