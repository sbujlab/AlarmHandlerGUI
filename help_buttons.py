'''
Green Monster GUI Revamp
Containing VQWK Tab
Code Commissioned 2019-01-16
Code by A.J. Zec
Alarm Handler GUI 
Cameron Clarke 2019-05-28
'''

import tkinter as tk
from tkinter import ttk
import utils as u
import bclient as bclient
import os
import time
from decimal import Decimal

class HELP_BUTTONS():
  def __init__(self):
    self.displays = {}
    pass

  def display(self, but):
    for key, value in self.displays.items():
      if value != None:
        value.grid_forget()
    for eachLabel in self.displays.get(but['text'],u.defaultKey).winfo_children():
      eachLabel.grid(columnspan=len(self.displays), sticky='NSEW')
    self.displays.get(but['text'],u.defaultKey).grid(columnspan=len(self.displays), sticky='NSEW')

  def helpMe(self,alarmHandlerGUI):
    # Method for helping to use the alarm handler
    window = tk.Toplevel(alarmHandlerGUI.win)
    helpFrame = tk.LabelFrame(window, text='Information to Aid in Alarm Response for PREXII/CREX', background=u.grey_color)
    helpFrame.grid(column=0, row=0, sticky='NSEW')
    helpHandler = tk.LabelFrame(helpFrame, text='Alarm Handler', bg=u.lightgrey_color)
    self.displays["Alarm Handler"] = helpHandler
    alarm_handler_str = "The Experimental Alarm Handler is a Python GUI. The purpose of this alarm handler is to interface with the various data collection, analysis, and display programs that are in use during the experiment. We expect that this GUI should be run in the background at all times, and that whenever an alarm is activated a sound will play on speakers and the GUI will display a red indicator for the alarm that went off. \n\nThe user is responsible for finding the tripped alarm in question and using this GUI to find out the nature of the alarm and assess the situation."
    alarm_handler_main_page_str = "Upon opening the Alarm Handler, the user is greeted with the front page, featuring under all-clear circumstances a happy green thumbs up, and in alarming circumstances a red alarm indicator. \n\nThe main page features several columns of alarm status indicators, these have the name, category, and type of alarm indicated, along with a status indicator and a button whose text is the value of the analysis/tracked quantity. \n\nThe key features are the status indicator and the nature of the button. Clicking the button brings the alarm handler's focus onto that alarm. The button has a right click context menu (which requires continuous pressing to keep it from vanishing, contrary to normal context menu behavior), whose options are to open an information panelfor, \"Acknowledge\", or \"Silence\" the alarm in question (which doesn't have to be the one currently in focus). The status indicator has 4 states: OK, Alarmed, Acknowledged and cooling down, and Silenced. The status indicator also serves as a button for the purpose of acknowledging an alarm or un-silencing."
    alarm_handler_button_details_str = "The Status Indicator is intended to instantly convey the relevant information of the given alarm. \n\n - Red indicates that the alarm has been tripped, and the box will display the alarm status (High, Low, Exactly, etc.) in this case.\n\n - - While Red, the status indicator serves as a button for acknowledging the alarm. When clicked, the alarm will be acknowledgedand a cooldown period will begin in which the alarm status won't affect the global Alarm Status and the Orange cooldown indicator will be activated. \n\n - Green indicates that the alarm is ok. \n\n - - While Green, the status indicator serves as a button for refreshing the screen (but not the alarm statuses). This isn't particularly functional, but it may be useful in some circumstances. \n\n - Yellow indicates that the alarm has been silenced by the user and cannot generate further alarms until unsilenced. \n\n - - While Yellow, the status indicator serves as a button for un-silencing. When clicked, the alarm will resume its normal alarm checking routine. \n\n - Orange indicates that the alarm has been acknowledged and that a cooldown period has begun. During this cooldown period the alarm status will not affect the Global Alarm status, primarily for the convenience of the user. \n\n - - While Orange, the status indicator will also display the approximate number of seconds until the cooldown is complete and the alarm is un-acknowledged. Also the indicator will serve as a button to manually un-acknowledge the alarm and turn back on its alarm-checking routine."
    tk.Label(helpHandler, text="Alarm Handler", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(helpHandler, text=alarm_handler_str, wraplength=500, justify='left')
    tk.Label(helpHandler, text="\"Alarm Handler\": Main Page Functionality", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(helpHandler, text=alarm_handler_main_page_str, wraplength=500, justify='left')
    tk.Label(helpHandler, text="Status Indicator Functionality", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(helpHandler, text=alarm_handler_button_details_str, wraplength=500, justify='left')

    mainBut = tk.Button(helpFrame, text="Alarm Handler", justify='center')
    mainBut.config(command=lambda but=mainBut: self.display(but))
    mainBut.grid(row=0,column=0,padx=5,pady=5)
    tk.Button(window, text="Close", command=window.destroy).grid(row=1,column=0,padx=5,pady=5)

  def responseInfo(self,alarmHandlerGUI):
    # Method for helping respond to alarms in alarm handler
    window = tk.Toplevel(alarmHandlerGUI.win)
    responseFrame = tk.LabelFrame(window, text='Information to Aid in Alarm Response for PREXII/CREX', background=u.grey_color)
    responseFrame.grid(column=0, row=0, sticky='NSEW')

    responseHall = tk.LabelFrame(responseFrame, text='Hall A Alarms', bg=u.lightgrey_color)
    self.displays["Hall A Alarms"] = responseHall
    hall_str = "Hall A has many systems, most of which have useful components logged in the EPICS slow logging system. This Alarm Handler is able to read from JLab's EPICS database and perform alarm checks on the results. \n\nIn the event of a Hall A alarm going off, please start diagnosing the issue with more advanced GUIs and EPICS information by using the camera to visually inspect the Hall, pulling up an instance of the Hall A General Tools GUI, and by going to the PREX Wiki Shift Checklist, section Beam and Hall Checks."
    hall_mag_str = "Hall A relies on high reliability from the magnets in its two High Resolution Spectrometers (HRSs) to precisely resolve specific scattered momentum (to 10-4 precision) and the PREX Septum magnet to bring the lowest angle scattered electrons (~5 degrees) into the acceptance of the HRSs \n\nHall A's magnets are rather old at this point and the radiation field generated by our low energy beam on large nuclei will cause many single event upsets (radiation flipping a bit somewhere inside a magnet control or monitoring computer) and superconducting magnet trips. \n\nWe want to avoid damaging these magnets at all costs, repair them the moment something goes wrong, and to never accidentally take data with any incorrect or disabled magnet settings. It is the job of the shift crew to regularly monitor the magnet momentum, field, and current set and read-back points and to verify that the values match those needed by the experiment. \n\nThis Alarm Handler will keep track of the specific values we want to use to set these magnets, but it is not a substitute for proper care and attention."
    tk.Label(responseHall, text="Hall A", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(responseHall, text=hall_str, wraplength=500, justify='left')
    tk.Label(responseHall, text="Hall A Magnets", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(responseHall, text=hall_mag_str, wraplength=500, justify='left')

    responseBMW = tk.LabelFrame(responseFrame, text='Beam Modulation Alarms', bg=u.lightgrey_color)
    self.displays["Beam Modulation Alarms"] = responseBMW
    bmw_str = "Parity Experiments rely on a process called \"Dithering\" or \"Beam Modulation\" (often abbreviated as BMW) to measure helicity correlated asymmetries coming from beam energy, motion, and current fluctuations. \n\nThe idea behind BMW is to modulate the beam intentionally and at a larger amplitude than normal fluctuations occur at, in order to measure the response slopes more precisely so they can be applied to the normal fluctuation data and used to subract those spurious signals out of our physics asymmetry measurement."
    bmw_soft_str = "Because of the critical importance for our analysis of removing helicity correlated beam noise it is imperitive that out Beam Modulation system is always running (it physically modulates modulation coils in the Hall A arc region of the accelerator and wiggles the beam for a few seconds out of every few minutes) and is properly communicating with the DAQ and MCC/OPS systems. \n\nWe have several alarms in place to verify that our system is communicating with theirs, but you should still be careful to check the online analysis plots to verify that the BMW system is producing the signals that we expect (see Physics/Analysis help screen for more information on what you should expect in the plots)."
    tk.Label(responseBMW, text="Beam Modulation", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(responseBMW, text=bmw_str, wraplength=500, justify='left')
    tk.Label(responseBMW, text="Beam Modulation Software", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(responseBMW, text=bmw_soft_str, wraplength=500, justify='left')

    responseJAPAN = tk.LabelFrame(responseFrame, text='Parity Alarms', bg=u.lightgrey_color)
    self.displays["Parity Alarms"] = responseJAPAN
    japan_str = "PREXII/CREX have many components in the injector devoted to ensuring our beam is of high enough quality to perform a parity violation measurement, and they have an analyzer (Called JAPAN, Just ANother PArity aNalyzer) which is capable of running in an online mode, attaching to the CODA Event Transfer (ET) system and analyzing the data quickly on the fly. \n\nIt is imperitive for our Parity Quality Beam efforts, which maintain low beam current and position asymmetries, that our anaylzer is able to read the data quickly and instantly provide Fast Feedback information to the Accelerator for tuning their parameters." 
    japan_soft_str = "In addition to using JAPAN for monitoring the settings and beam parameters in the injector, beam, and hall, we also have a set of programs in place to launch the online anaylzer, produce plots from it for visual diagnostics, and to provide the feedback information for the Accelerator. We can also use this Alarm Handler to interface with JAPAN's own alarm system and respond to non-ideal conditions, either with analyzed data or with the status of the programs mentioned before. \n\nIt is your job as a shift worker to keep track of these programs and analysis results and to get things back online or to alert experts or the RC if systems cease working. Please see the Physics/Analysis help screen for more information on interpreting alarms. This Alarm Handler will serve as a tool for helping you do this, but it should not substitute for direct care and attention."
    tk.Label(responseJAPAN, text="JAPAN Analyzer", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(responseJAPAN, text=japan_str, wraplength=500, justify='left')
    tk.Label(responseJAPAN, text="Analysis Software", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(responseJAPAN, text=japan_soft_str, wraplength=500, justify='left')

    responseDAQ = tk.LabelFrame(responseFrame, text='DAQ Alarms', bg=u.lightgrey_color)
    self.displays["DAQ Alarms"] = responseDAQ
    daq_str = "In addition to keeping track of the JAPAN analysis results and the programs responsible for producing and responding to it (see Parity Alarms), we also use JAPAN analysis results and various Linux programs to ensure that our Data Acquisition software and hardware are operating correctly. \n\nIt is your job as a shift worker to ensure that the DAQs are running, taking data correctly, and if anything goes wrong in the DAQ, online analysis, or in the programs and hardware responsible for the DAQ, to notify the expert and RC to get it fixed as quickly as possible."
    tk.Label(responseDAQ, text="DAQ", wraplength = 500, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(responseDAQ, text=daq_str, wraplength=500, justify='left')

    hallBut = tk.Button(responseFrame, text="Hall A Alarms", justify='center')
    hallBut.config(command=lambda but=hallBut: self.display(but))
    hallBut.grid(row=0,column=0,padx=5,pady=5)
    bmwBut = tk.Button(responseFrame, text="Beam Modulation Alarms", justify='center')
    bmwBut.config(command=lambda but=bmwBut: self.display(but))
    bmwBut.grid(row=0,column=1,padx=5,pady=5)
    japanBut = tk.Button(responseFrame, text="Parity Alarms", justify='center')
    japanBut.config(command=lambda but=japanBut: self.display(but))
    japanBut.grid(row=0,column=2,padx=5,pady=5)
    daqBut = tk.Button(responseFrame, text="DAQ Alarms", justify='center')
    daqBut.config(command=lambda but=daqBut: self.display(but))
    daqBut.grid(row=0,column=3,padx=5,pady=5)

    tk.Button(window, text="Close", justify='center', command=window.destroy).grid(row=1,column=0,padx=5,pady=5)

  def physicsAnalysis(self,alarmHandlerGUI):
    # Method for helping to use the alarm handler
    window = tk.Toplevel(alarmHandlerGUI.win)
    label_str = "Help Text"
    tk.Label(window, text=label_str, wraplength=500).grid(row=0,column=0,padx=5,pady=5)
    tk.Button(window, text="Close", command=window.destroy).grid(row=1,column=0,padx=5,pady=5)


