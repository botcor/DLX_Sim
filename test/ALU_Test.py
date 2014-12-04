import sys
sys.path.append("./src")
import logging
import logging.config
import logging.handlers
from bitstring import * 
from DLX_ALU import *

#configure logger
logging.config.fileConfig("logging.conf")

#create logger
my_logger = logging.getLogger("ALU")

alu = DLX_ALU()
a = BitArray(int=8, length=32)
b = BitArray(int=8, length=32)
x = BitArray()

x = alu.ADD(a,b)
y = alu.ADDU(a,b)
print("ADD: " + repr(x) )
print("ADDU: " + repr(y) )

x = alu.SUB(a,b)
y = alu.SUBU(a,b)
print("SUBU: " + repr(x) )
print("SUB: " + repr(y) )

x = alu.AND(a,b)
y = alu.OR(a,b)
print("AND: " + repr(x) )
print("OR: " + repr(y) )

x = alu.XOR(a,b)
y = alu.SRA(a,b)
print("XOR: " + repr(x) )
print("SRA: " + repr(y) )

x = alu.SLL(a,b)
y = alu.SRL(a,b)
print("SLL: " + repr(x) )
print("SRL: " + repr(y) )

x = alu.SEQU(a,b)
y = alu.SNEU(a,b)
print("SEQU: " + repr(x) )
print("SNEU: " + repr(y) )

x = alu.SLTU(a,b)
y = alu.SGTU(a,b)
print("SLTU: " + repr(x) )
print("SGTU: " + repr(y) )

x = alu.SLEU(a,b)
y = alu.SGEU(a,b)
print("SLEU: " + repr(x) )
print("SGEU: " + repr(y) )

x = alu.SEQ(a,b)
y = alu.SNE(a,b)
print("SEQ: " + repr(x) )
print("SNE: " + repr(y) )

x = alu.SLT(a,b)
y = alu.SGT(a,b)
print("SLT: " + repr(x) )
print("SGT: " + repr(y) )

x = alu.SLE(a,b)
y = alu.SGE(a,b)
print("SLE: " + repr(x) )
print("SGE: " + repr(y) )
