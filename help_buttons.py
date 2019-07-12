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
    helpFrame = tk.LabelFrame(window, text='How-to: Alarm Handler GUI and Alarm Loop', background=u.grey_color)
    helpFrame.grid(column=0, row=0, sticky='NSEW')

    helpHandler = tk.LabelFrame(helpFrame, text='Alarm Handler - Main Tab', bg=u.lightgrey_color)
    self.displays["Alarm Handler - Main Tab"] = helpHandler
    alarm_handler_str = "The Experimental Alarm Handler is a Python GUI. The purpose of this alarm handler is to interface with the various data collection, analysis, and display programs that are in use during the experiment. We expect that this GUI should be run in the background at all times, and that whenever an alarm is activated a sound will play on speakers and the GUI will display a red indicator for the alarm that went off. \n\nThe user is responsible for finding the tripped alarm in question and using this GUI to find out the nature of the alarm and assess the situation."
    alarm_handler_main_page_str = "Upon opening the Alarm Handler, the user is greeted with the front page, featuring under all-clear circumstances a happy green thumbs up, and in alarming circumstances a red alarm indicator. \n\nThe main page features several columns of alarm status indicators, these have the name, category, and type of alarm indicated, along with a status indicator and a button whose text is the value of the analysis/tracked quantity. \n\nThe key features are the status indicator and the nature of the button. Clicking the button brings the alarm handler's focus onto that alarm. The button has a right click context menu (which requires continuous pressing to keep it from vanishing, contrary to normal context menu behavior), whose options are to open an information panelfor, \"Acknowledge\", or \"Silence\" the alarm in question (which doesn't have to be the one currently in focus). The status indicator has 4 states: OK, Alarmed, Acknowledged and cooling down, and Silenced. The status indicator also serves as a button for the purpose of acknowledging an alarm or un-silencing."
    alarm_handler_button_details_str = "The Status Indicator is intended to instantly convey the relevant information of the given alarm. \n\n - Red: indicates that the alarm has been tripped, and the box will display the alarm status (High, Low, Exactly, etc.) in this case.\n - - While Red, the status indicator serves as a button for acknowledging the alarm. When clicked, the alarm will be acknowledgedand a cooldown period will begin in which the alarm status won't affect the global Alarm Status and the Orange cooldown indicator will be activated. \n - Green: indicates that the alarm is ok. \n - - While Green, the status indicator serves as a button for refreshing the screen (but not the alarm statuses). This isn't particularly functional, but it may be useful in some circumstances. \n - Yellow: indicates that the alarm has been silenced by the user and cannot generate further alarms until unsilenced. \n - - While Yellow, the status indicator will display in text the underlying alarm status that has been silenced, and it serves as a button for un-silencing. When clicked, the alarm will resume its normal alarm checking routine. \n - Orange: indicates that the alarm has been acknowledged and that a cooldown period has begun. During this cooldown period the alarm status will not affect the Global Alarm status, primarily for the convenience of the user. \n - - While Orange, the status indicator will also display the approximate number of seconds until the cooldown is complete and the alarm is un-acknowledged. Also the indicator will serve as a button to manually un-acknowledge the alarm and turn back on its alarm-checking routine."
    alarm_parameters_str = "Another of the right-click context menu options is \"Information\", to display that alarm's information. The alarm parameters will be displayed in a white background box to the right of the existing GUI. This parameter display can be removed/deactivated by clicking the \"Reset GUI\" button on the top right control buttons bar."
    alarm_control_buttons_str = "Along the top of the Alarm Handler are 4 control buttons. These allow the user some control over the internal parameters of the program. \n\n - Alarm Status/Find Alarm: indicates the current alarm status through its color. \nIt can be either \"OK\" == Green, \"Silenced\" or \"Paused\" == Yellow, or \"Alarmed\" == Red. \nClicking on this button will  bring the most recently triggered alarm into focus. \n - Alarm Checker/Turn Off (On): displays the current status of the alarm loop - when it is Yellow that means the alarm loop is paused, otherwise the loop is active. \nClicking on this button will toggle the alarm loop status, and the lower line of text indicates what you will do by clicking it. \nNote that the alarm loop is discretized into N seconds, where N is user defined, default = 10 seconds. \n - Silencer/Turn On (Off): will silence the Global Alarm status entirely off and make the GUI effectively deactivated, but it will continue to perform the alarm checking loop and upadting the displayed values. \nWhen silenced this button and the Alarm Status button will both turn yellow as an indicator to the user. \n - Reset GUI: serves as a refresh button for the GUI. It does not affect the alarm loop, but it will re-poll the GUI's underlying text-file memory storage and reset all values to match what is contained within. \n\nPlease note that it is not safe to try to make any edits to the alarm parameters using the pop-up dialog boxes in expert mode or the underlying text-file while the alarm loop is active, as those changes will be overwritten by the alarms status storing stage of the alarm loop itself. Similarly it is not safe to run two instances of the Alarm Handler without pointing them to separate alarm.csv memory files, to avoid write/read clashes."
    tk.Label(helpHandler, text="Alarm Handler", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(helpHandler, text=alarm_handler_str, wraplength=1100, justify='left')
    tk.Label(helpHandler, text="\"Alarm Handler\": Main Page Functionality", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(helpHandler, text=alarm_handler_main_page_str, wraplength=1100, justify='left')
    tk.Label(helpHandler, text="Status Indicator Functionality", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(helpHandler, text=alarm_handler_button_details_str, wraplength=1100, justify='left')
    tk.Label(helpHandler, text="Parameter List Side Bar", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(helpHandler, text=alarm_parameters_str, wraplength=1100, justify='left')
    tk.Label(helpHandler, text="Control Buttons Top Bar", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(helpHandler, text=alarm_control_buttons_str, wraplength=1100, justify='left')

    typeHandler = tk.LabelFrame(helpFrame, text='Alarm Category Definitions', bg=u.lightgrey_color)
    self.displays["Alarm Category Definitions"] = typeHandler

    alarm_type_general_str = "The underlying data format for the Alarm Handler is a text file CSV that encodes the alarm's parameters along with some organizational heirarchichal book-keeping. An example is shown below.\n\nThe purpose of including the organizational heirarchy is two-fold. First it is designed to enable organizing similar kinds of alarms into groups, and to simplify the control over responding to, editing, and generating new groups of alarms in the Expert Alarm Handler page. Secondly it is utilized (externally) to store the channel map information for the JAPAN PREXII/CREX analysis alarm handler, and can be used similarly for other extensions as well. \n\nThe alarm parameters (which live in the 5th column of the 2D CSV file) are the information and control points for the Alarm Handler's alarm loop rountine. The alarm loop will parse the list of parameters as it goes through its chain of possible kinds of alarm analyses to perform. \n\nAfter the alarm loop routine has been performed and the information has been updated it will be stored back in the original alarm memory file, overwriting the previous alarm data. User actions, such as silencing or acknowledging an alarm, will also trigger the write process, allowing those parameter changes to be stored and kept track of as well."
    alarm_kind_type_channel_str = "The alarm categorization can be optimally utilized at 1st order (the first column) by separating different knids of alarms into groups of either similar \"Kinds\" of value checks (Magnet Currents, analysis measurement read-backs, DAQ status, etc.) or similar \"Kinds\" of techniques of checking them (EPICS, JAPAN analysis, System Calls, etc.). \n\nCategorization at 2nd order can be separated into \"Channels\", where the categories of things to be checked in each \"Kind\" can be listed (a list of beam line monitors, for example). \n\nCategorization at 3rd order should lastly be separated into \"Types\", which will be the \"Alarm\" definitions themselves. As it is simply a tier of alarm categorization, each Type/Alarm gets exactly 1 parameter to be checked and compared to expectation parametersi. \nIt is likely that one \"Kind\"->\"Channel\" could have multiple different \"Types\" of Alarms for it, given different running conditions (in which case the innactive alarm could be silenced temporarily) or for comparing different types of checks (for example, widths, yields, or asymmetry means for a single detector, or multiple diagnostic parameters for a beamline magnet)."
    alarm_example_csv_str = "An example of what the alarms look like in the CSV file used to generate the alarms is given here: \n\nHall A,Beam,Beam Energy,Alarm Status,OK\nHall A,Beam,Beam Energy,HighHigh,960\nHall A,Beam,Beam Energy,High,951\nHall A,Beam,Beam Energy,Value,950.397\nHall A,Beam,Beam Energy,Low,949\nHall A,Beam,Beam Energy,LowLow,940\nHall A,Beam,Beam Energy,Alarm Type,EPICS\nHall A,Beam,Beam Energy,Variable Name,HALLA:p\nHall A,Beam,Beam Energy,User Silence Status,Alert\nHall A,Beam,Beam Energy,User Notify Status,OK"

    tk.Label(typeHandler, text="Alarm File Definitions", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(typeHandler, text=alarm_type_general_str, wraplength=1100, justify='left')
    tk.Label(typeHandler, text="Categorization Options", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(typeHandler, text=alarm_kind_type_channel_str, wraplength=1100, justify='left')
    tk.Label(typeHandler, text="Example CSV Alarm Memory File", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(typeHandler, text=alarm_example_csv_str, wraplength=1100, justify='left')

    paramHandler = tk.LabelFrame(helpFrame, text='Alarm Parameter Definitions', bg=u.lightgrey_color)
    self.displays["Alarm Parameter Definitions"] = paramHandler

    alarm_default_params_str = "The default needed parameters in order to function as an alarm are: \n - Value: where the result of obtaining the raw data to be analyzed and compared to alarm limits is stored and updated and checked from. \n - Alarm Status: where the resultant status generated by the alarm looping routine is stored. This is the information that is used to determine the local and global alarm statuses and is used to communicate the situation to the user. \n\n - - An alarm status of \"OK\" means everything is fine, and otherwise the alarm status takes on the name of the violated limit (so if an alarm is low, the alarm status will read \"Low\", or if it fails the exactly == cut then it will read \"Exactly\") \n\n - - Technically the Alarm Status parameter is optional, and if it is left out then the alarm handler will not perform any alarm routine at all, and this \"alarm\" functions as a simple value indicator (which may be useful for difficult to pin down parameters or for things that are nice to know (like injector slow control settings and things for checklist checking) but that don't need alarms put on them. \n - Alarm Type: the flag that tells the alarm loop routine which mode to use for obtaining the fresh raw values. This parameter is currently limited to \"EPICS\" and \"External\". \n\n - - External refers to using an additional alarm CSV file to read the alarm information from. External files should not contain any user parameters, as this Alarm Handler does not edit the external file and always updates its internal values with what it finds in the externals. The only external file currently in use is from the Online Analysis instance of JAPAN running on apar@adaq1."
    alarm_kinds_of_limits_str = "Currently implemented in the Alarm Handler are several forms of value checks. The code allows for comparing a value against other values and determining if the raw value in question is outside of bounds. The supported limit parameters are: \n - Low: checks that the value isn't lower than this number \n - High: \"\" but higher \n - LowLow: \"\" identically, but it gives the user additional information about how significant the violation was \n - HighHigh: \"\" the same but high. And not that the alarm status will latch, meaning the most recent non-\"OK\" alarm status will persist until the user Acknowledges the status, so having distinctions like this can be useful  \n - Exactly: checks whether the raw value == the given number exactly (and the alarm status will say exactly if this isn't true, because the value is exactly not this number). Because Python is highly extensible, this \"Exactly\" value can actually be any object at all and is not limited to doubles (EPICS string outputs are particularly useful for this) \n - Difference High or Low: This is a kind of alarm that checks a \"Difference Reference Value\" determined by an EPICs \"Difference Reference Variable Name\" and then compares the difference of the \"Value\" of the alarm EPICs variable to the High or Low value given here \n - Case and Double Case: These are reference EPICs variables that are checked to establish which of the Low, High, Exactly, etc. alarm limits should be utilized. The return value of the EPICs call to \"Case Variable Name\" goes into \"Case Value\" and is used as the string appended to the Low, High, Exactly, etc. name to be chosen from \n\n Additionally, in the JAPAN Alarm handler analysis there are two more parameters, Ring-Length and Tolerance, which respectively represent the number of events that the analyzer will remember the alarm violations status of, and how many violations of the alarm status within that time frame it takes in order to set the alarm status to alarmed, or to cool down and reset to \"OK\". \n\n In CODA/RCND/RCDB type alarms there is a parameter to store the current Parity DAQ run number, which is used to obtain RCDB data about the current CODA run. The time since last CODA run start is computed by the alarm handler itself and is in Epoch time (which can be hard to read, but is easy to convert)"
    alarm_user_params_str = "Lastly, there are several parameters which are entirely optional, but which give significant control over the alarm reporting to the user: \n - User Silence Status: gives the status (\"Alert\" or \"Silenced\") that the user has set for a given alarm. Without these parameters to serve as status storage the independent alarm silence status will not persist from one instance of the loop to the next. \n - User Notify Status: used to store (similarly to silence status) whether or not the user has recently acknowledged the alarm state. \n - - If the user has then this parameter will take on a \"Cooldown\" status, which is the word cooldown plus the number of seconds remaining in the cooldown. \n - - If the user has not acknowldeged the status then this will latch onto the most recent non-\"OK\" alarm status and remember it until the alarm is acknowledged. This alarm acknowledge status is exactly the parameter used to determine the alarm indicator and Global Alarm status, so it actually is necessary for proper functioning of the Alarm Handler (though that can be changed if really needed)"
    tk.Label(paramHandler, text="Baseline Parameter Definitions", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(paramHandler, text=alarm_default_params_str, wraplength=1100, justify='left')
    tk.Label(paramHandler, text="Alarm Limit Parameter Definitions", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(paramHandler, text=alarm_kinds_of_limits_str, wraplength=1100, justify='left')
    tk.Label(paramHandler, text="User Interaction Parameter Definitions", wraplength = 1100, justify='center', font=('Helvetica 12 bold')) 
    tk.Label(paramHandler, text=alarm_user_params_str, wraplength=1100, justify='left')


    mainBut = tk.Button(helpFrame, text="Alarm Handler - Main Tab", justify='center')
    mainBut.config(command=lambda but=mainBut: self.display(but))
    mainBut.grid(row=0,column=0,padx=5,pady=5)
    typeBut = tk.Button(helpFrame, text="Alarm Category Definitions", justify='center')
    typeBut.config(command=lambda but=typeBut: self.display(but))
    typeBut.grid(row=0,column=1,padx=5,pady=5)
    paramBut = tk.Button(helpFrame, text="Alarm Parameter Definitions", justify='center')
    paramBut.config(command=lambda but=paramBut: self.display(but))
    paramBut.grid(row=0,column=2,padx=5,pady=5)
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


