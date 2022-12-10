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
    
    def fetch_two_bytes(self): #@@@TODO: RENAME this to better reflect 2 next 2 8 bit bytes to 16 bit
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


    def get_MSB(self):
        bits = (self.A & (1 << 7))  #1 << 7 is the same as 1000 0000
        return ((bits >> 7))

    def get_LSB(self):
        bit = (self.A & 1)
        return bit

    def RLC(self):
        self.CY = self.get_MSB(A) # store the MSB
        self.A = ((self.A << 1) & 0xFF) #shift Left
        # if CY == 1:
            # A = A | 0b0000001 -- not necessary below is nicer and same
        self.A = self.A | self.CY #if CY is 1, then 1 appended, if 0, nothing happens
        
    def RAL(self):
        LSB = self.CY
        self.CY = self.get_MSB(A)
        self.A = ((self.A << 1) & 0xFF) # shifted left
        self.A = self.A| LSB
    
    def RRC(self):
        self.CY = self.get_LSB(A)
        self.A = ((self.A >> 1) & 0xFF)
        self.A = self.A | (self.CY << 7)
        
    def RAR(self):
        MSB = self.CY
        self.CY = self.get_LSB(self.A)
        self.A = ((self.A >> 1) & 0xFF)
        self.A = self.A | (MSB << 7)

    def DAA(self):
        value = self.A & 15
        if value > 9 or self.AC == True:
            self.A += 6
        
        mask = 0b11110000
        value = (self.A & mask)
        value = value >> 4 #shift the back to the bottom 4 bits
        if value > 9 or self.CY == 1:
            self.A += (6 << 4) 
        #COME BACK AND FIX THESE FLAGS....

    #--------------------------------------------------#
    
    # Branch Group
    def JMP(self):
        self.PC = self.fetch_two_bytes
        return
    
    
    #--------------------------------------------------#
    # Stack, I/O, and Machine Control Group:

 #@@@TODO: some are 1, some True... I need to deal with this
 # function might not actually be working otherwise
    def PUSH_PSW(self):
        self.memory[self.SP - 1] = self.A
        flag_word = 0
        flag_word += self.CY << 0 | 1 << 1 | self.P << 2 | self.AC << 4 | self.Z << 6 | self.S << 7
        self.memory[self.SP - 2] = flag_word
        self.SP -= 2
        return

    def PUSH_B(self):
        mask = 0xFF #255 same as 0b0000000011111111 same as 0b11111111
        high = self.BC & mask
        low = self.BC >> 8
        self.memory[self.SP - 1] = high
        self.memory[self.SP - 2] = low
        self.SP -= 2
        return

    def PUSH_D(self):
        mask = 0xFF
        self.memory[self.SP - 1] = self.DE & mask
        self.memory[self.SP - 2] = self.DE >> 8
        self.SP -= 2
        return

    def PUSH_H(self):
        mask = 0xFF
        self.memory[self.SP - 1] = self.HL & mask
        self.memory[self.SP - 2] = self.HL >> 8
        self.SP -= 2
        return
    #--------------------------------------------------#
    #Arithmetic Group:
    def ADD_B(self):
        self.A = self.A + self.B
       
        self.Z = True if self.A == 0 else False
        self.S = True if self.A & 0x80 else False #reminder - as long as greater 0, all good
        self.P = True if add_bits(self.A) % 2 == 0 else False
        self.AC = 0 #@@@come back and complete
        return

    def ADC_H(self):
        self.A = self.A + self.H + self.CY
        # I Should make a function that handless this stuff for me cause too much repition 
        # @@@TODO: Check this correct below
        self.Z = True if self.A == 0 else False
        self.S = True if self.A & 0x80 else False
        self.P = True if add_bits(self.A) % 2 == 0 else False
        #@@@TODO:CARRY and AUX CARRY

    def DCR_M(self):
        self.memory[self.HL] -= 1
        #@@@TODO: FLAGS TOMORROWWWWWWWWWWWW
    #--------------------------------------------------#
    # Data Transfer Group:
    
    # @@@TODO: Check if this is right... too simple
    def MVI_B_d8(self):
        self.B = self.fetch_byte()
        return

    def MVI_A_d8(self):
        self.A = self.fetch_byte()
        return

    # @@@TODO: Make a general function that does it for all above,
    # instead of doing it seperately 

    def STA(self):
        self.memory[self.fetch_two_bytes()] = self.A
        return

    def MOV_M_D():
        self.memory[self.HL] = self.D
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
            case 0xc3:
                self.JMP()
            case 0xf5:
                self.PUSH_PSW()
            case 0xc5:
                self.PUSH_B()
            case 0xd5:
                self.PUSH_D()
            case 0xe5:
                self.PUSH_H()
            case 0x8c:
                self.ADC_H()
            case 0x3e:
                self.MVI_A_d8()
            case 0x32:
                self.STA()
            case 0x72:
                self.MOVE_M_D()
            case 0x21:
                self.LXI_H()
            case 0xc8:
                # NEED TO IMPLEMENT RNZ? No clue what this is yet...
            case 0x20:
                # Similar to above
            case 0x35:
                self.DCR_M()
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
