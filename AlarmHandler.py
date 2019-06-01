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
    self.bm_test_setting = tk.StringVar()
    self.clean_setting = tk.StringVar()
    self.get_alarm_handler_style()
    self.filename = "/adaqfs/home/apar/bin/alarm.csv"
    self.delim = ','
    self.fileArray = alarm_object.FILE_ARRAY(self.filename,self.delim)
    # u.parse_textfile(self.filename,self.delim)
    self.OL = alarm_object.OBJECT_LIST(self.fileArray)
    #self.objectList = u.create_objects(self.fileArray) 
    #self.create_objects()
    self.fGlobalAlarmStatus = 0 # Start in non-alarmed state
    self.fGlobalLoopStatus = 1 # Start in looping state
    self.create_widgets()
    #self.alarm_loop()
  
  def alarm_loop(self):
    if (self.fGlobalLoopStatus==1):
      #self.win.after(1000,print("waited 1 seconds"))
      self.win.after(10000,self.alarm_loop)
      print("waited 10 seconds")
      #for i in range(0,5):
      #  print("new column")
      #  for j in range(0,len(self.OL.objectList[i])):
      #    print(self.OL.objectList[i][j].value)
      #print(self.OL.objectList[len(self.OL.objectList)-2][len(self.OL.objectList[len(self.OL.objectList)-2])-1].value)
      #print(self.OL.objectList[len(self.OL.objectList)-2][len(self.OL.objectList[len(self.OL.objectList)-2])-1].parentIndices)
      u.write_textfile(self.OL,self.fileArray)
    # Loop over the global objectData and call data updating methods

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

  def educate_yourself(self, event):
    webbrowser.open_new(r"https://en.wikipedia.org/wiki/Green_Monster")

#    def alarm_handler_tab(self, expt_tab):
#        tab_control = ttk.Notebook(expt_tab)
#        tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER)]
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
    #tab_titles = [('Alarm Handler', self.alarm_handler_tab),('Alarm History', self.alarm_history_tab)]
    tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER),('Alarm History', alarm_history.ALARM_HISTORY)]
    for title, fn in tab_titles:
      tab = ttk.Frame(tab_control, width=800, height=600, style="My.TFrame")
      tab_control.add(tab, text=title)
      fn(self.win,tab,self.OL,self.fileArray)
    tab_control.grid(row=0, column=0, columnspan=2)
    fenway = tk.PhotoImage(file='gm.ppm')
    fenway_pahk = tk.Label(self.win, image=fenway, cursor="hand2", bg=u.lightgrey_color)
    fenway_pahk.image = fenway
    fenway_pahk.grid(row=1, column=0, padx=5, pady=10, sticky='SW')
    fenway_pahk.bind("<Button-1>", self.educate_yourself)
    tk.Button(self.win, text='QUIT', command=quit, background=u.lightgrey_color, width=15, height=3).grid(
      row=1, column=1, padx=15, pady=5, sticky='SE')

alarm_handler_GUI = AlarmHandler()
alarm_handler_GUI.alarm_loop()
alarm_handler_GUI.win.mainloop()
