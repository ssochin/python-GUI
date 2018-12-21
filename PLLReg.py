import sys
from aardvark_py import *
import time


class PLLReg:
    slave_select_dict = {
        # first demux
        "PLL1": 0b10000000,
        "PLL2": 0b10000001,
        "PLL3": 0b10000010,
        "PLL4": 0b10000011,
        "LO2 Reg Map": 0b10000100,
        "DNC 1": 0b10000101,
        "DNC 2": 0b10000110,
        "LO1 UPC 1": 0b10000111,
        # second demux
        "LO1 UPC 2": 0b01000000,
        "LO1 Reg Map": 0b01001000,
        "DNC 3": 0b01010000,
        "DNC 4": 0b01011000,
        "TP 19": 0b01100000,
        "TP 20": 0b01101000,
        "TP 21": 0b01110000,
        "TP 22": 0b01111000
    }



    def __init__(self):
        self.bitrate = 4000  # set bit rate in KHz
        self.handle = 0         # to be set when aardvark is connected to later


    # wrapper function to connect to aardvark
    def connect2aardvark(self):
        self.find_connected_aardvarks()


    # Detect connected Aardvarks
    def find_connected_aardvarks(self):
        detectControl = True  # true to connect to aardvark
        while detectControl:
            print("Detecting Aardvark adapters...")

            # Find all the attached devices
            (num, ports, unique_ids) = aa_find_devices_ext(16, 16)

            if num > 0:
                print("{:d} device(s) found:".format(int(num)))
                detectControl = False
                # Print the information on each device
                for i in range(num):
                    port = ports[i]
                    unique_id = unique_ids[i]

                    # Determine if the device is in-use
                    inuse = "(avail)"
                    if (port & AA_PORT_NOT_FREE):
                        inuse = "(in-use)"
                        port = port & ~AA_PORT_NOT_FREE

                    # Display device port number, in-use status, and serial number
                    print("    port = {:d}   {:s}  ({:04f}-{:06f})".format(int(port), inuse, unique_id / 1000000, unique_id % 1000000))

                # connect to last aardvark (hopefully only one is connected to the computer
                self.configureaardvark(port)

            else:
                print("No devices found.")
                time.sleep(1)



    # destroy connection to aardvark
    def disconnectaardvark(self):
        aa_close(self.handle)
        print("Disconnected from Aardvark")

    # sets up and connects to aardvark
    def configureaardvark(self, port):
        # Open the device
        self.handle = aa_open(port)
        if (self.handle <= 0):
            print("Unable to open Aardvark device on port {:d}".format(port))
            print("Error code = {:d}".format(self.handle))
            sys.exit()

        # Ensure that the SPI subsystem is enabled
        aa_configure(self.handle, AA_CONFIG_SPI_I2C)
        # Power the EEPROM using the Aardvark adapter's power supply.
        aa_target_power(self.handle, AA_TARGET_POWER_BOTH)
        # configure the SPI bus
        aa_spi_configure(self.handle, AA_SPI_POL_RISING_FALLING, AA_SPI_PHASE_SAMPLE_SETUP, AA_SPI_BITORDER_MSB)  # original, now only for PLLs = rising falling, sample setup
        # SET PULLUPS
        aa_i2c_pullup(self.handle, AA_I2C_PULLUP_BOTH)
        # Set the bitrate
        bitrate = aa_spi_bitrate(self.handle, self.bitrate)
        print("Bitrate set to {:d} kHz".format(bitrate))
        aa_gpio_set(self.handle, 0)


