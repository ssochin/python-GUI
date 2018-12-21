import PLLReg
import PLLSheet
import PLLSheet
class PLLFunc:

    def __init__(self):
        self.PLLReg = PLLReg.PLLReg()  # initialize a PLLReg object to write & read on SPI bus
        self.PLLSheet = PLLSheet.PLLSheet()  # initialize a PLLSheet object to create spreadsheet
        self.freqrange = range(6000, 11510, 10)  # frequency in MHz  # expanded for debug
        self.registers = range(112, -1, -1)  # create numbers from 112 to 0

        # create and initialize lookup table
        self.lookuptable = {}  # creates lookup table dictionary
        self.initialize_lookuptable()  # initializes the lookup table
        self.autocal_lookuptable()  # sets 10 registers to default values for autocal

        # initialization / startup routine
        self.autocal_array = {}  #  generic initialization autocal array, selected in GUI between 10 and 100 MHz ref
        self.autocal_array10 = {}  # 10 Mhz initialization autocal array
        self.autocal_array100 = {}  # 100 Mhz initialization autocal array
        self.setup_autocal_array()  # populate 10 Mhz and 100 MHz arrays

        # spreadsheet
        self.spreadsheet_name = "Invalid Filename"

    # wrapper function to connect to aardvark
    def connect2aardvark():
        PLLReg.connect2aardvark()  # connect to aardvark

    # wrapper function to disconnect from aardvark
    def disconnectaardvark():
        PLLReg.disconnectaardvark()  # disconnect from aardvark


    # create A->B->A spreadsheet wrapper function
    def make_spreadsheet(filename, freq1, freq2, delay):
        PLLSheet.create_spreadsheet(filename)  # create spreadsheet
        PLLSheet.add_mosidata(delay, freq1, freq2, lookuptable[freq1], lookuptable[freq2])  # add mosi data to spreadsheet

    # creat cal table spreadsheet wrapper function
    def generate_caltable_spreadsheet(, filename):
        PLLSheet.generate_caltable_spreadsheet(filename, freqrange, lookuptable)

    # create and initialize lookuptable with all zeros for all frequencies in freqrange
    def initialize_lookuptable():
        tenreglist = [46, 45, 44, 37, 36, 20, 19, 14, 8, 0]  # Ten Registers for each frequency
        for a in freqrange:
            lookuptable[a] = {}
            for b in tenreglist:
                lookuptable[a][b] = 0  # initialize each of the ten registers to zero for every frequency

    #  Sets up the Lookup Table with all frequency dependant registers to hop through in autocal mode
    def autocal_lookuptable():
        for f in freqrange:
            # non frequency dependant registers

            # reg 0
            lookuptable[f][0] = 0b0010010000010100
            # reg 8
            lookuptable[f][8] = 0b0010100000000000
            # reg 14
            lookuptable[f][14] = 0b0001111001110000
            # reg 19 (replace lower byte with value read back from R111)
            lookuptable[f][19] = 0b0010011100000000
            # reg 44
            lookuptable[f][44] = 0b0011010010000000

            # frequency dependant registers
            # replace VCO band in R20 with data read back from R110
            # reg 20
            if f >= 6000 and f < 6450:  # VCO 5  # inserted to test lower freq range
                lookuptable[f][20] = 0b1110110001001000
            elif f >= 6450 and f < 6950:  # VCO 6
                lookuptable[f][20] = 0b1111010001001000
            elif f >= 6950 and f < 7500:  # VCO 7
                lookuptable[f][20] = 0b1111110001001000
            elif f >= 7500 and f < 8600:  # VCO 1
                lookuptable[f][20] = 0b1100110001001000
            elif f >= 8600 and f < 9800:  # VCO 2
                lookuptable[f][20] = 0b1101010001001000
            elif f >= 9800 and f < 10800:  # VCO 3
                lookuptable[f][20] = 0b1101110001001000
            elif f >= 10800 and f < 12000:  # VCO 4
                lookuptable[f][20] = 0b1110010001001000
            elif f >= 12000 and f < 12900:  # VCO 5
                lookuptable[f][20] = 0b1110110001001000
            else:
                print("INVALID FREQUENCY R20! Frequency: ", f)

            # reg 36, 37, 45, 46
            if f < 7500:
                lookuptable[f][36] = int(f*2/10)  # reg 36 ( PLL_N = fout*2/10)
                lookuptable[f][37] = 0b0000001000000100  # reg 37
                lookuptable[f][45] = 0b1100000011000000  # reg 45 (OUTA_MUX = 00)
                lookuptable[f][46] = 0b0000011111111100  # reg 46 (OUTB_MUX = 00)
            elif f >= 7500:
                lookuptable[f][36] = int(f/10)  # reg 36 (PLL_N = fout/ 10)
                lookuptable[f][37] = 0b0000000100000100  # reg 37
                lookuptable[f][45] = 0b1100100011000000  # reg 45 (OUTA_MUX = 01)
                lookuptable[f][46] = 0b0000011111111101  # reg 46 (OUTB_MUX = 01)


    # Sets read back bit in register 0 then prints registers in order from 112 to 0
    def print_registers():
        PLLReg.spi_write(0x002410)  # set R0 D2 to 0 to enable readback mode
        for i in registers:
            address = i
            readback = PLLReg.spi_read(address)  # read specified address
            data1 = readback[0]  # first byte read back
            data2 = readback[1]  # second byte read back
            address = address << 16  # shift address to top of word
            data1 = data1 << 8  # shift 1st data byte to middle of word
            full_reg = address | data1 | data2  # create 24 bit register value
            print("R" + str(i), hex(full_reg))  # print full register value


    # allows user to edit lookuptable entry given a register address, reg value, and frequency
    def changetable(freq, add, val):
        lookuptable[freq][add] = val  # change lookuptable entry

    # Enable autocal mode by setting register 0
    def autocal_enable():
        PLLReg.spi_write(0b000000000010010000011100)  # set reg 0 to autocal mode D[3] = 1

    # look up all frequency dependant registers in lookup table,
    # and then and program registers 113 to 0 with those values
    def autocal_freq(freq):

        # write registers 112 to 0 on spi bus
        for r in registers:
            if r == 36 or r == 37 or r == 45 or r == 46:  # replace R36, R37, R45, and R46 with frequency dependant version
                add = r << 16  # put register number in the address byte
                data = 0x00FFFF & lookuptable[freq][r]  # clear top byte and add data from lookup table
                word = add | data  # create register write with address and data
                PLLReg.spi_write(word)  # write value along SPI bus
                #print("Register ", r, ": ", word)
            elif r == 0:
                PLLReg.spi_write(0b000000000010010000011100)  # set reg 0 to autocal mode D[3] = 1
                #print("Register ", r, ": ", 0b000000000010010000011100)
            else:
                PLLReg.spi_write(autocal_array[r])  # write whats in autocal register (non freq. dependant registers)
                #print("Register ", r, ": ", autocal_array[r])

        PLLReg.spi_write(0b000000000010010000011100)   # write register 0 a second time
        #print("zero again: ", 0b000000000010010000011100)

    # set R0 D[2] to enable readback mode, readback value for R111, store R111 D[7:0] in R19 D[7:0] in lookup table
    def updateR19(freq):
        PLLReg.spi_write(0x2410)  # change R0 D2 from 1 to zero to enable readback mode
        R111 = PLLReg.spi_read(111)  # readback register 111
        R19_old = lookuptable[freq][19]  # get old value of R19
        R19_old = R19_old & 0xFF00  # clear lower byte of R19
        R19_new = R19_old | R111[1]  # add D[7:0] of R111 to D[7:0] of R19
        lookuptable[freq][19] = R19_new  # update lookup table with new value of R19
        # print("R111[1]: ", R111[1])
        # print("R19_new: ", R19_new)
        # print("R19_old: ", R19_old)

    # set R0 D[2] to enable readback mode, readback value for R110, store R110 D[7:5] in R20 D[13:11] in lookup table
    def updateR20(freq):
        PLLReg.spi_write(0x2410)  # change R0 D2 from 1 to zero to enable readback mode
        R110 = PLLReg.spi_read(110)  # readback register 110
        R20_old = lookuptable[freq][20]  # get old value of R20
        R20_old = R20_old & 0xC7FF  # clear D[13:11]
        R110_clr = R110[1] & 0xE0  # clear D[4:0]
        R110_new = R110_clr << 6  # shift VCO band from D[7:5] into D[13:11]
        R20_new = R20_old | R110_new  # insert R110 D[7:5] into R20 D[13:11]
        lookuptable[freq][20] = R20_new  # update lookup table with new value of R19

    # enables autocal bypass mode by writing to register 0
    def bypassautocalenable():
        PLLReg.spi_write(0x002414)  # set Reg 0 D[3] to 0 to bypass autocal mode

    # write to R0 to enable bypass autocal mode
    # write registers R46, R45, R44, R37, R36, R20, R19, R14, R8, R0 along SPI bus to jump to requested freq.
    def bypassautocal(freq):
        # create data from lookup table
        R46 = 46 << 16  # put address in first byte
        R46 = R46 | lookuptable[freq][46]  # put data in bytes 2 and 3
        R45 = 45 << 16  # put address in first byte
        R45 = R45 | lookuptable[freq][45]  # put data in bytes 2 and 3
        R44 = 44 << 16  # put address in first byte
        R44 = R44 | lookuptable[freq][44]  # put data in bytes 2 and 3
        R37 = 37 << 16  # put address in first byte
        R37 = R37 | lookuptable[freq][37]  # put data in bytes 2 and 3
        R36 = 36 << 16  # put address in first byte
        R36 = R36 | lookuptable[freq][36]  # put data in bytes 2 and 3
        R20 = 20 << 16  # put address in first byte
        R20 = R20 | lookuptable[freq][20]  # put data in bytes 2 and 3
        R19 = 19 << 16  # put address in first byte
        R19 = R19 | lookuptable[freq][19]  # put data in bytes 2 and 3
        R14 = 14 << 16  # put address in first byte
        R14 = R14 | lookuptable[freq][14]  # put data in bytes 2 and 3
        R8 = 8 << 16  # put address in first byte
        R8 = R8 | lookuptable[freq][8]  # put data in bytes 2 and 3
        R0 = 0 << 16  # put address in first byte
        R0 = R0 | lookuptable[freq][0]  # put data in bytes 2 and 3

        # send data along SPI bus
        PLLReg.spi_write(R46)  # write register 46 from lookup table
        PLLReg.spi_write(R45)  # write register 45 from lookup table
        PLLReg.spi_write(R44)  # write register 44 from lookup table
        PLLReg.spi_write(R37)  # write register 37 from lookup table
        PLLReg.spi_write(R36)  # write register 36 from lookup table
        PLLReg.spi_write(R20)  # write register 20 from lookup table
        PLLReg.spi_write(R19)  # write register 19 from lookup table
        PLLReg.spi_write(R14)  # write register 14 from lookup table
        PLLReg.spi_write(R8)  # write register 8 from lookup table
        PLLReg.spi_write(R0)  # write register 0 from lookup table

        #print("R46: ", hex(R46))
        #print("R45: ", hex(R45))
        #print("R44: ", hex(R44))
        #print("R37: ", hex(R37))
        #print("R36: ", hex(R36))
        #print("R20: ", hex(R20))
        #print("R19: ", hex(R19))
        #print("R14: ", hex(R14))
        #print("R08: ", hex(R8))
        #print("R00: ", hex(R0))


    # initialize the PLL to 6500 MHz with 10 or 100 MHz reference signal
    def pll_init(ref):
        if ref == 10:
            autocal_array = autocal_array10
        elif ref == 100:
            autocal_array = autocal_array100
        else:
            print("INVALID REF FREQ! Ref: ", ref)
            autocal_array = autocal_array10  # default

        # write registers 112 to 0 on spi bus
        for r in registers:
            PLLReg.spi_write(autocal_array[r])

        PLLReg.spi_write(autocal_array[0])  # write register 0 a second time
        print("finished")


    # populate 10 MHz and 100 MHz initialization arrays
    def setup_autocal_array():
        # 10 MHz array
        autocal_array10[112] = 0x700000
        autocal_array10[111] = 0x6F0000
        autocal_array10[110] = 0x6E0000
        autocal_array10[109] = 0x6D0000
        autocal_array10[108] = 0x6C0000
        autocal_array10[107] = 0x6B0000
        autocal_array10[106] = 0x6A0007
        autocal_array10[105] = 0x690000
        autocal_array10[104] = 0x6803E8
        autocal_array10[103] = 0x670000
        autocal_array10[102] = 0x660000
        autocal_array10[101] = 0x650000
        autocal_array10[100] = 0x6403E8
        autocal_array10[99] = 0x63999A
        autocal_array10[98] = 0x620064
        autocal_array10[97] = 0x610800
        autocal_array10[96] = 0x600000
        autocal_array10[95] = 0x5F0000
        autocal_array10[94] = 0x5E0000
        autocal_array10[93] = 0x5D0000
        autocal_array10[92] = 0x5C0000
        autocal_array10[91] = 0x5B0000
        autocal_array10[90] = 0x5A0000
        autocal_array10[89] = 0x590000
        autocal_array10[88] = 0x580000
        autocal_array10[87] = 0x570000
        autocal_array10[86] = 0x560001
        autocal_array10[85] = 0x550000
        autocal_array10[84] = 0x540001
        autocal_array10[83] = 0x53FFFF
        autocal_array10[82] = 0x52FFFF
        autocal_array10[81] = 0x510000
        autocal_array10[80] = 0x500000
        autocal_array10[79] = 0x4F0300
        autocal_array10[78] = 0x4E0001
        autocal_array10[77] = 0x4D0000
        autocal_array10[76] = 0x4C000C
        autocal_array10[75] = 0x4B0800
        autocal_array10[74] = 0x4A0000
        autocal_array10[73] = 0x49003F
        autocal_array10[72] = 0x480001
        autocal_array10[71] = 0x470081
        autocal_array10[70] = 0x46C350
        autocal_array10[69] = 0x450000
        autocal_array10[68] = 0x4403E8
        autocal_array10[67] = 0x430000
        autocal_array10[66] = 0x4201F4
        autocal_array10[65] = 0x410000
        autocal_array10[64] = 0x401388
        autocal_array10[63] = 0x3F0000
        autocal_array10[62] = 0x3E0322
        autocal_array10[61] = 0x3D00A8
        autocal_array10[60] = 0x3C0000
        autocal_array10[59] = 0x3B0001
        autocal_array10[58] = 0x3A8001
        autocal_array10[57] = 0x390020
        autocal_array10[56] = 0x380000
        autocal_array10[55] = 0x370000
        autocal_array10[54] = 0x360000
        autocal_array10[53] = 0x350000
        autocal_array10[52] = 0x340820
        autocal_array10[51] = 0x330080
        autocal_array10[50] = 0x320000
        autocal_array10[49] = 0x314180
        autocal_array10[48] = 0x300300
        autocal_array10[47] = 0x2F0300
        autocal_array10[46] = 0x2E07FC
        autocal_array10[45] = 0x2DC0DF
        autocal_array10[44] = 0x2C3280
        autocal_array10[43] = 0x2B0000
        autocal_array10[42] = 0x2A0000
        autocal_array10[41] = 0x290000
        autocal_array10[40] = 0x280000
        autocal_array10[39] = 0x2703E8
        autocal_array10[38] = 0x260000
        autocal_array10[37] = 0x250204
        autocal_array10[36] = 0x240514
        autocal_array10[35] = 0x230004
        autocal_array10[34] = 0x220000
        autocal_array10[33] = 0x211E21
        autocal_array10[32] = 0x200393
        autocal_array10[31] = 0x1F03EC
        autocal_array10[30] = 0x1E318C
        autocal_array10[29] = 0x1D318C
        autocal_array10[28] = 0x1C0488
        autocal_array10[27] = 0x1B0002
        autocal_array10[26] = 0x1A0DB0
        autocal_array10[25] = 0x190624
        autocal_array10[24] = 0x18071A
        autocal_array10[23] = 0x17007C
        autocal_array10[22] = 0x160001
        autocal_array10[21] = 0x150401
        autocal_array10[20] = 0x14F048
        autocal_array10[19] = 0x1327B7
        autocal_array10[18] = 0x120064
        autocal_array10[17] = 0x1100FA
        autocal_array10[16] = 0x100080
        autocal_array10[15] = 0x0F064F
        autocal_array10[14] = 0x0E1E70
        autocal_array10[13] = 0x0D4000
        autocal_array10[12] = 0x0C5001
        autocal_array10[11] = 0x0B0018
        autocal_array10[10] = 0x0A10D8
        autocal_array10[9] = 0x090604
        autocal_array10[8] = 0x082000
        autocal_array10[7] = 0x0740B2
        autocal_array10[6] = 0x06C802
        autocal_array10[5] = 0x0500C8
        autocal_array10[4] = 0x040A43
        autocal_array10[3] = 0x030642
        autocal_array10[2] = 0x020500
        autocal_array10[1] = 0x010808
        autocal_array10[0] = 0x00241C

        # 100 MHz array
        autocal_array100[112] = 0x700000
        autocal_array100[111] = 0x6F0000
        autocal_array100[110] = 0x6E0000
        autocal_array100[109] = 0x6D0000
        autocal_array100[108] = 0x6C0000
        autocal_array100[107] = 0x6B0000
        autocal_array100[106] = 0x6A0000
        autocal_array100[105] = 0x690021
        autocal_array100[104] = 0x680000
        autocal_array100[103] = 0x670000
        autocal_array100[102] = 0x663600
        autocal_array100[101] = 0x650011
        autocal_array100[100] = 0x640000
        autocal_array100[99] = 0x630000
        autocal_array100[98] = 0x622800
        autocal_array100[97] = 0x610888
        autocal_array100[96] = 0x600000
        autocal_array100[95] = 0x5F0000
        autocal_array100[94] = 0x5E0000
        autocal_array100[93] = 0x5D0000
        autocal_array100[92] = 0x5C0000
        autocal_array100[91] = 0x5B0000
        autocal_array100[90] = 0x5A0000
        autocal_array100[89] = 0x590000
        autocal_array100[88] = 0x580000
        autocal_array100[87] = 0x570000
        autocal_array100[86] = 0x560001
        autocal_array100[85] = 0x550000
        autocal_array100[84] = 0x540001
        autocal_array100[83] = 0x53FFFF
        autocal_array100[82] = 0x52FFFF
        autocal_array100[81] = 0x510000
        autocal_array100[80] = 0x500000
        autocal_array100[79] = 0x4F0300
        autocal_array100[78] = 0x4E0003
        autocal_array100[77] = 0x4D0000
        autocal_array100[76] = 0x4C000C
        autocal_array100[75] = 0x4B0800
        autocal_array100[74] = 0x4A0000
        autocal_array100[73] = 0x49003F
        autocal_array100[72] = 0x480001
        autocal_array100[71] = 0x470081
        autocal_array100[70] = 0x46C350
        autocal_array100[69] = 0x450000
        autocal_array100[68] = 0x4403E8
        autocal_array100[67] = 0x430000
        autocal_array100[66] = 0x4201F4
        autocal_array100[65] = 0x410000
        autocal_array100[64] = 0x401388
        autocal_array100[63] = 0x3F0000
        autocal_array100[62] = 0x3E0322
        autocal_array100[61] = 0x3D00A8
        autocal_array100[60] = 0x3C0000
        autocal_array100[59] = 0x3B0001
        autocal_array100[58] = 0x3A8001
        autocal_array100[57] = 0x390020
        autocal_array100[56] = 0x380000
        autocal_array100[55] = 0x370000
        autocal_array100[54] = 0x360000
        autocal_array100[53] = 0x350000
        autocal_array100[52] = 0x340820
        autocal_array100[51] = 0x330080
        autocal_array100[50] = 0x320000
        autocal_array100[49] = 0x314180
        autocal_array100[48] = 0x300300
        autocal_array100[47] = 0x2F0300
        autocal_array100[46] = 0x2E07FC
        autocal_array100[45] = 0x2DC0DF
        autocal_array100[44] = 0x2C1F80
        autocal_array100[43] = 0x2B0000
        autocal_array100[42] = 0x2A0000
        autocal_array100[41] = 0x290000
        autocal_array100[40] = 0x280000
        autocal_array100[39] = 0x2703E8
        autocal_array100[38] = 0x260000
        autocal_array100[37] = 0x250204
        autocal_array100[36] = 0x240514
        autocal_array100[35] = 0x230004
        autocal_array100[34] = 0x220000
        autocal_array100[33] = 0x211E21
        autocal_array100[32] = 0x200393
        autocal_array100[31] = 0x1F03EC
        autocal_array100[30] = 0x1E318C
        autocal_array100[29] = 0x1D318C
        autocal_array100[28] = 0x1C0488
        autocal_array100[27] = 0x1B0002
        autocal_array100[26] = 0x1A0DB0
        autocal_array100[25] = 0x190624
        autocal_array100[24] = 0x18071A
        autocal_array100[23] = 0x17007C
        autocal_array100[22] = 0x160001
        autocal_array100[21] = 0x150401
        autocal_array100[20] = 0x14F048
        autocal_array100[19] = 0x1327B7
        autocal_array100[18] = 0x120064
        autocal_array100[17] = 0x1100FA
        autocal_array100[16] = 0x100080
        autocal_array100[15] = 0x0F064F
        autocal_array100[14] = 0x0E1E70
        autocal_array100[13] = 0x0D4000
        autocal_array100[12] = 0x0C500A
        autocal_array100[11] = 0x0B0018
        autocal_array100[10] = 0x0A10D8
        autocal_array100[9] = 0x090604
        autocal_array100[8] = 0x082000
        autocal_array100[7] = 0x0740B2
        autocal_array100[6] = 0x06C802
        autocal_array100[5] = 0x0500C8
        autocal_array100[4] = 0x040A43
        autocal_array100[3] = 0x030642
        autocal_array100[2] = 0x020500
        autocal_array100[1] = 0x010808
        autocal_array100[0] = 0x00241C


