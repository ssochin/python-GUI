import PLLFunc
import tkinter as tk
from tkinter import filedialog
import time
import getpass
from datetime import date
from aardvark_py import *
import os, sys
from random import randint

class LO1Gui:

    def __init__(self):
        self.PLLFunc = PLLFunc.PLLFunc() # create PLLFunc object to acccess functions like spi read etc
        self.PLLFunc.connect2aardvark()
        self.PLLFunc.PLLReg.slave_select_pca_config()

        self.LO1_gui = tk.Tk()
        self.LO1_gui.title("LO1 Reg Map")


        self.LO1_reg_frame = tk.Frame(self.LO1_gui) # frame containing reg map
        self.LO1_middle_frame = tk.Frame(self.LO1_gui) # frame contatining peripherals
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
        self.LO1_soft_name_label = tk.Label(self.LO1_reg_frame, text="Return FPGA to known State", font="Helvetica 10 bold")
        self.LO1_soft_name_label.pack()
        self.LO1_s0 = tk.IntVar()  # tkinter variable(s) for checkbutton(s) that can be accessed globally
        self.LO1_schecks = tk.Frame(self.LO1_reg_frame)  # frame to contain all check buttons in one line
        # checkbutton (this data is only one bit)
        self.LO1_spacer_c = tk.Canvas(self.LO1_schecks, width=101, height=0, bg="grey94")
        self.LO1_spacer_c.pack(side="left")
        self.LO1_sc0 = tk.Checkbutton(self.LO1_schecks, text="Soft Reset", font="Consolas 10", variable=self.LO1_s0)
        self.LO1_schecks.pack(fill="x")
        # send button (only a write, no read for this one)
        self.LO1_send_but_frame = tk.Frame(self.LO1_schecks)
        self.LO1_send_but_frame.pack(side="right")
        self.LO1_sc0.pack(fill="both")  # pack left so that the buttons stack horizontally, pad helps de-clutter
        self.LO1_soft_send_button = tk.Button(self.LO1_send_but_frame, text="Send Bits", bg="lime green", width=15, height=1, command=self.LO1_soft_reset_send)
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
        self.LO1_dc1 = tk.Checkbutton(self.LO1_dchecks, text="DNC3 SEL", font="Consolas 10", variable=self.LO1_d1)
        self.LO1_dc0 = tk.Checkbutton(self.LO1_dchecks, text="DNC4 SEL", font="Consolas 10", variable=self.LO1_d0)
        self.LO1_drc1 = tk.Checkbutton(self.LO1_drchecks, text="DNC3 SEL", font="Consolas 10", variable=self.LO1_dr1)
        self.LO1_drc0 = tk.Checkbutton(self.LO1_drchecks, text="DNC4 SEL", font="Consolas 10", variable=self.LO1_dr0)
        self.LO1_dchecks.pack(fill="x")
        self.LO1_drchecks.pack(fill="x")
        self.LO1_spacer_dnc = tk.Canvas(self.LO1_dchecks, width=246, height=0, bg="grey94")
        self.LO1_spacer_dnc.pack(side="left")
        self.LO1_dc1.pack(side="left")
        self.LO1_dc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_dncr = tk.Canvas(self.LO1_drchecks, width=246, height=0, bg="grey94")
        self.LO1_spacer_dncr.pack(side="left")
        self.LO1_drc1.pack(side="left")
        self.LO1_drc0.pack(side="left")
        # read and write buttons for this address
        self.LO1_dnc_con_send_button = tk.Button(self.LO1_dchecks, text="Send Bits", bg="lime green", width=15, height=1,
                                             command=self.LO1_dnc_con_send)
        self.LO1_dnc_con_send_button.pack(side="right")
        self.LO1_dnc_con_read_button = tk.Button(self.LO1_drchecks, text="Read Bits", bg="black", fg="white", width=15,
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
        self.LO1_tc1 = tk.Checkbutton(self.LO1_tchecks, text="TP1", font="Consolas 10", variable=self.LO1_t1)
        self.LO1_tc0 = tk.Checkbutton(self.LO1_tchecks, text="TP2", font="Consolas 10", variable=self.LO1_t0)
        self.LO1_trc1 = tk.Checkbutton(self.LO1_trchecks, text="TP1", font="Consolas 10", variable=self.LO1_tr1)
        self.LO1_trc0 = tk.Checkbutton(self.LO1_trchecks, text="TP2", font="Consolas 10", variable=self.LO1_tr0)
        self.LO1_tchecks.pack(fill="x")
        self.LO1_trchecks.pack(fill="x")
        self.LO1_spacer_t = tk.Canvas(self.LO1_tchecks, width=282, height=0, bg="grey94")
        self.LO1_spacer_t.pack(side="left") # reg ex and stuff
        self.LO1_tc1.pack(side="left")  # pad helps de-clutter
        self.LO1_tc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_tr = tk.Canvas(self.LO1_trchecks, width=282, height=0, bg="grey94")
        self.LO1_spacer_tr.pack(side="left")
        self.LO1_trc1.pack(side="left")
        self.LO1_trc0.pack(side="left")
        # read and write buttons for this address
        self.LO1_test_send_button = tk.Button(self.LO1_tchecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.LO1_test_pts_send)
        self.LO1_test_send_button.pack(side="right")
        self.LO1_test_read_button = tk.Button(self.LO1_trchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.LO1_test_pts_read)
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
        self.LO1_cc1 = tk.Checkbutton(self.LO1_cchecks, text="CE PLO", font="Consolas 10", variable=self.LO1_c1)
        self.LO1_cc0 = tk.Checkbutton(self.LO1_cchecks, text="CE LO2", font="Consolas 10", variable=self.LO1_c0)
        self.LO1_crc1 = tk.Checkbutton(self.LO1_crchecks, text="CE PLO", font="Consolas 10", variable=self.LO1_cr1)
        self.LO1_crc0 = tk.Checkbutton(self.LO1_crchecks, text="CE LO2", font="Consolas 10", variable=self.LO1_cr0)
        self.LO1_cchecks.pack(fill="x")
        self.LO1_crchecks.pack(fill="x")
        self.LO1_spacer_cen = tk.Canvas(self.LO1_cchecks, width=260, height=0, bg="grey94")
        self.LO1_spacer_cen.pack(side="left")
        self.LO1_cc1.pack(side="left")  # padx adds space on either side of each button. helps spread out
        self.LO1_cc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_cenr = tk.Canvas(self.LO1_crchecks, width=260, height=0, bg="grey94")
        self.LO1_spacer_cenr.pack(side="left")
        self.LO1_crc1.pack(side="left")
        self.LO1_crc0.pack(side="left")
        # individual read and write buttons for specific address
        self.LO1_chip_send_button = tk.Button(self.LO1_cchecks, text="Send Bits", bg="lime green", width=15, height=1,
                                          command=self.LO1_chip_en_send)
        self.LO1_chip_send_button.pack(side="right")
        self.LO1_chip_read_button = tk.Button(self.LO1_crchecks, text="Read Bits", bg="black", fg="white", width=15, height=1,
                                          command=self.LO1_chip_en_read)
        self.LO1_chip_read_button.pack(side="right")
        self.LO1_spacer4.pack()
        # end of chip enable section

        # imp det read section
        self.LO1_imp_name_label = tk.Label(self.LO1_reg_frame, text="Input Power Detect", font="Helvetica 10 bold")
        self.LO1_imp_name_label.pack()
        self.LO1_ichecks = tk.Frame(self.LO1_reg_frame)
        self.LO1_ir0 = tk.IntVar()
        self.LO1_imp_check = tk.Checkbutton(self.LO1_ichecks, text="Power Detect", font="Consolas 10", variable=self.LO1_ir0)
        self.LO1_ichecks.pack(fill="x")
        self.LO1_spacer_ir = tk.Canvas(self.LO1_ichecks, width=109, height=0, bg="grey94")
        self.LO1_spacer_ir.pack(side="left")
        self.LO1_read_but_frame = tk.Frame(self.LO1_ichecks)
        self.LO1_read_but_frame.pack(side="right")
        self.LO1_imp_check.pack(fill="both")
        # read button for this address (no write)
        self.LO1_imp_read_button = tk.Button(self.LO1_read_but_frame, text="Read Bits", fg="white", bg="black", width=15,
                                         height=1, command=self.LO1_imp_det_read)
        self.LO1_imp_read_button.pack()
        self.LO1_spacer5.pack()
        # end imp det section


        # LO1 attenuator settings
        self.LO1_att_name_label = tk.Label(self.LO1_reg_frame, text="LO1 Digital Step Attenuator Settings", font="Helvetica 10 bold")
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
        self.LO1_attc5 = tk.Checkbutton(self.LO1_attchecks, text="ATT 5", font="Consolas 10", variable=self.LO1_att5)
        self.LO1_attc4 = tk.Checkbutton(self.LO1_attchecks, text="ATT 4", font="Consolas 10", variable=self.LO1_att4)
        self.LO1_attc3 = tk.Checkbutton(self.LO1_attchecks, text="ATT 3", font="Consolas 10", variable=self.LO1_att3)
        self.LO1_attc2 = tk.Checkbutton(self.LO1_attchecks, text="ATT 2", font="Consolas 10", variable=self.LO1_att2)
        self.LO1_attc1 = tk.Checkbutton(self.LO1_attchecks, text="ATT 1", font="Consolas 10", variable=self.LO1_att1)
        self.LO1_attc0 = tk.Checkbutton(self.LO1_attchecks, text="ATT 0", font="Consolas 10", variable=self.LO1_att0)
        self.LO1_attrc5 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 5", font="Consolas 10", variable=self.LO1_attr5)
        self.LO1_attrc4 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 4", font="Consolas 10", variable=self.LO1_attr4)
        self.LO1_attrc3 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 3", font="Consolas 10", variable=self.LO1_attr3)
        self.LO1_attrc2 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 2", font="Consolas 10", variable=self.LO1_attr2)
        self.LO1_attrc1 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 1", font="Consolas 10", variable=self.LO1_attr1)
        self.LO1_attrc0 = tk.Checkbutton(self.LO1_attrchecks, text="ATT 0", font="Consolas 10", variable=self.LO1_attr0)
        self.LO1_attchecks.pack(fill="x")
        self.LO1_attrchecks.pack(fill="x")
        self.LO1_spacer_att = tk.Canvas(self.LO1_attchecks, width=141, height=0, bg="grey94")
        self.LO1_spacer_att.pack(side="left")
        self.LO1_attc5.pack(side="left")
        self.LO1_attc4.pack(side="left")
        self.LO1_attc3.pack(side="left")
        self.LO1_attc2.pack(side="left")
        self.LO1_attc1.pack(side="left")
        self.LO1_attc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_attr = tk.Canvas(self.LO1_attrchecks, width=141, height=0, bg="grey94")
        self.LO1_spacer_attr.pack(side="left")
        self.LO1_attrc5.pack(side="left")
        self.LO1_attrc4.pack(side="left")
        self.LO1_attrc3.pack(side="left")
        self.LO1_attrc2.pack(side="left")
        self.LO1_attrc1.pack(side="left")
        self.LO1_attrc0.pack(side="left")
        # read and write buttons
        self.LO1_att_send_button = tk.Button(self.LO1_attchecks, text="Send Bits", bg="lime green", width=15, height=1,
                                         command=self.LO1_att_send)
        self.LO1_att_send_button.pack(side="right")
        self.LO1_att_read_button = tk.Button(self.LO1_attrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1,
                                         command=self.LO1_att_read)
        self.LO1_att_read_button.pack(side="right")
        self.LO1_spacer6.pack()
        # end att settings


        # RF DSA checkbutton setup section
        self.LO1_DSA_name_label = tk.Label(self.LO1_reg_frame, text="RF Digital Step Attenuator Settings", font="Helvetica 10 bold")
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
        self.LO1_dsc5 = tk.Checkbutton(self.LO1_dschecks, text="D5 ATT", font="Consolas 10", variable=self.LO1_ds5)
        self.LO1_dsc4 = tk.Checkbutton(self.LO1_dschecks, text="D4 ATT", font="Consolas 10", variable=self.LO1_ds4)
        self.LO1_dsc3 = tk.Checkbutton(self.LO1_dschecks, text="D3 ATT", font="Consolas 10", variable=self.LO1_ds3)
        self.LO1_dsc2 = tk.Checkbutton(self.LO1_dschecks, text="D2 ATT", font="Consolas 10", variable=self.LO1_ds2)
        self.LO1_dsc1 = tk.Checkbutton(self.LO1_dschecks, text="D1 ATT", font="Consolas 10", variable=self.LO1_ds1)
        self.LO1_dsc0 = tk.Checkbutton(self.LO1_dschecks, text="D0 ATT", font="Consolas 10", variable=self.LO1_ds0)
        self.LO1_dsrc5 = tk.Checkbutton(self.LO1_dsrchecks, text="D5 ATT", font="Consolas 10", variable=self.LO1_dsr5)
        self.LO1_dsrc4 = tk.Checkbutton(self.LO1_dsrchecks, text="D4 ATT", font="Consolas 10", variable=self.LO1_dsr4)
        self.LO1_dsrc3 = tk.Checkbutton(self.LO1_dsrchecks, text="D3 ATT", font="Consolas 10", variable=self.LO1_dsr3)
        self.LO1_dsrc2 = tk.Checkbutton(self.LO1_dsrchecks, text="D2 ATT", font="Consolas 10", variable=self.LO1_dsr2)
        self.LO1_dsrc1 = tk.Checkbutton(self.LO1_dsrchecks, text="D1 ATT", font="Consolas 10", variable=self.LO1_dsr1)
        self.LO1_dsrc0 = tk.Checkbutton(self.LO1_dsrchecks, text="D0 ATT", font="Consolas 10", variable=self.LO1_dsr0)
        self.LO1_dschecks.pack(fill="x")
        self.LO1_dsrchecks.pack(fill="x")
        self.LO1_spacer_ds = tk.Canvas(self.LO1_dschecks, width=120, height=0, bg="grey94")
        self.LO1_spacer_ds.pack(side="left")
        self.LO1_dsc5.pack(side="left")
        self.LO1_dsc4.pack(side="left")
        self.LO1_dsc3.pack(side="left")
        self.LO1_dsc2.pack(side="left")
        self.LO1_dsc1.pack(side="left")
        self.LO1_dsc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_dsr = tk.Canvas(self.LO1_dsrchecks, width=120, height=0, bg="grey94")
        self.LO1_spacer_dsr.pack(side="left")
        self.LO1_dsrc5.pack(side="left")
        self.LO1_dsrc4.pack(side="left")
        self.LO1_dsrc3.pack(side="left")
        self.LO1_dsrc2.pack(side="left")
        self.LO1_dsrc1.pack(side="left")
        self.LO1_dsrc0.pack(side="left")
        # read and write buttons
        self.LO1_dsa_send_button = tk.Button(self.LO1_dschecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.LO1_dsa_send)
        self.LO1_dsa_send_button.pack(side="right")
        self.LO1_dsa_read_button = tk.Button(self.LO1_dsrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.LO1_dsa_read)
        self.LO1_dsa_read_button.pack(side="right")
        self.LO1_spacer7.pack()
        # end DSA LO1


        #dsa LO2 section
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
        self.LO1_dstc5 = tk.Checkbutton(self.LO1_dstchecks, text="D5 ATT", font="Consolas 10", variable=self.LO1_dst5)
        self.LO1_dstc4 = tk.Checkbutton(self.LO1_dstchecks, text="D4 ATT", font="Consolas 10", variable=self.LO1_dst4)
        self.LO1_dstc3 = tk.Checkbutton(self.LO1_dstchecks, text="D3 ATT", font="Consolas 10", variable=self.LO1_dst3)
        self.LO1_dstc2 = tk.Checkbutton(self.LO1_dstchecks, text="D2 ATT", font="Consolas 10", variable=self.LO1_dst2)
        self.LO1_dstc1 = tk.Checkbutton(self.LO1_dstchecks, text="D1 ATT", font="Consolas 10", variable=self.LO1_dst1)
        self.LO1_dstc0 = tk.Checkbutton(self.LO1_dstchecks, text="D0 ATT", font="Consolas 10", variable=self.LO1_dst0)
        self.LO1_dstrc5 = tk.Checkbutton(self.LO1_dstrchecks, text="D5 ATT", font="Consolas 10", variable=self.LO1_dstr5)
        self.LO1_dstrc4 = tk.Checkbutton(self.LO1_dstrchecks, text="D4 ATT", font="Consolas 10", variable=self.LO1_dstr4)
        self.LO1_dstrc3 = tk.Checkbutton(self.LO1_dstrchecks, text="D3 ATT", font="Consolas 10", variable=self.LO1_dstr3)
        self.LO1_dstrc2 = tk.Checkbutton(self.LO1_dstrchecks, text="D2 ATT", font="Consolas 10", variable=self.LO1_dstr2)
        self.LO1_dstrc1 = tk.Checkbutton(self.LO1_dstrchecks, text="D1 ATT", font="Consolas 10", variable=self.LO1_dstr1)
        self.LO1_dstrc0 = tk.Checkbutton(self.LO1_dstrchecks, text="D0 ATT", font="Consolas 10", variable=self.LO1_dstr0)
        self.LO1_dstchecks.pack(fill="x")
        self.LO1_dstrchecks.pack(fill="x")
        self.LO1_spacer_dst = tk.Canvas(self.LO1_dstchecks, width=120, height=0, bg="grey94")
        self.LO1_spacer_dst.pack(side="left")
        self.LO1_dstc5.pack(side="left")
        self.LO1_dstc4.pack(side="left")
        self.LO1_dstc3.pack(side="left")
        self.LO1_dstc2.pack(side="left")
        self.LO1_dstc1.pack(side="left")
        self.LO1_dstc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_dstr = tk.Canvas(self.LO1_dstrchecks, width=120, height=0, bg="grey94")
        self.LO1_spacer_dstr.pack(side="left")
        self.LO1_dstrc5.pack(side="left")
        self.LO1_dstrc4.pack(side="left")
        self.LO1_dstrc3.pack(side="left")
        self.LO1_dstrc2.pack(side="left")
        self.LO1_dstrc1.pack(side="left")
        self.LO1_dstrc0.pack(side="left")
        # read and write buttons
        self.LO1_dsat_send_button = tk.Button(self.LO1_dstchecks, text="Send Bits", bg="lime green", width=15, height=1,
                                         command=self.LO1_dsat_send)
        self.LO1_dsat_send_button.pack(side="right")
        self.LO1_dsat_read_button = tk.Button(self.LO1_dstrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1,
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
        self.LO1_swc5 = tk.Checkbutton(self.LO1_swchecks, text="LO1 MUTE", font="Consolas 10", variable=self.LO1_sw5)
        self.LO1_swc4 = tk.Checkbutton(self.LO1_swchecks, text="BPF SWA", font="Consolas 10", variable=self.LO1_sw4)
        self.LO1_swc3 = tk.Checkbutton(self.LO1_swchecks, text="BPF SWB", font="Consolas 10", variable=self.LO1_sw3)
        self.LO1_swc2 = tk.Checkbutton(self.LO1_swchecks, text="BPF SWC", font="Consolas 10", variable=self.LO1_sw2)
        self.LO1_swc1 = tk.Checkbutton(self.LO1_swchecks, text="RF COMB", font="Consolas 10", variable=self.LO1_sw1)
        self.LO1_swc0 = tk.Checkbutton(self.LO1_swchecks, text="RF SPLIT", font="Consolas 10", variable=self.LO1_sw0)
        self.LO1_swrc5 = tk.Checkbutton(self.LO1_swrchecks, text="LO1 MUTE", font="Consolas 10", variable=self.LO1_swr5)
        self.LO1_swrc4 = tk.Checkbutton(self.LO1_swrchecks, text="BPF SWA", font="Consolas 10", variable=self.LO1_swr4)
        self.LO1_swrc3 = tk.Checkbutton(self.LO1_swrchecks, text="BPF SWB", font="Consolas 10", variable=self.LO1_swr3)
        self.LO1_swrc2 = tk.Checkbutton(self.LO1_swrchecks, text="BPF SWC", font="Consolas 10", variable=self.LO1_swr2)
        self.LO1_swrc1 = tk.Checkbutton(self.LO1_swrchecks, text="RF COMB", font="Consolas 10", variable=self.LO1_swr1)
        self.LO1_swrc0 = tk.Checkbutton(self.LO1_swrchecks, text="RF SPLIT", font="Consolas 10", variable=self.LO1_swr0)
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
        self.LO1_sw_send_button = tk.Button(self.LO1_swchecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.LO1_sw_send)
        self.LO1_sw_send_button.pack(side="right")
        self.LO1_sw_read_button = tk.Button(self.LO1_swrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.LO1_sw_read)
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
        self.LO1_swc6_2 = tk.Checkbutton(self.LO1_swchecks_2, text="RFO BYP", font="Consolas 10", variable=self.LO1_sw6_2)
        self.LO1_swc5_2 = tk.Checkbutton(self.LO1_swchecks_2, text="LO1 IMP", font="Consolas 10", variable=self.LO1_sw5_2)
        self.LO1_swc4_2 = tk.Checkbutton(self.LO1_swchecks_2, text="UPC LO1", font="Consolas 10", variable=self.LO1_sw4_2)
        self.LO1_swc3_2 = tk.Checkbutton(self.LO1_swchecks_2, text="IF BYP", font="Consolas 10", variable=self.LO1_sw3_2)
        self.LO1_swc2_2 = tk.Checkbutton(self.LO1_swchecks_2, text="AMP BIAS", font="Consolas 10", variable=self.LO1_sw2_2)
        self.LO1_swc1_2 = tk.Checkbutton(self.LO1_swchecks_2, text="RFO 1", font="Consolas 10", variable=self.LO1_sw1_2)
        self.LO1_swc0_2 = tk.Checkbutton(self.LO1_swchecks_2, text="RFO 0", font="Consolas 10", variable=self.LO1_sw0_2)
        self.LO1_swrc6_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="RFO BYP", font="Consolas 10", variable=self.LO1_swr6_2)
        self.LO1_swrc5_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="LO1 IMP", font="Consolas 10", variable=self.LO1_swr5_2)
        self.LO1_swrc4_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="UPC LO1", font="Consolas 10", variable=self.LO1_swr4_2)
        self.LO1_swrc3_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="IF BYP", font="Consolas 10", variable=self.LO1_swr3_2)
        self.LO1_swrc2_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="AMP BIAS", font="Consolas 10", variable=self.LO1_swr2_2)
        self.LO1_swrc1_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="RFO 1", font="Consolas 10", variable=self.LO1_swr1_2)
        self.LO1_swrc0_2 = tk.Checkbutton(self.LO1_swrchecks_2, text="RFO 0", font="Consolas 10", variable=self.LO1_swr0_2)
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
        self.LO1_sw_send_button_2 = tk.Button(self.LO1_swchecks_2, text="Send Bits", bg="lime green", width=15, height=1, command=self.LO1_sw_send_2)
        self.LO1_sw_send_button_2.pack(side="right")
        self.LO1_sw_read_button_2 = tk.Button(self.LO1_swrchecks_2, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.LO1_sw_read_2)
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
        self.LO1_swc2_3 = tk.Checkbutton(self.LO1_swchecks_3, text="LO2 IMP SEL", font="Consolas 10", variable=self.LO1_sw2_3)
        self.LO1_swc1_3 = tk.Checkbutton(self.LO1_swchecks_3, text="LO2 DEST SEL", font="Consolas 10", variable=self.LO1_sw1_3)
        self.LO1_swc0_3 = tk.Checkbutton(self.LO1_swchecks_3, text="TP SEL", font="Consolas 10", variable=self.LO1_sw0_3)
        self.LO1_swrc2_3 = tk.Checkbutton(self.LO1_swrchecks_3, text="LO2 IMP SEL", font="Consolas 10", variable=self.LO1_swr2_3)
        self.LO1_swrc1_3 = tk.Checkbutton(self.LO1_swrchecks_3, text="LO2 DEST SEL", font="Consolas 10", variable=self.LO1_swr1_3)
        self.LO1_swrc0_3 = tk.Checkbutton(self.LO1_swrchecks_3, text="TP SEL", font="Consolas 10", variable=self.LO1_swr0_3)
        self.LO1_swchecks_3.pack(fill="x")
        self.LO1_swrchecks_3.pack(fill="x")
        self.LO1_spacer_sw_3 = tk.Canvas(self.LO1_swchecks_3, bg="grey94", width=185, height=0)
        self.LO1_spacer_sw_3.pack(side="left")
        self.LO1_swc2_3.pack(side="left")
        self.LO1_swc1_3.pack(side="left")
        self.LO1_swc0_3.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_swr_3 = tk.Canvas(self.LO1_swrchecks_3, bg="grey94", width=185, height=0)
        self.LO1_spacer_swr_3.pack(side="left")
        self.LO1_swrc2_3.pack(side="left")
        self.LO1_swrc1_3.pack(side="left")
        self.LO1_swrc0_3.pack(side="left")
        # read and write buttons
        self.LO1_sw_send_button_3 = tk.Button(self.LO1_swchecks_3, text="Send Bits", bg="lime green", width=15, height=1,
                                          command=self.LO1_sw_send_3)
        self.LO1_sw_send_button_3.pack(side="right")
        self.LO1_sw_read_button_3 = tk.Button(self.LO1_swrchecks_3, text="Read Bits", bg="black", fg="white", width=15,
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
        self.LO1_lpfc4 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 5", font="Consolas 10", variable=self.LO1_lpf4)
        self.LO1_lpfc3 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 4", font="Consolas 10", variable=self.LO1_lpf3)
        self.LO1_lpfc2 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 3", font="Consolas 10", variable=self.LO1_lpf2)
        self.LO1_lpfc1 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 2", font="Consolas 10", variable=self.LO1_lpf1)
        self.LO1_lpfc0 = tk.Checkbutton(self.LO1_lpfchecks, text="SW 1", font="Consolas 10", variable=self.LO1_lpf0)
        self.LO1_lpfrc4 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 5", font="Consolas 10", variable=self.LO1_lpfr4)
        self.LO1_lpfrc3 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 4", font="Consolas 10", variable=self.LO1_lpfr3)
        self.LO1_lpfrc2 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 3", font="Consolas 10", variable=self.LO1_lpfr2)
        self.LO1_lpfrc1 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 2", font="Consolas 10", variable=self.LO1_lpfr1)
        self.LO1_lpfrc0 = tk.Checkbutton(self.LO1_lpfrchecks, text="SW 1", font="Consolas 10", variable=self.LO1_lpfr0)
        self.LO1_lpfchecks.pack(fill="x")
        self.LO1_lpfrchecks.pack(fill="x")
        self.LO1_spacer_lpf = tk.Canvas(self.LO1_lpfchecks, bg="grey94", height=0, width=190)
        self.LO1_spacer_lpf.pack(side="left")
        self.LO1_lpfc4.pack(side="left")
        self.LO1_lpfc3.pack(side="left")
        self.LO1_lpfc2.pack(side="left")
        self.LO1_lpfc1.pack(side="left")
        self.LO1_lpfc0.pack(side="left")  # pack left so that the buttons stack horizontally
        self.LO1_spacer_lpfr = tk.Canvas(self.LO1_lpfrchecks, bg="grey94", height=0, width=190)
        self.LO1_spacer_lpfr.pack(side="left")
        self.LO1_lpfrc4.pack(side="left")
        self.LO1_lpfrc3.pack(side="left")
        self.LO1_lpfrc2.pack(side="left")
        self.LO1_lpfrc1.pack(side="left")
        self.LO1_lpfrc0.pack(side="left")
        # read and write buttons
        self.LO1_lpf_send_button = tk.Button(self.LO1_lpfchecks, text="Send Bits", bg="lime green", width=15, height=1, command=self.LO1_lpf_send)
        self.LO1_lpf_send_button.pack(side="right")
        self.LO1_lpf_read_button = tk.Button(self.LO1_lpfrchecks, text="Read Bits", bg="black", fg="white", width=15, height=1, command=self.LO1_lpf_read)
        self.LO1_lpf_read_button.pack(side="right")
        # end low pass filter


        self.LO1_reg_test_button = tk.Button(self.LO1_reg_frame, text="Test Reg Map", width=15, height=1, bg='orange', command=self.LO1_reg_test)
        self.LO1_reg_test_button.pack()  # register test button that writes and reads data back to verify registers work

        # begin middle frame code
        # bpf dac
        self.LO1_bpf_header = tk.Label(self.LO1_middle_frame, text="BPF DAC", font="Helvetica 10 bold")
        self.LO1_bpf_header.pack()
        self.LO1_bpf_dac_label = tk.Label(self.LO1_middle_frame, text="Enter a voltage 0-2.5V")
        self.LO1_bpf_dac_label.pack()
        self.LO1_bpf_dac_voltage = tk.StringVar()
        self.LO1_bpf_dac_entry = tk.Entry(self.LO1_middle_frame, textvariable=self.LO1_bpf_dac_voltage)
        self.LO1_bpf_dac_entry.pack()
        self.LO1_bpf_dac_button = tk.Button(self.LO1_middle_frame, text="BPF DAC Write", bg="steel blue", command=self.LO1_bpf_dac_write)
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
        self.LO1_vxp_dac_a_buton = tk.Button(self.LO1_middle_frame, text="VXP DAC A Write", bg="yellow2", command=self.LO1_vxp_dac_a_write)
        self.LO1_vxp_dac_a_buton.pack()
        self.LO1_vxp_dac_b_buton = tk.Button(self.LO1_middle_frame, text="VXP DAC B Write", bg="medium orchid", command=self.LO1_vxp_dac_b_write)
        self.LO1_vxp_dac_b_buton.pack()

        self.LO1_spacer13 = tk.Canvas(self.LO1_middle_frame, bg="grey94", height=5, width=200)
        self.LO1_spacer13.pack()
        # Temp monitor
        self.LO1_temp_header = tk.Label(self.LO1_middle_frame, text="Temperature Monitor", font="Helvetica 10 bold")
        self.LO1_temp_header.pack()
        self.LO1_temp_string = tk.StringVar()
        self.LO1_temp_display = tk.Entry(self.LO1_middle_frame, textvariable=self.LO1_temp_string)
        self.LO1_temp_display.pack()
        self.LO1_temp_read_button = tk.Button(self.LO1_middle_frame, bg="orange", text="Read Temp", command=self.LO1_temp_read)
        self.LO1_temp_read_button.pack()

        self.LO1_spacer14 = tk.Canvas(self.LO1_middle_frame, bg="grey94", height=5, width=200)
        self.LO1_spacer14.pack()
        # ADC
        self.LO1_adc_header = tk.Label(self.LO1_middle_frame, text="LTC2313-12 ADC", font="Helvetica 10 bold")
        self.LO1_adc_header.pack()
        self.LO1_adc_value = tk.StringVar()
        self.LO1_adc_display = tk.Entry(self.LO1_middle_frame, textvariable=self.LO1_adc_value)
        self.LO1_adc_display.pack()
        self.LO1_adc_read_button = tk.Button(self.LO1_middle_frame, text="Read ADC", bg="seagreen1", command=self.LO1_adc_read)
        self.LO1_adc_read_button.pack()

        self.LO1_spacer15 = tk.Canvas(self.LO1_middle_frame, bg="grey94", height=20, width=200)
        self.LO1_spacer15.pack()
        self.quit_button = tk.Button(self.LO1_middle_frame, width=15, height=1, text="Quit", bg="red", command=self.LO1_gui.destroy)
        self.quit_button.pack()

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


    # applies for all of the following read functions:
    # 1: reads data from spi bus and stores the array
    # 2: converts the binary form of the data from the array into a string
    # 3.0: string looks something like "0b100010101" so the values we are interested in are the last 8 bits,
    # 3.1: the actual data, not the address. depending on mapping, only a certain amount of the last 8 bits are needed.
    # 4.0: assigns the notable data (starting from end of string) to the variables associated with the read checkbuttons,
    # 4.1: which will become checked or unchecked based on if it is assigned a one or a zero. this allows the user to
    # 4.2: visualize the data and settings currently stored on the aardvark.

    def LO1_dnc_con_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x01)
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.LO1_dr1.set(int(string[-2]))
        self.LO1_dr0.set(int(string[-1]))

    def LO1_test_pts_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x02)
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.LO1_tr1.set(int(string[-2]))
        self.LO1_tr0.set(int(string[-1]))

    def LO1_chip_en_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # choose slave to read from
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x03)
        read = 0b100 | raw_read[0]
        string = str(bin(read))
        self.LO1_cr1.set(int(string[-2]))
        self.LO1_cr0.set(int(string[-1]))

    def LO1_imp_det_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # choose slave to read from
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
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
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
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
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
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
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
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # add correct slave
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x0A)
        read = 0b1000 | raw_read[0]
        string = str(bin(read))
        self.LO1_swr2_3.set(int(string[-3]))
        self.LO1_swr1_3.set(int(string[-2]))
        self.LO1_swr0_3.set(int(string[-1]))

    def LO1_lpf_read(self):
        self.PLLFunc.PLLReg.slave_select_write(self.PLLFunc.PLLReg.slave_select_dict["LO1 Reg Map"])  # replace with correct slave number
        raw_read = self.PLLFunc.PLLReg.sixteen_spi_read(0x0B)
        read = 0b100000 | raw_read[0]
        string = str(bin(read))
        self.LO1_lpfr4.set(int(string[-5]))
        self.LO1_lpfr3.set(int(string[-4]))
        self.LO1_lpfr2.set(int(string[-3]))
        self.LO1_lpfr1.set(int(string[-2]))
        self.LO1_lpfr0.set(int(string[-1]))



x = LO1Gui()
x.LO1_gui.mainloop()
x.PLLFunc.disconnectaardvark()
