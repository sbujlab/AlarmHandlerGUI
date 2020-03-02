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
    self.buttons = []
    self.buttons = self.display_settings_list(alarmHandlerWindow)
    self.make_screen()

  def make_screen(self):
    self.erase_settingsFrame()
    self.settingsFrame.grid(column=0, row=1, sticky='NW')
    for k in range(0,len(self.buttons)):
      self.buttons[k].grid(row=k,column=0,padx=5,pady=2,sticky='W')
      self.buttons[k].button.grid(row=0,column=0,padx=5,pady=2,sticky='W')

  def update_settings(self,alarmHandlerWindow):
    for k in range(0,len(self.buttons)):
      self.buttons[k].button.config(text=alarmHandlerWindow.conf.conf[self.buttons[k].button.key])

  def erase_settingsFrame(self):
    for k in range(0,len(self.buttons)):
      self.buttons[k].grid_forget()
      self.buttons[k].button.grid_forget()
    self.settingsFrame.grid_forget()

  def display_settings_list(self,alarmHandlerWindow):
    self.erase_settingsFrame()
    lgrid = []
    print(alarmHandlerWindow.conf.conf)
    localSlist = alarmHandlerWindow.conf.conf
    #self.settingsFrame.pack(padx=20,pady=20,anchor='nw')
    self.settingsFrame.grid(column=0,row=0,sticky='NW')
    k = 0
    for key in localSlist.keys():
      disp = tk.LabelFrame(self.settingsFrame, text=key, font=('Helvetica 8'), background=u.lightgrey_color) 
      #disp.button = tk.Label(self.settingsFrame, text=localSlist[key], background=u.lightgrey_color)
      lgrid.append(disp)
      lgrid[k].button = tk.Button(lgrid[k], text=localSlist[key], background=u.lightgrey_color)
      lgrid[k].button.index = k
      lgrid[k].button.key = key
      lgrid[k].button.config(command = lambda but=lgrid[k].button: self.edit_setting(but,alarmHandlerWindow.conf.conf,alarmHandlerWindow))
      lgrid[k].grid(row=k,column=0,padx=5,pady=2,sticky='W')
      lgrid[k].button.grid(row=0,column=0,padx=5,pady=2,sticky='W')
      k+=1
    return lgrid

  def edit_setting(self,but,conf,alarmHandlerWindow):
    lk = but.index
    key = but.key
    localStr = simpledialog.askstring("Input", "New setting value: ",parent = self.buttons[lk]) 
    conf[key] = localStr
    u.write_conf(conf)
    self.buttons[lk].button.config(text = localStr)
    print(conf)
    self.update_settings(alarmHandlerWindow)
    #self.make_screen()
    
  def refresh_screen(self,alarmHandlerWindow):
    u.update_config(alarmHandlerWindow)
    self.update_settings(alarmHandlerWindow)
    #self.make_screen()

