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
import alarm_object
import help_buttons
import tabs.expert_alarm_handler as expert_alarm_handler
import tabs.alarm_handler as alarm_handler
import tabs.grid_alarm_handler as grid_alarm_handler
import tabs.active_alarm_handler as active_alarm_handler
import tabs.alarm_history as alarm_history
import tabs.settings as settings
import utils as u
import bclient as bclient
import rcdb as rcdb
from distutils.util import strtobool
from threading import Thread, Lock


class AlarmHandler:

  def __init__(self):
    os.environ["TCL_LIBRARY"] = "/lib64/tcl8.5/"
    self.win = tk.Tk()
    self.win.title("Continuous Aggregate Monitor: Alarm Handler")
    self.win.configure(background=u.lightergrey_color)
    self.get_alarm_handler_style()
    self.delim = ','
    self.pdelim = '='

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", help="Configuration File Location", metavar="FILE", default="/adaqfs/home/apar/alarms/alarmConfig.txt")
    args = vars(parser.parse_args())
    self.conf = alarm_object.FILE_ARRAY(args['filename'],self.pdelim)

    u.parse_config(self.conf)
    u.update_config(self)

    self.fileArray = alarm_object.FILE_ARRAY(self.filename,self.delim)
    self.HL = alarm_object.HISTORY_LIST(self.histfilename,self.delim,self.pdelim,self.timeWait)
    if os.path.exists(self.externalFilename): # Special case for running in an external situation like Japan or camguin analysis
      self.externalFileArray = alarm_object.FILE_ARRAY(self.externalFilename,self.delim)
    else:
      self.externalFileArray = None
    self.OL = alarm_object.OBJECT_LIST(self.fileArray,self.cooldownLength)
    self.masterAlarmImage = tk.PhotoImage(file='ok.ppm').subsample(2)
    self.masterAlarmButton = tk.Label(self.win, image=self.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
    self.alarmClient = bclient.sockClient(self.remoteName)
    self.alarmLoop = alarm_object.ALARM_LOOP(self)
    self.alarmLoopGUI = alarm_object.ALARM_LOOP_GUI(self)
    self.alarmLoopMonitor = alarm_object.ALARM_LOOP_MONITOR(self)
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

  def update_show_alarms(self, event):
    for key in self.tabs:
      if key != "Alarm History" and key!= "Active Alarm Handler" and self.OL.currentlySelectedButton != -1:
        #self.OL.selectedButtonColumnIndicesList[2]=u.recentAlarmButtons[2] # Update the currently clicked button index to the alarming one
        self.tabs[key].select_control_buttons(self.OL,self.fileArray,self.alarmLoop,self.tabs[key].controlButtons[3])
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
      tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER),('Active Alarm Handler', active_alarm_handler.ACTIVE_ALARM_HANDLER),('Alarm History', alarm_history.ALARM_HISTORY),('Settings',settings.SETTINGS)]
    tabs = {}
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

alarm_handler_GUI = AlarmHandler()
Thread(alarm_handler_GUI.alarmLoopMonitor.alarm_loop_monitor(alarm_handler_GUI)).start()
Thread(alarm_handler_GUI.alarmLoop.alarm_loop(alarm_handler_GUI)).start()
Thread(alarm_handler_GUI.alarmLoopGUI.GUI_loop(alarm_handler_GUI)).start()
Thread(alarm_handler_GUI.win.mainloop()).start()
