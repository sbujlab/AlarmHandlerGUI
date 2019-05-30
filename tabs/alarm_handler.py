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
  def __init__(self, tab, OL):

    self.alarmFrame = tk.LabelFrame(tab, text='Alarm Handler', background=u.lightgrey_color)
    self.alarmColumns = []
    self.columnTitles = ["Kinds","Channel","Type","Parameter"]
    self.columnButtons = []
    self.newText = ["New\nKind","New\nChannel","New\nType","New\nParameter"]
    self.buttons = self.initialize_buttons(OL)
    self.alarmFrame.pack(padx=20,pady=20,anchor='w')

  def initialize_buttons(self,OL):
    grid = []
    for i in range(0, 4):
      row = []
      self.alarmColumns.append(tk.LabelFrame(self.alarmFrame, text=self.columnTitles[i], background=u.lightgrey_color))
      # First add the "New Button" button
      newButt = tk.Button(self.alarmColumns[i], text=self.newText[i], default='active', justify='center', background=u.lightgrey_color)
      newButt.indices = (i,len(row))
      newButt.config(command = lambda newBut=newButt: self.select_add_button(OL,newBut))
      #row.append(newButt)
      # end new button button, this can just as easily go at the end of the below for
      if len(OL.objectList)>(i):
        for j in range(0,len(OL.objectList[i])):
          # Loop over the list of objects, creating buttons
          butt = tk.Button(self.alarmColumns[i], text=OL.objectList[i][j].value, justify='center', background=OL.objectList[i][j].color) # loop over buttons
          butt.indices = (i,j)
          butt.config(command = lambda but=butt: self.select_button(OL,but))
          row.append(butt)
      if i==3:
        newButt.grid(row=0,column=i,columnspan=2,padx=10,pady=10,sticky='N')
        for j in range(0,len(row)):
          row[j].grid(row=j+1,column=i,columnspan=2,padx=10,pady=10,sticky='N')
      else:
        newButt.grid(row=0,column=i,padx=10,pady=10,sticky='N')
        for j in range(0,len(row)):
          row[j].grid(row=j+1,column=i,padx=10,pady=10,sticky='N')
      self.alarmColumns[i].grid(row=0,column=i,pady=10,padx=10,sticky='N')
      grid.append(row)
    return grid

  def select_button(self,OL,but):
    i,j = but.indices
    print(i)
    print(j)
    OL.objectList[i][j].color=u.grey_color
    self.buttons[i][j].config(background=u.grey_color) # Equivalent to using just but.confi....
    OL.selectedButtonColumnIndices[i]=j

  def select_add_button(self,OL,but):
    i,j = but.indices
    j = len(self.buttons[i]) #- 1 
    print(i)
    print(j)
    u.add_object(OL,i)
    butt = tk.Button(self.alarmColumns[i], text=OL.objectList[i][j].identifier, justify='center', background=OL.objectList[i][j].color)
    butt.indices = (i,j) #FIXME get the indices right and pass/edit locations of new buttons correctly
    butt.config(command = lambda butte=butt: self.select_button(OL,butte))
    self.buttons[i].append(butt)
    if i==3:
      self.buttons[i][j].grid(row=j+1,column=i,columnspan=2,pady=10,padx=10,sticky='N')
    else:
      self.buttons[i][j].grid(row=j+1,column=i,pady=10,padx=10,sticky='N')
    self.alarmColumns[i].grid(row=0,column=i,pady=10,padx=10,sticky='N')
    self.alarmFrame.pack(padx=20,pady=20,anchor='w')

  def add_to_columnButtons(self,columnIndex,lButton):
    self.columnButtons[columnIndex].append(lButton)

