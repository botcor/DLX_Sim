import unittest
import sys
sys.path.append('../src')
import logging.config
from UnitTestsALU import *
from UnitTestsReg import *
from IntegTestPipeline_IF import *
from IntegTestPipeline_ID import *

class TestHandler:
    def __init__(self):
        pass
 
    def write(self, string):
        # write to console
        print(string)
        # write to logger
        test_logger.info(string)
 
    def close(self):
        pass
    def flush(self):
        pass


#configure logger
logging.config.fileConfig("logging.conf")

#create logger
test_logger = logging.getLogger("TESTRUNNER")

test_logger.info("########## START TESTRUN ##########")

original_stderr = sys.stderr
sys.stderr = TestHandler()


testmodules = [
    #'UnitTestsALU',
    #'UnitTestsReg',
    # 'IntegTestPipeline_IF',
    #'IntegTestPipeline_ID',
    # 'IntegTestPipeline_EX',
    #'IntegTestPipeline_MEM',
    #'UnitTestSim',
    'IntegTestPipeline'
    ]

suite = unittest.TestSuite()

for t in testmodules:
    suite.addTest(unittest.TestLoader().loadTestsFromName(t))

testResult = unittest.TextTestRunner(verbosity=2).run(suite)

sys.stderr = original_stderr
test_logger.info("########## FINISHED TESTRUN ##########\n")
