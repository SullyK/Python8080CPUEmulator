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
        self.memory = []

    #The game will be loaded into memory, so retrieve the next byte
    def fetch_byte(self):
        byte = self.memory[self.PC]
        self.PC += 1
        return byte
    
    def fetch_two_bytes(self):
        low_byte = self.memory[self.PC] # The CPU is low endian so we start with the low byte
        high_byte = self.memory[self.PC+1]
        self.PC += 2 
        data = high_byte << 8 | low_byte  #(high_byte << 8 + low_byte) works too
        # print(hex(data)) #debugging
        return data

    #--------------------------------------------------#

    #setting the 16 bit registers 
    def set_register_BC(self, data):
        self.BC = data 
        return 

    def set_register_DE(self,data):
        self.DE = data
        return 

    def set_register_HL(self, data):
        self.HL = data
        return 

    def set_register_SP(self, data):
        self.SP = data
        return 

    #--------------------------------------------------#

    #write 16 bit number to given register pair
    def LXI_B(self):
        data_16 = self.fetch_two_bytes()
        self.set_register_BC(data_16)
        return

    def LXI_D(self):
        data_16 = self.fetch_two_bytes()
        self.set_register_DE(data_16)
        return

    def LXI_H(self):
        data_16 = self.fetch_two_bytes()
        self.set_register_HL(data_16)
        return

    def LXI_SP(self):
        data_16 = self.fetch_two_bytes()
        self.set_register_SP(data_16)
        return

    def STAX_B(self):
        addr = self.BC
        self.memory[addr] = self.A & 0xFF     
        return                                #@@@ refactor this?

    def STAX_B(self):
        addr = self.BC
        self.memory[addr] = self.A & 0xFF    
        return
    

    #--------------------------------------------------#

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
  
    def read_instruction(self): 
        op_code = self.memory[self.PC]
        match op_code:
            case 0x00:
                return
            case 0x01:
                self.LXI_B()
                return
            case 0x02:
                self.STAX_B()
                return
            

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
data = cpu.fetch_two_bytes()
assert data == 0x18d4
data = cpu.fetch_two_bytes()
data = cpu.fetch_two_bytes()
assert data == 0xc5f5
cpu.test_reset()

