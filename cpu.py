MEMORY_SIZE = 65536

class Cpu:
    def __init__(self):
        """create the registers"""
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.H = 0 
        self.L = 0 
        self.BC = 0
        self.DE = 0
        self.HL = 0
        self.SP = 0

        """condition flags"""
        self.Z = False
        self.S = False
        self.P = False
        self.CY = False
        self.AC = False

        """memory of max size, set to 0"""
        self.memory = [] * MEMORY_SIZE


    
    def read_instruction(self, instruction):
        if





