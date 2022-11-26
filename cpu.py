def add_bits(hex):
    total = 0
    for i in range(8):
        total += ((hex >> i)& 1)
    return total
    
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

    def INX_B(self):
        self.BC = (self.BC + 1) & 0xFF #no carry over? what happens when over 255.
        return 

    def INR_B(self):
        self.B += 1 & 0xFF #The value of register b is incremented by one.
        #all flags are affected besides CY.
        self.Z = True if self.B == 0 else False
        # We need to get the first bit (this one-->(1)0000000)
        # if it isn't greater than 128 it is 0, else its 128 (which isn't 0, hence setting flag)
        self.S = True if self.B & 0x80 else False 
        self.P = True if add_bits(self.B) % 2 == 0 else False
        self.AC = 0 #@@@come back and complete
    
    def DCR_B(self):
        self.B -= 1 & 0xFF
        self.Z = True if self.B == 0 else False
        self.S = True if self.B & 0x80 else False
        self.P = True if add_bits(self.B) % 2 == 0 else False
        self.AC = 0 #@@@come back and complete

    def MVI_B_d8(self):
        self.B = self.fetch_byte()

    def get_MSB(self,A):
        bits = (A & (1 << 7))  #1 << 7 is the same as 1000 0000
        return ((bits >> 7))

    def get_LSB(self,A):
        bit = (A & 1)
        return bit

    def RLC(self,A):
        self.CY = self.get_MSB(A) # store the MSB
        A = (( A << 1) & 0xFF) #shift Left
        # if CY == 1:
            # A = A | 0b0000001 -- not necessary below is nicer and same
        A = A | self.CY #if CY is 1, then 1 appended, if 0, nothing happens
        
    def RAL(self,A):
        LSB = self.CY
        self.CY = self.get_MSB(A)
        A = ((A << 1) & 0xFF) # shifted left
        A = A | LSB
    
    def RRC(self,A):
        self.CY = self.get_LSB(A)
        A = ((A >> 1) & 0xFF)
        A = A | (self.CY << 7)
        
    def RAR(self,A):
        MSB = self.CY
        self.CY = self.get_LSB(A)
        A = ((A >> 1) & 0xFF)
        A = A | (MSB << 7)
        

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
  
    def read_instruction(self, op_code): 
        match op_code:
            case 0x00:
                return
            case 0x01:
                self.LXI_B()
                return
            case 0x02:
                self.STAX_B()
                return
            case 0x03:
                self.INX_B()
                return
            case 0x04:
                self.INR_B()
                return

#--------------------------------------------------#

# init the Cpu() and open spaceinvaders
cpu = Cpu()
with open("invaders", "rb") as b_file:
    cpu.memory = bytearray(b_file.read())
#--------------------------------------------------#

# main loop
#--------------------------------------------------#

while True:
    data = cpu.fetch_byte()
    cpu.read_instruction(data)

# testing

# assert cpu.memory[0] == 0x00
# assert cpu.memory[9] == 0xc5
# assert cpu.memory[len(cpu.memory)-1] == 0x00

# data = cpu.fetch_byte()
# assert data == 0x00

# cpu.test_reset()

# data = cpu.fetch_two_bytes()
# assert data == 0x00
# data = cpu.fetch_two_bytes()
# data = cpu.fetch_two_bytes()
# assert data == 0x18d4
# data = cpu.fetch_two_bytes()
# data = cpu.fetch_two_bytes()
# assert data == 0xc5f5
# cpu.test_reset()
