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

        """program counter""" 
        self.PC = 0
        """memory is a list"""
        self.memory = 0

    #The game will be loaded into memory, so retrieve the next byte
    def fetch_byte(self):
        byte = self.memory[self.PC]
        self.PC += 1
        return byte
    
    def fetch_two_bytes(self):
        high_byte = self.memory[self.PC]
        low_byte = self.memory[self.PC+1]
        self.PC += 2 
        data = high_byte << 8 | low_byte
        return data

    #MEMORY IS NOT RESET FOR TESTING PURPOSES
    def test_reset(self):
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
        self.Z = False
        self.S = False
        self.P = False
        self.CY = False
        self.AC = False
        self.PC = 0

    
#--------------------------------------------------#

# testing
cpu = Cpu()
# step 1. load spaceinvaders into memory
with open("invaders", "rb") as b_file:
    cpu.memory = bytearray(b_file.read())

assert cpu.memory[0] == 0x00
assert cpu.memory[9] == 0xc5
assert cpu.memory[len(cpu.memory)-1] == 0x00

data = cpu.fetch_byte()
assert data == 0x00

cpu.test_reset()

data = cpu.fetch_two_bytes()
assert data == 0x00
data = cpu.fetch_two_bytes()
assert data == 0x00
data = cpu.fetch_two_bytes()
assert data == 0x00
data = cpu.fetch_two_bytes()
assert data == 0x00



#--------------------------------------------------#

#set register BC within this function
def set_register_BC(self, high_byte, low_byte):
    self.BC = high_byte << 8 | low_byte # (high_byte << 8 + low_byte) works too
    self.PC += 3 
    return #incomplete function

#set register DE within this function
def set_register_DE(self, high_byte, low_byte):
    self.DE = high_byte << 8 | low_byte
    self.PC += 3 
    return #incomplete function

#set register HL within this function
def set_register_HL(self, high_byte, low_byte):
    self.HL = high_byte << 8 | low_byte
    self.PC += 3 
    return #incomplete function

#set SP within this function
def set_register_SP(self, high_byte, low_byte):
    self.SP = high_byte << 8 | low_byte
    self.PC += 3 
    return #incomplete function

#--------------------------------------------------#

#write 16 bit number to given register pair
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

def LXI_H(self):
    byte_two = self.fetch_byte()
    byte_three = self.fetch_byte()
    self.set_register_HL(byte_two,byte_three)
    return

def LXI_SP(self):
    byte_two = self.fetch_byte()
    byte_three = self.fetch_byte()
    self.set_register_SP(byte_two,byte_three)
    return

#--------------------------------------------------#

def read_instruction(self, instruction): 
    #for now I kept it as instruction (above), need to figure out where it's read from, memory?
    if(instruction == '00'):
        pass

    if(instruction == '01'):
        self.LXI_B()
