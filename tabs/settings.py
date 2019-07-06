
'''
Green Monster GUI Revamp
Containing ADC18s Tab
Code Commissioned 2019-01-16
Code by A.J. Zec
Alarm Handler GUI Update
Cameron Clarke 2019-05-28
'''

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import utils as u

class SETTINGS(tk.Frame):
  def __init__(self, alarmHandlerWindow, tab, OL, fileArray, alarmLoop, HL):
    self.settingsFrame = tk.LabelFrame(tab, text='Settings', background=u.lightgrey_color)
    self.disp = []
    self.display_settings_list(alarmHandlerWindow)
    self.make_screen(alarmHandlerWindow)

  def make_screen(self,alarmHandlerWindow):
    self.settingsFrame.grid_forget()
    self.settingsFrame.grid(column=0, row=1, sticky='NW')

  def erase_settingsFrame(self):
    for k in range(0,len(self.disp)):
      self.disp[k].grid_forget()
    self.settingsFrame.grid_forget()

  def display_settings_list(self,alarmHandlerWindow):
    self.erase_settingsFrame()
    self.disp = []
    print(alarmHandlerWindow.conf)
    print(alarmHandlerWindow.conf.conf)
    localSlist = alarmHandlerWindow.conf.conf
    #self.settingsFrame.pack(padx=20,pady=10,anchor='nw')
    self.settingsFrame.grid(column=0,row=0,sticky='NW')
    k = 0
    for key in localSlist.keys():
      self.disp.append(tk.Label(self.settingsFrame, text="{} = {}".format(key, localSlist[key]), background=u.lightgrey_color)) 
      self.disp[k].grid(row=k,column=0,padx=5,pady=5,sticky='W')
      k+=1

  def refresh_screen(self,alarmHandlerWindow):
    self.make_screen(alarmHandlerWindow)

