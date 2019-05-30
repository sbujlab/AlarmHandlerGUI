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

class ALARM_OBJECT():
  def __init__(self):
    self.indexStart = 0
    self.indexEnd = 0
    self.column = 0
    self.columnIndex = 0
    self.parentIndex = 0
    self.identifier = "NULL"
    self.value = "NULL"
    self.parameterList = []
    self.parameterListHistory = []
    self.color = u.lightgrey_color
    self.alarm_status = 0

  def add_parameter(self,val1,val2):
    self.parameterList.append([val1,val2])

  def add_parameter_history(self,val1,val2):
    self.parameterListHistory.append([val1,val2])
    # add a pair to a list of parameter names and values

#  def click_button():
    # based on column number and start-end indices populate the column+1 with start-end indexed buttons, then click it's button 0

#  def right_click_button():
    # display drop down menu with 
    #  edit entry value
    #  delete entry
    #  add new entry below this one
    #  move entry up 1
    #  move entry down 1
    #  move entry around N - user specifies N
    #  deactivate all alarms contained within or below