# return an array of four bytes created from a 32 bit word
    def word2bytearray(self, word):
        num_bytes = 3
        buffer24 = array_u08(num_bytes)
        buffer24[0] = (word >> 16) & 0x0000FF # 1st byte
        buffer24[1] = (word >> 8) & 0x0000FF # 2nd byte
        buffer24[2] = word & 0x0000FF # 3rd byte
        return buffer24

    # sends a given 24 bit integer along the mosi of SPI BUS
    def spi_write(self, mosi_data):
        bytearray = self.word2bytearray(mosi_data)
        num_bytes = 3
        read_buffer = array_u08(num_bytes)
        read_buffer[0] = 0x00
        read_buffer[1] = 0x00
        read_buffer[2] = 0x00
        (num_bytes_response, read_buffer) = aa_spi_write(self.handle, bytearray, read_buffer)
        return read_buffer

    # sends one byte of address with R/W bit set to indicate a read.  Then returns the two bytes of data read from the muxout line
    def spi_read(self, address):
        address = 0x80 | address  # set the R/W bit to indicate a read
        address = address << 16  # make address 24 bits with address as first byte
        bytearray = self.word2bytearray(address)
        num_bytes = 3
        read_buffer = array_u08(num_bytes)
        read_buffer[0] = 0x00
        read_buffer[1] = 0x00
        read_buffer[2] = 0x00
        (num_bytes_response, read_buffer) = aa_spi_write(self.handle, bytearray, read_buffer)
        read_return = []
        read_return.append(read_buffer[1])  # convert 1st byte to hex and store it in array
        read_return.append(read_buffer[2])  # convert 2nd byte to hex and store it in array
        return read_return

    # create array of 2 bytes from 16 bit data
    def sixteen_word2bytearray(self, word):
        num_bytes = 2
        buffer16 = array_u08(num_bytes)
        buffer16[0] = (word >> 8) & 0x0000FF  # 1st byte
        buffer16[1] = word & 0x0000FF  # 2nd byte
        return buffer16

    # create array of 14 bytes from 112 bit data
    def stream_word2bytearray(self, stream_data):
        buffer = array_u08(8)
        buffer[0] = (stream_data >> 56) & 0xFF
        buffer[1] = (stream_data >> 48) & 0xFF
        buffer[2] = (stream_data >> 40) & 0xFF
        buffer[3] = (stream_data >> 32) & 0xFF
        buffer[4] = (stream_data >> 24) & 0xFF
        buffer[5] = (stream_data >> 16) & 0xFF
        buffer[6] = (stream_data >>8) & 0xFF
        buffer[7] = stream_data & 0xFF
        print(buffer)
        return buffer

    # sends a 14 byte integer to along the MOSI spi bus
    def sixteen_bit_stream_write(self, big_data):
        bytearray = self.stream_word2bytearray(big_data)
        read_buffer = array_u08(8)
        read_buffer[0] = 0x00
        read_buffer[1] = 0x00
        read_buffer[2] = 0x00
        read_buffer[3] = 0x00
        read_buffer[4] = 0x00
        read_buffer[5] = 0x00
        read_buffer[6] = 0x00
        read_buffer[7] = 0x00
        (num_bytes_response, read_buffer) = aa_spi_write(self.handle, bytearray, read_buffer)
        return read_buffer

    # sends a 16 bit integer along MOSI spi bus
    def sixteen_spi_write(self, sixteen_mosi_data):
        sixteen_bytearray = self.sixteen_word2bytearray(sixteen_mosi_data)
        num_bytes = 2
        sixteen_read_buffer = array_u08(num_bytes)
        sixteen_read_buffer[0] = 0x00
        sixteen_read_buffer[1] = 0x00
        (num_bytes_response, sixteen_read_buffer) = aa_spi_write(self.handle, sixteen_bytearray, sixteen_read_buffer)
        return sixteen_read_buffer

    # reads sixteen bit integer from spi bus
    def sixteen_spi_read(self, address):
        address = 0x80 | address  # set r/w bit to one indicating a read
        address = address << 8
        bytearray = self.sixteen_word2bytearray(address)
        num_bytes = 2
        read_buffer = array_u08(num_bytes)
        read_buffer[0] = 0x00
        read_buffer[1] = 0x00
        (num_bytes_response, read_buffer) = aa_spi_write(self.handle, bytearray, read_buffer)
        #print(num_bytes_response)  # test
        #print("read_buffer:", read_buffer)
        #print("read_buffer[1]:", read_buffer[1])
        read_return = []
        read_return.append(read_buffer[1])
        return read_return

    def slave_select_pca_config(self):
        # function to be ran once on startup of gui
        i2c_address = 0b0011000  # address of slave doesnt change, but data does (corrrect address) last bit is 0=write
        # set bits of expander as outputs w/ config array
        config_array = array_u08(2)
        config_array[0] = 0x03  # command byte for config register of expander
        config_array[1] = 0b00000000  # set all pins to outputs
        config = aa_i2c_write(self.handle, i2c_address, AA_I2C_NO_FLAGS, config_array)
        print("PCA9557 Configured")

    def slave_select_write(self, slave_select):
        #self.slave_select_pca_config()
        i2c_address = 0b0011000  # address of slave doesnt change, but data does (corrrect address) last bit is 0=write
        # create data to be sent
        data_array = array_u08(2)
        data_array[0] = 0b00000001  # command byte for output ports
        data_array[1] = slave_select & 0x00FF  # data to be sent
        response = aa_i2c_write(self.handle, i2c_address, AA_I2C_NO_FLAGS, data_array)
        # print slave that is being sent to
        print("sending to", list(self.slave_select_dict.keys())[list(self.slave_select_dict.values()).index(slave_select)])
        return response



    # 8 bit / 1 byte functions probably not useful
    # creates a one byte array
    def eight_word2bytearray(self, word):
        num_bytes = 1
        buffer8 = array_u08(num_bytes)
        buffer8[0] = word & 0x0000FF
        return buffer8

    # sends a one byte integer along mosi spi bus
    def eight_spi_write(self, eight_mosi_data):
        eight_bytearray = self.eight_word2bytearray(eight_mosi_data)
        num_bytes = 1
        eight_read_buffer = array_u08(num_bytes)
        eight_read_buffer[0] = 0x00
        (num_bytes_response, eight_read_buffer) = aa_spi_write(self.handle, eight_bytearray, eight_read_buffer)
        return eight_read_buffer

    # reads a one byte integer from spi bus
    def eight_spi_read(self, address):
        address = 0x80 | address
        eight_bytearray = self.eight_word2bytearray(address)
        num_bytes = 1
        eight_read_buffer = array_u08(num_bytes)
        eight_read_buffer[0] = 0x00
        (num_bytes_response, eight_read_buffer) = aa_spi_write(self.handle, eight_bytearray, eight_read_buffer)


    def toggleGpio(self):
            aa_gpio_direction(self.handle,3)
            aa_gpio_set(self.handle,1)
            aa_gpio_set(self.handle, 0)









