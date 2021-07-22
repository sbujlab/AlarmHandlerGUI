'''
Alarm Handler GUI Revamp
Code Commissioned 2019-01-04
Code by A.J. Zec
Greyed and Alarmed by Cameron
  2019-05-28
'''

import tkinter as tk
from tkinter import ttk
import os
import webbrowser
from argparse import ArgumentParser
import csv

# Header file for data storage objects
import alarm_object
# Header file for miscellaneous file management, etc.
import utils as u
# Header file for some text dump help buttons at the bottom
import help_buttons
# Different tabs handled separately
## Expert mode tries to have a nested tree - never quite got the display settings to work perfectly
## FIXME Features that this mode has that would be good to replicate later is the ability to change groupings/labels of alarms and change any paramter name or value
import tabs.expert_alarm_handler as expert_alarm_handler
## The main alarm handler tab
import tabs.alarm_handler as alarm_handler
## Another version with all alarms displayed efficiently, but less readable info
import tabs.grid_alarm_handler as grid_alarm_handler
## A tab that only shows alarms that aren't "good" green
import tabs.active_alarm_handler as active_alarm_handler
## A tab that tracks recent alarms - FIXME needs a feature for auto-deleting old alarms rather than just getting too large
import tabs.alarm_history as alarm_history
## A tab for seeing the settings, and editing them too (FIXME requires being paused... which isn't obvious and should become a default feature)
import tabs.settings as settings
## TCP/IP software for communicating with a remove server
import bclient as bclient
## Communicating with PVDB/RCDB database - unused
#import rcdb as rcdb
import gc
from distutils.util import strtobool
# Multi-threating support
from threading import Thread, Lock


