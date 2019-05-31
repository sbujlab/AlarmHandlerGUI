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

class FILE_ARRAY():
  def __init__(self,filen,delimiter):
    self.filename = filen
    self.delim = delimiter
    self.filearray = u.parse_textfile(self)

class OBJECT_LIST():
  def __init__(self,fileArray):
    self.objectList = u.create_objects(fileArray)
    self.selectedButtonColumnIndicesList = []
    self.activeObjectColumnIndicesList = [] # This stores the location where insertion will take place
    self.selectedColumnButtonLengthList = [] # This is the thing to store the number of buttons that should be displayed -> == the number of children of the parent clicked button
    for i in range(0,len(self.objectList)): # Look in the list of columns of objects, neglect final row
      self.selectedButtonColumnIndicesList.append(0) # This looks stupid because I'm being safe, initialize to the top row, first object child of each one
      self.activeObjectColumnIndicesList.append(0) # This looks stupid because I'm being safe, initialize to the top row, first object child of each one
      self.selectedColumnButtonLengthList.append(0) # Safety initialization
    for i in range(0,len(self.objectList)-1): # Look in the list of columns of objects
      for j in range(0,len(self.objectList[i])): # For all entries in the column
        for k in range(0,len(self.objectList[i+1])): # For each entry in the column to the right
          if self.objectList[i][j].columnIndex == self.objectList[i+1][k].parentIndices[i]: # If the columnIndex is the child's parent's column index, then ++ children
            self.objectList[i][j].numberChildren += 1
            #self.activeObjectColumnIndicesList[i+1]=self.objectList[i+1][k].columnIndex
    self.activeObjectColumnIndicesList[0]=self.objectList[0][len(self.objectList[0])-1].columnIndex
    for i in range(0,len(self.objectList)-1): # Look in the list of columns of objects, minus last column doesn't matter
      self.selectedColumnButtonLengthList[i+1]=self.objectList[i][self.selectedButtonColumnIndicesList[i]].numberChildren
    self.selectedColumnButtonLengthList[0] = len(self.objectList[0]) # Initialize first column length to be just the number there


  def set_clicked(self,i,j):
    self.activeObjectColumnIndicesList[i]=j
    self.selectedButtonColumnIndicesList[i]=j
    for column in range(0,len(self.objectList)):
      for obj in range(0,len(self.objectList[column])):
        if obj != self.selectedButtonColumnIndicesList[column]:
          self.objectList[column][obj].click(0)
        if column>i:
          self.objectList[column][obj].click(0)
    self.objectList[i][j].click(1)
    for ind in range(i,len(self.objectList)-1): # Look in the list of columns of objects, neglect final row
 #     print("Looking in column {}".format(ind))
      #for j in range(0,len(self.objectList[ind])): # For all entries in the column
      jNew = self.activeObjectColumnIndicesList[ind] # Entry in the column
      for k in range(0,len(self.objectList[ind+1])): # For each entry in the column to the right
 #       print("Check if self.objectList[{}][{}].columnIndex = {} == {} = self.objectList[{}][{}].parentIndices[{}]".format(ind,jNew,self.objectList[ind][jNew].columnIndex,self.objectList[ind+1][k].parentIndices[ind],ind+1,k,ind))
           #self.objectList[ind][jNew].columnIndex==self.objectList[ind+1][k].parentIndices[ind]
 #       print("{} == {}".format(self.objectList[ind][jNew].columnIndex,self.objectList[ind+1][k].parentIndices[ind]))
        if self.objectList[ind][jNew].columnIndex==self.objectList[ind+1][k].parentIndices[ind]:
 #         print("true")
          self.activeObjectColumnIndicesList[ind+1]=self.objectList[ind+1][k].columnIndex  # loop until the end of children of this active click, then the inserting goes at the end of child lists
          break
 #       print("Col index active for {} = {}:".format(ind+1,self.activeObjectColumnIndicesList[ind+1]))
    # If i+1 then take last parentIndex==columnIndex columnIndex as activeObjectIndicesList[i+1]
    if i < 4:
      for k in range(0,len(self.objectList[i+1])): # For each entry on the right
        # Take the button that was clicked and find the greatest child of it
 #       print("i+1 = {}, j = {}, k = {}".format(i+1,j,k))
        if self.objectList[i][j].columnIndex == self.objectList[i+1][k].parentIndices[i]: # Take clicked colInd, if one to right's PI[of mine] == colInd, then set it as the activeObject on right (for file appending purposes)
          self.activeObjectColumnIndicesList[i+1]=self.objectList[i+1][k].columnIndex
 #     print("Col index active for {} = {}:".format(i+1,self.activeObjectColumnIndicesList[i+1]))


class ALARM_OBJECT():
  def __init__(self):
    self.indexStart = 0
    self.indexEnd = 0
    self.column = 0
    self.columnIndex = 0
    self.parentIndices = []
    self.numberChildren = 0
    self.identifier = "NULL"
    self.value = "NULL"
    self.parameterList = []
    self.parameterListHistory = []
    self.color = u.lightgrey_color
    self.alarm_status = 0
    self.clicked = 0

  def click(self,clickStat):
    self.clicked = clickStat
    if (clickStat == 0 and self.alarm_status == 0):
      self.color = u.lightgrey_color
    if (clickStat == 1):
      self.color = u.grey_color
    if (clickStat == 0 and self.alarm_status == 1):
      self.color = u.red_button_color

  def add_parameter(self,val1,val2):
    self.parameterList.append([val1,val2])

  def add_parameter_history(self,val1,val2):
    self.parameterListHistory.append([val1,val2])
    # add a pair to a list of parameter names and values

#  def right_click_button():
    # display drop down menu with 
    #  edit entry value
    #  delete entry
    #  add new entry below this one
    #  move entry up 1
    #  move entry down 1
    #  move entry around N - user specifies N
    #  deactivate all alarms contained within or below