# MAIN PROGRAM




# port    = 0
# In kHz - 1000 is default
# bitrate = 1000

# Open the device
# handle = aa_open(port)
# if (handle <= 0):
#    print("Unable to open Aardvark device on port {:d}".format(port))
#    print("Error code = {:d}".format(handle))
#    sys.exit()

# Ensure that the SPI subsystem is enabled
# aa_configure(handle,  AA_CONFIG_SPI_I2C)  # configure subsystem

# Power the EEPROM using the Aardvark adapter's power supply.
# This command is only effective on v2.0 hardware or greater.
# The power pins on the v1.02 hardware are not enabled by default.
# aa_target_power(handle, AA_TARGET_POWER_BOTH)  # set power
# aa_target_power(handle, AA_TARGET_POWER_NONE)

# Setup the clock phase
# aa_spi_configure(handle, polarity, phase, bitorder)
# polarity	AA_SPI_POL_RISING_FALLING or AA_SPI_POL_FALLING_RISING
# phase	AA_SPI_PHASE_SAMPLE_SETUP or AA_SPI_PHASE_SETUP_SAMPLE
# bitorder	AA_SPI_BITORDER_MSB or AA_SPI_BITORDER_LSB
#aa_spi_configure(handle, AA_SPI_POL_FALLING_RISING, AA_SPI_PHASE_SETUP_SAMPLE, AA_SPI_BITORDER_MSB)
#aa_spi_configure(handle, AA_SPI_POL_RISING_FALLING, AA_SPI_PHASE_SAMPLE_SETUP, AA_SPI_BITORDER_MSB) # configure SPI BUS

# print("AA_SPI_POL_RISING_FALLING: ", AA_SPI_POL_RISING_FALLING)
# print("AA_SPI_POL_FALLING_RISING: ", AA_SPI_POL_FALLING_RISING)
# print("AA_SPI_PHASE_SAMPLE_SETUP: ", AA_SPI_PHASE_SAMPLE_SETUP)
# print("AA_SPI_PHASE_SETUP_SAMPLE: ",  AA_SPI_PHASE_SETUP_SAMPLE)



# Set the bitrate
# bitrate = aa_spi_bitrate(handle, bitrate) # set the bitrate
# print("Bitrate set to {:d} kHz".format(bitrate)) # print hte bit rate


#PLL_Init() # initialize to 6.5 GHz with 10 MHz reference clock
#spi_write(0x002418) # set R0 D2 to 0 to enable readback mode
#print_registers()  # print all registers

# PLLReg = PLLReg()
# handle = PLLReg.connect2aardvark()



#PLLReg.PLL_Init()

# disconnect from aardvark
#PLLReg.disconnectaardvark(handle)

# Close the device
#aa_close(handle)

