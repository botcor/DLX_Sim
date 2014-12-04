import unittest
from bitstring import *
from DLX_ALU import *

#create logger
mylogger = logging.getLogger("ALU")

class TestCasesALU(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mylogger.info("----------Unit Test ALU SetUp----------")
        cls.alu = DLX_ALU()
        return super().setUpClass()

#    Testcase Prototype
#    def test_(self):
#        mylogger.info("TestCase: test_ START")
#        self.a = BitArray(int=0, length=32)
#        self.b = BitArray(int=0, length=32)
#        self.assertEqual(self.alu. (self.a,self.b).int, 0, "")
#        mylogger.info("TestCase: test_ SUCCSESSFUL")

    #Testcases for Logical Operations
    def test_AND(self):
        mylogger.info("TestCase: test_AND START")
        self.a = BitArray(int=255, length=32)
        self.b = BitArray(int=15, length=32)
        self.assertEqual(self.alu.AND(self.a,self.b).int, 15, "Logical AND Failed")
        mylogger.info("TestCase: test_AND SUCCSESSFUL")

    def test_OR(self):
        mylogger.info("TestCase: test_OR START")
        self.a = BitArray(int=255, length=32)
        self.b = BitArray(int=15, length=32)
        self.assertEqual(self.alu.OR(self.a,self.b).int, 255, "Logical OR Failed")
        mylogger.info("TestCase: test_OR SUCCSESSFUL")

    def test_XOR(self):
        mylogger.info("TestCase: test_XOR START")
        self.a = BitArray(int=255, length=32)
        self.b = BitArray(int=15, length=32)
        self.assertEqual(self.alu.XOR(self.a,self.b).int, 240, "Logical XOR Failed")
        mylogger.info("TestCase: test_XOR SUCCSESSFUL")


    #Testcases for Bitshift Operations
    def test_SRA1(self):
        mylogger.info("TestCase: test_SRA1 START")
        self.a = BitArray(int=15, length=32)
        self.b = BitArray(int=1, length=32)
        self.assertEqual(self.alu.SRA(self.a,self.b).int, 7, "Shift Right Arithemtic 1 Failed")
        mylogger.info("TestCase: test_SRA1 SUCCSESSFUL")

    def test_SRA2(self):
        mylogger.info("TestCase: test_SRA2 START")
        self.a = BitArray(int=-2147483633, length=32)
        self.b = BitArray(int=1, length=32)
        self.assertEqual(self.alu.SRA(self.a,self.b).int, -1073741817, "Shift Right Arithemtic 2 Failed, Wrong Sign Extension")
        mylogger.info("TestCase: test_SRA2 SUCCSESSFUL")

    def test_SRL1(self):
        mylogger.info("TestCase: test_SRL1 START")
        self.a = BitArray(int=15, length=32)
        self.b = BitArray(int=1, length=32)
        self.assertEqual(self.alu.SRL(self.a,self.b).int, 7, "Shift Right Logical 1 Failed")
        mylogger.info("TestCase: test_SRL1 SUCCSESSFUL")

    def test_SRL2(self):
        mylogger.info("TestCase: test_SRL2 START")
        self.a = BitArray(int=-2147483633 , length=32)
        self.b = BitArray(int=1, length=32)
        self.assertEqual(self.alu.SRL(self.a,self.b).int, 1073741831, "Shift Right Logical 2 Failed")
        mylogger.info("TestCase: test_SRL2 SUCCSESSFUL")

    def test_SLL1(self):
        mylogger.info("TestCase: test_SLL1 START")
        self.a = BitArray(int=15, length=32)
        self.b = BitArray(int=1, length=32)
        self.assertEqual(self.alu.SLL(self.a,self.b).int, 30, "Shift Left Logical 1 Failed")
        mylogger.info("TestCase: test_SLL1 SUCCSESSFUL")
        
    def test_SLL2(self):
        mylogger.info("TestCase: test_SLL2 START")
        self.a = BitArray(int=-2147483633, length=32)
        self.b = BitArray(int=1, length=32)
        self.assertEqual(self.alu.SLL(self.a,self.b).int, 30, "Shift Left Logical 2 Failed")
        mylogger.info("TestCase: test_SLL2 SUCCSESSFUL") 
     
    #Testcases Unsigned Conditional Operations      
    def test_SEQU1(self):
        mylogger.info("TestCase: test_SEQU1 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SEQU(self.a,self.b).uint, 1, "Set Equal Unsigned 1 Failed")
        mylogger.info("TestCase: test_SEQU1 SUCCSESSFUL")
   
    def test_SEQU2(self):
        mylogger.info("TestCase: test_SEQU2 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=1, length=32)
        self.assertEqual(self.alu.SEQU(self.a,self.b).uint, 0, "Set Equal Unsigned 2 Failed")
        mylogger.info("TestCase: test_SEQU2 SUCCSESSFUL") 
        
    def test_SNEU1(self):
        mylogger.info("TestCase: test_SNEU1 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=1, length=32)
        self.assertEqual(self.alu.SNEU(self.a,self.b).uint, 1, "Set Not Equal Unsigned 1 Failed")
        mylogger.info("TestCase: test_SNEU1 SUCCSESSFUL")
        
    def test_SNEU2(self):
        mylogger.info("TestCase: test_SNEU2 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SNEU(self.a,self.b).uint, 0, "Set Not Equal Unsigned 2Failed")
        mylogger.info("TestCase: test_SNEU2 SUCCSESSFUL")
   
    def test_SLTU1(self):
        mylogger.info("TestCase: test_SLTU1 START")
        self.a = BitArray(uint=1, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SLTU(self.a,self.b).uint, 1, "Set Less Than Unsigned 1 Failed")
        mylogger.info("TestCase: test_SLTU1 SUCCSESSFUL")
       
    def test_SLTU2(self):
        mylogger.info("TestCase: test_SLTU2 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=1, length=32)
        self.assertEqual(self.alu.SLTU(self.a,self.b).uint, 0, "Set Less Than Unsigned 2 Failed")
        mylogger.info("TestCase: test_SLTU2SUCCSESSFUL")
       
    def test_SLTU3(self):
        mylogger.info("TestCase: test_SLTU3 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SLTU(self.a,self.b).uint, 0, "Set Less Than Unsigned 3 Failed")
        mylogger.info("TestCase: test_SLTU3 SUCCSESSFUL")
        
    def test_SGTU1(self):
        mylogger.info("TestCase: test_SGTU1 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=1, length=32)
        self.assertEqual(self.alu.SGTU(self.a,self.b).uint, 1, "Set Greater Than Unsigned 2 Failed")
        mylogger.info("TestCase: test_SGTU1 SUCCSESSFUL")
        
    def test_SGTU2(self):
        mylogger.info("TestCase: test_SGTU2 START")
        self.a = BitArray(uint=1, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SGTU(self.a,self.b).uint, 0, "Set Greater Than Unsigned 3 Failed")
        mylogger.info("TestCase: test_SGTU2 SUCCSESSFUL")
        
    def test_SGTU3(self):
        mylogger.info("TestCase: test_SGTU3 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SGTU(self.a,self.b).uint, 0, "Set Greater Than Unsigned 1 Failed")
        mylogger.info("TestCase: test_SGTU3 SUCCSESSFUL")  
     
    def test_SLEU1(self):
        mylogger.info("TestCase: test_SLEU1 START")
        self.a = BitArray(uint=1, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SLEU(self.a,self.b).uint, 1, "Set Less Or Equal Unsigned 1 Failed")
        mylogger.info("TestCase: test_SLEU1 SUCCSESSFUL")
       
    def test_SLEU2(self):
        mylogger.info("TestCase: test_SLEU2 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=1, length=32)
        self.assertEqual(self.alu.SLEU(self.a,self.b).uint, 0, "Set Less Or Equal Unsigned 2 Failed")
        mylogger.info("TestCase: test_SLEU2 SUCCSESSFUL")
       
    def test_SLEU3(self):
        mylogger.info("TestCase: test_SLEU3 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SLEU(self.a,self.b).uint, 1, "Set Less Or Equal Unsigned 3 Failed")
        mylogger.info("TestCase: test_SLEU3 SUCCSESSFUL")
        
    def test_SGEU1(self):
        mylogger.info("TestCase: test_SGEU1START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=1, length=32)
        self.assertEqual(self.alu.SGEU(self.a,self.b).uint, 1, "Set Greater Or Equal Unsigned 1 Failed")
        mylogger.info("TestCase: test_SGEU1 SUCCSESSFUL")
        
    def test_SGEU2(self):
        mylogger.info("TestCase: test_SGEU2 START")
        self.a = BitArray(uint=1, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SGEU(self.a,self.b).uint, 0, "Set Greater Or Equal Unsigned 2 Failed")
        mylogger.info("TestCase: test_SGEU2 SUCCSESSFUL")
        
    def test_SGEU3(self):
        mylogger.info("TestCase: test_SGEU3 START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SGEU(self.a,self.b).uint, 1, "Set Greater Or Equal Unsigned 3 Failed")
        mylogger.info("TestCase: test_SGEU3 SUCCSESSFUL")
        
    #Testcases Conditional Operations      
    def test_SEQ1(self):
        mylogger.info("TestCase: test_SEQ1 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SEQ(self.a,self.b).int, 1, "Set Equal  1 Failed")
        mylogger.info("TestCase: test_SEQ1 SUCCSESSFUL")
   
    def test_SEQU2(self):
        mylogger.info("TestCase: test_SEQ2 START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SEQ(self.a,self.b).int, 0, "Set Equal  2 Failed")
        mylogger.info("TestCase: test_SEQ2 SUCCSESSFUL") 
        
    def test_SNE1(self):
        mylogger.info("TestCase: test_SNE1 START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SNE(self.a,self.b).int, 1, "Set Not Equal  1 Failed")
        mylogger.info("TestCase: test_SNE1 SUCCSESSFUL")
        
    def test_SNE2(self):
        mylogger.info("TestCase: test_SNE2 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SNE(self.a,self.b).int, 0, "Set Not Equal  2 Failed")
        mylogger.info("TestCase: test_SNE2 SUCCSESSFUL")
   
    def test_SLT1(self):
        mylogger.info("TestCase: test_SLT1 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=8, length=32)
        self.assertEqual(self.alu.SLT(self.a,self.b).int, 1, "Set Less Than  1 Failed")
        mylogger.info("TestCase: test_SLT1 SUCCSESSFUL")
       
    def test_SLT2(self):
        mylogger.info("TestCase: test_SLT2 START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SLT(self.a,self.b).int, 0, "Set Less Than  2 Failed")
        mylogger.info("TestCase: test_SLT2SUCCSESSFUL")
       
    def test_SLT3(self):
        mylogger.info("TestCase: test_SLT3 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SLT(self.a,self.b).int, 0, "Set Less Than  3 Failed")
        mylogger.info("TestCase: test_SLT3 SUCCSESSFUL")
        
    def test_SGT1(self):
        mylogger.info("TestCase: test_SGT1 START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SGT(self.a,self.b).int, 1, "Set Greater Than  2 Failed")
        mylogger.info("TestCase: test_SGT1 SUCCSESSFUL")
        
    def test_SGT2(self):
        mylogger.info("TestCase: test_SGT2 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=8, length=32)
        self.assertEqual(self.alu.SGT(self.a,self.b).int, 0, "Set Greater Than  3 Failed")
        mylogger.info("TestCase: test_SGT2 SUCCSESSFUL")
        
    def test_SGT3(self):
        mylogger.info("TestCase: test_SGT3 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SGT(self.a,self.b).int, 0, "Set Greater Than  1 Failed")
        mylogger.info("TestCase: test_SGT3 SUCCSESSFUL")  
     
    def test_SLE1(self):
        mylogger.info("TestCase: test_SLE1 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=8, length=32)
        self.assertEqual(self.alu.SLE(self.a,self.b).int, 1, "Set Less Or Equal  1 Failed")
        mylogger.info("TestCase: test_SLE1 SUCCSESSFUL")
       
    def test_SLE2(self):
        mylogger.info("TestCase: test_SLE2 START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SLE(self.a,self.b).int, 0, "Set Less Or Equal  2 Failed")
        mylogger.info("TestCase: test_SLE2 SUCCSESSFUL")
       
    def test_SLE3(self):
        mylogger.info("TestCase: test_SLE3 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SLE(self.a,self.b).int, 1, "Set Less Or Equal  3 Failed")
        mylogger.info("TestCase: test_SLE3 SUCCSESSFUL")
        
    def test_SGE1(self):
        mylogger.info("TestCase: test_SGE1START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SGE(self.a,self.b).int, 1, "Set Greater Or Equal  1 Failed")
        mylogger.info("TestCase: test_SGE1 SUCCSESSFUL")
        
    def test_SGE2(self):
        mylogger.info("TestCase: test_SGE2 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=8, length=32)
        self.assertEqual(self.alu.SGE(self.a,self.b).int, 0, "Set Greater Or Equal  2 Failed")
        mylogger.info("TestCase: test_SGE2 SUCCSESSFUL")
        
    def test_SGE3(self):
        mylogger.info("TestCase: test_SGE3 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SGE(self.a,self.b).int, 1, "Set Greater Or Equal  3 Failed")
        mylogger.info("TestCase: test_SGE3 SUCCSESSFUL") 
        
        #Testcases Unsigned Arithmetic Operations
    def test_ADDU(self):
        mylogger.info("TestCase: test_ADDU START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.ADDU(self.a,self.b).uint, 16, "Unsigned Addition Failed")
        mylogger.info("TestCase: test_ADDU SUCCSESSFUL")

    def test_SUBU(self):
        mylogger.info("TestCase: test_SUBU START")
        self.a = BitArray(uint=8, length=32)
        self.b = BitArray(uint=8, length=32)
        self.assertEqual(self.alu.SUBU(self.a,self.b).uint, 0, "Unsigned Subtraction Failed")
        mylogger.info("TestCase: test_SUBU SUCCSESSFUL")

    def test_ADDU_overfl(self):
        mylogger.info("TestCase: test_ADDU_overfl START")
        self.a = BitArray(uint=4294967295, length=32)
        self.b = BitArray(uint=1, length=32)
        self.assertEqual(self.alu.ADDU(self.a,self.b).uint, 0, "Unsigned Addition with Overflow Failed")
        self.assertEqual(self.alu.overfl, 1, "Overflow was not detected")
        mylogger.info("TestCase: test_ADDU_overfl SUCCSESSFUL")

        
        #Testcases Arithmetic Operations  
    def test_ADD1(self):
        mylogger.info("TestCase: test_ADD1 START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=8, length=32)
        self.assertEqual(self.alu.ADD(self.a,self.b).int, 16, "Signed Addition 1 Failed")
        mylogger.info("TestCase: test_ADD1 SUCCSESSFUL") 
        
    def test_ADD2(self):
        mylogger.info("TestCase: test_ADD2 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=8, length=32)
        self.assertEqual(self.alu.ADD(self.a,self.b).int, 0, "Signed Addition 2 Failed")
        mylogger.info("TestCase: test_ADD2 SUCCSESSFUL")      
    
    def test_ADD3(self):
        mylogger.info("TestCase: test_ADD3 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.ADD(self.a,self.b).int, -16, "Signed Addition 3 Failed")
        mylogger.info("TestCase: test_ADD3 SUCCSESSFUL")
        
    def test_SUB1(self):
        mylogger.info("TestCase: test_SUB1 START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=8, length=32)
        self.assertEqual(self.alu.SUB(self.a,self.b).int, 0, "Signed Subtraction 1 Failed")
        mylogger.info("TestCase: test_SUB1 SUCCSESSFUL")  
        
    def test_SUB2(self):
        mylogger.info("TestCase: test_SUB2 START")
        self.a = BitArray(int=8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SUB(self.a,self.b).int, 16, "Signed Subtraction 2 Failed")
        mylogger.info("TestCase: test_SUB2 SUCCSESSFUL")  
     
    def test_SUB3(self):
        mylogger.info("TestCase: test_SUB3 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=8, length=32)
        self.assertEqual(self.alu.SUB(self.a,self.b).int, -16, "Signed Subtraction 3 Failed")
        mylogger.info("TestCase: test_SUB3 SUCCSESSFUL")  
        
    def test_SUB4(self):
        mylogger.info("TestCase: test_SUB4 START")
        self.a = BitArray(int=-8, length=32)
        self.b = BitArray(int=-8, length=32)
        self.assertEqual(self.alu.SUB(self.a,self.b).int, 0, "Signed Subtraction 4 Failed")
        mylogger.info("TestCase: test_SUB4 SUCCSESSFUL")      
               
        


    @classmethod
    def tearDownClass(cls):
        mylogger.info("----------Unit Test ALU TearDown----------\n")
        del cls.alu
        return super().tearDownClass()