class AlarmHandler:

  def __init__(self):
    os.environ["TCL_LIBRARY"] = "/lib64/tcl8.5/"
    self.win = tk.Tk()
    self.win.title("Continuous Aggregate Monitor: Alarm Handler")
    self.win.configure(background=u.lightgrey_color)
    self.get_alarm_handler_style()
    self.delim = ','
    self.pdelim = '='

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", help="Configuration File Location", metavar="FILE", default="alarmConfig.txt")
    args = vars(parser.parse_args())
    # File array is literally an array of data with methods for reading a writing to disk
    self.conf = alarm_object.FILE_ARRAY(args['filename'],self.pdelim)

    # This method gets config data from the array
    u.parse_config(self.conf)
    # This update changes the config data for this instance of AlarmHandler (probably should be more like self.update_config(), but this works)
    u.update_config(self)

    # This is the initial get of alarm handler data from disk
    self.fileArray = alarm_object.FILE_ARRAY(self.filename,self.delim)
    if len(self.fileArray.filearray) == 0:
      print("ERROR: Null alarm input file, please resolve in configure file")
      self.quit()
    # This is the initial get of alarm handler's previous instance history data from disk
    self.HL = alarm_object.HISTORY_LIST(self.histfilename,self.delim,self.pdelim,self.timeWait)
    # This tacks on to the end of the alarm handler data and "external" alarm information - allows an online analyzer or standalone script to supplement alarms into this GUI
    if os.path.exists(self.externalFilename): # Special case for running in an external situation like Japan or camguin analysis
      self.externalFileArray = alarm_object.FILE_ARRAY(self.externalFilename,self.delim)
    else:
      self.externalFileArray = None
    # FIXME here is the instantiation into memory of alarm data
    self.OL = alarm_object.OBJECT_LIST(self.fileArray,self.cooldownLength)
    # Alarm indicator image, also serves as a sound checker and GUI refresh when clicked
    self.masterAlarmImage = tk.PhotoImage(file='ok.ppm').subsample(2)
    self.masterAlarmButton = tk.Label(self.win, image=self.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
    # This is the TCP/IP connection to the alarm sound server
    self.alarmClient = bclient.sockClient(self.remoteName)
    # Loop checks alarms
    self.alarmLoop = alarm_object.ALARM_LOOP(self)
    # Loop controls GUI refreshes
    self.alarmLoopGUI = alarm_object.ALARM_LOOP_GUI(self)
    # Loop controls sound making in the background
    self.alarmLoopMonitor = alarm_object.ALARM_LOOP_MONITOR(self)
    # Creates all GUI tabs
    self.tabs = self.create_widgets()
  
  def get_alarm_handler_style(self):
    style = ttk.Style()
    style.theme_create("alarm_handler", parent="alt", settings={
      "TNotebook": {"configure": {"background": u.lightgrey_color}},
      "TNotebook.Tab": {"configure": {"background": u.lightgrey_color}}})
    style.theme_use("alarm_handler")

  def quit(self):
    self.win.quit()
    self.win.destroy()
    exit()

  # FIXME Depreciated method (as far as I can tell)
  def update_show_alarms(self, event):
    for key in self.tabs:
      if key == "Alarm Handler" and self.OL.currentlySelectedButton != -1:
        #self.OL.selectedButtonColumnIndicesList[2]=u.recentAlarmButtons[2] # Update the currently clicked button index to the alarming one
        #self.tabs[key].select_control_buttons(self.OL,self.fileArray,self.alarmLoop,self.tabs[key].controlButtons[3]) # If you want Green Man to beep
        self.tabs[key].select_control_buttons(self.OL,self.fileArray,self.alarmLoop,self.tabs[key].controlButtons[4])
      #webbrowser.open_new(r"https://en.wikipedia.org/wiki/Green_Monster")

#    def alarm_handler_tab(self, expt_tab):
#        tab_control = ttk.Notebook(expt_tab)
#        tab_titles = [('Expert Alarm Handler', expert_alarm_handler.EXPERT_ALARM_HANDLER)]
#        for title, fn in tab_titles:
#            sub_tab = ttk.Frame(tab_control, width=800, height=600, style="My.TFrame")
#            tab_control.add(sub_tab, text=title)
#            fn(sub_tab)
#        tab_control.grid(row=0, column=0, columnspan=2)
#
#    def alarm_history_tab(self, expt_tab):
#        tab_control = ttk.Notebook(expt_tab)
#        tab_titles = [('Alarm History', alarm_history.ALARM_HISTORY)]
#        for title, fn in tab_titles:
#            sub_tab = ttk.Frame(tab_control, width=800, height=600, style="My.TFrame")
#            tab_control.add(sub_tab, text=title)
#            fn(sub_tab)
#        tab_control.grid(row=0, column=0, columnspan=2)

  def create_widgets(self):
    gui_style = ttk.Style()
    gui_style.configure('My.TButton', foreground=u.lightgrey_color)
    gui_style.configure('My.TFrame', background=u.lightgrey_color)

    tab_control = ttk.Notebook(self.win)
    #tab_titles = [('Expert Alarm Handler', self.expert_alarm_handler_tab),('Alarm History', self.alarm_history_tab)]
    #tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER),('Grid Alarm Handler', grid_alarm_handler.GRID_ALARM_HANDLER),('Expert Alarm Handler', expert_alarm_handler.EXPERT_ALARM_HANDLER),('Alarm History', alarm_history.ALARM_HISTORY)]
    if self.includeExpert == True:
      tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER),('Active Alarm Handler', active_alarm_handler.ACTIVE_ALARM_HANDLER),('Expert Alarm Handler', expert_alarm_handler.EXPERT_ALARM_HANDLER),('Alarm History', alarm_history.ALARM_HISTORY),('Settings',settings.SETTINGS)]
    elif self.showGrid == True:
      tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER),('Grid Alarm Handler', grid_alarm_handler.GRID_ALARM_HANDLER),('Active Alarm Handler', active_alarm_handler.ACTIVE_ALARM_HANDLER),('Alarm History', alarm_history.ALARM_HISTORY),('Settings',settings.SETTINGS)]
    else:
      # Default case here
      tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER),('Active Alarm Handler', active_alarm_handler.ACTIVE_ALARM_HANDLER),('Alarm History', alarm_history.ALARM_HISTORY),('Settings',settings.SETTINGS)]
    tabs = {}
    # An elaborate loop over the tabs titles and calling their instantiations and attaching to the master GUI
    for title, fn in tab_titles:
      tab = ttk.Frame(tab_control, width=10, height=20, style="My.TFrame")
      tab_control.add(tab, text=title)
      tabs[title] = fn(self,tab,self.OL,self.fileArray,self.alarmLoop,self.HL)
    tab_control.grid(row=0, column=0, columnspan=3, sticky='NSEW')
    #self.masterAlarmButton = tk.Label(self.win, image=self.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
    self.masterAlarmButton.image = self.masterAlarmImage
    self.masterAlarmButton.grid(rowspan=3, row=1, column=0, padx=5, pady=10, sticky='NESW')
    #self.masterAlarmButton.bind("<Button-1>", self.update_show_alarms)
    phys_but = help_buttons.HELP_BUTTONS()
    help_but = help_buttons.HELP_BUTTONS()
    resp_but = help_buttons.HELP_BUTTONS()

    tk.Button(self.win, text='Help', command= lambda: help_but.helpMe(self), font = ('Helvetica 16 bold'), background=u.lightgrey_color, width=18).grid(row=1, column=1, padx=15, pady=3)#, sticky=tk.N+tk.S+tk.W+tk.E)
    tk.Button(self.win, text='Response Info', command= lambda: resp_but.responseInfo(self), font = ('Helvetica 16 bold'), background=u.lightgrey_color, width=18).grid(row=2, column=1, padx=15, pady=3)#, sticky=tk.N+tk.S+tk.W+tk.E)
    tk.Button(self.win, text='Physics/Analysis', command= lambda: phys_but.physicsAnalysis(self), font = ('Helvetica 16 bold'), background=u.lightgrey_color, width=18).grid(row=3, column=1, padx=15, pady=3)#, sticky=tk.N+tk.S+tk.W+tk.E)
    tk.Button(self.win, text='QUIT', command=quit, font = ('Helvetica 24 bold'), background=u.grey_color, width=5, height=2).grid(rowspan=3, row=1, column=2, padx=10, pady=10)#, sticky='NESW')
    return tabs

# Actually calls the above methods to set the alarm handler in motion - all are on loops
alarm_handler_GUI = AlarmHandler()
Thread(alarm_handler_GUI.alarmLoopMonitor.alarm_loop_monitor(alarm_handler_GUI)).start()
Thread(alarm_handler_GUI.alarmLoop.alarm_loop(alarm_handler_GUI)).start()
Thread(alarm_handler_GUI.alarmLoopGUI.GUI_loop(alarm_handler_GUI)).start()
Thread(alarm_handler_GUI.win.mainloop()).start()
