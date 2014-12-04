#!/usr/bin/env/python

import sys
sys.path.append("./src")
from bitstring import BitArray
from DLX_Translator import DLX_Disassembly

program = [ BitArray(int=5787683, length=32),
        BitArray(int=6051847, length=32),
        BitArray(int=605290496, length=32),
        BitArray(int=264905, length=32),
        BitArray(int=264267, length=32),
        BitArray(int=1343574080, length=32),
        BitArray(int=3671385, length=32),
        BitArray(int=3409178, length=32),
        BitArray(int=106505, length=32),
        BitArray(int=(-257399), length=32),
        BitArray(int=266377, length=32),
        BitArray(int=1209337984, length=32),
        BitArray(int=(-2357927), length=32),
        BitArray(int=6279, length=32),
        BitArray(int=270471, length=32),
        BitArray(int=1343561920, length=32),
        BitArray(int=(-1833639), length=32),
        BitArray(int=8328, length=32),
        BitArray(int=268424, length=32),
        BitArray(int=605290496, length=32),
        BitArray(int=(-2754), length=32),
        BitArray(int=63, length=32),
        BitArray(int=96, length=32),
        BitArray(int=128, length=32),
        BitArray(int=34, length=32),
        BitArray(int=2344, length=32),
        BitArray(int=0, length=32),
        BitArray(int=333, length=32),
        BitArray(int=(-34), length=32),
        BitArray(int=1, length=32),
        BitArray(int=444, length=32),
        BitArray(int=10, length=32),
        BitArray(int=1, length=32) ]

instruction_very_bad = 0xFFFFFFFF;


TL = DLX_Disassembly()
print(len(TL.l_instruction))
print(len(TL.l_opcode))
print(len(TL.l_funcins))
print(len(TL.l_funcopc))


for x in program:
    print(TL.OperationToAsm(x))
