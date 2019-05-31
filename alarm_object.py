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

class OBJECT_LIST():
  def __init__(self,filearray):
    self.objectList = u.create_objects(filearray)
    self.selectedButtonColumnIndicesList = []
    for i in range(0,len(self.objectList)):
      self.selectedButtonColumnIndicesList.append(0) # This looks stupid because I'm being safe
      #self.selectedButtonColumnIndicesList.append(len(self.objectList[i])-1) # This looks stupid because I'm being safe

  def set_clicked(self,i,j):
    self.selectedButtonColumnIndicesList[i]=j
    for column in range(0,len(self.objectList)):
      for row in range(0,len(self.objectList[column])):
        if row != self.selectedButtonColumnIndicesList[column]:
          self.objectList[column][row].click(0)
    self.objectList[i][j].click(1)



class ALARM_OBJECT():
  def __init__(self):
    self.indexStart = 0
    self.indexEnd = 0
    self.column = 0
    self.columnIndex = 0
    self.parentIndices = []
    self.identifier = "NULL"
    self.value = "NULL"
    self.parameterList = []
    self.parameterListHistory = []
    self.color = u.lightgrey_color
    self.alarm_status = 0
    self.clicked = 0

  def click(self,stat):
    self.clicked = stat
    if (stat == 0 and self.alarm_status == 0):
      self.color = u.lightgrey_color
    if (stat == 1):
      self.color = u.grey_color
    if (self.alarm_status == 1):
      self.color = u.red_button_color

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
