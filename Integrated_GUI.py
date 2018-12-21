import PLLFunc
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror
import time
import getpass
from datetime import date
from aardvark_py import *
import os, sys
from random import randint

autocalHis = []
        # general comments for repeated code:
        # send buttons packed to right side to ensure they arent squished by checkbuttons
        # checkbuttons are on or off (1 or 0) to represent the bits to be sent through the spi bus
        # send bits only sends the data from that line to a specific address corresponding to the mappings
class PLLGui():

    def __init__(self):
        # the initiate function sets up the GUI and declares all the necessary variables for writing/reading
        self.GUIversion = "V4.0"
        self.merge = tk.Tk()  # base Tk object to pack both GUIs into
        self.PLLFunc = PLLFunc.PLLFunc()  # initialize a PLLFunc object to run PLL functions
        # connect to aardvark
        self.PLLFunc.connect2aardvark()
        self.PLLFunc.PLLReg.slave_select_pca_config()
        # initialize Reg Map GUI
        self.base = tk.Frame(self.merge)  # create frame for reg map GUI
        self.base.pack(side="left")  # pack this frame left so Reg Map is on left and PLLGui is on right
        self.spacer1 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer2 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer3 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer4 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer5 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer6 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer6 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer7 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer8 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        self.spacer9 = tk.Canvas(self.base, bg="grey94", width="300", height="20")
        # spacers to prevent the GUI from getting cluttered, grey94 is the color of the window, looks like blank space

        self.reg_map_label = tk.Label(self.base, text="LO2 Register Map", font="Helvetica 15 bold")
        self.reg_map_label.pack()
        # soft reset checkbutton setup
        self.soft_name_label = tk.Label(self.base, text="Return FPGA to known State", font="Helvetica 10 bold")
        self.soft_name_label.pack()
        self.s0 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.schecks = tk.Frame(self.base)  # frame to contain all check buttons in one line
        # checkbutton (this data is only one bit)
        self.sc0 = tk.Checkbutton(self.schecks, text="Soft Reset", font="Consolas 8", variable=self.s0)
        self.schecks.pack(fill="x")
        # send button (only a write, no read for this one)
        self.send_but_frame = tk.Frame(self.schecks)
        self.send_but_frame.pack(side="right")
        self.spacer_s = tk.Canvas(self.schecks, width=200, height=0, bg="grey94")
        self.spacer_s.pack(side="left")
        self.sc0.pack(side="left")
        self.soft_send_button = tk.Button(self.send_but_frame, text="Send Bits", bg="lime green", width=10, height=1,
                                          command=self.soft_reset_send)
        self.soft_send_button.pack()
        self.spacer1.pack()
        # end soft reset section
        self.soft_reset_send() # send one to start so registers are all warmed up

        # ldo checkbutton setup section
        self.ldo_name_label = tk.Label(self.base, text="Enable Signal to LDOs", font="Helvetica 10 bold")
        self.ldo_name_label.pack()
        self.l4 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.l3 = tk.IntVar()
        self.l2 = tk.IntVar()
        self.L1 = tk.IntVar()
        self.l0 = tk.IntVar()
        self.lr4 = tk.IntVar()
        self.lr3 = tk.IntVar()
        self.lr2 = tk.IntVar()
        self.Lr1 = tk.IntVar()
        self.lr0 = tk.IntVar()
        self.lchecks = tk.Frame(self.base)  # frame to contain all check buttons in one line
        self.lrchecks = tk.Frame(self.base)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.lc4 = tk.Checkbutton(self.lchecks, text="+3.3V A_2", font="Consolas 8", variable=self.l4)
        self.lc3 = tk.Checkbutton(self.lchecks, text="+3.3V LO1", font="Consolas 8", variable=self.l3)
        self.lc2 = tk.Checkbutton(self.lchecks, text="+5.0V LO2", font="Consolas 8", variable=self.l2)
        self.Lc1 = tk.Checkbutton(self.lchecks, text="+5.0V LO1 A", font="Consolas 8", variable=self.L1)
        self.lc0 = tk.Checkbutton(self.lchecks, text="+3.3V B_2", font="Consolas 8", variable=self.l0)
        self.lrc4 = tk.Checkbutton(self.lrchecks, text="+3.3V A_2", font="Consolas 8", variable=self.lr4)
        self.lrc3 = tk.Checkbutton(self.lrchecks, text="+3.3V LO1", font="Consolas 8", variable=self.lr3)
        self.lrc2 = tk.Checkbutton(self.lrchecks, text="+5.0V LO2", font="Consolas 8", variable=self.lr2)
        self.Lrc1 = tk.Checkbutton(self.lrchecks, text="+5.0V LO1 A", font="Consolas 8", variable=self.Lr1)
        self.lrc0 = tk.Checkbutton(self.lrchecks, text="+3.3V B_2", font="Consolas 8", variable=self.lr0)
        self.lchecks.pack(fill="x")
        self.lrchecks.pack(fill="x")
        self.lc4.pack(side="left")
        self.lc3.pack(side="left")
        self.lc2.pack(side="left")
        self.Lc1.pack(side="left")
        self.lc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.lrc4.pack(side="left")
        self.lrc3.pack(side="left")
        self.lrc2.pack(side="left")
        self.Lrc1.pack(side="left")
        self.lrc0.pack(side="left")
        # read and write buttons for this address
        self.ldo_en_send_button = tk.Button(self.lchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                            command=self.ldo_en_send)
        self.ldo_en_send_button.pack(side="right")
        self.ldo_en_read_button = tk.Button(self.lrchecks, text="Read Bits", bg="black", fg="white", width=10, height=1,
                                            command=self.ldo_en_read)
        self.ldo_en_read_button.pack(side="right")
        self.spacer2.pack()
        # end ldo

        # dnc checkbutton setup section
        self.dnc_name_label = tk.Label(self.base, text="Downconverter Config", font="Helvetica 10 bold")
        self.dnc_name_label.pack()
        self.d1 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.d0 = tk.IntVar()
        self.dr1 = tk.IntVar()
        self.dr0 = tk.IntVar()
        self.dchecks = tk.Frame(self.base)  # frame to contain all check buttons in one line
        self.drchecks = tk.Frame(self.base)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.dc1 = tk.Checkbutton(self.dchecks, text="DNC2 CN SEL", font="Consolas 8", variable=self.d1)
        self.dc0 = tk.Checkbutton(self.dchecks, text="DNC1 CN SEL", font="Consolas 8", variable=self.d0)
        self.drc1 = tk.Checkbutton(self.drchecks, text="DNC2 CN SEL", font="Consolas 8", variable=self.dr1)
        self.drc0 = tk.Checkbutton(self.drchecks, text="DNC1 CN SEL", font="Consolas 8", variable=self.dr0)
        self.dchecks.pack(fill="x")
        self.drchecks.pack(fill="x")
        self.spacer_d = tk.Canvas(self.dchecks, width=155, height=0, bg="grey94")
        self.spacer_d.pack(side="left")
        self.dc1.pack(side="left")
        self.dc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_dr = tk.Canvas(self.drchecks, width=155, height=0, bg="grey94")
        self.spacer_dr.pack(side="left")
        self.drc1.pack(side="left")
        self.drc0.pack(side="left")
        # read and write buttons for this address
        self.dnc_con_send_button = tk.Button(self.dchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                             command=self.dnc_con_send)
        self.dnc_con_send_button.pack(side="right")
        self.dnc_con_read_button = tk.Button(self.drchecks, text="Read Bits", bg="black", fg="white", width=10,
                                             height=1, command=self.dnc_con_read)
        self.dnc_con_read_button.pack(side="right")
        self.spacer3.pack()
        # end dnc

        # test checkbutton setup section
        self.test_name_label = tk.Label(self.base, text="Test Points", font="Helvetica 10 bold")
        self.test_name_label.pack()
        self.t1 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.t0 = tk.IntVar()
        self.tr1 = tk.IntVar()
        self.tr0 = tk.IntVar()
        self.tchecks = tk.Frame(self.base)  # frame to contain all check buttons in one line
        self.trchecks = tk.Frame(self.base)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.tc1 = tk.Checkbutton(self.tchecks, text="TP2", font="Consolas 8", variable=self.t1)
        self.tc0 = tk.Checkbutton(self.tchecks, text="TP1", font="Consolas 8", variable=self.t0)
        self.trc1 = tk.Checkbutton(self.trchecks, text="TP2", font="Consolas 8", variable=self.tr1)
        self.trc0 = tk.Checkbutton(self.trchecks, text="TP1", font="Consolas 8", variable=self.tr0)
        self.tchecks.pack(fill="x")
        self.trchecks.pack(fill="x")
        self.spacer_t = tk.Canvas(self.tchecks, width=200, height=0, bg="grey94")
        self.spacer_t.pack(side="left")
        self.tc1.pack(side="left")  # pad helps de-clutter
        self.tc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_tr = tk.Canvas(self.trchecks, width=200, height=0, bg="grey94")
        self.spacer_tr.pack(side="left")
        self.trc1.pack(side="left")
        self.trc0.pack(side="left")
        # read and write buttons for this address
        self.test_send_button = tk.Button(self.tchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                          command=self.test_pts_send)
        self.test_send_button.pack(side="right")
        self.test_read_button = tk.Button(self.trchecks, text="Read Bits", bg="black", fg="white", width=10, height=1,
                                          command=self.test_pts_read)
        self.test_read_button.pack(side="right")
        self.spacer4.pack()
        # end test

        # chip checkbutton setup section
        self.chip_name_label = tk.Label(self.base, text="Chip Enables for RF Synths", font="Helvetica 10 bold")
        self.chip_name_label.pack()
        self.c3 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.c2 = tk.IntVar()
        self.c1 = tk.IntVar()
        self.c0 = tk.IntVar()
        self.cr3 = tk.IntVar()
        self.cr2 = tk.IntVar()
        self.cr1 = tk.IntVar()
        self.cr0 = tk.IntVar()
        self.cchecks = tk.Frame(self.base)  # frame to contain a ll check buttons in one horizontal line
        self.crchecks = tk.Frame(self.base)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.cc3 = tk.Checkbutton(self.cchecks, text="CE 4", font="Consolas 8", variable=self.c3)
        self.cc2 = tk.Checkbutton(self.cchecks, text="CE 3", font="Consolas 8", variable=self.c2)
        self.cc1 = tk.Checkbutton(self.cchecks, text="CE 2", font="Consolas 8", variable=self.c1)
        self.cc0 = tk.Checkbutton(self.cchecks, text="CE 1", font="Consolas 8", variable=self.c0)
        self.crc3 = tk.Checkbutton(self.crchecks, text="CE 4", font="Consolas 8", variable=self.cr3)
        self.crc2 = tk.Checkbutton(self.crchecks, text="CE 3", font="Consolas 8", variable=self.cr2)
        self.crc1 = tk.Checkbutton(self.crchecks, text="CE 2", font="Consolas 8", variable=self.cr1)
        self.crc0 = tk.Checkbutton(self.crchecks, text="CE 1", font="Consolas 8", variable=self.cr0)
        self.cchecks.pack(fill="x")
        self.crchecks.pack(fill="x")
        self.spacer_c = tk.Canvas(self.cchecks, width=160, height=0, bg="grey94")
        self.spacer_c.pack(side="left")
        self.cc3.pack(side="left")
        self.cc2.pack(side="left")
        self.cc1.pack(side="left")
        self.cc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_cr = tk.Canvas(self.crchecks, width=160, height=0, bg="grey94")
        self.spacer_cr.pack(side="left")
        self.crc3.pack(side="left")
        self.crc2.pack(side="left")
        self.crc1.pack(side="left")
        self.crc0.pack(side="left")
        # individual read and write buttons for specific address
        self.chip_send_button = tk.Button(self.cchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                          command=self.chip_en_send)
        self.chip_send_button.pack(side="right")
        self.chip_read_button = tk.Button(self.crchecks, text="Read Bits", bg="black", fg="white", width=10, height=1,
                                          command=self.chip_en_read)
        self.chip_read_button.pack(side="right")
        self.spacer5.pack()
        # end of chip enable section

        # imp det read section
        self.imp_name_label = tk.Label(self.base, text="Input Power Detect", font="Helvetica 10 bold")
        self.imp_name_label.pack()
        self.ichecks = tk.Frame(self.base)
        self.ir0 = tk.IntVar()
        self.imp_check = tk.Checkbutton(self.ichecks, text="Power Detect", font="Consolas 8", variable=self.ir0)
        self.ichecks.pack(fill="x")
        self.read_but_frame = tk.Frame(self.ichecks)
        self.read_but_frame.pack(side="right")
        self.spacer_im = tk.Canvas(self.ichecks, width=200, height=0, bg="grey94")
        self.spacer_im.pack(side="left")
        self.imp_check.pack(side="left")
        # read button for this address (no write)
        self.imp_read_button = tk.Button(self.read_but_frame, text="Read Bits", fg="white", bg="black", width=10,
                                         height=1, command=self.imp_det_read)
        self.imp_read_button.pack()
        self.spacer9.pack()
        # end imp det section

        # DSA checkbutton setup section
        self.DSA_name_label = tk.Label(self.base, text="Digital Step Attenuator Settings", font="Helvetica 10 bold")
        self.DSA_name_label.pack()
        self.ds5 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.ds4 = tk.IntVar()
        self.ds3 = tk.IntVar()
        self.ds2 = tk.IntVar()
        self.ds1 = tk.IntVar()
        self.ds0 = tk.IntVar()
        self.dsr5 = tk.IntVar()
        self.dsr4 = tk.IntVar()
        self.dsr3 = tk.IntVar()
        self.dsr2 = tk.IntVar()
        self.dsr1 = tk.IntVar()
        self.dsr0 = tk.IntVar()
        self.dschecks = tk.Frame(self.base)  # frame to contain all check buttons in one line
        self.dsrchecks = tk.Frame(self.base)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.dsc5 = tk.Checkbutton(self.dschecks, text="D5 ATT", font="Consolas 8", variable=self.ds5)
        self.dsc4 = tk.Checkbutton(self.dschecks, text="D4 ATT", font="Consolas 8", variable=self.ds4)
        self.dsc3 = tk.Checkbutton(self.dschecks, text="D3 ATT", font="Consolas 8", variable=self.ds3)
        self.dsc2 = tk.Checkbutton(self.dschecks, text="D2 ATT", font="Consolas 8", variable=self.ds2)
        self.dsc1 = tk.Checkbutton(self.dschecks, text="D1 ATT", font="Consolas 8", variable=self.ds1)
        self.dsc0 = tk.Checkbutton(self.dschecks, text="D0 ATT", font="Consolas 8", variable=self.ds0)
        self.dsrc5 = tk.Checkbutton(self.dsrchecks, text="D5 ATT", font="Consolas 8", variable=self.dsr5)
        self.dsrc4 = tk.Checkbutton(self.dsrchecks, text="D4 ATT", font="Consolas 8", variable=self.dsr4)
        self.dsrc3 = tk.Checkbutton(self.dsrchecks, text="D3 ATT", font="Consolas 8", variable=self.dsr3)
        self.dsrc2 = tk.Checkbutton(self.dsrchecks, text="D2 ATT", font="Consolas 8", variable=self.dsr2)
        self.dsrc1 = tk.Checkbutton(self.dsrchecks, text="D1 ATT", font="Consolas 8", variable=self.dsr1)
        self.dsrc0 = tk.Checkbutton(self.dsrchecks, text="D0 ATT", font="Consolas 8", variable=self.dsr0)
        self.dschecks.pack(fill="x")
        self.dsrchecks.pack(fill="x")
        self.spacer_ds = tk.Canvas(self.dschecks, width=23, height=0, bg="grey94")
        self.spacer_ds.pack(side="left")
        self.dsc5.pack(side="left")
        self.dsc4.pack(side="left")
        self.dsc3.pack(side="left")
        self.dsc2.pack(side="left")
        self.dsc1.pack(side="left")
        self.dsc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_dsr = tk.Canvas(self.dsrchecks, width=23, height=0, bg="grey94")
        self.spacer_dsr.pack(side="left")
        self.dsrc5.pack(side="left")
        self.dsrc4.pack(side="left")
        self.dsrc3.pack(side="left")
        self.dsrc2.pack(side="left")
        self.dsrc1.pack(side="left")
        self.dsrc0.pack(side="left")
        # read and write buttons
        self.dsa_send_button = tk.Button(self.dschecks, text="Send Bits", bg="lime green", width=10, height=1,
                                         command=self.dsa_send)
        self.dsa_send_button.pack(side="right")
        self.dsa_read_button = tk.Button(self.dsrchecks, text="Read Bits", bg="black", fg="white", width=10, height=1,
                                         command=self.dsa_read)
        self.dsa_read_button.pack(side="right")
        self.spacer7.pack()
        # end DSA

        # sw section
        self.sw_name_label = tk.Label(self.base, text="Switch Settings", font="Helvetica 10 bold")
        self.sw_name_label.pack()
        self.sw6 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.sw5 = tk.IntVar()
        self.sw4 = tk.IntVar()
        self.sw3 = tk.IntVar()
        self.sw2 = tk.IntVar()
        self.sw1 = tk.IntVar()
        self.sw0 = tk.IntVar()
        self.swr6 = tk.IntVar()
        self.swr5 = tk.IntVar()
        self.swr4 = tk.IntVar()
        self.swr3 = tk.IntVar()
        self.swr2 = tk.IntVar()
        self.swr1 = tk.IntVar()
        self.swr0 = tk.IntVar()
        self.swchecks = tk.Frame(self.base)  # frame to contain all check buttons in one line
        self.swrchecks = tk.Frame(self.base)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.swc6 = tk.Checkbutton(self.swchecks, text="SW 7", font="Consolas 8", variable=self.sw6)
        self.swc5 = tk.Checkbutton(self.swchecks, text="SW 6", font="Consolas 8", variable=self.sw5)
        self.swc4 = tk.Checkbutton(self.swchecks, text="SW 5", font="Consolas 8", variable=self.sw4)
        self.swc3 = tk.Checkbutton(self.swchecks, text="SW 4", font="Consolas 8", variable=self.sw3)
        self.swc2 = tk.Checkbutton(self.swchecks, text="SW 3", font="Consolas 8", variable=self.sw2)
        self.swc1 = tk.Checkbutton(self.swchecks, text="SW 2", font="Consolas 8", variable=self.sw1)
        self.swc0 = tk.Checkbutton(self.swchecks, text="SW 1", font="Consolas 8", variable=self.sw0)
        self.swrc6 = tk.Checkbutton(self.swrchecks, text="SW 7", font="Consolas 8", variable=self.swr6)
        self.swrc5 = tk.Checkbutton(self.swrchecks, text="SW 6", font="Consolas 8", variable=self.swr5)
        self.swrc4 = tk.Checkbutton(self.swrchecks, text="SW 5", font="Consolas 8", variable=self.swr4)
        self.swrc3 = tk.Checkbutton(self.swrchecks, text="SW 4", font="Consolas 8", variable=self.swr3)
        self.swrc2 = tk.Checkbutton(self.swrchecks, text="SW 3", font="Consolas 8", variable=self.swr2)
        self.swrc1 = tk.Checkbutton(self.swrchecks, text="SW 2", font="Consolas 8", variable=self.swr1)
        self.swrc0 = tk.Checkbutton(self.swrchecks, text="SW 1", font="Consolas 8", variable=self.swr0)
        self.swchecks.pack(fill="x")
        self.swrchecks.pack(fill="x")
        self.spacer_sw = tk.Canvas(self.swchecks, width=50, height=0, bg="grey94")
        self.spacer_sw.pack(side="left")
        self.swc6.pack(side="left")
        self.swc5.pack(side="left")
        self.swc4.pack(side="left")
        self.swc3.pack(side="left")
        self.swc2.pack(side="left")
        self.swc1.pack(side="left")
        self.swc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_swr = tk.Canvas(self.swrchecks, width=50, height=0, bg="grey94")
        self.spacer_swr.pack(side="left")
        self.swrc6.pack(side="left")
        self.swrc5.pack(side="left")
        self.swrc4.pack(side="left")
        self.swrc3.pack(side="left")
        self.swrc2.pack(side="left")
        self.swrc1.pack(side="left")
        self.swrc0.pack(side="left")
        # read and write buttons
        self.sw_send_button = tk.Button(self.swchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                        command=self.sw_send)
        self.sw_send_button.pack(side="right")
        self.sw_read_button = tk.Button(self.swrchecks, text="Read Bits", bg="black", fg="white", width=10, height=1,
                                        command=self.sw_read)
        self.sw_read_button.pack(side="right")
        self.spacer8.pack()
        # end sw

        self.reg_test_button = tk.Button(self.base, text="SS Test", width=10, height=1, bg='orange', command=self.LO2_reg_test)
        self.reg_test_button.pack() # register test button that writes and reads data back to verify registers work
        # reg test currently tests slave select buses^ by writing the PCA9557 then sending a spi signal that can be
        # detected on the slave select lines for that slave
        self.test_var = tk.StringVar()
        self.lo2_test_dropdown = tk.OptionMenu(self.base, self.test_var, *self.PLLFunc.PLLReg.slave_select_dict)
        self.lo2_test_dropdown.pack() # dropdown menu to test slave select lines
        # dropdown menu setup
        self.var = tk.StringVar()  # string variable to represent
        self.var.set("PLL1")  # default dropdown value
        self.ss = 0b10000000  # set default slave bus
        # 0b10000XXX is for first demux (slave 0-7)
        # 0b01XXX000 is for second demux (slave 8-15)

        # LO2 Peripherals Framing
        self.log_frame = tk.Frame(self.merge)
        self.log_frame.pack(side="left")
        self.LO2_periph_header = tk.Label(self.log_frame, text="LO2 Peripherals", font="Helvetica 10 bold")
        self.LO2_periph_header.pack()
        self.LO2_adc_header = tk.Label(self.log_frame, text="LTC2313-12 ADC", font="Helvetica 10 bold")
        self.LO2_adc_header.pack()
        self.adc_frame = tk.Frame(self.log_frame)
        self.adc_frame.pack()
        self.adc_data_disp = tk.IntVar()
        self.adc_calc = tk.IntVar()
        self.adc_kickoff_button = tk.Button(self.adc_frame, height=1, width=10, bg="gold", text="Read ADC",
                                            command=self.adc_kickoff)
        self.adc_kickoff_button.pack(side="left")
        self.adc_display = tk.Entry(self.adc_frame, textvariable=self.adc_data_disp)
        self.adc_display.pack()
        self.adc_calc_display = tk.Entry(self.adc_frame, textvariable=self.adc_calc)
        self.adc_calc_display.pack()
        self.pll_log_header = tk.Label(self.log_frame, text="PLL Logs", font="Helvetica 10 bold")
        self.pll_log_header.pack()

        # LO1 init
        self.LO1_gui = tk.Frame(self.merge)
        self.LO1_gui.pack(side="left")
        self.LO1_reg_frame = tk.Frame(self.LO1_gui)  # frame containing reg map
        self.LO1_middle_frame = tk.Frame(self.LO1_gui)  # frame contatining peripherals
        self.LO1_reg_frame.pack(side="left")
        self.LO1_middle_frame.pack(side="left")

        self.LO1_spacer1 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer2 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer3 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer4 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer5 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer6 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer7 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer8 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer9 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer10 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        self.LO1_spacer11 = tk.Canvas(self.LO1_reg_frame, bg="grey94", width=300, height=5)
        # spacers to prevent the GUI from getting cluttered, grey94 is the color of the window, looks like blank space

        self.LO1_reg_map_label = tk.Label(self.LO1_reg_frame, text="LO1 Register Map", font="Helvetica 15 bold")
        self.LO1_reg_map_label.pack()

        # soft reset checkbutton setup
        self.LO1_soft_name_label = tk.Label(self.LO1_reg_frame, text="Return FPGA to known State",
                                            font="Helvetica 10 bold")
        self.LO1_soft_name_label.pack()
        self.LO1_s0 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_schecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        # checkbutton (this data is only one bit)
        self.LO1_spacer_c = tk.Canvas(self.LO1_schecks, width=81, height=0, bg="grey94")
        self.LO1_spacer_c.pack(side="left")
        self.LO1_sc0 = tk.Checkbutton(self.LO1_schecks, text="Soft Reset", font="Consolas 8", variable=self.LO1_s0)
        self.LO1_schecks.pack(fill="x")
        # send button (only a write, no read for this one)
        self.LO1_send_but_frame = tk.Frame(self.LO1_schecks)
        self.LO1_send_but_frame.pack(side="right")
        self.LO1_sc0.pack(fill="both")  # pack left so that the buttons stack horizontally, pad helps de-clutter
        self.LO1_soft_send_button = tk.Button(self.LO1_send_but_frame, text="Send Bits", bg="lime green", width=10,
                                              height=1, command=self.LO1_soft_reset_send)
        self.LO1_soft_send_button.pack()
        self.LO1_spacer1.pack()
        # end soft reset section

        # dnc checkbutton setup section
        self.LO1_dnc_name_label = tk.Label(self.LO1_reg_frame, text="Downconverter Config", font="Helvetica 10 bold")
        self.LO1_dnc_name_label.pack()
        self.LO1_d1 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_d0 = tk.IntVar()
        self.LO1_dr1 = tk.IntVar()
        self.LO1_dr0 = tk.IntVar()
        self.LO1_dchecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_drchecks = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.LO1_dc1 = tk.Checkbutton(self.LO1_dchecks, text="DNC3 SEL", font="Consolas 8", variable=self.LO1_d1)
        self.LO1_dc0 = tk.Checkbutton(self.LO1_dchecks, text="DNC4 SEL", font="Consolas 8", variable=self.LO1_d0)
        self.LO1_drc1 = tk.Checkbutton(self.LO1_drchecks, text="DNC3 SEL", font="Consolas 8", variable=self.LO1_dr1)
        self.LO1_drc0 = tk.Checkbutton(self.LO1_drchecks, text="DNC4 SEL", font="Consolas 8", variable=self.LO1_dr0)
        self.LO1_dchecks.pack(fill="x")
        self.LO1_drchecks.pack(fill="x")
        self.LO1_spacer_dnc = tk.Canvas(self.LO1_dchecks, width=216, height=0, bg="grey94")
        self.LO1_spacer_dnc.pack(side="left")
        self.LO1_dc1.pack(side="left")
        self.LO1_dc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_dncr = tk.Canvas(self.LO1_drchecks, width=216, height=0, bg="grey94")
        self.LO1_spacer_dncr.pack(side="left")
        self.LO1_drc1.pack(side="left")
        self.LO1_drc0.pack(side="left")
        # read and write buttons for this address
        self.LO1_dnc_con_send_button = tk.Button(self.LO1_dchecks, text="Send Bits", bg="lime green", width=10,
                                                 height=1,
                                                 command=self.LO1_dnc_con_send)
        self.LO1_dnc_con_send_button.pack(side="right")
        self.LO1_dnc_con_read_button = tk.Button(self.LO1_drchecks, text="Read Bits", bg="black", fg="white", width=10,
                                                 height=1, command=self.LO1_dnc_con_read)
        self.LO1_dnc_con_read_button.pack(side="right")
        self.LO1_spacer2.pack()
        # end dnc

        # test checkbutton setup section
        self.LO1_test_name_label = tk.Label(self.LO1_reg_frame, text="Test Points", font="Helvetica 10 bold")
        self.LO1_test_name_label.pack()
        self.LO1_t2 = tk.IntVar()
        self.LO1_t1 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_t0 = tk.IntVar()
        self.LO1_tr2 = tk.IntVar()
        self.LO1_tr1 = tk.IntVar()
        self.LO1_tr0 = tk.IntVar()
        self.LO1_tchecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_trchecks = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.LO1_tc1 = tk.Checkbutton(self.LO1_tchecks, text="TP1", font="Consolas 8", variable=self.LO1_t1)
        self.LO1_tc0 = tk.Checkbutton(self.LO1_tchecks, text="TP2", font="Consolas 8", variable=self.LO1_t0)
        self.LO1_trc1 = tk.Checkbutton(self.LO1_trchecks, text="TP1", font="Consolas 8", variable=self.LO1_tr1)
        self.LO1_trc0 = tk.Checkbutton(self.LO1_trchecks, text="TP2", font="Consolas 8", variable=self.LO1_tr0)
        self.LO1_tchecks.pack(fill="x")
        self.LO1_trchecks.pack(fill="x")
        self.LO1_spacer_t = tk.Canvas(self.LO1_tchecks, width=252, height=0, bg="grey94")
        self.LO1_spacer_t.pack(side="left")  # reg ex and stuff
        self.LO1_tc1.pack(side="left")  # pad helps de-clutter
        self.LO1_tc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_tr = tk.Canvas(self.LO1_trchecks, width=252, height=0, bg="grey94")
        self.LO1_spacer_tr.pack(side="left")
        self.LO1_trc1.pack(side="left")
        self.LO1_trc0.pack(side="left")
        # read and write buttons for this address
        self.LO1_test_send_button = tk.Button(self.LO1_tchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                              command=self.LO1_test_pts_send)
        self.LO1_test_send_button.pack(side="right")
        self.LO1_test_read_button = tk.Button(self.LO1_trchecks, text="Read Bits", bg="black", fg="white", width=10,
                                              height=1, command=self.LO1_test_pts_read)
        self.LO1_test_read_button.pack(side="right")
        self.LO1_spacer3.pack()
        # end test

        # chip checkbutton setup section
        self.LO1_chip_name_label = tk.Label(self.LO1_reg_frame, text="PLL Chip Enable", font="Helvetica 10 bold")
        self.LO1_chip_name_label.pack()
        self.LO1_c1 = tk.IntVar()
        self.LO1_c0 = tk.IntVar()
        self.LO1_cr1 = tk.IntVar()
        self.LO1_cr0 = tk.IntVar()
        self.LO1_cchecks = tk.Frame(self.LO1_reg_frame)  # frame to contain a ll check buttons in one horizontal line
        self.LO1_crchecks = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.LO1_cc1 = tk.Checkbutton(self.LO1_cchecks, text="CE PLO", font="Consolas 8", variable=self.LO1_c1)
        self.LO1_cc0 = tk.Checkbutton(self.LO1_cchecks, text="CE LO2", font="Consolas 8", variable=self.LO1_c0)
        self.LO1_crc1 = tk.Checkbutton(self.LO1_crchecks, text="CE PLO", font="Consolas 8", variable=self.LO1_cr1)
        self.LO1_crc0 = tk.Checkbutton(self.LO1_crchecks, text="CE LO2", font="Consolas 8", variable=self.LO1_cr0)
        self.LO1_cchecks.pack(fill="x")
        self.LO1_crchecks.pack(fill="x")
        self.LO1_spacer_cen = tk.Canvas(self.LO1_cchecks, width=230, height=0, bg="grey94")
        self.LO1_spacer_cen.pack(side="left")
        self.LO1_cc1.pack(side="left")  # padx adds space on either side of each button. helps spread out
        self.LO1_cc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_cenr = tk.Canvas(self.LO1_crchecks, width=230, height=0, bg="grey94")
        self.LO1_spacer_cenr.pack(side="left")
        self.LO1_crc1.pack(side="left")
        self.LO1_crc0.pack(side="left")
        # individual read and write buttons for specific address
        self.LO1_chip_send_button = tk.Button(self.LO1_cchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                              command=self.LO1_chip_en_send)
        self.LO1_chip_send_button.pack(side="right")
        self.LO1_chip_read_button = tk.Button(self.LO1_crchecks, text="Read Bits", bg="black", fg="white", width=10,
                                              height=1,
                                              command=self.LO1_chip_en_read)
        self.LO1_chip_read_button.pack(side="right")
        self.LO1_spacer4.pack()
        # end of chip enable section

        # imp det read section
        self.LO1_imp_name_label = tk.Label(self.LO1_reg_frame, text="Input Power Detect", font="Helvetica 10 bold")
        self.LO1_imp_name_label.pack()
        self.LO1_ichecks = tk.Frame(self.LO1_reg_frame)
        self.LO1_ir0 = tk.IntVar()
        self.LO1_imp_check = tk.Checkbutton(self.LO1_ichecks, text="Power Detect", font="Consolas 8",
                                            variable=self.LO1_ir0)
        self.LO1_ichecks.pack(fill="x")
        self.LO1_spacer_ir = tk.Canvas(self.LO1_ichecks, width=79, height=0, bg="grey94")
        self.LO1_spacer_ir.pack(side="left")
        self.LO1_read_but_frame = tk.Frame(self.LO1_ichecks)
        self.LO1_read_but_frame.pack(side="right")
        self.LO1_imp_check.pack(fill="both")
        # read button for this address (no write)
        self.LO1_imp_read_button = tk.Button(self.LO1_read_but_frame, text="Read Bits", fg="white", bg="black",
                                             width=10,
                                             height=1, command=self.LO1_imp_det_read)
        self.LO1_imp_read_button.pack()
        self.LO1_spacer5.pack()
        # end imp det section

        # LO1 attenuator settings
        self.LO1_att_name_label = tk.Label(self.LO1_reg_frame, text="LO1 Digital Step Attenuator Settings",
                                           font="Helvetica 10 bold")
        self.LO1_att_name_label.pack()
        self.LO1_att5 = tk.IntVar()
        self.LO1_att4 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_att3 = tk.IntVar()
        self.LO1_att2 = tk.IntVar()
        self.LO1_att1 = tk.IntVar()
        self.LO1_att0 = tk.IntVar()
        self.LO1_attr5 = tk.IntVar()
        self.LO1_attr4 = tk.IntVar()
        self.LO1_attr3 = tk.IntVar()
        self.LO1_attr2 = tk.IntVar()
        self.LO1_attr1 = tk.IntVar()
        self.LO1_attr0 = tk.IntVar()
        self.LO1_attchecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_attrchecks = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.LO1_attc5 = tk.Checkbutton(self.LO1_attchecks, text="ATT 5", font="Consolas 8", variable=self.LO1_att5)
        self.LO1_attc4 = tk.Checkbutton(self.LO1_attchecks, text="ATT 4", font="Consolas 8", variable=self.LO1_att4)
        self.LO1_attc3 = tk.Checkbutton(self.LO1_attchecks, text="ATT 3", font="Consolas 8", variable=self.LO1_att3)
        self.LO1_attc2 = tk.Checkbutton(self.LO1_attchecks, text="ATT 2", font="Consolas 8", variable=self.LO1_att2)
        self.LO1_attc1 = tk.Checkbutton(self.LO1_attchecks, text="ATT 1", font="Consolas 8", variable=self.LO1_att1)
        self.LO1_attc0 = tk.Checkbutton(self.LO1_attchecks, text="ATT 0", font="Consolas 8", variable=self.LO1_att0)
        self.LO1_attrc5 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 5", font="Consolas 8", variable=self.LO1_attr5)
        self.LO1_attrc4 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 4", font="Consolas 8", variable=self.LO1_attr4)
        self.LO1_attrc3 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 3", font="Consolas 8", variable=self.LO1_attr3)
        self.LO1_attrc2 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 2", font="Consolas 8", variable=self.LO1_attr2)
        self.LO1_attrc1 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 1", font="Consolas 8", variable=self.LO1_attr1)
        self.LO1_attrc0 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 0", font="Consolas 8", variable=self.LO1_attr0)
        self.LO1_attchecks.pack(fill="x")
        self.LO1_attrchecks.pack(fill="x")
        self.LO1_spacer_att = tk.Canvas(self.LO1_attchecks, width=126, height=0, bg="grey94")
        self.LO1_spacer_att.pack(side="left")
        self.LO1_attc5.pack(side="left")
        self.LO1_attc4.pack(side="left")
        self.LO1_attc3.pack(side="left")
        self.LO1_attc2.pack(side="left")
        self.LO1_attc1.pack(side="left")
        self.LO1_attc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_attr = tk.Canvas(self.LO1_attrchecks, width=126, height=0, bg="grey94")
        self.LO1_spacer_attr.pack(side="left")
        self.LO1_attrc5.pack(side="left")
        self.LO1_attrc4.pack(side="left")
        self.LO1_attrc3.pack(side="left")
        self.LO1_attrc2.pack(side="left")
        self.LO1_attrc1.pack(side="left")
        self.LO1_attrc0.pack(side="left")
        # read and write buttons
        self.LO1_att_send_button = tk.Button(self.LO1_attchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                             command=self.LO1_att_send)
        self.LO1_att_send_button.pack(side="right")
        self.LO1_att_read_button = tk.Button(self.LO1_attrchecks, text="Read Bits", bg="black", fg="white", width=10,
                                             height=1,
                                             command=self.LO1_att_read)
        self.LO1_att_read_button.pack(side="right")
        self.LO1_spacer6.pack()
        # end att settings

        # RF DSA checkbutton setup section
        self.LO1_DSA_name_label = tk.Label(self.LO1_reg_frame, text="RF Digital Step Attenuator Settings",
                                           font="Helvetica 10 bold")
        self.LO1_DSA_name_label.pack()
        self.LO1_ds5 = tk.IntVar()
        self.LO1_ds4 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_ds3 = tk.IntVar()
        self.LO1_ds2 = tk.IntVar()
        self.LO1_ds1 = tk.IntVar()
        self.LO1_ds0 = tk.IntVar()
        self.LO1_dsr5 = tk.IntVar()
        self.LO1_dsr4 = tk.IntVar()
        self.LO1_dsr3 = tk.IntVar()
        self.LO1_dsr2 = tk.IntVar()
        self.LO1_dsr1 = tk.IntVar()
        self.LO1_dsr0 = tk.IntVar()
        self.LO1_dschecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_dsrchecks = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.LO1_dsc5 = tk.Checkbutton(self.LO1_dschecks, text="D5 ATT", font="Consolas 8", variable=self.LO1_ds5)
        self.LO1_dsc4 = tk.Checkbutton(self.LO1_dschecks, text="D4 ATT", font="Consolas 8", variable=self.LO1_ds4)
        self.LO1_dsc3 = tk.Checkbutton(self.LO1_dschecks, text="D3 ATT", font="Consolas 8", variable=self.LO1_ds3)
        self.LO1_dsc2 = tk.Checkbutton(self.LO1_dschecks, text="D2 ATT", font="Consolas 8", variable=self.LO1_ds2)
        self.LO1_dsc1 = tk.Checkbutton(self.LO1_dschecks, text="D1 ATT", font="Consolas 8", variable=self.LO1_ds1)
        self.LO1_dsc0 = tk.Checkbutton(self.LO1_dschecks, text="D0 ATT", font="Consolas 8", variable=self.LO1_ds0)
        self.LO1_dsrc5 = tk.Checkbutton(self.LO1_dsrchecks, text="D5 ATT", font="Consolas 8", variable=self.LO1_dsr5)
        self.LO1_dsrc4 = tk.Checkbutton(self.LO1_dsrchecks, text="D4 ATT", font="Consolas 8", variable=self.LO1_dsr4)
        self.LO1_dsrc3 = tk.Checkbutton(self.LO1_dsrchecks, text="D3 ATT", font="Consolas 8", variable=self.LO1_dsr3)
        self.LO1_dsrc2 = tk.Checkbutton(self.LO1_dsrchecks, text="D2 ATT", font="Consolas 8", variable=self.LO1_dsr2)
        self.LO1_dsrc1 = tk.Checkbutton(self.LO1_dsrchecks, text="D1 ATT", font="Consolas 8", variable=self.LO1_dsr1)
        self.LO1_dsrc0 = tk.Checkbutton(self.LO1_dsrchecks, text="D0 ATT", font="Consolas 8", variable=self.LO1_dsr0)
        self.LO1_dschecks.pack(fill="x")
        self.LO1_dsrchecks.pack(fill="x")
        self.LO1_spacer_ds = tk.Canvas(self.LO1_dschecks, width=110, height=0, bg="grey94")
        self.LO1_spacer_ds.pack(side="left")
        self.LO1_dsc5.pack(side="left")
        self.LO1_dsc4.pack(side="left")
        self.LO1_dsc3.pack(side="left")
        self.LO1_dsc2.pack(side="left")
        self.LO1_dsc1.pack(side="left")
        self.LO1_dsc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_dsr = tk.Canvas(self.LO1_dsrchecks, width=110, height=0, bg="grey94")
        self.LO1_spacer_dsr.pack(side="left")
        self.LO1_dsrc5.pack(side="left")
        self.LO1_dsrc4.pack(side="left")
        self.LO1_dsrc3.pack(side="left")
        self.LO1_dsrc2.pack(side="left")
        self.LO1_dsrc1.pack(side="left")
        self.LO1_dsrc0.pack(side="left")
        # read and write buttons
        self.LO1_dsa_send_button = tk.Button(self.LO1_dschecks, text="Send Bits", bg="lime green", width=10, height=1,
                                             command=self.LO1_dsa_send)
        self.LO1_dsa_send_button.pack(side="right")
        self.LO1_dsa_read_button = tk.Button(self.LO1_dsrchecks, text="Read Bits", bg="black", fg="white", width=10,
                                             height=1, command=self.LO1_dsa_read)
        self.LO1_dsa_read_button.pack(side="right")
        self.LO1_spacer7.pack()
        # end DSA LO1

        # dsa LO2 section
        self.LO1_DSAT_name_label = tk.Label(self.LO1_reg_frame, text="LO2 Digital Step Attenuator Settings",
                                            font="Helvetica 10 bold")
        self.LO1_DSAT_name_label.pack()
        self.LO1_dst5 = tk.IntVar()
        self.LO1_dst4 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_dst3 = tk.IntVar()
        self.LO1_dst2 = tk.IntVar()
        self.LO1_dst1 = tk.IntVar()
        self.LO1_dst0 = tk.IntVar()
        self.LO1_dstr5 = tk.IntVar()
        self.LO1_dstr4 = tk.IntVar()
        self.LO1_dstr3 = tk.IntVar()
        self.LO1_dstr2 = tk.IntVar()
        self.LO1_dstr1 = tk.IntVar()
        self.LO1_dstr0 = tk.IntVar()
        self.LO1_dstchecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_dstrchecks = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.LO1_dstc5 = tk.Checkbutton(self.LO1_dstchecks, text="D5 ATT", font="Consolas 8", variable=self.LO1_dst5)
        self.LO1_dstc4 = tk.Checkbutton(self.LO1_dstchecks, text="D4 ATT", font="Consolas 8", variable=self.LO1_dst4)
        self.LO1_dstc3 = tk.Checkbutton(self.LO1_dstchecks, text="D3 ATT", font="Consolas 8", variable=self.LO1_dst3)
        self.LO1_dstc2 = tk.Checkbutton(self.LO1_dstchecks, text="D2 ATT", font="Consolas 8", variable=self.LO1_dst2)
        self.LO1_dstc1 = tk.Checkbutton(self.LO1_dstchecks, text="D1 ATT", font="Consolas 8", variable=self.LO1_dst1)
        self.LO1_dstc0 = tk.Checkbutton(self.LO1_dstchecks, text="D0 ATT", font="Consolas 8", variable=self.LO1_dst0)
        self.LO1_dstrc5 = tk.Checkbutton(self.LO1_dstrchecks, text="D5 ATT", font="Consolas 8",
                                         variable=self.LO1_dstr5)
        self.LO1_dstrc4 = tk.Checkbutton(self.LO1_dstrchecks, text="D4 ATT", font="Consolas 8",
                                         variable=self.LO1_dstr4)
        self.LO1_dstrc3 = tk.Checkbutton(self.LO1_dstrchecks, text="D3 ATT", font="Consolas 8",
                                         variable=self.LO1_dstr3)
        self.LO1_dstrc2 = tk.Checkbutton(self.LO1_dstrchecks, text="D2 ATT", font="Consolas 8",
                                         variable=self.LO1_dstr2)
        self.LO1_dstrc1 = tk.Checkbutton(self.LO1_dstrchecks, text="D1 ATT", font="Consolas 8",
                                         variable=self.LO1_dstr1)
        self.LO1_dstrc0 = tk.Checkbutton(self.LO1_dstrchecks, text="D0 ATT", font="Consolas 8",
                                         variable=self.LO1_dstr0)
        self.LO1_dstchecks.pack(fill="x")
        self.LO1_dstrchecks.pack(fill="x")
        self.LO1_spacer_dst = tk.Canvas(self.LO1_dstchecks, width=110, height=0, bg="grey94")
        self.LO1_spacer_dst.pack(side="left")
        self.LO1_dstc5.pack(side="left")
        self.LO1_dstc4.pack(side="left")
        self.LO1_dstc3.pack(side="left")
        self.LO1_dstc2.pack(side="left")
        self.LO1_dstc1.pack(side="left")
        self.LO1_dstc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_dstr = tk.Canvas(self.LO1_dstrchecks, width=110, height=0, bg="grey94")
        self.LO1_spacer_dstr.pack(side="left")
        self.LO1_dstrc5.pack(side="left")
        self.LO1_dstrc4.pack(side="left")
        self.LO1_dstrc3.pack(side="left")
        self.LO1_dstrc2.pack(side="left")
        self.LO1_dstrc1.pack(side="left")
        self.LO1_dstrc0.pack(side="left")
        # read and write buttons
        self.LO1_dsat_send_button = tk.Button(self.LO1_dstchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                              command=self.LO1_dsat_send)
        self.LO1_dsat_send_button.pack(side="right")
        self.LO1_dsat_read_button = tk.Button(self.LO1_dstrchecks, text="Read Bits", bg="black", fg="white", width=10,
                                              height=1,
                                              command=self.LO1_dsat_read)
        self.LO1_dsat_read_button.pack(side="right")
        self.LO1_spacer8.pack()
        # end dsa lo2

        # sw section
        self.LO1_sw_name_label = tk.Label(self.LO1_reg_frame, text="Tune Switches", font="Helvetica 10 bold")
        self.LO1_sw_name_label.pack()
        # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_sw5 = tk.IntVar()
        self.LO1_sw4 = tk.IntVar()
        self.LO1_sw3 = tk.IntVar()
        self.LO1_sw2 = tk.IntVar()
        self.LO1_sw1 = tk.IntVar()
        self.LO1_sw0 = tk.IntVar()
        self.LO1_swr5 = tk.IntVar()
        self.LO1_swr4 = tk.IntVar()
        self.LO1_swr3 = tk.IntVar()
        self.LO1_swr2 = tk.IntVar()
        self.LO1_swr1 = tk.IntVar()
        self.LO1_swr0 = tk.IntVar()
        self.LO1_swchecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_swrchecks = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.LO1_swc5 = tk.Checkbutton(self.LO1_swchecks, text="LO1 MUTE", font="Consolas 8", variable=self.LO1_sw5)
        self.LO1_swc4 = tk.Checkbutton(self.LO1_swchecks, text="BPF SWA", font="Consolas 8", variable=self.LO1_sw4)
        self.LO1_swc3 = tk.Checkbutton(self.LO1_swchecks, text="BPF SWB", font="Consolas 8", variable=self.LO1_sw3)
        self.LO1_swc2 = tk.Checkbutton(self.LO1_swchecks, text="BPF SWC", font="Consolas 8", variable=self.LO1_sw2)
        self.LO1_swc1 = tk.Checkbutton(self.LO1_swchecks, text="RF COMB", font="Consolas 8", variable=self.LO1_sw1)
        self.LO1_swc0 = tk.Checkbutton(self.LO1_swchecks, text="RF SPLIT", font="Consolas 8", variable=self.LO1_sw0)
        self.LO1_swrc5 = tk.Checkbutton(self.LO1_swrchecks, text="LO1 MUTE", font="Consolas 8", variable=self.LO1_swr5)
        self.LO1_swrc4 = tk.Checkbutton(self.LO1_swrchecks, text="BPF SWA", font="Consolas 8", variable=self.LO1_swr4)
        self.LO1_swrc3 = tk.Checkbutton(self.LO1_swrchecks, text="BPF SWB", font="Consolas 8", variable=self.LO1_swr3)
        self.LO1_swrc2 = tk.Checkbutton(self.LO1_swrchecks, text="BPF SWC", font="Consolas 8", variable=self.LO1_swr2)
        self.LO1_swrc1 = tk.Checkbutton(self.LO1_swrchecks, text="RF COMB", font="Consolas 8", variable=self.LO1_swr1)
        self.LO1_swrc0 = tk.Checkbutton(self.LO1_swrchecks, text="RF SPLIT", font="Consolas 8", variable=self.LO1_swr0)
        self.LO1_swchecks.pack(fill="x")
        self.LO1_swrchecks.pack(fill="x")
        self.LO1_spacer_sw = tk.Canvas(self.LO1_swchecks, height=0, width=80, bg="grey94")
        self.LO1_spacer_sw.pack(side="left")
        self.LO1_swc5.pack(side="left")
        self.LO1_swc4.pack(side="left")
        self.LO1_swc3.pack(side="left")
        self.LO1_swc2.pack(side="left")
        self.LO1_swc1.pack(side="left")
        self.LO1_swc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_swr = tk.Canvas(self.LO1_swrchecks, height=0, width=80, bg="grey94")
        self.LO1_spacer_swr.pack(side="left")
        self.LO1_swrc5.pack(side="left")
        self.LO1_swrc4.pack(side="left")
        self.LO1_swrc3.pack(side="left")
        self.LO1_swrc2.pack(side="left")
        self.LO1_swrc1.pack(side="left")
        self.LO1_swrc0.pack(side="left")
        # read and write buttons
        self.LO1_sw_send_button = tk.Button(self.LO1_swchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                            command=self.LO1_sw_send)
        self.LO1_sw_send_button.pack(side="right")
        self.LO1_sw_read_button = tk.Button(self.LO1_swrchecks, text="Read Bits", bg="black", fg="white", width=10,
                                            height=1, command=self.LO1_sw_read)
        self.LO1_sw_read_button.pack(side="right")
        self.LO1_spacer9.pack()
        # end sw

        # start sw_2
        self.LO1_sw_name_label_2 = tk.Label(self.LO1_reg_frame, text="Mode Switches", font="Helvetica 10 bold")
        self.LO1_sw_name_label_2.pack()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_sw6_2 = tk.IntVar()
        self.LO1_sw5_2 = tk.IntVar()
        self.LO1_sw4_2 = tk.IntVar()
        self.LO1_sw3_2 = tk.IntVar()
        self.LO1_sw2_2 = tk.IntVar()
        self.LO1_sw1_2 = tk.IntVar()
        self.LO1_sw0_2 = tk.IntVar()
        self.LO1_swr6_2 = tk.IntVar()
        self.LO1_swr5_2 = tk.IntVar()
        self.LO1_swr4_2 = tk.IntVar()
        self.LO1_swr3_2 = tk.IntVar()
        self.LO1_swr2_2 = tk.IntVar()
        self.LO1_swr1_2 = tk.IntVar()
        self.LO1_swr0_2 = tk.IntVar()
        self.LO1_swchecks_2 = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_swrchecks_2 = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed (read checkbuttons have r)
        # write button sends checked boxes as binary number to bus
        self.LO1_swc6_2 = tk.Checkbutton(self.LO1_swchecks_2, text="RFO BYP", font="Consolas 8",
                                         variable=self.LO1_sw6_2)
        self.LO1_swc5_2 = tk.Checkbutton(self.LO1_swchecks_2, text="LO1 IMP", font="Consolas 8",
                                         variable=self.LO1_sw5_2)
        self.LO1_swc4_2 = tk.Checkbutton(self.LO1_swchecks_2, text="UPC LO1", font="Consolas 8",
                                         variable=self.LO1_sw4_2)
        self.LO1_swc3_2 = tk.Checkbutton(self.LO1_swchecks_2, text="IF BYP", font="Consolas 8",
                                         variable=self.LO1_sw3_2)
        self.LO1_swc2_2 = tk.Checkbutton(self.LO1_swchecks_2, text="AMP BIAS", font="Consolas 8",
                                         variable=self.LO1_sw2_2)
        self.LO1_swc1_2 = tk.Checkbutton(self.LO1_swchecks_2, text="RFO 1", font="Consolas 8", variable=self.LO1_sw1_2)
        self.LO1_swc0_2 = tk.Checkbutton(self.LO1_swchecks_2, text="RFO 0", font="Consolas 8", variable=self.LO1_sw0_2)
        self.LO1_swrc6_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="RFO BYP", font="Consolas 8",
                                          variable=self.LO1_swr6_2)
        self.LO1_swrc5_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="LO1 IMP", font="Consolas 8",
                                          variable=self.LO1_swr5_2)
        self.LO1_swrc4_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="UPC LO1", font="Consolas 8",
                                          variable=self.LO1_swr4_2)
        self.LO1_swrc3_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="IF BYP", font="Consolas 8",
                                          variable=self.LO1_swr3_2)
        self.LO1_swrc2_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="AMP BIAS", font="Consolas 8",
                                          variable=self.LO1_swr2_2)
        self.LO1_swrc1_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="RFO 1", font="Consolas 8",
                                          variable=self.LO1_swr1_2)
        self.LO1_swrc0_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="RFO 0", font="Consolas 8",
                                          variable=self.LO1_swr0_2)
        self.LO1_swchecks_2.pack(fill="x")
        self.LO1_swrchecks_2.pack(fill="x")
        self.LO1_spacer_sw_2 = tk.Canvas(self.LO1_swchecks_2, bg="grey94", width=50, height=0)
        self.LO1_spacer_sw_2.pack(side="left")
        self.LO1_swc6_2.pack(side="left")
        self.LO1_swc5_2.pack(side="left")
        self.LO1_swc4_2.pack(side="left")
        self.LO1_swc3_2.pack(side="left")
        self.LO1_swc2_2.pack(side="left")
        self.LO1_swc1_2.pack(side="left")
        self.LO1_swc0_2.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_swr_2 = tk.Canvas(self.LO1_swrchecks_2, bg="grey94", width=50, height=0)
        self.LO1_spacer_swr_2.pack(side="left")
        self.LO1_swrc6_2.pack(side="left")
        self.LO1_swrc5_2.pack(side="left")
        self.LO1_swrc4_2.pack(side="left")
        self.LO1_swrc3_2.pack(side="left")
        self.LO1_swrc2_2.pack(side="left")
        self.LO1_swrc1_2.pack(side="left")
        self.LO1_swrc0_2.pack(side="left")
        # read and write buttons
        self.LO1_sw_send_button_2 = tk.Button(self.LO1_swchecks_2, text="Send Bits", bg="lime green", width=10,
                                              height=1, command=self.LO1_sw_send_2)
        self.LO1_sw_send_button_2.pack(side="right")
        self.LO1_sw_read_button_2 = tk.Button(self.LO1_swrchecks_2, text="Read Bits", bg="black", fg="white", width=10,
                                              height=1, command=self.LO1_sw_read_2)
        self.LO1_sw_read_button_2.pack(side="right")
        self.LO1_spacer10.pack()
        # end sw_2

        # start sw_3
        self.LO1_sw_name_label_3 = tk.Label(self.LO1_reg_frame, text="ATE Test Switches", font="Helvetica 10 bold")
        self.LO1_sw_name_label_3.pack()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_sw2_3 = tk.IntVar()
        self.LO1_sw1_3 = tk.IntVar()
        self.LO1_sw0_3 = tk.IntVar()
        self.LO1_swr2_3 = tk.IntVar()
        self.LO1_swr1_3 = tk.IntVar()
        self.LO1_swr0_3 = tk.IntVar()
        self.LO1_swchecks_3 = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_swrchecks_3 = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed (read checkbuttons have r)
        # write button sends checked boxes as binary number to bus
        self.LO1_swc2_3 = tk.Checkbutton(self.LO1_swchecks_3, text="LO2 IMP SEL", font="Consolas 8",
                                         variable=self.LO1_sw2_3)
        self.LO1_swc1_3 = tk.Checkbutton(self.LO1_swchecks_3, text="LO2 DEST SEL", font="Consolas 8",
                                         variable=self.LO1_sw1_3)
        self.LO1_swc0_3 = tk.Checkbutton(self.LO1_swchecks_3, text="TP SEL", font="Consolas 8",
                                         variable=self.LO1_sw0_3)
        self.LO1_swrc2_3 = tk.Checkbutton(self.LO1_swrchecks_3, text="LO2 IMP SEL", font="Consolas 8",
                                          variable=self.LO1_swr2_3)
        self.LO1_swrc1_3 = tk.Checkbutton(self.LO1_swrchecks_3, text="LO2 DEST SEL", font="Consolas 8",
                                          variable=self.LO1_swr1_3)
        self.LO1_swrc0_3 = tk.Checkbutton(self.LO1_swrchecks_3, text="TP SEL", font="Consolas 8",
                                          variable=self.LO1_swr0_3)
        self.LO1_swchecks_3.pack(fill="x")
        self.LO1_swrchecks_3.pack(fill="x")
        self.LO1_spacer_sw_3 = tk.Canvas(self.LO1_swchecks_3, bg="grey94", width=170, height=0)
        self.LO1_spacer_sw_3.pack(side="left")
        self.LO1_swc2_3.pack(side="left")
        self.LO1_swc1_3.pack(side="left")
        self.LO1_swc0_3.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_swr_3 = tk.Canvas(self.LO1_swrchecks_3, bg="grey94", width=170, height=0)
        self.LO1_spacer_swr_3.pack(side="left")
        self.LO1_swrc2_3.pack(side="left")
        self.LO1_swrc1_3.pack(side="left")
        self.LO1_swrc0_3.pack(side="left")
        # read and write buttons
        self.LO1_sw_send_button_3 = tk.Button(self.LO1_swchecks_3, text="Send Bits", bg="lime green", width=10,
                                              height=1,
                                              command=self.LO1_sw_send_3)
        self.LO1_sw_send_button_3.pack(side="right")
        self.LO1_sw_read_button_3 = tk.Button(self.LO1_swrchecks_3, text="Read Bits", bg="black", fg="white", width=10,
                                              height=1, command=self.LO1_sw_read_3)
        self.LO1_sw_read_button_3.pack(side="right")
        self.LO1_spacer11.pack()
        # end sw_3

        # start low pass filter
        self.LO1_lpf_name_label = tk.Label(self.LO1_reg_frame, text="Tunable Low Pass Filter", font="Helvetica 10 bold")
        self.LO1_lpf_name_label.pack()
        self.LO1_lpf4 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_lpf3 = tk.IntVar()
        self.LO1_lpf2 = tk.IntVar()
        self.LO1_lpf1 = tk.IntVar()
        self.LO1_lpf0 = tk.IntVar()
        self.LO1_lpfr4 = tk.IntVar()
        self.LO1_lpfr3 = tk.IntVar()
        self.LO1_lpfr2 = tk.IntVar()
        self.LO1_lpfr1 = tk.IntVar()
        self.LO1_lpfr0 = tk.IntVar()
        self.LO1_lpfchecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        self.LO1_lpfrchecks = tk.Frame(self.LO1_reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed (read checkbuttons have r)
        # write button sends checked boxes as binary number to bus
        self.LO1_lpfc4 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 5", font="Consolas 8", variable=self.LO1_lpf4)
        self.LO1_lpfc3 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 4", font="Consolas 8", variable=self.LO1_lpf3)
        self.LO1_lpfc2 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 3", font="Consolas 8", variable=self.LO1_lpf2)
        self.LO1_lpfc1 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 2", font="Consolas 8", variable=self.LO1_lpf1)
        self.LO1_lpfc0 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 1", font="Consolas 8", variable=self.LO1_lpf0)
        self.LO1_lpfrc4 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 5", font="Consolas 8", variable=self.LO1_lpfr4)
        self.LO1_lpfrc3 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 4", font="Consolas 8", variable=self.LO1_lpfr3)
        self.LO1_lpfrc2 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 3", font="Consolas 8", variable=self.LO1_lpfr2)
        self.LO1_lpfrc1 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 2", font="Consolas 8", variable=self.LO1_lpfr1)
        self.LO1_lpfrc0 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 1", font="Consolas 8", variable=self.LO1_lpfr0)
        self.LO1_lpfchecks.pack(fill="x")
        self.LO1_lpfrchecks.pack(fill="x")
        self.LO1_spacer_lpf = tk.Canvas(self.LO1_lpfchecks, bg="grey94", height=0, width=167)
        self.LO1_spacer_lpf.pack(side="left")
        self.LO1_lpfc4.pack(side="left")
        self.LO1_lpfc3.pack(side="left")
        self.LO1_lpfc2.pack(side="left")
        self.LO1_lpfc1.pack(side="left")
        self.LO1_lpfc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_lpfr = tk.Canvas(self.LO1_lpfrchecks, bg="grey94", height=0, width=167)
        self.LO1_spacer_lpfr.pack(side="left")
        self.LO1_lpfrc4.pack(side="left")
        self.LO1_lpfrc3.pack(side="left")
        self.LO1_lpfrc2.pack(side="left")
        self.LO1_lpfrc1.pack(side="left")
        self.LO1_lpfrc0.pack(side="left")
        # read and write buttons
        self.LO1_lpf_send_button = tk.Button(self.LO1_lpfchecks, text="Send Bits", bg="lime green", width=10, height=1,
                                             command=self.LO1_lpf_send)
        self.LO1_lpf_send_button.pack(side="right")
        self.LO1_lpf_read_button = tk.Button(self.LO1_lpfrchecks, text="Read Bits", bg="black", fg="white", width=10,
                                             height=1, command=self.LO1_lpf_read)
        self.LO1_lpf_read_button.pack(side="right")
        # end low pass filter

        #self.LO1_reg_test_button = tk.Button(self.LO1_reg_frame, text="Test Reg Map", width=10, height=1, bg='orange',
                                             #command=self.LO1_reg_test)
        #self.LO1_reg_test_button.pack()  # register test button that writes and reads data back to verify registers work

        # begin middle frame code
        # bpf dac
        self.LO1_periph_hader = tk.Label(self.LO1_middle_frame, text="LO1 Peripherals", font="Helvetica 10 bold")
        self.LO1_periph_hader.pack()
        self.LO1_bpf_header = tk.Label(self.LO1_middle_frame, text="BPF DAC", font="Helvetica 10 bold")
        self.LO1_bpf_header.pack()
        self.LO1_bpf_dac_label = tk.Label(self.LO1_middle_frame, text="Enter a voltage 0-2.5V")
        self.LO1_bpf_dac_label.pack()
        self.LO1_bpf_dac_voltage = tk.StringVar()
        self.LO1_bpf_dac_entry = tk.Entry(self.LO1_middle_frame, textvariable=self.LO1_bpf_dac_voltage)
        self.LO1_bpf_dac_entry.pack()
        self.LO1_bpf_dac_button = tk.Button(self.LO1_middle_frame, text="BPF DAC Write", fg="white", bg="steel blue",
                                            command=self.LO1_bpf_dac_write)
        self.LO1_bpf_dac_button.pack()

        self.LO1_spacer12 = tk.Canvas(self.LO1_middle_frame, bg="grey94", height=5, width=200)
        self.LO1_spacer12.pack()
        # vxp dac
        self.LO1_vxp_header = tk.Label(self.LO1_middle_frame, text="VXP DAC", font="Helvetica 10 bold")
        self.LO1_vxp_header.pack()
        self.LO1_vxp_dac_label = tk.Label(self.LO1_middle_frame, text="Enter a voltage 0-2.5V")
        self.LO1_vxp_dac_label.pack()
        self.LO1_vxp_dac_voltage = tk.StringVar()
        self.LO1_vxp_dac_entry = tk.Entry(self.LO1_middle_frame, textvariable=self.LO1_vxp_dac_voltage)
        self.LO1_vxp_dac_entry.pack()
        self.LO1_vxp_dac_a_buton = tk.Button(self.LO1_middle_frame, text="VXP DAC A Write", bg="yellow2",
                                             command=self.LO1_vxp_dac_a_write)
        self.LO1_vxp_dac_a_buton.pack()
        self.LO1_vxp_dac_b_buton = tk.Button(self.LO1_middle_frame, text="VXP DAC B Write", bg="medium orchid",
                                             command=self.LO1_vxp_dac_b_write)
        self.LO1_vxp_dac_b_buton.pack()

        self.LO1_spacer13 = tk.Canvas(self.LO1_middle_frame, bg="grey94", height=5, width=200)
        self.LO1_spacer13.pack()
        # Temp monitor
        self.LO1_temp_header = tk.Label(self.LO1_middle_frame, text="Temperature Monitor", font="Helvetica 10 bold")
        self.LO1_temp_header.pack()
        self.LO1_temp_string = tk.StringVar()
        self.LO1_temp_display = tk.Entry(self.LO1_middle_frame, textvariable=self.LO1_temp_string)
        self.LO1_temp_display.pack()
        self.LO1_temp_read_button = tk.Button(self.LO1_middle_frame, bg="orange", text="Read Temp",
                                              command=self.LO1_temp_read)
        self.LO1_temp_read_button.pack()

        self.LO1_spacer14 = tk.Canvas(self.LO1_middle_frame, bg="grey94", height=5, width=200)
        self.LO1_spacer14.pack()
        # ADC
        self.LO1_adc_header = tk.Label(self.LO1_middle_frame, text="LTC2313-12 ADC", font="Helvetica 10 bold")
        self.LO1_adc_header.pack()
        self.LO1_adc_value = tk.StringVar()
        self.LO1_adc_display = tk.Entry(self.LO1_middle_frame, textvariable=self.LO1_adc_value)
        self.LO1_adc_display.pack()
        self.LO1_adc_read_button = tk.Button(self.LO1_middle_frame, text="Read ADC", bg="seagreen1",
                                             command=self.LO1_adc_read)
        self.LO1_adc_read_button.pack()

        self.LO1_spacer15 = tk.Canvas(self.LO1_middle_frame, bg="grey94", height=20, width=200)
        self.LO1_spacer15.pack()
        #self.LO1_quit_button = tk.Button(self.LO1_middle_frame, width=10, height=1, text="Quit", bg="red",
        #                             command=self.merge.destroy)
        #self.LO1_quit_button.pack()

        # DNC init
        self.dnc_gui = tk.Frame(self.merge)
        self.dnc_gui.pack(side="left")
        # yay

        # initialize PLLGui (right section of GUI)
        self.root = tk.Frame(self.merge)  # create frame for PLLGui
        self.root.pack(side="left", padx=40)
        #self.canvas = tk.Canvas(self.root, width=400, height=0)
        #self.canvas.pack(fill="both", expand=True)  # auto resizes window based off gui
        #self.canvas.pack()
        self.username = getpass.getuser()
        self.name_label = tk.Label(self.root)
        self.name_label.config(text="Hello " + self.username+"\n", font="Helvetica 10 bold")
        self.ref_label = tk.Label(self.root)
        self.ref_label.config(text="Reference Freq.", font="Helvetica 10 bold")
        self.tenmhz_button = tk.Button(self.root, text='10 MHz Ref.', width=25, command=self.pll_init_10)
        self.hundredmhz_button = tk.Button(self.root, text='100 MHz Ref.', width=25, command=self.pll_init_100)
        self.goBack_label = tk.Label(self.root)
        self.goBack_label.config(text="Back", font="Helvetica 10 bold")
        self.goBack_button = tk.Button(self.root, fg="Black", text='Back to main menu', width=25, command=self.goBack)
        self.quit_label = tk.Label(self.root)
        self.quit_label.config(text="Quit", font="Helvetica 10 bold")
        self.quit_button = tk.Button(self.root, bg="Red", text='Quit', width=25, command=self.merge.destroy)
        self.spacer10 = tk.Canvas(self.root, bg="grey94", width="10", height="20")


        # level one GUI, packed now
        # top level name
        self.name_label.pack()
        # reference frequency
        self.ref_label.pack()
        self.tenmhz_button.pack()
        self.hundredmhz_button.pack()
        # quit
        self.quit_label.pack()
        self.quit_button.pack()

        # level two GUI, packed later
        # calibration options
        self.cal_label = tk.Label(self.root)
        self.cal_label.config(text="Calibration Options", font="Helvetica 10 bold")
        self.fullcal_button = tk.Button(self.root, text="Run Full Calibration", width=25, command=self.fullcal)
        self.loadcal_button = tk.Button(self.root, text="Load Calibration", width=25, command=self.loadcal)
        # autocal frequency jump
        self.autocal_label = tk.Label(self.root)
        self.autocal_label.config(text="Auto Cal Frequency Jump", font="Helvetica 10 bold")
        self.autocal_freq = 6500
        self.autocal_entry = tk.Entry(self.root, width=25)
        self.autocal_button = tk.Button(self.root, text="Autocal Freq. Jump (MHz)", width=25, command=self.autocal_freq_fun)
        # debug options
        self.debug_label = tk.Label(self.root)
        self.debug_label.config(text="Debug Options", font="Helvetica 10 bold")
        self.printreg_button = tk.Button(self.root, text="Print Registers", width=25, command=self.printregisters)
        self.printcal_button = tk.Button(self.root, text="Print Cal Table", width=25, command=self.printcaltable)
        #self.test_button = tk.Button(self.root, text="TEST", width=25, command=self.test)
        self.PLL_frame = tk.Frame(self.root)
        self.slave_set_button = tk.Button(self.PLL_frame, text="Select PLL", width=10, height=1, bg="orange",
                                             command=self.slave_set)
        self.pll_ss_dict = {"PLL1":0b10000000, "PLL2":0b10000001, "PLL3":0b10000010, "PLL4":0b10000011}
        self.dropdown = tk.OptionMenu(self.PLL_frame, self.var, *self.pll_ss_dict)  # dropdown menu



        # level three GUI, packed later
        # full call option
        self.fullcal_button3 = tk.Button(self.root, text="Run Full Calibration", width=25, command=self.fullcal3)
        # autocal frequency option

        # bypass autocal frequency option
        self.freq_label = tk.Label(self.root)
        self.freq_label.config(text="Bypass Autocal Frequency Jump", font="Helvetica 10 bold")
        self.bypass_freq = 6500  # frequency entry
        self.freq_entry = tk.Entry(self.root, width=25)
        self.jump_button = tk.Button(self.root, text="Bypass Autocal Freq. Jump (MHz)", width=25, command=self.jumpfreq)
        # ABA spreadsheet
        # self.sheet_label = tk.Label(self.root)
        # self.sheet_label.config(text="Generate A->B->A Spreadsheet", font="Helvetica 10 bold")
        # self.freq1_label = tk.Label(self.root)
        # self.freq1_label.config(text="Frequency 1 (MHz)")
        # self.freq1 = 7000  # frequency 1 entry
        # self.freq1_entry = tk.Entry(self.root, width=25)
        # self.freq2_label = tk.Label(self.root)
        # self.freq2_label.config(text="Frequency 2 (MHz)")
        # self.freq2 = 8000  # frequency 2 entry
        # self.freq2_entry = tk.Entry(self.root, width=25)
        # self.delay_label = tk.Label(self.root)
        # self.delay_label.config(text="Delay between Freq.'s (uS)")
        # self.delay = 50  # delay between freq 1 and freq 2
        # self.delay_entry = tk.Entry(self.root, width=25)
        # self.sheet_button = tk.Button(self.root, text="Generate A->B->A Spreadsheet", width=25, command=self.generate_ABA_spreadsheet)


        # cal table spreadsheet debug option
        self.caltable_spreadsheet_button = tk.Button(self.root, text="Generate Cal. Table Spreadsheet", width=25, command=self.generate_caltable_spreadsheet)
        self.filename_ABA = "empty"
        self.filename_caltable = "empty"

        # debug lookuptable
        self.lookuptable_label = tk.Label(self.root)
        self.lookuptable_label.config(text="Lookuptable Debug", font="Helvetica 10 bold")
        self.reg_label = tk.Label(self.root)
        self.reg_label.config(text="Register Address")
        self.lookuptable_reg = 0  # lookuptable reg value
        self.lookuptable_reg_entry = tk.Entry(self.root, width=25)
        self.value_label = tk.Label(self.root)
        self.value_label.config(text="Register Value")
        self.lookuptable_value = 0  # lookuptable value to be stored in register
        self.lookuptable_value_entry = tk.Entry(self.root, width=25)
        self.lfreq_label = tk.Label(self.root)
        self.lfreq_label.config(text="Frequency (MHz)")
        self.lfreq = 6500  # lookuptable frequency to edit
        self.lfreq_entry = tk.Entry(self.root, width=25)
        # self.sheetPerFreq_button = tk.Button(self.root, text="Generate Bit Bang spreadsheets", width=25,command=self.generate_bypassautocal_spreadsheet_per_freq)
        self.lookuptable_button = tk.Button(self.root, text="Edit PLL Lookup Table", width=25, command=self.changetable)

        # PLL log section
        self.PLL1_string = tk.StringVar()
        self.PLL2_string = tk.StringVar()
        self.PLL3_string = tk.StringVar()
        self.PLL4_string = tk.StringVar()
        self.PLL1_label = tk.Label(self.log_frame, text="Last Entry to PLL1 (MHz)", font="Helvetica 10 bold")
        self.PLL1_label.pack()
        self.PLL1_last_entry = tk.Entry(self.log_frame, textvariable=self.PLL1_string)
        self.PLL1_last_entry.pack()
        self.PLL2_label = tk.Label(self.log_frame, text="Last Entry to PLL2 (MHz)", font="Helvetica 10 bold")
        self.PLL2_label.pack()
        self.PLL2_last_entry = tk.Entry(self.log_frame, textvariable=self.PLL2_string)
        self.PLL2_last_entry.pack()
        self.PLL3_label = tk.Label(self.log_frame, text="Last Entry to PLL3 (MHz)", font="Helvetica 10 bold")
        self.PLL3_label.pack()
        self.PLL3_last_entry = tk.Entry(self.log_frame, textvariable=self.PLL3_string)
        self.PLL3_last_entry.pack()
        self.PLL4_label = tk.Label(self.log_frame, text="Last Entry to PLL4 (MHz)", font="Helvetica 10 bold")
        self.PLL4_label.pack()
        self.PLL4_last_entry = tk.Entry(self.log_frame, textvariable=self.PLL4_string)
        self.PLL4_last_entry.pack()

        self.sensor_kickoff_header = tk.Label(self.log_frame, text="LO2 Sensor Values", font="Helvetica 10 bold")
        self.sensor_kickoff_header.pack()

        # values read from the V1-V8; raw and then converted with formula data (entries)
        self.five_volt1_raw = tk.IntVar()
        self.five_volt1_current = tk.IntVar()
        self.four_volt1_raw = tk.IntVar()
        self.four_volt1_current = tk.IntVar()
        self.four_volt2_raw = tk.IntVar()
        self.four_volt2_current = tk.IntVar()
        self.temp_raw = tk.IntVar()
        self.temperature = tk.IntVar()
        self.four_volt3_raw = tk.IntVar()
        self.four_volt3_current = tk.IntVar()
        self.five_volt2_raw = tk.IntVar()
        self.five_volt2_current = tk.IntVar()
        self.three_three_voltage = tk.IntVar()
        self.three_three_raw = tk.IntVar()
        self.two_five_voltage = tk.IntVar()
        self.two_five_raw = tk.IntVar()
        self.one_two_voltage = tk.IntVar()
        self.one_two_raw = tk.IntVar()

        self.five_volt_current1_label = tk.Label(self.log_frame, text="Current of +5V of LO2 @ output of LDO", font="Helvetica 10 bold")
        self.five_volt_current1_label.pack()
        self.calc_frame_1 = tk.Frame(self.log_frame)
        self.calc_frame_1.pack()
        self.calc_label_1 = tk.Label(self.calc_frame_1, text="value (uA):", font="Helvetica 8")
        self.calc_label_1.pack(side="left")
        self.five_volt_current1_entry = tk.Entry(self.calc_frame_1, textvariable=self.five_volt1_current)
        self.five_volt_current1_entry.pack()
        self.raw_frame_1 = tk.Frame(self.log_frame)
        self.raw_frame_1.pack()
        self.raw_label_1 = tk.Label(self.raw_frame_1, text=" raw data: ", font="Helvetica 8")
        self.raw_label_1.pack(side="left")
        self.five_volt_current1_raw_entry = tk.Entry(self.raw_frame_1, textvariable=self.five_volt1_raw)
        self.five_volt_current1_raw_entry.pack()

        self.four_volt_current1_label = tk.Label(self.log_frame, text="Current drawn from +4V by synths 1&2", font="Helvetica 10 bold")
        self.four_volt_current1_label.pack()
        self.calc_frame_2 = tk.Frame(self.log_frame)
        self.calc_frame_2.pack()
        self.calc_label_2 = tk.Label(self.calc_frame_2, text="value (uA):", font="Helvetica 8")
        self.calc_label_2.pack(side="left")
        self.four_volt_current1_entry = tk.Entry(self.calc_frame_2, textvariable=self.four_volt1_current)
        self.four_volt_current1_entry.pack()
        self.raw_frame_2 = tk.Frame(self.log_frame)
        self.raw_frame_2.pack()
        self.raw_label_2 = tk.Label(self.raw_frame_2, text=" raw data: ", font="Helvetica 8")
        self.raw_label_2.pack(side="left")
        self.four_volt_current1_raw_entry = tk.Entry(self.raw_frame_2, textvariable=self.four_volt1_raw)
        self.four_volt_current1_raw_entry.pack()

        self.four_volt_current2_label = tk.Label(self.log_frame, text="Current drawn from +4V by synths 3&4", font="Helvetica 10 bold")
        self.four_volt_current2_label.pack()
        self.calc_frame_3 = tk.Frame(self.log_frame)
        self.calc_frame_3.pack()
        self.calc_label_3 = tk.Label(self.calc_frame_3, text="value (uA):", font="Helvetica 8")
        self.calc_label_3.pack(side="left")
        self.four_volt_current2_entry = tk.Entry(self.calc_frame_3, textvariable=self.four_volt2_current)
        self.four_volt_current2_entry.pack()
        self.raw_frame_3 = tk.Frame(self.log_frame)
        self.raw_frame_3.pack()
        self.raw_label_3 = tk.Label(self.raw_frame_3, text=" raw data: ", font="Helvetica 8")
        self.raw_label_3.pack(side="left")
        self.four_volt_current2_raw_entry = tk.Entry(self.raw_frame_3, textvariable=self.four_volt2_raw)
        self.four_volt_current2_raw_entry.pack()

        self.LO2_temp_label = tk.Label(self.log_frame, text="Temperature of LO2 board", font="Helvetica 10 bold")
        self.LO2_temp_label.pack()
        self.calc_frame_4 = tk.Frame(self.log_frame)
        self.calc_frame_4.pack()
        self.calc_label_4 = tk.Label(self.calc_frame_4, text="value (°C):", font="Helvetica 8")
        self.calc_label_4.pack(side="left")
        self.LO2_temp_entry = tk.Entry(self.calc_frame_4, textvariable=self.temperature)
        self.LO2_temp_entry.pack()
        self.raw_frame_4 = tk.Frame(self.log_frame)
        self.raw_frame_4.pack()
        self.raw_label_4 = tk.Label(self.raw_frame_4, text=" raw data: ", font="Helvetica 8")
        self.raw_label_4.pack(side="left")
        self.LO2_temp_raw_entry = tk.Entry(self.raw_frame_4, textvariable=self.temp_raw)
        self.LO2_temp_raw_entry.pack()

        self.four_volt_current3_label = tk.Label(self.log_frame, text="Current drawn from +4V by LO1&LO2 synths", font="Helvetica 10 bold")
        self.four_volt_current3_label.pack()
        self.calc_frame_5 = tk.Frame(self.log_frame)
        self.calc_frame_5.pack()
        self.calc_label_5 = tk.Label(self.calc_frame_5, text="value (uA):", font="Helvetica 8")
        self.calc_label_5.pack(side="left")
        self.four_volt_current3_entry = tk.Entry(self.calc_frame_5, textvariable=self.four_volt3_current)
        self.four_volt_current3_entry.pack()
        self.raw_frame_5 = tk.Frame(self.log_frame)
        self.raw_frame_5.pack()
        self.raw_label_5 = tk.Label(self.raw_frame_5, text=" raw data: ", font="Helvetica 8")
        self.raw_label_5.pack(side="left")
        self.four_volt_current3_raw_entry = tk.Entry(self.raw_frame_5, textvariable=self.four_volt3_raw)
        self.four_volt_current3_raw_entry.pack()

        self.five_volt_current2_label = tk.Label(self.log_frame, text="Current of +5VA of LO1/UPC board @ output of LDO", font="Helvetica 10 bold")
        self.five_volt_current2_label.pack()
        self.calc_frame_6 = tk.Frame(self.log_frame)
        self.calc_frame_6.pack()
        self.calc_label_6 = tk.Label(self.calc_frame_6, text="value (uA):", font="Helvetica 8")
        self.calc_label_6.pack(side="left")
        self.five_volt_current2_entry = tk.Entry(self.calc_frame_6, textvariable=self.five_volt2_current)
        self.five_volt_current2_entry.pack()
        self.raw_frame_6 = tk.Frame(self.log_frame)
        self.raw_frame_6.pack()
        self.raw_label_6 = tk.Label(self.raw_frame_6, text=" raw data: ", font="Helvetica 8")
        self.raw_label_6.pack(side="left")
        self.five_volt_current2_raw_entry = tk.Entry(self.raw_frame_6, textvariable=self.five_volt2_raw)
        self.five_volt_current2_raw_entry.pack()

        self.three_three_voltage_label = tk.Label(self.log_frame, text="+3.3V Voltage", font="Helvetica 10 bold")
        self.three_three_voltage_label.pack()
        self.calc_frame_7 = tk.Frame(self.log_frame)
        self.calc_frame_7.pack()
        self.calc_label_7 = tk.Label(self.calc_frame_7, text="value (V): ", font="Helvetica 8")
        self.calc_label_7.pack(side="left")
        self.three_three_voltage_entry = tk.Entry(self.calc_frame_7, textvariable=self.three_three_voltage)
        self.three_three_voltage_entry.pack()
        self.raw_frame_7 = tk.Frame(self.log_frame)
        self.raw_frame_7.pack()
        self.raw_label_7 = tk.Label(self.raw_frame_7, text="raw data: ", font="Helvetica 8")
        self.raw_label_7.pack(side="left")
        self.three_three_raw_entry = tk.Entry(self.raw_frame_7, textvariable=self.three_three_raw)
        self.three_three_raw_entry.pack()

        self.two_five_voltage_label = tk.Label(self.log_frame, text="+2.5V Voltage", font="Helvetica 10 bold")
        self.two_five_voltage_label.pack()
        self.calc_frame_8 = tk.Frame(self.log_frame)
        self.calc_frame_8.pack()
        self.calc_label_8 = tk.Label(self.calc_frame_8, text="value (V): ", font="Helvetica 8")
        self.calc_label_8.pack(side="left")
        self.two_five_voltage_entry = tk.Entry(self.calc_frame_8, textvariable=self.two_five_voltage)
        self.two_five_voltage_entry.pack()
        self.raw_frame_8 = tk.Frame(self.log_frame)
        self.raw_frame_8.pack()
        self.raw_label_8 = tk.Label(self.raw_frame_8, text="raw data: ", font="Helvetica 8")
        self.raw_label_8.pack(side="left")
        self.two_five_raw_entry = tk.Entry(self.raw_frame_8, textvariable=self.two_five_raw)
        self.two_five_raw_entry.pack()

        self.one_two_voltage_label = tk.Label(self.log_frame, text="+1.2V Voltage", font="Helvetica 10 bold")
        self.one_two_voltage_label.pack()
        self.calc_frame_9 = tk.Frame(self.log_frame)
        self.calc_frame_9.pack()
        self.calc_label_9 = tk.Label(self.calc_frame_9, text="value (V): ", font="Helvetica 8")
        self.calc_label_9.pack(side="left")
        self.one_two_voltage_entry = tk.Entry(self.calc_frame_9, textvariable=self.one_two_voltage)
        self.one_two_voltage_entry.pack()
        self.raw_frame_9 = tk.Frame(self.log_frame)
        self.raw_frame_9.pack()
        self.raw_label_9 = tk.Label(self.raw_frame_9, text="raw data: ", font="Helvetica 8")
        self.raw_label_9.pack(side="left")
        self.one_two_raw_entry = tk.Entry(self.raw_frame_9, textvariable=self.one_two_raw)
        self.one_two_raw_entry.pack()

        self.sensor_kickoff_button = tk.Button(self.log_frame, width=10, height=1, bg="steel blue", fg="white", text="Sensor Kickoff", command=self.sensor_kickoff)
        self.sensor_kickoff_button.pack()


    # sets up level two GUI
    def leveltwoGui(self, Ref):
        # kill level one buttons
        self.name_label.pack_forget()
        self.ref_label.pack_forget()
        self.tenmhz_button.pack_forget()
        self.hundredmhz_button.pack_forget()
        self.quit_label.pack_forget()
        self.quit_button.pack_forget()
        self.PLL_frame.pack_forget()
        self.spacer10.pack_forget()
        self.slave_set_button.pack_forget()
        self.dropdown.pack_forget()

        # Create buttons to decide what to do next
        self.name_label.config(text="Init'd @ 6500 MHz, " + Ref + "MHz Ref\n")
        self.name_label.pack()
        self.cal_label.pack()
        self.fullcal_button.pack()
        #self.loadcal_button.pack()
        self.autocal_label.pack()
        self.autocal_entry.pack()
        self.autocal_button.pack()
        self.debug_label.pack()
        self.printreg_button.pack()
        self.printcal_button.pack()
        #self.test_button.pack()
        self.quit_label.pack()
        self.quit_button.pack()
        self.goBack_label.pack()
        self.goBack_button.pack()
        #dropwdown PLL select
        self.spacer10.pack()
        self.PLL_frame.pack()
        self.dropdown.pack(side="left")
        self.slave_set_button.pack()  # dropdown menu shows options, slave select sets the ss to the selected value



    # sets up level three GUI
    def levelthreeGui(self, cal):
        # kill level two buttons
        self.name_label.pack_forget()
        self.cal_label.pack_forget()
        self.fullcal_button.pack_forget()
        #self.loadcal_button.pack_forget()
        self.autocal_label.pack_forget()
        self.autocal_entry.pack_forget()
        self.autocal_button.pack_forget()
        self.debug_label.pack_forget()
        self.printreg_button.pack_forget()
        self.printcal_button.pack_forget()
        #self.test_button.pack_forget()
        self.quit_label.pack_forget()
        self.quit_button.pack_forget()
        self.goBack_label.pack_forget()
        self.goBack_button.pack_forget()
        self.PLL_frame.pack_forget()
        self.spacer10.pack_forget()
        self.slave_set_button.pack_forget()
        self.dropdown.pack_forget()

        # pack level three Gui
        self.name_label.config(text=cal+"\n")
        self.name_label.pack()

        self.cal_label.pack()
        self.fullcal_button3.pack()

        self.autocal_label.pack()
        self.autocal_entry.pack()
        self.autocal_button.pack()

        self.freq_label.pack()
        self.freq_entry.pack()
        self.jump_button.pack()

        # self.sheet_label.pack()
        # self.freq1_entry.pack()
        # self.freq1_label.pack()
        # self.freq2_entry.pack()
        # self.freq2_label.pack()
        # self.delay_entry.pack()
        # self.delay_label.pack()
        # self.sheet_button.pack()
        # self.sheetPerFreq_button.pack()

        self.debug_label.pack()
        self.printreg_button.pack()
        self.printcal_button.pack()
        self.caltable_spreadsheet_button.pack()

        # lookup table debug
        self.lookuptable_label.pack()
        self.lookuptable_reg_entry.pack()
        self.reg_label.pack()
        self.lookuptable_value_entry.pack()
        self.value_label.pack()
        self.lfreq_entry.pack()
        self.lfreq_label.pack()
        self.lookuptable_button.pack()

        #quit
        self.quit_label.pack()
        self.quit_button.pack()

        #go back to main menu
        self.goBack_label.pack()
        self.goBack_button.pack()

        # dropdown slave select
        self.spacer10.pack()
        self.PLL_frame.pack()
        self.dropdown.pack(side="left")
        self.slave_set_button.pack()

    def slave_set(self):
        self.ss = self.pll_ss_dict[self.var.get()]  # assign value from dropdown menu to a seperate ss variable
        print("slave", self.ss - 64, "selected")  # subtracting 64 is a patchup

    def LO2_reg_test(self):
        # new func: test all slave select lines of the test board
        number = self.PLLFunc.PLLReg.slave_select_dict[self.test_var.get()]
        self.PLLFunc.PLLReg.slave_select_write(number)
        self.PLLFunc.PLLReg.sixteen_spi_write(0xFFF0)
        # before: tested all registers of LO2
        # passes = 0
        # fails = 0
        # num_tests=50000
        # for i in range(0,num_tests):
        #     address = randint(1, 42) # random address within bounds of DNC's memory map
        #     wr_data = randint(0, 255) # generate random 8 bit number
        #     concat = ((address << 8) | wr_data)
        #     self.PLLFunc.PLLReg.sixteen_spi_write(concat) # write data to random register
        #     read = self.PLLFunc.PLLReg.sixteen_spi_read(address)[0] # read data from the register
        #     if (wr_data == read):  # compare the read and written values
        #         passes += 1  # test passes if the values are equal
        #     else:
        #         fails += 1  # fails if values unequal and prints what address it failed at
        #         print("RANDOM REG WRITE TEST FAILED @ ADDRESS:", bin(address), "WRITE DATA:", bin(wr_data), "READ DATA:", bin(read))
        # print("RANDOM REG WRITE TEST FAILS:", fails, "/", num_tests, "TESTS") # print the total passes/fails over test
        # print("RANDOM REG WRITE TEST PASSES:", passes, "/", num_tests, "TESTS")

    # LO2 send functions
    def soft_reset_data(self):
        # retrieves and returns data from soft reset checkbutton
        concat = self.s0.get()
        return concat

    # slave select testing one
    def soft_reset_send(self):
        # sends the retrieved data to the designated address using spi write function
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"]) # choose slave to send to
        address = 0x00
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        concat = self.soft_reset_data()  #retrieve data from data function
        mosi_data = address | concat  # concatenate address and data into proper format
        #print(bin(mosi_data))
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)

    def ldo_en_data(self):
        # retrieves data from ldo check buttons and converts them into one number from several IntVars
        by = [0, 0, 0, 0, 0]
        bx = [self.l4.get(), self.l3.get(), self.l2.get(), self.L1.get(),
              self.l0.get()]  # store value of each button in a list
        for x in range(0, 4):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (4 - x))
        by[4] = self.l0.get()  # the last element of the array didn't need to be bit shifted so its manually assigned
        concat = by[0] | by[1] | by[2] | by[3] | by[4]  # bitwise 'or' the numbers in the array into one number
        return concat

    def ldo_en_send(self):
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to send to
        flag = 0
        switch_check = self.sw_read()
        dsa_check = self.dsa_read()
        if switch_check != '10000000' or dsa_check != '1000000':
            tk.messagebox.showerror("Error", "Make sure to turn off all SW and DSA switches before powering down!")
        else:
            print("test")
            address = 0x01
            address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
            concat = self.ldo_en_data()
            mosi_data = address | concat  # concatenate address and data into proper format
            self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def dnc_con_data(self):
        # retrieves data from dnc check buttons and converts into a single binary number
        by = [0, 0]
        bx = [self.d1.get(), self.d0.get()]  # store value of each button in a list
        for x in range(0, 1):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (1 - x))
        by[1] = self.d0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1]
        return concat

    def dnc_con_send(self):
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to send to
        address = 0x02
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        concat = self.dnc_con_data()
        mosi_data = address | concat # concatenate address and data into proper format
        print(bin(mosi_data))
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def test_pts_data(self):
        # retrieves data from test point check buttons and converts into a single binary number
        by = [0, 0]
        bx = [self.t1.get(), self.t0.get()]  # store value of each button in a list
        for x in range(0, 1):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (1 - x))
        by[1] = self.t0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1]
        # bitwise 'or' the numbers in the array into one number
        return concat

    def test_pts_send(self):
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to send to
        address = 0x03
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        concat = self.test_pts_data()
        mosi_data = address | concat # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def chip_en_data(self):
        # retrieves data from chip enable check buttons and converts into a single binary number
        by = [0, 0, 0, 0]
        bx = [self.c3.get(), self.c2.get(), self.c1.get(), self.c0.get()]  # store value of each button in a list
        for x in range(0, 3):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (3 - x))
        by[3] = self.c0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3]
        # bitwise 'or' the numbers in the array into one number
        return concat

    def chip_en_send(self):
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["DNC 4"])  # choose slave to send to
        address = 0x04
        address = address << 8   # bitshift to fit the format 1/7/8 rw/address/data
        concat = self.chip_en_data()
        mosi_data = address | concat # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def dsa_data(self):
        # retrieves data from dsa check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0, 0]
        bx = [self.ds5.get(), self.ds4.get(), self.ds3.get(), self.ds2.get(), self.ds1.get(),
              self.ds0.get()]  # store value of each button in a list
        for x in range(0, 5):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (5 - x))
        by[5] = self.ds0.get()  # the last element of the array didn't need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5]
        # bitwise 'or' the numbers in the array into one number
        return concat

    def dsa_send(self):
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to send to
        power_check = self.ldo_en_read()
        if power_check[1] == '0' or power_check[5] == '0':
            tk.messagebox.showerror("Error", "You may not send until power (both +3.3V A&B) is on!")
        else:
            address = 0x06
            address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
            concat = self.dsa_data()
            mosi_data = address | concat  # concatenate address and data into proper format
            self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def sw_data(self):
        # retrieves data from switch check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0, 0, 0]
        bx = [self.sw6.get(), self.sw5.get(), self.sw4.get(), self.sw3.get(), self.sw2.get(), self.sw1.get(),
              self.sw0.get()]  # store value of each button in a list
        for x in range(0, 6):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (6 - x))
        by[6] = self.sw0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5] | by[6]
        # bitwise 'or' the numbers in the array into one number
        return concat

    def sw_send(self):
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to send to
        power_check = self.ldo_en_read()
        if power_check[1] == '0' or power_check[5] == '0':
            tk.messagebox.showerror("Error", "You may not send until power (both +3.3V A&B) is on!")
        else:
            #print("test")
            address = 0x07
            address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
            concat = self.sw_data()
            mosi_data = address | concat  # concatenate address and data into proper format
            self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    # LO1 send funcs
    def LO1_soft_reset_send(self):
        # sends the retrieved data to the designated address using spi write function
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x00
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        concat = self.LO1_s0.get()  # retrieve data from data function
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)

    def LO1_dnc_con_send(self):
        # retrieves data from test point check buttons and converts into a single binary number
        by = [0, 0]
        bx = [self.LO1_d1.get(), self.LO1_d0.get()]  # store value of each button in a list
        for x in range(0, 1):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (1 - x))
        by[1] = self.LO1_d0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1]  # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x01
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def LO1_test_pts_send(self):
        # retrieves data from test point check buttons and converts into a single binary number
        by = [0, 0]
        bx = [self.LO1_t1.get(), self.LO1_t0.get()]  # store value of each button in a list
        for x in range(0, 1):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (1 - x))
        by[1] = self.LO1_t0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1]  # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x02
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def LO1_chip_en_send(self):
        # retrieves data from chip enable check buttons and converts into a single binary number
        by = [0, 0]
        bx = [self.LO1_c1.get(), self.LO1_c0.get()]  # store value of each button in a list
        for x in range(0, 1):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (1 - x))
        by[1] = self.LO1_c0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1]
        # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # choose slave to send to
        address = 0x03
        address = address << 8   # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def LO1_att_send(self):
        by = [0, 0, 0, 0, 0, 0]
        bx = [self.LO1_att5.get(), self.LO1_att4.get(), self.LO1_att3.get(), self.LO1_att2.get(), self.LO1_att1.get(), self.LO1_att0.get()]
        for x in range(0,5): # assign get values to a new array while also bitshifting them
            by[x] = (bx[x] << (5 - x))
        by[5] = self.LO1_att0.get()
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5]
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"]) # select correct slave
        address = 0x05
        address = address << 8 # bitshift address
        mosi_data = address | concat # create mosi data w address and data to send
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data) # send on spi bus

    def LO1_dsa_send(self):
        # retrieves data from dsa check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0, 0]
        bx = [self.LO1_ds5.get(), self.LO1_ds4.get(), self.LO1_ds3.get(), self.LO1_ds2.get(), self.LO1_ds1.get(),
              self.LO1_ds0.get()]  # store value of each button in a list
        for x in range(0, 5):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (5 - x))
        by[5] = self.LO1_ds0.get()  # the last element of the array didn't need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5]  # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x06
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def LO1_dsat_send(self):
        # retrieves data from dsa check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0, 0]
        bx = [self.LO1_dst5.get(), self.LO1_dst4.get(), self.LO1_dst3.get(), self.LO1_dst2.get(), self.LO1_dst1.get(),
              self.LO1_dst0.get()]  # store value of each button in a list
        for x in range(0, 5):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (5 - x))
        by[5] = self.LO1_ds0.get()  # the last element of the array didn't need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5] # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x07
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def LO1_sw_send(self):
        # retrieves data from switch check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0, 0]
        bx = [self.LO1_sw5.get(), self.LO1_sw4.get(), self.LO1_sw3.get(), self.LO1_sw2.get(), self.LO1_sw1.get(),
              self.LO1_sw0.get()]  # store value of each button in a list
        for x in range(0, 5):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (5 - x))
        by[5] = self.LO1_sw0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5]
        # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x08
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def LO1_sw_send_2(self):
        # retrieves data from switch check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0, 0, 0]
        bx = [self.LO1_sw6_2.get(),  self.LO1_sw5_2.get(), self.LO1_sw4_2.get(), self.LO1_sw3_2.get(), self.LO1_sw2_2.get(), self.LO1_sw1_2.get(),
              self.LO1_sw0_2.get()]  # store value of each button in a list
        for x in range(0, 6):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (6 - x))
        by[6] = self.LO1_sw0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5] | by[6]
        # bitwise 'or' the numbers in the array into one number
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x09
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def LO1_sw_send_3(self):
        # retrieves data from switch check buttons and converts into a single binary number
        by = [0, 0, 0]
        bx = [self.LO1_sw2_3.get(), self.LO1_sw1_3.get(), self.LO1_sw0_3.get()]  # store value of each button in a list
        for x in range(0, 2):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (2 - x))
        by[2] = self.LO1_sw0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2]
        # bitwise 'or' the numbers in the array into one number
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x0A
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def LO1_lpf_send(self):
        # retrieves data from low pass filter checkbuttons and converts to an integer
        by = [0, 0, 0, 0, 0]
        bx = [self.LO1_lpf4.get(), self.LO1_lpf3.get(), self.LO1_lpf2.get(), self.LO1_lpf1.get(), self.LO1_lpf0.get()]  # store value of each button in a list
        for x in range(0, 4):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (4 - x))
        by[4] = self.LO1_lpf0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4]  # bitwise 'or' the numbers in the array into one number
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave to send to
        address = 0x0B
        address = address << 8
        mosi_data = address | concat
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)

    # DNC send functions


    # applies for all of the following read functions:
    # 1: reads data from spi bus and stores the array
    # 2: converts the binary form of the data from the array into a string
    # 3.0: string looks something like "0b100010101" so the values we are interested in are the last 8 bits,
    # 3.1: the actual data, not the address. depending on mapping, only a certain amount of the last 8 bits are needed.
    # 4.0: assigns the notable data (starting from end of string) to the variables associated with the read checkbuttons,
    # 4.1: which will become checked or unchecked based on if it is assigned a one or a zero. this allows the user to
    # 4.2: visualize the data and settings currently stored on the aardvark.

    # LO2 read functions
    def ldo_en_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x01)
        print("raw_read:", raw_read) # test
        read = 0b100000 | raw_read[0]
        string = str(bin(read))
        self.lr4.set(int(string[-5]))
        self.lr3.set(int(string[-4]))
        self.lr2.set(int(string[-3]))
        self.Lr1.set(int(string[-2]))
        self.lr0.set(int(string[-1]))
        return string[2:] # need to return to check power condition in another function

    def dnc_con_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x02)
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.dr1.set(int(string[-2]))
        self.dr0.set(int(string[-1]))

    def test_pts_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x03)
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.tr1.set(int(string[-2]))
        self.tr0.set(int(string[-1]))

    def chip_en_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x04)
        read = 0b10000 | raw_read[0]
        string = str(bin(read))
        self.cr3.set(int(string[-4]))
        self.cr2.set(int(string[-3]))
        self.cr1.set(int(string[-2]))
        self.cr0.set(int(string[-1]))

    def imp_det_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x05)
        read = 0b10 | raw_read[0]
        string = str(bin(read))
        self.ir0.set(int(string[-1]))
        # read data from address 0x05 because its a read only signal

    def dsa_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x06)
        read = 0b1000000 | raw_read[0]
        string = str(bin(read))
        self.dsr5.set(int(string[-6]))
        self.dsr4.set(int(string[-5]))
        self.dsr3.set(int(string[-4]))
        self.dsr2.set(int(string[-3]))
        self.dsr1.set(int(string[-2]))
        self.dsr0.set(int(string[-1]))
        return string[2:] # need to return to check power condition in another function

    def sw_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"]) # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x07)
        read = 0b10000000 | raw_read[0]
        string = str(bin(read))
        self.swr6.set(int(string[-7]))
        self.swr5.set(int(string[-6]))
        self.swr4.set(int(string[-5]))
        self.swr3.set(int(string[-4]))
        self.swr2.set(int(string[-3]))
        self.swr1.set(int(string[-2]))
        self.swr0.set(int(string[-1]))
        return string[2:] # need to return to check power condition in another function

    # LO1 read functions
    def LO1_dnc_con_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x01)
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.LO1_dr1.set(int(string[-2]))
        self.LO1_dr0.set(int(string[-1]))

    def LO1_test_pts_read(self):
        self.PLLFunc.PLLReg.slave_select_write(
            self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x02)
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.LO1_tr1.set(int(string[-2]))
        self.LO1_tr0.set(int(string[-1]))

    def LO1_chip_en_read(self):
        self.PLLFunc.PLLReg.slave_select_write(
            self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x03)
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.LO1_cr1.set(int(string[-2]))
        self.LO1_cr0.set(int(string[-1]))

    def LO1_imp_det_read(self):
        self.PLLFunc.PLLReg.slave_select_write(
            self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x04)
        read = 0b10 | raw_read[0]
        string = str(bin(read))
        self.LO1_ir0.set(int(string[-1]))
        # read data from address 0x04 because its a read only signal

    def LO1_att_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x05)
        read = 0b1000000 | raw_read[0]
        string = str(bin(read))
        self.LO1_attr5.set(int(string[-6]))
        self.LO1_attr4.set(int(string[-5]))
        self.LO1_attr3.set(int(string[-4]))
        self.LO1_attr2.set(int(string[-3]))
        self.LO1_attr1.set(int(string[-2]))
        self.LO1_attr0.set(int(string[-1]))

    def LO1_dsa_read(self):
        self.PLLFunc.PLLReg.slave_select_write(
            self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x06)
        read = 0b1000000 | raw_read[0]
        string = str(bin(read))
        self.LO1_dsr5.set(int(string[-6]))
        self.LO1_dsr4.set(int(string[-5]))
        self.LO1_dsr3.set(int(string[-4]))
        self.LO1_dsr2.set(int(string[-3]))
        self.LO1_dsr1.set(int(string[-2]))
        self.LO1_dsr0.set(int(string[-1]))

    def LO1_dsat_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x07)
        read = 0b01000000 | raw_read[0]
        string = str(bin(read))
        self.LO1_dstr5.set(int(string[-6]))
        self.LO1_dstr4.set(int(string[-5]))
        self.LO1_dstr3.set(int(string[-4]))
        self.LO1_dstr2.set(int(string[-3]))
        self.LO1_dstr1.set(int(string[-2]))
        self.LO1_dstr0.set(int(string[-1]))

    def LO1_sw_read(self):
        self.PLLFunc.PLLReg.slave_select_write(
            self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x08)
        read = 0b100000000 | raw_read[0]
        string = str(bin(read))
        self.LO1_swr5.set(int(string[-6]))
        self.LO1_swr4.set(int(string[-5]))
        self.LO1_swr3.set(int(string[-4]))
        self.LO1_swr2.set(int(string[-3]))
        self.LO1_swr1.set(int(string[-2]))
        self.LO1_swr0.set(int(string[-1]))

    def LO1_sw_read_2(self):
        self.PLLFunc.PLLReg.slave_select_write(
            self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x09)
        read = 0b10000000 | raw_read[0]
        string = str(bin(read))
        self.LO1_swr6_2.set(int(string[-7]))
        self.LO1_swr5_2.set(int(string[-6]))
        self.LO1_swr4_2.set(int(string[-5]))
        self.LO1_swr3_2.set(int(string[-4]))
        self.LO1_swr2_2.set(int(string[-3]))
        self.LO1_swr1_2.set(int(string[-2]))
        self.LO1_swr0_2.set(int(string[-1]))

    def LO1_sw_read_3(self):
        self.PLLFunc.PLLReg.slave_select_write(
            self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x0A)
        read = 0b1000 | raw_read[0]
        string = str(bin(read))
        self.LO1_swr2_3.set(int(string[-3]))
        self.LO1_swr1_3.set(int(string[-2]))
        self.LO1_swr0_3.set(int(string[-1]))

    def LO1_lpf_read(self):
        self.PLLFunc.PLLReg.slave_select_write(
            self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # replace with correct slave number
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x0B)
        read = 0b100000 | raw_read[0]
        string = str(bin(read))
        self.LO1_lpfr4.set(int(string[-5]))
        self.LO1_lpfr3.set(int(string[-4]))
        self.LO1_lpfr2.set(int(string[-3]))
        self.LO1_lpfr1.set(int(string[-2]))
        self.LO1_lpfr0.set(int(string[-1]))

    # DNC read functions


    # LO2 periph functions
    def adc_kickoff(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"]) # choose reg map slave
        self.PLLFunc.PLLReg.sixteen_spi_write(0b0010101100000001) # send kickoff bit

        self.adc_msb = self.PLLFunc.PLLReg.sixteen_spi_read(0x2C)[0]
        self.adc_lsb = self.PLLFunc.PLLReg.sixteen_spi_read(0x2D)[0]
        self.adc_data = self.adc_msb << 8 | self.adc_lsb # read from adc registers
        self.adc_data_disp.set(bin(self.adc_data)) # display raw
        self.adc_calc.set(self.adc_data * .0005) # display calculated voltage

    def sensor_kickoff(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO2 Reg Map"])  # chose slave
        self.PLLFunc.PLLReg.sixteen_spi_write(0b0000100000000001)  # kickoff the sensor by writing a 1 to an address
        # read and store values from registers for parts 1/2
        # part une
        self.msb7_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0xD)[0]
        self.lsb7_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0xE)[0]
        self.v7_1 = (self.msb7_1 << 8) | self.lsb7_1

        self.msb6_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0xF)[0]
        self.lsb6_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0x10)[0]
        self.v6_1 = (self.msb6_1 << 8) | self.lsb6_1

        self.msb5_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0x11)[0]
        self.lsb5_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0x12)[0]
        self.v5_1 = (self.msb5_1 << 8) | self.lsb5_1

        self.msb4_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0x13)[0]
        self.lsb4_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0x14)[0]
        self.v4_1 = (self.msb4_1 << 8) | self.lsb4_1


        self.msb2_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0x17)[0]
        self.lsb2_1 = self.PLLFunc.PLLReg.sixteen_spi_read(0x18)[0]
        self.v2_1 = (self.msb2_1 << 8) | self.lsb2_1

        # part deux
        self.msb7_0 = self.PLLFunc.PLLReg.sixteen_spi_read(0x1D)[0]
        self.lsb7_0 = self.PLLFunc.PLLReg.sixteen_spi_read(0x1E)[0]
        self.v7_0 = (self.msb7_0 << 8) | self.lsb7_0

        self.msb6_0 = self.PLLFunc.PLLReg.sixteen_spi_read(0x1F)[0]
        self.lsb6_0 = self.PLLFunc.PLLReg.sixteen_spi_read(0x20)[0]
        self.v6_0 = (self.msb6_0 << 8) | self.lsb6_0


        self.msb4_0 = self.PLLFunc.PLLReg.sixteen_spi_read(0x23)[0]
        self.lsb4_0 = self.PLLFunc.PLLReg.sixteen_spi_read(0x24)[0]
        self.v4_0 = (self.msb4_0 << 8) | self.lsb4_0


        self.msb2_0 = self.PLLFunc.PLLReg.sixteen_spi_read(0x27)[0]
        self.lsb2_0 = self.PLLFunc.PLLReg.sixteen_spi_read(0x28)[0]
        self.v2_0 = (self.msb2_0 << 8) | self.lsb2_0


        # set entry fields to raw data values
        self.five_volt1_raw.set(bin(self.v2_0))
        self.four_volt1_raw.set(bin(self.v4_0))
        self.four_volt2_raw.set(bin(self.v6_0))
        self.temp_raw.set(bin(self.v7_0))
        self.four_volt3_raw.set(bin(self.v2_1))
        self.five_volt2_raw.set(bin(self.v4_1))
        self.three_three_raw.set(bin(self.v5_1))
        self.two_five_raw.set(bin(self.v6_1))
        self.one_two_raw.set(bin(self.v7_1))

        # make the krabby patty formula
        #currents: last 14 [13:0] bits
        #temp: last 13 [12:0] bits
        #voltage: last 14 [13:0]
        calcstr1 = str(bin(0b10000000000000000 | self.v2_0))
        calcstr2 = str(bin(0b10000000000000000 | self.v4_0))
        calcstr3 = str(bin(0b10000000000000000 | self.v6_0))
        calcstr4 = str(bin(0b10000000000000000 | self.v7_0))
        calcstr5 = str(bin(0b10000000000000000 | self.v2_1))
        calcstr6 = str(bin(0b10000000000000000 | self.v4_1))
        calcstr7 = str(bin(0b10000000000000000 | self.v5_1))
        calcstr8 = str(bin(0b10000000000000000 | self.v6_1))
        calcstr9 = str(bin(0b10000000000000000 | self.v7_1))
        Rsense = 0.22 # ohms
        Rsense1 = 0.05
        Rsense2 = 0.24
        calcint1 = int(calcstr1[-14:], 2)  # actual number excluding 0b and excluding the 2 leading because D[13:0]
        calcint2 = int(calcstr2[-14:], 2)
        calcint3 = int(calcstr3[-14:], 2)
        calcint4 = int(calcstr4[-13:], 2)
        calcint5 = int(calcstr5[-14:], 2)
        calcint6 = int(calcstr6[-14:], 2)
        calcint7 = int(calcstr7[-14:], 2)
        calcint8 = int(calcstr8[-14:], 2)
        calcint9 = int(calcstr9[-14:], 2)
        # for following: calculate and set the actual current/temp/voltage values and display on GUI
        if calcstr1[-15] == "0": #(first bit 0)
            self.five_volt1_current.set(calcint1 * (19.075/Rsense2)) # or v2_0
        elif calcstr1[-15] == "1": #(first bit 1)
            self.five_volt1_current.set((~calcint1 + 1) * (-19.075/Rsense2)) # or v2_0

        if calcstr2[-15] == "0":
            self.four_volt1_current.set(calcint2 * (19.075 / Rsense)) # or v4_0
        elif calcstr2[-15] == "1":
            self.four_volt1_current.set((~calcint2 + 1) * (-19.075 / Rsense))

        if calcstr3[-15] == "0":
            self.four_volt2_current.set(calcint3 * (19.075 / Rsense)) # or v6_0
        elif calcstr3[-15] == "1":
            self.four_volt2_current.set((~calcint3 + 1) * (-19.075 / Rsense))

        self.temperature.set(calcint4 / 16) # set temperature display

        if calcstr5[-15] == "0":
            self.four_volt3_current.set(calcint5 * (19.075 / Rsense))  # or v2_1
        elif calcstr5[-15] == "1":
            self.four_volt3_current.set((~calcint5 + 1) * (-19.075 / Rsense))

        if calcstr6[-15] == "0":
            self.five_volt2_current.set(calcint6 * (19.075 / Rsense1))  # or v4_1
        elif calcstr6[-15] == "1":
            self.five_volt2_current.set((~calcint6 + 1) * (-19.075 / Rsense1))

        self.three_three_voltage.set(calcint7 * 305.18)
        self.two_five_voltage.set(calcint8 * 305.18)
        self.one_two_voltage.set(calcint9 * 305.18)

    # LO1 periph functions
    def LO1_bpf_dac_write(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        address_1 = 0xc # 1100
        address_2 = 0xd # 1101
        address_3 = 0xe # 1110
        voltage = float(self.LO1_bpf_dac_voltage.get()) # get voltage from user
        digital_voltage = int(409.6 * voltage) # apply formula to get digital version of desired voltage
        dac_num = (0b11 << 10) | digital_voltage # combine command (0011) with actual data for dac
        dac_word = '0000' + str(bin(dac_num))[2:] # cast to a string, add 4 zeros for unused bits and command bits
        mosi_data_1 = (address_1 << 8) | int(dac_word[:8], 2) # create spi word for mosi bus
        mosi_data_2 = (address_2 << 8) | int(dac_word[8:], 2)
        mosi_data_kickoff = (address_3 << 8) | 1
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_1) # write each word to the bus
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_2)
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_kickoff)
        print("", dac_word, "\n", bin(mosi_data_1), '\n', bin(mosi_data_2), '\n', bin(mosi_data_kickoff))

    def LO1_vxp_dac_a_write(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        address_config = 0x0f
        config_dat = 0b00100001
        config = (address_config << 8) | config_dat
        self.PLLFunc.PLLReg.sixteen_spi_write(config) # configure dac
        address_1 = 0x10
        address_2 = 0x11
        address_kickoff = 0x12
        voltage = float(self.LO1_vxp_dac_voltage.get()) # get voltage from user
        digital_voltage = int(819.2 * voltage) # convert to 12 bit data value
        dac_word = str(bin(0b1000000000000 | digital_voltage))  # str to make it indexable
        mosi_data_1 = (address_1 << 8) | int(dac_word[3:7], 2) # format for registers on max10
        mosi_data_2 = (address_2 << 8) | int(dac_word[7:], 2)
        mosi_data_kickoff = (address_kickoff << 8) | 1 # create kickoff bit
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_1) # send data to registers then kickoff write
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_2)
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_kickoff)

    def LO1_vxp_dac_b_write(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        address_config = 0x13
        config_dat = 0b00101000
        config = (address_config << 8) | config_dat
        self.PLLFunc.PLLReg.sixteen_spi_write(config) # configure dac
        address_1 = 0x14
        address_2 = 0x15
        address_kickoff = 0x16
        voltage = float(self.LO1_vxp_dac_voltage.get()) # get voltage from user
        digital_voltage = int(819.2 * voltage) # convert to 12 bit data value
        dac_word = str(bin(0b1000000000000 | digital_voltage)) # str to make it indexable
        mosi_data_1 = (address_1 << 8) | int(dac_word[3:7], 2) # format data for registers on max10
        mosi_data_2 = (address_2 << 8) | int(dac_word[7:], 2)
        mosi_data_kickoff = (address_kickoff << 8) | 1 # create kickoff bit
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_1) # send data to registers then kickoff write
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_2)
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_kickoff)

    def LO1_temp_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        address_kickoff = 0x17
        kickoff = (address_kickoff << 8) | 1
        self.PLLFunc.PLLReg.sixteen_spi_write(kickoff) # send read kickoff
        address_1 = 0x19
        address_2 = 0x1A
        msb_data = str(bin(0b100000000 | self.PLLFunc.PLLReg.sixteen_spi_read(address_1)[0])) # read data from registers
        lsb_data = str(bin(0b100000000 | self.PLLFunc.PLLReg.sixteen_spi_read(address_2)[0]))
        data = msb_data + lsb_data[3:] # combine MSB register with LSB register
        if data[6] == '0': # if positive temp
            temp = float(int(data[7:], 2) / 16) # apply formula
            self.LO1_temp_string.set(str(temp)) # set display to temperature calculated
        elif data[6] == '1': # if negative temp
            temp = float((int(data[7:], 2) - 4096) / 16) # apply formula
            self.LO1_temp_string.set(str(temp)) # set display to temperature calculated

    def LO1_adc_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        address_kickoff = 0x1B
        address_1 = 0x1C
        address_2 = 0x1D
        kickoff = (address_kickoff << 8) | 1
        self.PLLFunc.PLLReg.sixteen_spi_write(kickoff) # kickoff read from adc
        adc_msb = self.PLLFunc.PLLReg.sixteen_spi_read(address_1)[0] # read msb and lsb registers
        adc_lsb = self.PLLFunc.PLLReg.sixteen_spi_read(address_2)[0]
        adc_data = (adc_msb << 8 | adc_lsb) / 4096 * 2.048 # apply formula
        self.LO1_adc_value.set(str(adc_data)) # set display to voltage calculated

    def LO1_reg_test(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        num_tests = 50000
        passes = 0
        fails = 0
        for i in range(0,num_tests):
            address = randint(0, 29) # random address within bounds of LO1's memory map
            wr_data = randint(0, 255) # generate random 8 bit number
            concat = ((address << 8) | wr_data)
            self.PLLFunc.PLLReg.sixteen_spi_write(concat) # write the data
            read = self.PLLFunc.PLLReg.sixteen_spi_read(address)[0] # read back the data
            if (wr_data == read): # compare data and increment appropriate counter
                passes += 1
            else:
                fails += 1
                # print where address fails if it does
                print("RANDOM REG WRITE TEST FAILED @ ADDRESS:", bin(address), "WRITE DATA:", bin(wr_data), "READ DATA:", bin(read))
        print("RANDOM REG WRITE TEST FAILS:", fails, "/", num_tests, "TESTS") # print total fails/passes
        print("RANDOM REG WRITE TEST PASSES:", passes, "/", num_tests, "TESTS")

    # DNC periph functions



    # PLL functions
    #  generate spreadsheet for hopping from freq A to B back to A
    def generate_ABA_spreadsheet(self):
        # get name of spreadsheet
        self.filename_ABA = filedialog.asksaveasfilename(initialdir="//Chlm2efs01/ITAR/HELIOS - 3U VPX 2-18 GHz Rx Tx/Engineering/GUI/LMX2594_PLL_GUI/Excel_Hopping_Files", title="Select file", filetypes=[("Excel Workbook", "*.xlsx")])
        if self.filename_ABA[-4:] != "xlsx":  # invalid filename
            print("ERROR: File must end with extension .xlsx")
        else:  # valid filename
            # get freq1 freq2 and delay
            self.freq1 = self.freq1_entry.get()  # get first frequency
            self.freq2 = self.freq2_entry.get()  # get second frequency
            self.delay = self.delay_entry.get()  # get delay between frequencies

            # validate inputs
            if int(self.freq1) in self.PLLFunc.freqrange and int(self.freq2) in self.PLLFunc.freqrange and int(self.delay) > 0:
                # valid filename AND valid freq1 freq2 and delay
                self.PLLFunc.make_spreadsheet(self.filename_ABA, int(self.freq1), int(self.freq2), int(self.delay))  # create spreadsheet

            else:  # invalid inputs
                print("Invalid Inputs Freq1: " + str(self.freq1) + "Freq2: " + str(self.freq2) + "Delay: " + self.delay)

        # delete freq1 freq2 and delay entries
        self.freq1_entry.delete(0, 'end')
        self.freq2_entry.delete(0, 'end')
        self.delay_entry.delete(0, 'end')

    # creates full calibration spreadsheet
    def generate_caltable_spreadsheet(self):
        # generate full calibration table spreadsheet
        self.filename_caltable = filedialog.asksaveasfilename(initialdir="//Chlm2efs01/ITAR/HELIOS - 3U VPX 2-18 GHz Rx Tx/Engineering/GUI/LMX2594_PLL_GUI/Cal_Table", title="Select file", filetypes=[("Excel Workbook", "*.xlsx")])

        if self.filename_caltable[-4:] != "xlsx":  # invalid filename
            print("ERROR: File must end with extension .xlsx")
        else:  # valid filename
            self.PLLFunc.generate_caltable_spreadsheet(self.filename_caltable)

    # creates full calibration spreadsheet
    def generate_bypassautocal_spreadsheet_per_freq(self):
        path = "//Chlm2efs01/ITAR/HELIOS - 3U VPX 2-18 GHz Rx Tx/Engineering/GUI/LMX2594_PLL_GUI/Excel_Hopping_Files_per_freq/"+str(date.today()) + "time "+str(time.time())
        os.makedirs(path)
        for p in self.PLLFunc.freqrange:
            self.filename_ABAperFreq = path +"/"+ "BypassAutocal@"+ str(p)+ "freq"+".xlsx"
            self.PLLFunc.make_spreadsheetPerFreq(self.filename_ABAperFreq,p)

    def test(self):
        # write guess for 6500 MHz Jump
        print("TEST DONE")

    # jump to arbitrary freq.
    def jumpfreq(self):
        self.PLLFunc.PLLReg.slave_select_write(self.ss)  # configure slave
        #aa_spi_configure(self.PLLFunc.PLLReg.handle, AA_SPI_POL_RISING_FALLING, AA_SPI_PHASE_SAMPLE_SETUP, AA_SPI_BITORDER_MSB)  # configure spi format that PLL expects
        self.bypass_freq = self.freq_entry.get()  # get input from user after button push
        if int(self.bypass_freq) in self.PLLFunc.freqrange:
            self.PLLFunc.bypassautocalenable()  # enable autocal bypass mode
            self.PLLFunc.bypassautocal(int(self.bypass_freq))  # hop to requested frequency (self.bypass_freq) bypassing autocal routine
            print("Autocal Bypass Jump to", self.bypass_freq, "MHz")  # alert user to what just happened
            if self.ss == 0b10000000:
                self.PLL1_string.set(self.bypass_freq)  # set "last value sent" to last value sent
            elif self.ss == 0b10000001:
                self.PLL2_string.set(self.bypass_freq)
            elif self.ss == 0b10000010:
                self.PLL3_string.set(self.bypass_freq)
            elif self.ss == 0b10000011:
                self.PLL4_string.set(self.bypass_freq)
        else:
            print("Invalid Frequency Input: ", self.bypass_freq)

        self.freq_entry.delete(0, 'end')  # clear entry field for next entry
        #aa_spi_configure(self.PLLFunc.PLLReg.handle, AA_SPI_POL_FALLING_RISING, AA_SPI_PHASE_SETUP_SAMPLE, AA_SPI_BITORDER_MSB)  # return spi format to default

    # Hops to arbitrary frequency using full autocal routine
    def autocal_freq_fun(self):
        self.PLLFunc.PLLReg.slave_select_write(self.ss)  # configure slave
        #aa_spi_configure(self.PLLFunc.PLLReg.handle, AA_SPI_POL_RISING_FALLING, AA_SPI_PHASE_SAMPLE_SETUP, AA_SPI_BITORDER_MSB)  # configure spi format that PLL expects
        self.autocal_freq = self.autocal_entry.get()  # get input from user after button push
        if int(self.autocal_freq) in self.PLLFunc.freqrange:
            self.PLLFunc.autocal_enable()  # enable autocal mode by writing to register 0
            self.PLLFunc.autocal_freq(int(self.autocal_freq))  # run autocal with freq
            # print("Autocal Freq. Jump to", self.autocal_freq, "MHz")  # print statement to alert user to what they did
            autocalHis.append(self.autocal_freq)
            print("This is the array that stores history")
            print(autocalHis)
            if self.ss == 0b10000000:
                self.PLL1_string.set(self.autocal_freq)  # set "last value sent" to last value sent
            elif self.ss == 0b10000001:
                self.PLL2_string.set(self.autocal_freq)
            elif self.ss == 0b10000010:
                self.PLL3_string.set(self.autocal_freq)
            elif self.ss == 0b10000011:
                self.PLL4_string.set(self.autocal_freq)
        else:
            print("Invalid Frequency Input: ", self.autocal_freq)

        self.autocal_entry.delete(0, 'end')  # clear entry field for next entry
        #aa_spi_configure(self.PLLFunc.PLLReg.handle, AA_SPI_POL_FALLING_RISING, AA_SPI_PHASE_SETUP_SAMPLE, AA_SPI_BITORDER_MSB)  # return spi format to default
    # initializes PLL to 6.5 GHz w/ 10 MHz Ref, Sets up level two GUI menu
    def pll_init_10(self):
        self.PLLFunc.pll_init(10)  # initialize PLL to 6.5 GHz w/ 10 Mhz ref
        self.leveltwoGui("10")  # creates second level gui with 10 MHz reference

    # initializes PLL to 6.5 GHz w/ 100 MHz Ref, Sets up level two GUI menu
    def pll_init_100(self):
        self.PLLFunc.pll_init(100)  # initialize PLL to 6.5 GHz w/ 100 Mhz ref
        self.leveltwoGui("100")  # creates second level gui with 100 MHz reference

    # wrapper function that reads back and prints contents of registers
    def printregisters(self):
        self.PLLFunc.print_registers()

    # fills full calibration table with R19 & R20 values, launched from GUI 2
    def fullcal(self):
        self.PLLFunc.PLLReg.slave_select_write(self.ss)
        self.levelthreeGui("Full Calibration Done")  # create third level GUI
        self.PLLFunc.autocal_enable()  # enable autocal mode by writing to register 0

        # run full autocal routine reading back R111 and replacing R19 D[7:0] in the lookup table
        for freq in self.PLLFunc.freqrange:
            self.PLLFunc.autocal_freq(freq)  # program PLL in autocal mode
            time.sleep(.001)  # wait 1 millisecond for PLL to lock
            self.PLLFunc.updateR19(freq)  # update R19 in lookup table
            self.PLLFunc.updateR20(freq)  # update R20 in lookup table

        print("Done Full Calibration")

    # fills full calibration table with R19 & R20 values launched from GUI level 3
    def fullcal3(self):
        self.fullcal()


    # loads calibration table from memory
    def loadcal(self):
        self.levelthreeGui("Load Cal. Not implemented")
        print("LOAD CAL NOT IMPLEMENTED YET")
        # load cal
        # create third level GUI

    # prints full call table
    def printcaltable(self):
        for j in self.PLLFunc.freqrange:
            print_line = "Freq=" + str(j) + " "
            for k in self.PLLFunc.lookuptable[j]:
                print_line = print_line + "R" + str(k) + "=" + str(hex(self.PLLFunc.lookuptable[j][k])) + " "  # jk LOL
            print(print_line)

    # allows user to edit specific entry in lookuptable at a specified frequency
    def changetable(self):
        self.lookuptable_reg = self.lookuptable_reg_entry.get()  # get input from user after button push
        self.lookuptable_value = self.lookuptable_value_entry.get()  # get input from user after button push
        self.lfreq = self.lfreq_entry.get()  # get input from user after button push


        self.lookuptable_reg_entry.delete(0, 'end')  # clear entry field for next entry
        self.lookuptable_value_entry.delete(0, 'end')  # clear entry field for next entry
        self.lfreq_entry.delete(0, 'end')  # clear entry field for next entry

        valid_reg = [46, 45, 44, 37, 36, 19, 14, 8, 0]

        # validate input
        if(int(self.lfreq) in self.PLLFunc.freqrange):
            if(int(self.lookuptable_reg) in valid_reg):
                if(int(self.lookuptable_value) > 0):
                    self.PLLFunc.changetable(int(self.lfreq), int(self.lookuptable_reg), int(self.lookuptable_value))  # edit lookuptable value
                    print("PLL Register: ", self.lookuptable_reg)
                    print("Register Value: ", self.lookuptable_value)
                    print("Frequency: ", self.lfreq, "MHz")

                else:
                    print("Invalid Register Value", self.lookuptable_reg)
            else:
                print("Invalid Register Address", self.lookuptable_value)
        else:
            print("Invalid Frequency", self.lfreq, "MHz")

    def goBack(self):
        #clears gui for main menu
        # kill level two buttons
        self.name_label.pack_forget()
        self.cal_label.pack_forget()
        self.fullcal_button.pack_forget()
        self.autocal_label.pack_forget()
        self.autocal_entry.pack_forget()
        self.autocal_button.pack_forget()
        self.debug_label.pack_forget()
        self.printreg_button.pack_forget()
        self.printcal_button.pack_forget()
        self.quit_label.pack_forget()
        self.quit_button.pack_forget()
        self.PLL_frame.pack_forget()
        self.spacer10.pack_forget()
        self.slave_set_button.pack_forget()
        self.dropdown.pack_forget()
        #kill level 3
        self.name_label.pack_forget()
        self.cal_label.pack_forget()
        self.fullcal_button3.pack_forget()
        self.autocal_label.pack_forget()
        self.autocal_entry.pack_forget()
        self.autocal_button.pack_forget()
        self.freq_label.pack_forget()
        self.freq_entry.pack_forget()
        self.jump_button.pack_forget()
        # self.sheet_label.pack_forget()
        # self.freq1_entry.pack_forget()
        # self.freq1_label.pack_forget()
        # self.freq2_entry.pack_forget()
        # self.freq2_label.pack_forget()
        # self.delay_entry.pack_forget()
        # self.delay_label.pack_forget()
        # self.sheet_button.pack_forget()
        # self.sheetPerFreq_button.pack_forget()
        self.debug_label.pack_forget()
        self.printreg_button.pack_forget()
        self.printcal_button.pack_forget()
        self.caltable_spreadsheet_button.pack_forget()
        self.lookuptable_label.pack_forget()
        self.lookuptable_reg_entry.pack_forget()
        self.reg_label.pack_forget()
        self.lookuptable_value_entry.pack_forget()
        self.value_label.pack_forget()
        self.lfreq_entry.pack_forget()
        self.lfreq_label.pack_forget()
        self.lookuptable_button.pack_forget()
        self.quit_label.pack_forget()
        self.quit_button.pack_forget()
        self.goBack_button.pack_forget()
        self.PLL_frame.pack_forget()
        self.spacer10.pack_forget()
        self.slave_set_button.pack_forget()
        self.dropdown.pack_forget()


        self.ref_label.pack()
        self.tenmhz_button.pack()
        self.hundredmhz_button.pack()
        self.quit_label.pack()
        self.quit_button.pack()
        self.goBack_label.pack_forget()
        self.goBack_button.pack_forget()


# MAIN
x = PLLGui()  # create an object of class PLLGui
x.merge.mainloop()  # this is a tkinter function that launches the GUI

# disconnect from aardvark
x.PLLFunc.disconnectaardvark()
