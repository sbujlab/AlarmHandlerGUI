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
from functools import partial
import utils as u

class Callback:
  def __init__(self, func, *args, **kwargs):
    self.func = func
    self.args = args
    self.kwargs = kwargs
  def __call__(self):
    self.func(*self.args,**self.kwargs)

class ALARM_HANDLER(tk.Frame):
  def __init__(self, tab, objectList):

    self.alarm_frame = tk.LabelFrame(tab, text='Alarm Handler', background=u.lightgrey_color)
    #self.alarm_frame.grid(row=0,column=0,pady=10,padx=10,sticky='W')
    self.button_ls = []
    self.int_es = []
    self.conv_es = []
    self.dac_settings = []
    self.sample_settings = []

    self.alarmColumns = []
    self.columnTitles = ["Kinds","Channel","Type","Parameter"]
    self.columnButtons = []
    self.newText = ["New\nKind","New\nChannel","New\nType","New\nParameter"]
    self.buttons = self.initialize_buttons(objectList)

    #self.select_buttons = []
    #self.select_add_buttons = []

    self.alarm_frame.pack(padx=20,pady=20,anchor='w')

    #numberButtons = []
  def initialize_buttons(self,objectList):
    grid = []
    for i in range(0, 4):
      row = []
      self.alarmColumns.append(tk.LabelFrame(self.alarm_frame, text=self.columnTitles[i], background=u.lightgrey_color))
 #     self.columnButtons.append([])
    #  numberButtons.append(0)
      # This is a list of button functions to be added to buttons themselves
      #self.select_buttons.append([])
      #self.select_add_buttons.append(self.select_add_button(objectList,i,numberButtons[i]))
      for j in range(0,len(objectList[i])):
        # Loop over the list of objects, creating buttons
        #self.select_buttons[i].append(self.select_button(objectList,i,j))
        #self.columnButtons[i].append(tk.Button(self.alarmColumns[i], text=objectList[i][j].value, command = self.select_buttons[i][j], justify='center', background=objectList[i][j].color)) # loop over buttons
        #self.columnButtons[i].append(tk.Button(self.alarmColumns[i], text=objectList[i][j].value, command = lambda: self.select_button(objectList,i,j), justify='center', background=objectList[i][j].color)) # loop over buttons
        #self.columnButtons[i].append(tk.Button(self.alarmColumns[i], text=objectList[i][j].value, command = self.select_button(objectList), index_i = i, index_j = j, justify='center', background=objectList[i][j].color)) # loop over buttons
        butt = tk.Button(self.alarmColumns[i], text=objectList[i][j].value, justify='center', background=objectList[i][j].color) # loop over buttons
        butt.indices = (i,j)
        butt.config(command = lambda but=butt: self.select_button(objectList,but))
 #       self.columnButtons[i].append(butt) # loop over buttons
        row.append(butt)
        #self.columnButtons[i].append(tk.Button(self.alarmColumns[i], text=objectList[i][j].value, command = Callback(self.select_button, objectList[i][j]), justify='center', background=objectList[i][j].color)) # loop over buttons
    #    numberButtons[i] += 1
      # Finally add the "New Button" button
 #     self.columnButtons[i].append(tk.Button(self.alarmColumns[i], text=self.newText[i], command = lambda: self.select_add_buttons(objectList,i,j), default='active', justify='center', background=u.lightgrey_color)) # loop over buttons
 #     butt = tk.Button(self.alarmColumns[i], text=self.newText[i], command = lambda: self.select_add_buttons(objectList,i,j), default='active', justify='center', background=u.lightgrey_color)
      butt = tk.Button(self.alarmColumns[i], text=self.newText[i], default='active', justify='center', background=u.lightgrey_color)
      butt.indices = (i,len(row)-1)
      butt.config(command = lambda but=butt: self.select_add_button(objectList,but))
      row.append(butt)
 #     row.append(tk.Button(self.alarmColumns[i], text=self.newText[i], command = lambda: self.select_add_buttons(objectList,i,j), default='active', justify='center', background=u.lightgrey_color)) # loop over buttons
 #     for j in range(0,len(self.columnButtons[i])):
      for j in range(0,len(row)):
        if i==3:
 #         self.columnButtons[i][j].grid(row=j,column=i,columnspan=2,padx=10,pady=10,sticky='W')
          row[j].grid(row=j,column=i,columnspan=2,padx=10,pady=10,sticky='W')
        else:
 #         self.columnButtons[i][j].grid(row=j,column=i,padx=10,pady=10,sticky='W')
          row[j].grid(row=j,column=i,padx=10,pady=10,sticky='W')
      self.alarmColumns[i].grid(row=0,column=i,pady=10,padx=10,sticky='N')
      grid.append(row)
    return grid
    #  self.alarmColumns[i].pack(padx=20,pady=20,anchor='w')

#    i = 0
#    while i < numBUTTON:
#      self.button_ls.append(tk.Label(self.alarm_frame, text='BUTTON '+str(BUTTONlabels[i]), background=u.lightgrey_color))
#      self.int_es.append(tk.Entry(self.alarm_frame, width=3))
#      self.conv_es.append(tk.Entry(self.alarm_frame, width=3))
#      self.dac_settings.append(tk.StringVar())
#      self.sample_settings.append(tk.IntVar())
#      i += 1
      
#    labels = ['Label', 'Int', 'Conv', '-----', 'DAC', 'Settings', '-----', 'Sample by:']
#    for i, label in enumerate(labels):
#      tk.Label(self.alarm_frame, text=label, background=u.lightgrey_color).grid(
#          row=0, column=i, padx=8, pady=10, sticky='W')
    
#    self.create_table(numBUTTON)
#    self.check_values()


  #def select_button(self,objectList,coli,rowi):
  #  print(coli)
  #  print(rowi)
  #  objectList[coli][rowi].color=u.grey_color
  #  self.background=u.grey_color
  def select_button(self,objectList,but):
    i,j = but.indices
    print(i)
    print(j)
    objectList[i][j].color=u.grey_color
    self.buttons[i][j].background=u.grey_color
    #self.columnButtons[i][j].background=u.grey_color
    #but.background=u.grey_color
  
  def select_add_button(self,objectList,but):
    i,j = but.indices
    print(i)
    print(j)
    butt = tk.Button(self.alarmColumns[i], text=objectList[i][j].identifier, justify='center', background=objectList[i][j].color)
    j += 1
    butt.indices = (i,j) #FIXME get the indices right and pass/edit locations of new buttons correctly
    butt.config(command = lambda but=butt: self.select_button(objectList,but))
    self.buttons[i].append(butt)
#    self.buttons[coli].append(tk.Button(self.alarmColumns[coli], text=objectList[coli][rowi].identifier, command=lambda but=butt: self.select_button(objectList,but), justify='center', background=objectList[coli][rowi].color))
    #self.columnButtons[coli].append(tk.Button(self.alarmColumns[coli], text=objectList[coli][rowi].identifier, command=lambda: self.select_button(objectList,i,j), justify='center', background=objectList[coli][rowi].color))
    u.add_object(objectList,i)

  def add_to_columnButtons(self,columnIndex,lButton):
    self.columnButtons[columnIndex].append(lButton)

