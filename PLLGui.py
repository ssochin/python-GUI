import PLLFunc
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import time
import getpass
from datetime import date
import os, sys

autocalHis = []


class PLLGui:

    def __init__(self):
        self.GUIversion = "V3.0"
        self.PLLFunc = PLLFunc.PLLFunc()  # initialize a PLLFunc object to run PLL functions
        #connect to aardvark
        self.PLLFunc.connect2aardvark()

        # initialize GUI
        self.root = tk.Tk()
        self.root.title("LMX2594 " + self.GUIversion + " by Steve")
        self.canvas = tk.Canvas(self.root, width=400, height=0)
        self.canvas.pack(fill="both",expand=True) #auto resizes window based off gui
        self.canvas.pack()
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
        self.quit_button = tk.Button(self.root, fg="Red", text='Quit', width=25, command=self.root.destroy)

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
        self.sheet_label = tk.Label(self.root)
        self.sheet_label.config(text="Generate A->B->A Spreadsheet", font="Helvetica 10 bold")
        self.freq1_label = tk.Label(self.root)
        self.freq1_label.config(text="Frequency 1 (MHz)")
        self.freq1 = 7000  # frequency 1 entry
        self.freq1_entry = tk.Entry(self.root, width=25)
        self.freq2_label = tk.Label(self.root)
        self.freq2_label.config(text="Frequency 2 (MHz)")
        self.freq2 = 8000  # frequency 2 entry
        self.freq2_entry = tk.Entry(self.root, width=25)
        self.delay_label = tk.Label(self.root)
        self.delay_label.config(text="Delay between Freq.'s (uS)")
        self.delay = 50  # delay between freq 1 and freq 2
        self.delay_entry = tk.Entry(self.root, width=25)
        self.sheet_button = tk.Button(self.root, text="Generate A->B->A Spreadsheet", width=25, command=self.generate_ABA_spreadsheet)



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
        self.sheetPerFreq_button = tk.Button(self.root, text="Generate Bit Bang spreadsheets", width=25,command=self.generate_bypassautocal_spreadsheet_per_freq)
        self.lookuptable_button = tk.Button(self.root, text="Edit PLL Lookup Table", width=25, command=self.changetable)

        # launch GUI?
        self.root.mainloop()

    # sets up level two GUI
    def leveltwoGui(self, Ref):
        # kill level one buttons
        self.name_label.pack_forget()
        self.ref_label.pack_forget()
        self.tenmhz_button.pack_forget()
        self.hundredmhz_button.pack_forget()
        self.quit_label.pack_forget()
        self.quit_button.pack_forget()

        # Create buttons to decide what to do next
        self.name_label.config(text="Initialized to 6500 MHz w/ " + Ref + "MHz Ref\n")
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

        self.sheet_label.pack()
        self.freq1_entry.pack()
        self.freq1_label.pack()
        self.freq2_entry.pack()
        self.freq2_label.pack()
        self.delay_entry.pack()
        self.delay_label.pack()
        self.sheet_button.pack()
        self.sheetPerFreq_button.pack()

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

        #go back to manin menu
        self.goBack_label.pack()
        self.goBack_button.pack()

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
        self.bypass_freq = self.freq_entry.get()  # get input from user after button push
        if int(self.bypass_freq) in self.PLLFunc.freqrange:
            self.PLLFunc.bypassautocalenable()  # enable autocal bypass mode
            self.PLLFunc.bypassautocal(int(self.bypass_freq))  # hop to requested frequency (self.bypass_freq) bypassing autocal routine
            print("Autocal Bypass Jump to", self.bypass_freq, "MHz")  # alert user to what just happened
        else:
            print("Invalid Frequency Input: ", self.bypass_freq)

        self.freq_entry.delete(0, 'end')  # clear entry field for next entry


    # Hops to arbitrary frequency using full autocal routine
    def autocal_freq_fun(self):
        self.autocal_freq = self.autocal_entry.get()  # get input from user after button push
        if int(self.autocal_freq) in self.PLLFunc.freqrange:
            self.PLLFunc.autocal_enable()  # enable autocal mode by writing to register 0
            self.PLLFunc.autocal_freq(int(self.autocal_freq))  # run autocal with freq
           # print("Autocal Freq. Jump to", self.autocal_freq, "MHz")  # print statement to alert user to what they did
            autocalHis.append(self.autocal_freq)
            print("This is the array that stores history")
            print(autocalHis)
        else:
            print("Invalid Frequency Input: ", self.autocal_freq)

        self.autocal_entry.delete(0, 'end')  # clear entry field for next entry

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
        #  load cal
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
        self.sheet_label.pack_forget()
        self.freq1_entry.pack_forget()
        self.freq1_label.pack_forget()
        self.freq2_entry.pack_forget()
        self.freq2_label.pack_forget()
        self.delay_entry.pack_forget()
        self.delay_label.pack_forget()
        self.sheet_button.pack_forget()
        self.sheetPerFreq_button.pack_forget()
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



        self.ref_label.pack()
        self.tenmhz_button.pack()
        self.hundredmhz_button.pack()
        self.quit_label.pack()
        self.quit_button.pack()
        self.goBack_label.pack_forget()
        self.goBack_button.pack_forget()




# MAIN
PLLGui = PLLGui()  # create Gui class

# GUI CODE HERE


# disconnect from aardvark
PLLGui.PLLFunc.disconnectaardvark()

