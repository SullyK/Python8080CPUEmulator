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
        self.memory = [] * 65536


    """"The game will be loaded into memory, so retrieve the next byte from the ROM?"""
    def fetch_byte(self):
        return #incomplete function

    """set register BC within this function"""
    def set_register_BC(self, high_end, low_end):
        self.BC = #how would they go into this? Pick up from here.
        return #incomplete function
    
    """set register DE within this function"""
    def set_register_DE(self, high_end, low_end):
        return #incomplete function


    """write 16 bit number to given register pair """
    def LXI_B(self):
        byte_two = self.fetch_byte()
        byte_three = self.fetch_byte()
        self.set_register_BC(byte_two,byte_three)
        return

    def LXI_D(self):
        byte_two = self.fetch_byte()
        byte_three = self.fetch_byte()
        self.set_register_DE(byte_two,byte_three)
        return



    def read_instruction(self, instruction): 
        #for now I kept it as instruction (above), need to figure out where it's read from, memory?
        if(instruction == '00'):
            pass

        if(instruction == '01'):
            self.LXI_B()
