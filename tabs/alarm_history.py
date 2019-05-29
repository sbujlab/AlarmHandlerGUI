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
import utils as u

ALARM_GET_NUMBUTTON	=1001
ALARM_GET_LABEL		=1002
ALARM_GET_CSR		=1003
ALARM_SET_CONV		=1004
ALARM_SET_INT		=1005
ALARM_SET_PED		=1006
ALARM_GET_CONV		=1007
ALARM_GET_INT		=1008
ALARM_GET_PED		=1009
ALARM_SET_DAC		=1010
ALARM_GET_DAC		=1011
ALARM_SET_SAMP		=1012
ALARM_GET_SAMP		=1013
GA_MAXBUTTON		=20
DACRADIO18		=100
GM_BUTTON_GET		=101
GM_BUTTON_SET		=201
DACTRI			=0
DACSAW			=1
DACCONST		=2
DACOFF18		=3

class ALARM_HISTORY(tk.Frame):
  def __init__(self, tab):
    global numBUTTON
    numBUTTON = self.get_num_button()
    BUTTONlabels = []

    i = 0
    while i < numBUTTON:
      BUTTONlabels.append(self.get_label_button(i))
      i += 1

    self.ch_frame = tk.LabelFrame(tab, text='CH', background=u.lightgrey_color)
    self.button_ls = []
    self.int_es = []
    self.conv_es = []
    self.dac_settings = []
    self.sample_settings = []

    i = 0
    while i < numBUTTON:
      self.button_ls.append(tk.Label(self.ch_frame, text='BUTTON '+str(BUTTONlabels[i]), background=u.lightgrey_color))
      self.int_es.append(tk.Entry(self.ch_frame, width=3))
      self.conv_es.append(tk.Entry(self.ch_frame, width=3))
      self.dac_settings.append(tk.StringVar())
      self.sample_settings.append(tk.IntVar())
      i += 1
      
    labels = ['Label', 'Int', 'Conv', '-----', 'DAC', 'Settings', '-----', 'Sample by:']
    for i, label in enumerate(labels):
      tk.Label(self.ch_frame, text=label, background=u.lightgrey_color).grid(
          row=0, column=i, padx=8, pady=10, sticky='W')
    
    self.create_table(numBUTTON)
    self.check_values()

  def get_num_button(self):
    packet = [u.COMMAND_ALARM, ALARM_GET_NUMBUTTON, 0, 0, 0, "BUTTON Get Number", "Y"]
    err_flag, reply = u.send_command(u.Crate_CH, packet)

    if err_flag == u.SOCK_OK:
      return int(reply[3])

    else:
      print("ERROR, Could not access socket.")
      return -1

  def get_label_button(self, index):
    packet = [u.COMMAND_ALARM, ALARM_GET_LABEL, index, 0, 0, "BUTTON Get Label", "Y"]
    err_flag, reply = u.send_command(u.Crate_CH, packet)
    
    if err_flag == u.SOCK_OK:
      return int(reply[3])

    else:
      print("ERROR, Could not access socket.")
      return -1
    
    
  def create_table(self, value):
    for i in range(1, value+1):
      self.button_ls[i-1].grid(row=i, column=0, padx=10, pady=10, sticky='W')
      u.set_text(self.int_es[i-1], '3').grid(row=i, column=1, padx=10, pady=10)
      u.set_text(self.conv_es[i-1], '0').grid(row=i, column=2, padx=10, pady=10)
      setting = self.dac_settings[i-1]
      settings = ['Tri', 'Saw', 'Const', 'Off']
      setting.set('Tri')
      for j,s in enumerate(settings):
        tk.Radiobutton(self.ch_frame, text=s, variable=setting, value=s, background=u.lightgrey_color).grid(
          row=i, column=j+3, padx=5, pady=10, sticky='W')
      sample_by = self.sample_settings[i-1]
      sample_by.set(1)
      tk.OptionMenu(self.ch_frame, sample_by, 1, 2, 4, 8).grid(row=i, column=7)
    tk.Button(self.ch_frame, text='Get Settings', background=u.lightgrey_color, command=self.check_values).grid(
        row=6, column=1, columnspan=2, pady=50, sticky='S')
    tk.Button(self.ch_frame, text='Apply Settings', background=u.lightgrey_color, command=self.set_values).grid(
        row=6, column=3, columnspan=2, pady=50, sticky='S')
    tk.Button(self.ch_frame, text='Cancel', background=u.lightgrey_color, command=self.check_values).grid(
        row=6, column=5, pady=50, sticky='S')
    self.ch_frame.pack(padx=20, pady=20)

  def check_values(self):
    fSample = []
    fIntGain = []
    fConvGain = []
    fDAC = []
    value = numBUTTON

    i = 0
    while i < value:
      packet = [u.COMMAND_ALARM, ALARM_GET_SAMP, i, 0, 0, "ALARM Get Sample", "Y"]
      err_flag, reply = u.send_command(u.Crate_CH, packet)
    
      if err_flag == u.SOCK_OK:
        fSample.append(reply[3])
        self.sample_settings[i].set(reply[3])

      else:
        print("ERROR, Could not access socket.")
        return -1

      packet = [u.COMMAND_ALARM, ALARM_GET_INT, i, 0, 0, "ALARM Get Int", "Y"]
      err_flag, reply = u.send_command(u.Crate_CH, packet)
    
      if err_flag == u.SOCK_OK:
        fIntGain.append(reply[3])
        self.int_es[i].delete(0, tk.END)
        self.int_es[i].insert(0, str(reply[3]))

      else:
        print("ERROR, Could not access socket.")
        return -1

      packet = [u.COMMAND_ALARM, ALARM_GET_CONV, i, 0, 0, "ALARM Get Conv", "Y"]
      err_flag, reply = u.send_command(u.Crate_CH, packet)
    
      if err_flag == u.SOCK_OK:
        fConvGain.append(reply[3])
        self.conv_es[i].delete(0, tk.END)
        self.conv_es[i].insert(0, str(reply[3]))

      else:
        print("ERROR, Could not access socket.")
        return -1

      packet = [u.COMMAND_ALARM, ALARM_GET_DAC, i, 0, 0, "ALARM Get DAC", "Y"]
      err_flag, reply = u.send_command(u.Crate_CH, packet)
    
      if err_flag == u.SOCK_OK:
        fDAC.append(reply[3])
        if reply[3] == DACSAW:
          self.dac_settings[i].set('Saw')
        elif reply[3] == DACCONST:
          self.dac_settings[i].set('Const')
        elif reply[3] == DACTRI:
          self.dac_settings[i].set('Tri')
        else:
          self.dac_settings[i].set('Off')

      else:
        print("ERROR, Could not access socket.")
        return -1
      i += 1

  def set_values(self):
    fSample = []
    fIntGain = []
    fConvGain = []
    fDAC = []
    value = numBUTTON

    i = 0
    while i < value:
      fIntGain.append(int(self.int_es[i].get()))

      if fIntGain[i] < 0 or fIntGain[i] > 3:
        print("ERROR: Int Value is out of range! Try (0-3)...")
      else:
        packet = [u.COMMAND_ALARM, ALARM_SET_INT, i, fIntGain[i], 0, "ALARM Set Int", "Y"]
        err_flag, reply = u.send_command(u.Crate_CH, packet)
      
        if err_flag == u.SOCK_OK:
          pass
        else:
          print("ERROR, Could not access socket.")
          return -1

      fConvGain.append(int(self.conv_es[i].get()))

      if fConvGain[i] < 0 or fConvGain[i] > 15:
        print("ERROR: Conv Value is out of range! Try (0-15)...")
      else:
        packet = [u.COMMAND_ALARM, ALARM_SET_CONV, i, fConvGain[i], 0, "ALARM Set Conv", "Y"]
        err_flag, reply = u.send_command(u.Crate_CH, packet)
       
        if err_flag == u.SOCK_OK:
          pass
        else:
          print("ERROR, Could not access socket.")
          return -1
      
      fDAC.append(self.dac_settings[i].get())

      if fDAC[i]=='Tri':
        dacflag = DACTRI
      elif fDAC[i]=='Saw':
        dacflag = DACSAW
      elif fDAC[i] == 'Const':
        dacflag = DACCONST
      else:
        dacflag = DACOFF18

      packet = [u.COMMAND_ALARM, ALARM_SET_DAC, i, dacflag, 0, "ALARM Set DAC", "Y"]
      err_flag, reply = u.send_command(u.Crate_CH, packet)
       
      if err_flag == u.SOCK_OK:
        pass
      else:
        print("ERROR, Could not access socket.")
        return -1

      fSample.append(int(self.sample_settings[i].get()))

      packet = [u.COMMAND_ALARM, ALARM_SET_SAMP, i, fSample[i], 0, "ALARM Set Sample", "Y"]
      err_flag, reply = u.send_command(u.Crate_CH, packet)
      
      if err_flag == u.SOCK_OK:
        pass
      else:
        print("ERROR, Could not access socket.")
        return -1
      i += 1

    self.check_values()
