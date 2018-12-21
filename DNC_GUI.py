import PLLFunc
import tkinter as tk
from tkinter import filedialog
import time
import getpass
from datetime import date
from aardvark_py import *
import os, sys
from random import randint

class DNCGui:

    def __init__(self):
        self.PLLFunc = PLLFunc.PLLFunc() # create PLLFunc object to acccess functions like spi read etc
        self.PLLFunc.connect2aardvark()
        self.PLLFunc.PLLReg.slave_select_pca_config()

        self.dnc_gui = tk.Tk()
        self.dnc_gui.title("DNC 1 Reg Map")
        self.reg_frame = tk.Frame(self.dnc_gui) # frame containing register map
        self.middle_frame = tk.Frame(self.dnc_gui) # frame containing peripherals
        self.reg_frame.pack(side="left")
        self.middle_frame.pack(side="left")

        self.spacer1 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer2 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer3 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer4 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer5 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer6 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer7 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer8 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer9 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer10 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        self.spacer11 = tk.Canvas(self.reg_frame, bg="grey94", width=300, height=20)
        # spacers to prevent the GUI from getting cluttered, grey94 is the color of the window, looks like blank space

        self.reg_map_label = tk.Label(self.reg_frame, text="DNC Register Map", font="Helvetica 15 bold")
        self.reg_map_label.pack()

        # soft reset checkbutton setup
        self.soft_name_label = tk.Label(self.reg_frame, text="Return FPGA to known State", font="Helvetica 10 bold")
        self.soft_name_label.pack()
        self.s0 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.schecks = tk.Frame(self.reg_frame)  # frame to contain all check buttons in one line
        # checkbutton (this data is only one bit)
        self.spacer_c = tk.Canvas(self.schecks, width=101, height=0, bg="grey94")
        self.spacer_c.pack(side="left")
        self.sc0 = tk.Checkbutton(self.schecks, text="Soft Reset", font="Consolas 10", variable=self.s0)
        self.schecks.pack(fill="x")
        # send button (only a write, no read for this one)
        self.send_but_frame = tk.Frame(self.schecks)
        self.send_but_frame.pack(side="right")
        self.sc0.pack(fill="both")  # pack left so that the buttons stack horizontally, pad helps de-clutter
        self.soft_send_button = tk.Button(self.send_but_frame, text="Send Bits", bg="lime green", width=15, height=1, command=self.soft_reset_send)
        self.soft_send_button.pack()
        self.spacer1.pack()
        # end soft reset section


        # test checkbutton setup section
        self.test_name_label = tk.Label(self.reg_frame, text="Test Points", font="Helvetica 10 bold")
        self.test_name_label.pack()
        self.t0 = tk.IntVar()
        self.tr0 = tk.IntVar()
        self.tchecks = tk.Frame(self.reg_frame)  # frame to contain all check buttons in one line
        self.trchecks = tk.Frame(self.reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.tc0 = tk.Checkbutton(self.tchecks, text="TP1", font="Consolas 10", variable=self.t0)
        self.trc0 = tk.Checkbutton(self.trchecks, text="TP1", font="Consolas 10", variable=self.tr0)
        self.tchecks.pack(fill="x")
        self.trchecks.pack(fill="x")
        self.spacer_t = tk.Canvas(self.tchecks, width=358, height=0, bg="grey94")
        self.spacer_t.pack(side="left")
        self.tc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_tr = tk.Canvas(self.trchecks, width=358, height=0, bg="grey94")
        self.spacer_tr.pack(side="left")
        self.trc0.pack(side="left")
        # read and write buttons for this address
        self.test_send_button = tk.Button(self.tchecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.test_pts_send)
        self.test_send_button.pack(side="right")
        self.test_read_button = tk.Button(self.trchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.test_pts_read)
        self.test_read_button.pack(side="right")
        self.spacer4.pack()
        # end test


        # DSA checkbutton setup section
        self.DSA_name_label = tk.Label(self.reg_frame, text="IF Digital Step Attenuator Settings", font="Helvetica 10 bold")
        self.DSA_name_label.pack()
        self.ds4 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.ds3 = tk.IntVar()
        self.ds2 = tk.IntVar()
        self.ds1 = tk.IntVar()
        self.ds0 = tk.IntVar()
        self.dsr4 = tk.IntVar()
        self.dsr3 = tk.IntVar()
        self.dsr2 = tk.IntVar()
        self.dsr1 = tk.IntVar()
        self.dsr0 = tk.IntVar()
        self.dschecks = tk.Frame(self.reg_frame)  # frame to contain all check buttons in one line
        self.dsrchecks = tk.Frame(self.reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.dsc4 = tk.Checkbutton(self.dschecks, text="D4 ATT", font="Consolas 10", variable=self.ds4)
        self.dsc3 = tk.Checkbutton(self.dschecks, text="D3 ATT", font="Consolas 10", variable=self.ds3)
        self.dsc2 = tk.Checkbutton(self.dschecks, text="D2 ATT", font="Consolas 10", variable=self.ds2)
        self.dsc1 = tk.Checkbutton(self.dschecks, text="D1 ATT", font="Consolas 10", variable=self.ds1)
        self.dsc0 = tk.Checkbutton(self.dschecks, text="D0 ATT", font="Consolas 10", variable=self.ds0)
        self.dsrc4 = tk.Checkbutton(self.dsrchecks, text="D4 ATT", font="Consolas 10", variable=self.dsr4)
        self.dsrc3 = tk.Checkbutton(self.dsrchecks, text="D3 ATT", font="Consolas 10", variable=self.dsr3)
        self.dsrc2 = tk.Checkbutton(self.dsrchecks, text="D2 ATT", font="Consolas 10", variable=self.dsr2)
        self.dsrc1 = tk.Checkbutton(self.dsrchecks, text="D1 ATT", font="Consolas 10", variable=self.dsr1)
        self.dsrc0 = tk.Checkbutton(self.dsrchecks, text="D0 ATT", font="Consolas 10", variable=self.dsr0)
        self.dschecks.pack(fill="x")
        self.dsrchecks.pack(fill="x")
        self.spacer_ds = tk.Canvas(self.dschecks, width=206, height=0, bg="grey94")
        self.spacer_ds.pack(side="left")
        self.dsc4.pack(side="left")
        self.dsc3.pack(side="left")
        self.dsc2.pack(side="left")
        self.dsc1.pack(side="left")
        self.dsc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_dsr = tk.Canvas(self.dsrchecks, width=206, height=0, bg="grey94")
        self.spacer_dsr.pack(side="left")
        self.dsrc4.pack(side="left")
        self.dsrc3.pack(side="left")
        self.dsrc2.pack(side="left")
        self.dsrc1.pack(side="left")
        self.dsrc0.pack(side="left")
        # read and write buttons
        self.dsa_send_button = tk.Button(self.dschecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.dsa_send)
        self.dsa_send_button.pack(side="right")
        self.dsa_read_button = tk.Button(self.dsrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.dsa_read)
        self.dsa_read_button.pack(side="right")
        self.spacer7.pack()
        # end DSA


        # ldo checkbutton setup section
        self.ldo_name_label = tk.Label(self.reg_frame, text="Enable Signal to LDOs", font="Helvetica 10 bold")
        self.ldo_name_label.pack()
        self.L1 = tk.IntVar()
        self.l0 = tk.IntVar()
        self.Lr1 = tk.IntVar()
        self.lr0 = tk.IntVar()
        self.lchecks = tk.Frame(self.reg_frame)  # frame to contain all check buttons in one line
        self.lrchecks = tk.Frame(self.reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.Lc1 = tk.Checkbutton(self.lchecks, text="5V LDO B", font="Consolas 10", variable=self.L1)
        self.lc0 = tk.Checkbutton(self.lchecks, text="5V LDO A", font="Consolas 10", variable=self.l0)
        self.Lrc1 = tk.Checkbutton(self.lrchecks, text="5V LDO B", font="Consolas 10", variable=self.Lr1)
        self.lrc0 = tk.Checkbutton(self.lrchecks, text="5V LDO A", font="Consolas 10", variable=self.lr0)
        self.lchecks.pack(fill="x")
        self.lrchecks.pack(fill="x")
        self.spacer_L = tk.Canvas(self.lchecks, width=299, height=0, bg="grey94")
        self.spacer_L.pack(side="left")
        self.Lc1.pack(side="left")
        self.lc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_Lr = tk.Canvas(self.lrchecks, width=299, height=0, bg="grey94")
        self.spacer_Lr.pack(side="left")
        self.Lrc1.pack(side="left")
        self.lrc0.pack(side="left")
        # read and write buttons for this address
        self.ldo_en_send_button = tk.Button(self.lchecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.ldo_en_send)
        self.ldo_en_send_button.pack(side="right")
        self.ldo_en_read_button = tk.Button(self.lrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.ldo_en_read)
        self.ldo_en_read_button.pack(side="right")
        self.spacer2.pack()
        # end ldo


        # sw section
        self.sw_name_label = tk.Label(self.reg_frame, text="Switch 1 Settings", font="Helvetica 10 bold")
        self.sw_name_label.pack()
        self.sw7 = tk.IntVar()
        self.sw6 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.sw5 = tk.IntVar()
        self.sw4 = tk.IntVar()
        self.sw3 = tk.IntVar()
        self.sw2 = tk.IntVar()
        self.sw1 = tk.IntVar()
        self.sw0 = tk.IntVar()
        self.swr7 = tk.IntVar()
        self.swr6 = tk.IntVar()
        self.swr5 = tk.IntVar()
        self.swr4 = tk.IntVar()
        self.swr3 = tk.IntVar()
        self.swr2 = tk.IntVar()
        self.swr1 = tk.IntVar()
        self.swr0 = tk.IntVar()
        self.swchecks = tk.Frame(self.reg_frame)  # frame to contain all check buttons in one line
        self.swrchecks = tk.Frame(self.reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed
        # write button sends checked boxes as binary number to bus
        self.swc7 = tk.Checkbutton(self.swchecks, text="RF COMB", font="Consolas 10", variable=self.sw7)
        self.swc6 = tk.Checkbutton(self.swchecks, text="PRE 2_1", font="Consolas 10", variable=self.sw6)
        self.swc5 = tk.Checkbutton(self.swchecks, text="PRE 2_0", font="Consolas 10", variable=self.sw5)
        self.swc4 = tk.Checkbutton(self.swchecks, text="PRE 1", font="Consolas 10", variable=self.sw4)
        self.swc3 = tk.Checkbutton(self.swchecks, text="RF IN 2_1", font="Consolas 10", variable=self.sw3)
        self.swc2 = tk.Checkbutton(self.swchecks, text="RF IN 2_0", font="Consolas 10", variable=self.sw2)
        self.swc1 = tk.Checkbutton(self.swchecks, text="RF IN 1_1", font="Consolas 10", variable=self.sw1)
        self.swc0 = tk.Checkbutton(self.swchecks, text="RF IN 1_0", font="Consolas 10", variable=self.sw0)
        self.swrc7 = tk.Checkbutton(self.swrchecks, text="RF COMB", font="Consolas 10", variable=self.swr7)
        self.swrc6 = tk.Checkbutton(self.swrchecks, text="PRE 2_1", font="Consolas 10", variable=self.swr6)
        self.swrc5 = tk.Checkbutton(self.swrchecks, text="PRE 2_0", font="Consolas 10", variable=self.swr5)
        self.swrc4 = tk.Checkbutton(self.swrchecks, text="PRE 1", font="Consolas 10", variable=self.swr4)
        self.swrc3 = tk.Checkbutton(self.swrchecks, text="RF IN 2_1", font="Consolas 10", variable=self.swr3)
        self.swrc2 = tk.Checkbutton(self.swrchecks, text="RF IN 2_0", font="Consolas 10", variable=self.swr2)
        self.swrc1 = tk.Checkbutton(self.swrchecks, text="RF IN 1_1", font="Consolas 10", variable=self.swr1)
        self.swrc0 = tk.Checkbutton(self.swrchecks, text="RF IN 1_0", font="Consolas 10", variable=self.swr0)
        self.swchecks.pack(fill="x")
        self.swrchecks.pack(fill="x")
        #self.spacer_sw = tk.Canvas(self.swchecks, height=0, width=115, bg="grey94")
        #self.spacer_sw.pack(side="left")
        self.swc7.pack(side="left")
        self.swc6.pack(side="left")
        self.swc5.pack(side="left")
        self.swc4.pack(side="left")
        self.swc3.pack(side="left")
        self.swc2.pack(side="left")
        self.swc1.pack(side="left")
        self.swc0.pack(side="left")  # pack left so that the buttons stack horizontally
        #self.spacer_swr = tk.Canvas(self.swrchecks, height=0, width=115, bg="grey94")
        #self.spacer_swr.pack(side="left")
        self.swrc7.pack(side="left")
        self.swrc6.pack(side="left")
        self.swrc5.pack(side="left")
        self.swrc4.pack(side="left")
        self.swrc3.pack(side="left")
        self.swrc2.pack(side="left")
        self.swrc1.pack(side="left")
        self.swrc0.pack(side="left")
        # read and write buttons
        self.sw_send_button = tk.Button(self.swchecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.sw_send)
        self.sw_send_button.pack(side="right")
        self.sw_read_button = tk.Button(self.swrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.sw_read)
        self.sw_read_button.pack(side="right")
        self.spacer8.pack()
        # end sw


        # start sw_2
        # sw section
        self.sw_name_label_2 = tk.Label(self.reg_frame, text="Switch 2 Settings", font="Helvetica 10 bold")
        self.sw_name_label_2.pack()
        self.sw3_2 = tk.IntVar()
        self.sw2_2 = tk.IntVar()
        self.sw1_2 = tk.IntVar()
        self.sw0_2 = tk.IntVar()
        self.swr3_2 = tk.IntVar()
        self.swr2_2 = tk.IntVar()
        self.swr1_2 = tk.IntVar()
        self.swr0_2 = tk.IntVar()
        self.swchecks_2 = tk.Frame(self.reg_frame)  # frame to contain all check buttons in one line
        self.swrchecks_2 = tk.Frame(self.reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed (read checkbuttons have r)
        # write button sends checked boxes as binary number to bus
        self.swc3_2 = tk.Checkbutton(self.swchecks_2, text="IF BYP", font="Consolas 10", variable=self.sw3_2)
        self.swc2_2 = tk.Checkbutton(self.swchecks_2, text="LO MUTE", font="Consolas 10", variable=self.sw2_2)
        self.swc1_2 = tk.Checkbutton(self.swchecks_2, text="IF OUT SW1", font="Consolas 10", variable=self.sw1_2)
        self.swc0_2 = tk.Checkbutton(self.swchecks_2, text="IF OUT SW0", font="Consolas 10", variable=self.sw0_2)
        self.swrc3_2 = tk.Checkbutton(self.swrchecks_2, text="IF BYP", font="Consolas 10", variable=self.swr3_2)
        self.swrc2_2 = tk.Checkbutton(self.swrchecks_2, text="LO MUTE", font="Consolas 10", variable=self.swr2_2)
        self.swrc1_2 = tk.Checkbutton(self.swrchecks_2, text="IF OUT SW1", font="Consolas 10", variable=self.swr1_2)
        self.swrc0_2 = tk.Checkbutton(self.swrchecks_2, text="IF OUT SW0", font="Consolas 10", variable=self.swr0_2)
        self.swchecks_2.pack(fill="x")
        self.swrchecks_2.pack(fill="x")
        self.spacer_sw_2 = tk.Canvas(self.swchecks_2, bg="grey94", width=210, height=0)
        self.spacer_sw_2.pack(side="left")
        self.swc3_2.pack(side="left")
        self.swc2_2.pack(side="left")
        self.swc1_2.pack(side="left")
        self.swc0_2.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_swr_2 = tk.Canvas(self.swrchecks_2, bg="grey94", width=210, height=0)
        self.spacer_swr_2.pack(side="left")
        self.swrc3_2.pack(side="left")
        self.swrc2_2.pack(side="left")
        self.swrc1_2.pack(side="left")
        self.swrc0_2.pack(side="left")
        # read and write buttons
        self.sw_send_button_2 = tk.Button(self.swchecks_2, text="Send Bits", bg="lime green", width=15, height=1, command=self.sw_send_2)
        self.sw_send_button_2.pack(side="right")
        self.sw_read_button_2 = tk.Button(self.swrchecks_2, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.sw_read_2)
        self.sw_read_button_2.pack(side="right")
        self.spacer9.pack()
        # end sw_2


        # start LO2 DSA
        self.lo2_name_label = tk.Label(self.reg_frame, text="LO2 Digital Step Attenuator", font="Helvetica 10 bold")
        self.lo2_name_label.pack()
        self.lo2_5 = tk.IntVar()
        self.lo2_4 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.lo2_3 = tk.IntVar()
        self.lo2_2 = tk.IntVar()
        self.lo2_1 = tk.IntVar()
        self.lo2_0 = tk.IntVar()
        self.lo2r5 = tk.IntVar()
        self.lo2r4 = tk.IntVar()
        self.lo2r3 = tk.IntVar()
        self.lo2r2 = tk.IntVar()
        self.lo2r1 = tk.IntVar()
        self.lo2r0 = tk.IntVar()
        self.lo2checks = tk.Frame(self.reg_frame)  # frame to contain all check buttons in one line
        self.lo2rchecks = tk.Frame(self.reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed (read checkbuttons have r)
        # write button sends checked boxes as binary number to bus
        self.lo2c5 = tk.Checkbutton(self.lo2checks, text="SW 6", font="Consolas 10", variable=self.lo2_5)
        self.lo2c4 = tk.Checkbutton(self.lo2checks, text="SW 5", font="Consolas 10", variable=self.lo2_4)
        self.lo2c3 = tk.Checkbutton(self.lo2checks, text="SW 4", font="Consolas 10", variable=self.lo2_3)
        self.lo2c2 = tk.Checkbutton(self.lo2checks, text="SW 3", font="Consolas 10", variable=self.lo2_2)
        self.lo2c1 = tk.Checkbutton(self.lo2checks, text="SW 2", font="Consolas 10", variable=self.lo2_1)
        self.lo2c0 = tk.Checkbutton(self.lo2checks, text="SW 1", font="Consolas 10", variable=self.lo2_0)
        self.lo2rc5 = tk.Checkbutton(self.lo2rchecks, text="SW 5", font="Consolas 10", variable=self.lo2r5)
        self.lo2rc4 = tk.Checkbutton(self.lo2rchecks, text="SW 5", font="Consolas 10", variable=self.lo2r4)
        self.lo2rc3 = tk.Checkbutton(self.lo2rchecks, text="SW 4", font="Consolas 10", variable=self.lo2r3)
        self.lo2rc2 = tk.Checkbutton(self.lo2rchecks, text="SW 3", font="Consolas 10", variable=self.lo2r2)
        self.lo2rc1 = tk.Checkbutton(self.lo2rchecks, text="SW 2", font="Consolas 10", variable=self.lo2r1)
        self.lo2rc0 = tk.Checkbutton(self.lo2rchecks, text="SW 1", font="Consolas 10", variable=self.lo2r0)
        self.lo2checks.pack(fill="x")
        self.lo2rchecks.pack(fill="x")
        self.spacer_lo2 = tk.Canvas(self.lo2checks, bg="grey94", height=0, width=210)
        self.spacer_lo2.pack(side="left")
        self.lo2c5.pack(side="left")
        self.lo2c4.pack(side="left")
        self.lo2c3.pack(side="left")
        self.lo2c2.pack(side="left")
        self.lo2c1.pack(side="left")
        self.lo2c0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_lo2r = tk.Canvas(self.lo2rchecks, bg="grey94", height=0, width=210)
        self.spacer_lo2r.pack(side="left")
        self.lo2rc5.pack(side="left")
        self.lo2rc4.pack(side="left")
        self.lo2rc3.pack(side="left")
        self.lo2rc2.pack(side="left")
        self.lo2rc1.pack(side="left")
        self.lo2rc0.pack(side="left")
        # read and write buttons
        self.lo2_send_button = tk.Button(self.lo2checks, text="Send Bits", bg="lime green", width=15, height=1,
                                         command=self.lo2_send)
        self.lo2_send_button.pack(side="right")
        self.lo2_read_button = tk.Button(self.lo2rchecks, text="Read Bits", bg="black", fg="white", width=15, height=1,
                                         command=self.lo2_read)
        self.lo2_read_button.pack(side="right")
        # end LO2 DSA


        # start low pass filter
        self.lpf_name_label = tk.Label(self.reg_frame, text="Tunable Low Pass Filter", font="Helvetica 10 bold")
        self.lpf_name_label.pack()
        self.lpf4 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.lpf3 = tk.IntVar()
        self.lpf2 = tk.IntVar()
        self.lpf1 = tk.IntVar()
        self.lpf0 = tk.IntVar()
        self.lpfr4 = tk.IntVar()
        self.lpfr3 = tk.IntVar()
        self.lpfr2 = tk.IntVar()
        self.lpfr1 = tk.IntVar()
        self.lpfr0 = tk.IntVar()
        self.lpfchecks = tk.Frame(self.reg_frame)  # frame to contain all check buttons in one line
        self.lpfrchecks = tk.Frame(self.reg_frame)
        # read and write checkbuttons. read checkbuttons display read info when read button pressed (read checkbuttons have r)
        # write button sends checked boxes as binary number to bus
        self.lpfc4 = tk.Checkbutton(self.lpfchecks, text="SW 5", font="Consolas 10", variable=self.lpf4)
        self.lpfc3 = tk.Checkbutton(self.lpfchecks, text="SW 4", font="Consolas 10", variable=self.lpf3)
        self.lpfc2 = tk.Checkbutton(self.lpfchecks, text="SW 3", font="Consolas 10", variable=self.lpf2)
        self.lpfc1 = tk.Checkbutton(self.lpfchecks, text="SW 2", font="Consolas 10", variable=self.lpf1)
        self.lpfc0 = tk.Checkbutton(self.lpfchecks, text="SW 1", font="Consolas 10", variable=self.lpf0)
        self.lpfrc4 = tk.Checkbutton(self.lpfrchecks, text="SW 5", font="Consolas 10", variable=self.lpfr4)
        self.lpfrc3 = tk.Checkbutton(self.lpfrchecks, text="SW 4", font="Consolas 10", variable=self.lpfr3)
        self.lpfrc2 = tk.Checkbutton(self.lpfrchecks, text="SW 3", font="Consolas 10", variable=self.lpfr2)
        self.lpfrc1 = tk.Checkbutton(self.lpfrchecks, text="SW 2", font="Consolas 10", variable=self.lpfr1)
        self.lpfrc0 = tk.Checkbutton(self.lpfrchecks, text="SW 1", font="Consolas 10", variable=self.lpfr0)
        self.lpfchecks.pack(fill="x")
        self.lpfrchecks.pack(fill="x")
        self.spacer_lpf = tk.Canvas(self.lpfchecks, bg="grey94", height=0, width=243)
        self.spacer_lpf.pack(side="left")
        self.lpfc4.pack(side="left")
        self.lpfc3.pack(side="left")
        self.lpfc2.pack(side="left")
        self.lpfc1.pack(side="left")
        self.lpfc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.spacer_lpfr = tk.Canvas(self.lpfrchecks, bg="grey94", height=0, width=243)
        self.spacer_lpfr.pack(side="left")
        self.lpfrc4.pack(side="left")
        self.lpfrc3.pack(side="left")
        self.lpfrc2.pack(side="left")
        self.lpfrc1.pack(side="left")
        self.lpfrc0.pack(side="left")
        # read and write buttons
        self.lpf_send_button = tk.Button(self.lpfchecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.lpf_send)
        self.lpf_send_button.pack(side="right")
        self.lpf_read_button = tk.Button(self.lpfrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.lpf_read)
        self.lpf_read_button.pack(side="right")
        # end low pass filter


        # begin middle frame stuff (sensors/dacs)
        # dict for dnc selector
        self.dnc_dict = {"DNC 1": 0b10000101, "DNC 2": 0b10000110, "DNC 3": 0b01010000, "DNC 4": 0b01011000, }

        self.dnc_label = tk.Label(self.middle_frame, text="Select DNC", font="Helvetica 10 bold")
        self.dnc_label.pack() # instructions
        self.dnc_var = tk.StringVar()
        self.dnc_var.set("DNC 1")  # default value
        self.dnc_drowpdown = tk.OptionMenu(self.middle_frame, self.dnc_var, *self.dnc_dict)
        self.dnc_drowpdown.pack()  # dropdown to choose whic dnc (automatically sets it as well)

        # LTC2991 sensor section
        self.sensor_header = tk.Label(self.middle_frame, text="I/T Sensor Readout", font="Helvetica 10 bold")
        self.sensor_header.pack()
        self.raw_temp_value = tk.StringVar()
        self.temp_value = tk.StringVar()
        self.five_a_raw_value = tk.StringVar()
        self.five_a_current_value = tk.StringVar()
        self.five_b_raw_value = tk.StringVar()
        self.five_b_current_value = tk.StringVar()

        self.temp_header = tk.Label(self.middle_frame, text="Temp (raw|actual):", font="Helvetica 8")
        self.temp_header.pack()
        self.raw_temp_display = tk.Entry(self.middle_frame, textvariable=self.raw_temp_value)
        self.raw_temp_display.pack()
        self.temp_display = tk.Entry(self.middle_frame, textvariable=self.temp_value)
        self.temp_display.pack()

        self.five_a_header = tk.Label(self.middle_frame, text="+5.0V DNC A Current (raw|actual)", font="Helvetica 8")
        self.five_a_header.pack()
        self.five_a_raw_display = tk.Entry(self.middle_frame, textvariable=self.five_a_raw_value)
        self.five_a_raw_display.pack()
        self.five_a_current_display = tk.Entry(self.middle_frame, textvariable=self.five_a_current_value)
        self.five_a_current_display.pack()

        self.five_b_header = tk.Label(self.middle_frame, text="+5.0V DNC B Current (raw|actual)", font="Helvetica 8")
        self.five_b_header.pack()
        self.five_b_raw_display = tk.Entry(self.middle_frame, textvariable=self.five_b_raw_value)
        self.five_b_raw_display.pack()
        self.five_b_current_display = tk.Entry(self.middle_frame, textvariable=self.five_b_current_value)
        self.five_b_current_display.pack()

        self.sensor_read_button = tk.Button(self.middle_frame, text="Read LTC2991", bg="mediumpurple1", command=self.ltc2991_read)
        self.sensor_read_button.pack()
        # end LTC2991

        # start LTC2640-10 DAC
        self.ltc_dac_header = tk.Label(self.middle_frame, text="LTC2640-10 DAC", font="Helvetica 10 bold")
        self.ltc_dac_header.pack()
        self.ltc_dac_volt_label = tk.Label(self.middle_frame, text="Enter a voltage 0-2.5V:", font="Helvetica 8")
        self.ltc_dac_volt_label.pack()
        self.ltc_dac_user_voltage = tk.StringVar()
        self.ltc_dac_volt_entry = tk.Entry(self.middle_frame, textvariable=self.ltc_dac_user_voltage)
        self.ltc_dac_volt_entry.pack()
        self.ltc_dac_write_button = tk.Button(self.middle_frame, text="Kickoff DAC Write", bg="seagreen1", command=self.ltc_dac_write)
        self.ltc_dac_write_button.pack()
        # end DAC

        # exit button
        self.spacer12 = tk.Canvas(self.middle_frame, width=200, height=20, bg="grey94")
        self.spacer12.pack()
        self.quit_button = tk.Button(self.middle_frame, width=15, height=1, text="Quit", bg="red",
                                     command=self.dnc_gui.destroy)
        self.quit_button.pack()
        #self.reg_test_button = tk.Button(self.reg_frame, text="Test Reg Map", width=15, height=1, bg='orange', command=self.DNC_reg_test)
        #self.reg_test_button.pack()  # register test button that writes and reads data back to verify registers work

   # def dnc_set(self):
       # print(self.dnc_var.get())

    def ltc2991_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])
        rsense = 0.51 # store rsense for current calculations
        kickoff_data = (0xA << 8) | 1
        self.PLLFunc.PLLReg.sixteen_spi_write(kickoff_data) # write to kickoff register to populate registers

        v7_msb_address = 0x10
        v7_lsb_address = 0x11
        v7_msb = self.PLLFunc.PLLReg.sixteen_spi_read(v7_msb_address)[0] # retrieve raw data for temperature
        v7_lsb = self.PLLFunc.PLLReg.sixteen_spi_read(v7_lsb_address)[0]
        v7 = (v7_msb << 8) | v7_lsb # concatenate data
        self.raw_temp_value.set(str(bin(v7))) # set raw display to raw temp value
        temperature = v7 / 16 # calculate temperature from raw data in celsius
        self.temp_value.set(temperature) # set temp display to temperature value

        v4_msb_address = 0x16
        v4_lsb_address = 0x17
        v4_msb = self.PLLFunc.PLLReg.sixteen_spi_read(v4_msb_address)[0] # retrieve raw current data for current A
        v4_lsb = self.PLLFunc.PLLReg.sixteen_spi_read(v4_lsb_address)[0]
        v4 = (v4_msb << 8) | v4_lsb # concat
        sign_check = str(bin(0b100000000 | v4_msb)) # need to check the sign (two's comp) so make the msb indexable
        self.five_a_raw_value.set(str(bin(v4))) # set raw current A value display
        if sign_check[4] == '0': # check signs
            a_current = (v4 * 19.075 / rsense)
            self.five_a_current_value.set(a_current) # calculate and set current A display
        elif sign_check[4] == '1':
            a_current = ((~v4 + 1) * 19.075 / rsense) # same here but if negative
            self.five_a_current_value.set(a_current)

        v2_msb_address = 0x1A # all of this block is same as above but for current B
        v2_lsb_address = 0x1B
        v2_msb = self.PLLFunc.PLLReg.sixteen_spi_read(v2_msb_address)[0]
        v2_lsb = self.PLLFunc.PLLReg.sixteen_spi_read(v2_lsb_address)[0]
        v2 = (v2_msb << 8) | v2_lsb
        sign_check = str(bin(0b100000000 | v2_msb))
        self.five_b_raw_value.set(str(bin(v2)))
        if sign_check[4] == '0':
            b_current = (v2 * 19.075 / rsense)
            self.five_b_current_value.set(b_current)
        elif sign_check[4] == '1':
            b_current = ((~v2 + 1) * (-19.075) / rsense)
            self.five_b_current_value.set(b_current)

    def ltc_dac_write(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])
        address_command = 0x8
        address_data = 0x9
        address_kickoff = 0xA
        user_volt = float(self.ltc_dac_user_voltage.get()) # get voltage from user entry
        ten_bit_voltage = int(user_volt * (2 ** 10) / 2.5) # convert to digital voltage value
        dac_num = (0b11 << 10) | ten_bit_voltage # add command bits
        dac_word = '0000' + str(bin(dac_num))[2:] # format dac word
        mosi_data_command = (address_command << 8) | int(dac_word[:8], 2) # create spi bus data
        mosi_data_data = (address_data << 8) | int(dac_word[8:], 2)
        mosi_data_kickoff = (address_kickoff << 8) | 1
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_command) # send data on spi bus to dac registers
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_data)
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data_kickoff) # kickoff register to set off dac write

    def DNC_reg_test(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])
        num_tests = 50000
        passes = 0
        fails = 0
        for i in range(0,num_tests):
            address = randint(0, 28) # random address within bounds of DNC's memory map
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

    def soft_reset_send(self):
        # sends the retrieved data to the designated address using spi write function
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave to send to
        address = 0x00
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        concat = self.s0.get()  # retrieve data from data function
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)

    def test_pts_send(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave to send to
        address = 0x01
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        concat = self.t0.get()
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def dsa_send(self):
        # retrieves data from dsa check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0]
        bx = [self.ds4.get(), self.ds3.get(), self.ds2.get(), self.ds1.get(),
              self.ds0.get()]  # store value of each button in a list
        for x in range(0, 4):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (4 - x))
        by[4] = self.ds0.get()  # the last element of the array didn't need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4]  # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave to send to
        address = 0x02
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def ldo_en_send(self):
        # retrieves data from ldo check buttons and converts them into one number from several IntVars
        by = [0, 0]
        bx = [self.L1.get(), self.l0.get()]  # store value of each button in a list
        for x in range(0, 1):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (1 - x))
        by[1] = self.l0.get()  # the last element of the array didn't need to be bit shifted so its manually assigned
        concat = by[0] | by[1]  # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave to send to
        address = 0x03
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def sw_send(self):
        # retrieves data from switch check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0, 0, 0, 0]
        bx = [self.sw7.get(), self.sw6.get(), self.sw5.get(), self.sw4.get(), self.sw3.get(), self.sw2.get(), self.sw1.get(),
              self.sw0.get()]  # store value of each button in a list
        for x in range(0, 7):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (7 - x))
        by[7] = self.sw0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5] | by[6] | by[7]
        # bitwise 'or' the numbers in the array into one number
        # sends the data returned from data function to designated address
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave to send to
        address = 0x04
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def sw_send_2(self):
        # retrieves data from switch check buttons and converts into a single binary number
        by = [0, 0, 0, 0]
        bx = [self.sw3_2.get(), self.sw2_2.get(), self.sw1_2.get(),
              self.sw0_2.get()]  # store value of each button in a list
        for x in range(0, 3):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (3 - x))
        by[3] = self.sw0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3]
        # bitwise 'or' the numbers in the array into one number
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave to send to
        address = 0x05
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def lo2_send(self):
        # retrieves data from switch check buttons and converts into a single binary number
        by = [0, 0, 0, 0, 0, 0]
        bx = [self.sw5_2.get(), self.sw4_2.get(), self.sw3_2.get(), self.sw2_2.get(), self.sw1_2.get(),
              self.sw0_2.get()]  # store value of each button in a list
        for x in range(0, 5):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (5 - x))
        by[5] = self.sw0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4] | by[5]
        # bitwise 'or' the numbers in the array into one number
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave to send to
        address = 0x06
        address = address << 8  # bitshift to fit the format 1/7/8 rw/address/data
        mosi_data = address | concat  # concatenate address and data into proper format
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)  # send on SPI bus

    def lpf_send(self):
        # retrieves data from low pass filter checkbuttons and converts to an integer
        by = [0, 0, 0, 0, 0]
        bx = [self.lpf4.get(), self.lpf3.get(), self.lpf2.get(), self.lpf1.get(), self.lpf0.get()]  # store value of each button in a list
        for x in range(0, 4):  # assign the value of the 'gets' to a new list because IntVars cant be easily manipulated
            by[x] = (bx[x] << (4 - x))
        by[4] = self.lpf0.get()  # the last element of the array didnt need to be bitshifted so manually assign
        concat = by[0] | by[1] | by[2] | by[3] | by[4]  # bitwise 'or' the numbers in the array into one number
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave to send to
        address = 0x07
        address = address << 8
        mosi_data = address | concat
        self.PLLFunc.PLLReg.sixteen_spi_write(mosi_data)

    # applies for all of the following read functions:
    # 1: reads data from spi bus and stores the array
    # 2: converts the binary form of the data from the array into a string
    # 3.0: string looks something like "0b100010101" so the values we are interested in are the last 8 bits,
    # 3.1: the actual data, not the address. depending on mapping, only a certain amount of the last 8 bits are needed.
    # 4.0: assigns the notable data (starting from end of string) to the variables associated with the read checkbuttons,
    # 4.1: which will become checked or unchecked based on if it is assigned a one or a zero. this allows the user to
    # 4.2: visualize the data and settings currently stored on the aardvark.

    def test_pts_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x01)
        read = 0b10 | raw_read[0]
        string = str(bin(read))
        self.tr0.set(int(string[-1]))

    def dsa_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x02)
        read = 0b100000 | raw_read[0]
        string = str(bin(read))
        self.dsr4.set(int(string[-5]))
        self.dsr3.set(int(string[-4]))
        self.dsr2.set(int(string[-3]))
        self.dsr1.set(int(string[-2]))
        self.dsr0.set(int(string[-1]))

    def ldo_en_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x03)
        # print("raw_read:", raw_read)  # test
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.Lr1.set(int(string[-2]))
        self.lr0.set(int(string[-1]))

    def sw_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x04)
        read = 0b100000000 | raw_read[0]
        string = str(bin(read))
        self.swr7.set(int(string[-8]))
        self.swr6.set(int(string[-7]))
        self.swr5.set(int(string[-6]))
        self.swr4.set(int(string[-5]))
        self.swr3.set(int(string[-4]))
        self.swr2.set(int(string[-3]))
        self.swr1.set(int(string[-2]))
        self.swr0.set(int(string[-1]))

    def sw_read_2(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x05)
        read = 0b10000 | raw_read[0]
        string = str(bin(read))
        self.swr3_2.set(int(string[-4]))
        self.swr2_2.set(int(string[-3]))
        self.swr1_2.set(int(string[-2]))
        self.swr0_2.set(int(string[-1]))

    def lo2_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x06)
        read = 0b1000000 | raw_read[0]
        string = str(bin(read))
        self.lo2r5.set(int(string[-6]))
        self.lo2r5.set(int(string[-5]))
        self.lo2r5.set(int(string[-4]))
        self.lo2r5.set(int(string[-3]))
        self.lo2r5.set(int(string[-2]))
        self.lo2r5.set(int(string[-1]))

    def lpf_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict[self.dnc_var.get()])  # replace with correct slave number
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x07)
        read = 0b100000 | raw_read[0]
        string = str(bin(read))
        self.lpfr4.set(int(string[-5]))
        self.lpfr3.set(int(string[-4]))
        self.lpfr2.set(int(string[-3]))
        self.lpfr1.set(int(string[-2]))
        self.lpfr0.set(int(string[-1]))



x = DNCGui()
x.dnc_gui.mainloop()
x.PLLFunc.disconnectaardvark()
