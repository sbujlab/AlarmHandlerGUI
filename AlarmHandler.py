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

import csv
import alarm_object
import tabs.expert_alarm_handler as expert_alarm_handler
import tabs.alarm_handler as alarm_handler
import tabs.alarm_history as alarm_history
import utils as u


class AlarmHandler:

  def __init__(self):
    os.environ["TCL_LIBRARY"] = "/lib64/tcl8.5/"
    self.win = tk.Tk()
    self.win.title("Continuous Aggregate Monitor: Alarm Handler")
    self.win.configure(background=u.lightgrey_color)
    self.adc_options_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
    self.get_alarm_handler_style()
    self.filename = "/adaqfs/home/apar/alarms/alarm.csv" # FIXME this should eventually be pushed into the config file read by default main program at runtime
    self.externalFilename = "/adaqfs/home/apar/alarms/japanAlarms.csv"
    self.delim = ','
    self.fileArray = alarm_object.FILE_ARRAY(self.filename,self.delim)
    if os.path.exists(self.externalFilename): # Special case for running in an external situation like Japan or camguin analysis
      self.externalFileArray = alarm_object.FILE_ARRAY(self.externalFilename,self.delim)
    else:
      self.externalFileArray = None
    self.OL = alarm_object.OBJECT_LIST(self.fileArray)
    self.masterAlarmImage = tk.PhotoImage(file='ok.ppm')
    self.masterAlarmButton = tk.Label(self.win, image=self.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
    self.alarmLoop = alarm_object.ALARM_LOOP(self)
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
      if key != "Alarm History":
        self.tabs[key].select_control_buttons(self.OL,self.fileArray,self.alarmLoop,self.tabs[key].controlButtons[0])
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
    tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER),('Expert Alarm Handler', expert_alarm_handler.EXPERT_ALARM_HANDLER),('Alarm History', alarm_history.ALARM_HISTORY)]
    tabs = {}
    for title, fn in tab_titles:
      tab = ttk.Frame(tab_control, width=800, height=600, style="My.TFrame")
      tab_control.add(tab, text=title)
      tabs[title] = fn(self.win,tab,self.OL,self.fileArray,self.alarmLoop)
    tab_control.grid(row=0, column=0, columnspan=2)
    #self.masterAlarmButton = tk.Label(self.win, image=self.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
    self.masterAlarmButton.image = self.masterAlarmImage
    self.masterAlarmButton.grid(row=1, column=0, padx=5, pady=10, sticky='SW')
    self.masterAlarmButton.bind("<Button-1>", self.update_show_alarms)
    tk.Button(self.win, text='QUIT', command=quit, background=u.lightgrey_color, width=15, height=3).grid(
      row=1, column=1, padx=15, pady=5, sticky='SE')
    return tabs

alarm_handler_GUI = AlarmHandler()
alarm_handler_GUI.alarmLoop.alarm_loop(alarm_handler_GUI)
alarm_handler_GUI.win.mainloop()
