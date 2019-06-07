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
import os
from decimal import Decimal

# EPICS
import logging
import rcdb
import subprocess
import socket
from datetime import datetime

class ALARM_LOOP():
  def __init__(self,alarmHandlerGUI):
    self.alarmList = []
    for i in range(0,len(alarmHandlerGUI.OL.objectList[2])):
      self.alarmList.append(alarmHandlerGUI.OL.objectList[2][i].alarm)
    print("Initializing, adding alarm list pList = {}".format(alarmHandlerGUI.OL.objectList[2][i].alarm.pList))
    self.globalAlarmStatus = "OK" # Start in non-alarmed state
    self.globalLoopStatus = True # Start in looping state
    self.globalUserAlarmSilence = False
    #self.alarm_loop(alarmHandlerGUI)
    #  self.win.after(10000,self.alarm_loop)
    #  print("waited 10 seconds")
    
  def alarm_loop(self,alarmHandlerGUI):
    if (self.globalLoopStatus==True):
      print("waited 10 seconds, analyzing alarms")
      for i in range (0,len(self.alarmList)):
        print("Loop, column index {} for i = {}".format(alarmHandlerGUI.OL.objectList[2][i].columnIndex,i)) # BREAKS HERE FIXME
        print("Before: pList value for \"Value\" updated to be {}".format(self.alarmList[i].pList))
        print("Before: pList value for \"Value\" updated to be {}".format(self.alarmList[i].pList.get("Value",u.defaultKey)))
        #alarmHandlerGUI.OL.objectList[2][i].alarm.alarm_analysis()
        #alarmHandlerGUI.OL.objectList[2][i].alarm.alarm_evaluate()
        self.alarmList[i].alarm_analysis()
        self.alarmList[i].alarm_evaluate()
        print("After: pList value for \"Value\" updated to be {}".format(self.alarmList[i].pList.get("Value",u.defaultKey)))
        print("After: Parameter list value for \"Value\" updated to be {}".format(self.alarmList[i].pList.get("Value",u.defaultKey)))
        for k in range(0,len(alarmHandlerGUI.OL.objectList[4])):
          print("Values of parameters in objects updated to be: {}".format(alarmHandlerGUI.OL.objectList[4][k].value)) 
        #alarmHandlerGUI.OL.objectList[2][i].alarm.do_alarm_analysis(alarmHandlerGUI.OL.objectList[2][i])
        #alarmHandlerGUI.OL.objectList[2][i].alarm.do_alarm_evaluate(alarmHandlerGUI.OL.objectList[2][i])
      u.update_objectList(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,self.alarmList)
      u.write_textfile(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray) #FIXME Do this here?
      if alarmHandlerGUI.tabs.get("Alarm Handler",u.defaultKey) != u.defaultKey:
        print("1 The selected buttons are indexed globally as {}".format(alarmHandlerGUI.OL.selectedButtonColumnIndicesList))
        alarmHandlerGUI.tabs["Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray)
        print("2 The selected buttons are indexed globally as {}".format(alarmHandlerGUI.OL.selectedButtonColumnIndicesList))
      alarmHandlerGUI.win.after(10000,self.alarm_loop, alarmHandlerGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
    if (self.globalLoopStatus==False):
      alarmHandlerGUI.win.after(10000,self.alarm_loop, alarmHanderGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
      print("waited 10 seconds to try again")

class ALARM():
  def __init__(self,myAO):
    #self.alarmName = myAO.name
    #self.runNumber = os.getenv($RUNNUM)
    self.pList = myAO.parameterList # FIXME FIXME FIXME test and prove that this is true!!! This parameterList is built out of the object's parameter list which is built out of the values of all objects, so editing them here edits them everywhere - be careful!! FIXME - to edit all of objectLists' values it may be necessary to make the constituent local objects into arrays so the pointer logic works
    print("Initializing: pList = {}".format(self.pList))
    self.alarmAnalysisReturn = None
    self.alarmErrorReturn = None
    self.alarmType = self.pList.get("Alarm Type",u.defaultKey)
    self.alarmEvaluateType = "Exists" # Default alarm criteria is whether the value is not-null and otherwise is defined on context from given parameterList entries
    # Do I need to make a lambda initialized instance of the alarm action per event? I don't think this matters like it did for button context menu placements.... especially since these actions are being taken by the alarm handler in a loop over objectList
    print("Initializing new alarm for object {} {}, name = {}".format(myAO.column,myAO.columnIndex,myAO.name+" "+myAO.value))
    self.alarm_analysis = lambda myAOhere = myAO: self.do_alarm_analysis(myAOhere)
    self.alarm_evaluate = lambda myAOhere = myAO: self.do_alarm_evaluate(myAOhere) # Just keep this stub here in case

    #subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None)
  def do_alarm_analysis(self,myAO):
    print("Trying alarm analysis for object {} {}, name = {}, = {}".format(myAO.column,myAO.columnIndex,myAO.name+" "+myAO.value,self.pList))
    if "Camguin" in self.alarmType: # Alarm Type is the parameter (level 4 object) which keeps track of what analysis to do
      #Standard form: ./camguin.C(string "type of analysis" (rms), string "tree" (mul), string "branch" (asym_vqwk_04_0ch0), string "leaf" (hw_sum), string "cuts" (defaultCuts), int overWriteCut (0, boolean to overwrite default cuts), string "histMode" (defaultHist, doesn't rebin), int runNumber ($RUNNUM), int nRuns ($NRUNS), double data (0.0))
      subprocess("root -L camguin_C.so({},{},{},{},{},{},{},{},{},{},{})".format(self.pList["Analysis"],self.pList["Tree"],self.pList["Branch"],self.pList["Leaf"],self.pList["Cuts"],int(self.pList["Ignore Event Cuts"]),self.pList["Hist Rebinning"],int(self.pList["Stability Ring Length"]),self.runNumber,1,0.0), stdout=self.alarmAnalysisReturn, stderr=self.alarmErrorReturn, timeout=30)
      # Parse alarm return values into results and determine alarm status upadte
      # Use dictionaries to map the return string names and values into the parameter list values
      #self.do_alarm_valuate(self,myAO)

    if "EPICS" in self.alarmType:
      if self.pList.get("Variable Name"):
        cmds = ['caget', '-t', self.pList["Variable Name"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful #FIXME
        print("EPICS: Doing alarm analysis for object {} {}, name = {}".format(myAO.column,myAO.columnIndex,myAO.name+" "+myAO.value))
        print("The epics output for variable {} is {}".format(self.pList["Variable Name"],cond_out))
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.pList["Variable Name"]))
          cond_out = "NULL"
        self.pList["Value"] = cond_out
        print("Parameter list value for \"Value\" updated to be {}".format(self.pList["Value"]))
      else: # User didn't have "Value" in their parameter list, add it and make it init to NULL
        self.pList["Variable Name"] = "NULL"
        self.pList["Value"] = "NULL"
      print("Parameter list value for \"Value\" updated to be {}".format(self.pList["Value"]))

      #self.do_alarm_evaluate(myAO)

    if "Japan" in self.alarmType: # Alarm Type is the parameter (level 4 object) which keeps track of what analysis to do
      # Read the JAPAN output text file, parse each line, compare with current alarm object's dictionaries, update object's values, evaluate status, continue
      pass

  def do_alarm_evaluate(self,myAO):
    # Consider making a candidate list of possible key words, but for now stick to hard-coded names... 
    print("Updating: pList = {}".format(self.pList))
    val = self.pList.get("Value",u.defaultKey)
    lowlow = self.pList.get("Low Low",u.defaultKey)
    low = self.pList.get("Low",u.defaultKey)
    high = self.pList.get("High",u.defaultKey)
    highhigh = self.pList.get("High High",u.defaultKey)
    if not u.is_number(str(val)): # Then we are not dealing with a number alarm - for now just return false
      print("ERROR: Assume alarms values can only be numbers for now")
      return "Invalid"
    else:
      val = Decimal(self.pList.get("Value",u.defaultKey))
      if u.is_number(str(lowlow)): # And now check the other ones too
        lowlow = Decimal(self.pList.get("Low Low",u.defaultKey))
      if u.is_number(str(low)):
        low = Decimal(self.pList.get("Low",u.defaultKey))
      if u.is_number(str(high)):
        high = Decimal(self.pList.get("High",u.defaultKey))
      if u.is_number(str(highhigh)):
        highhigh = Decimal(self.pList.get("High High",u.defaultKey))
    if lowlow != "NULL" or low != "NULL" or high != "NULL" or highhigh != "NULL":
      if lowlow != "NULL" and low != "NULL" and high != "NULL" and highhigh != "NULL":
        self.alarmEvaluateType = "Soft and Hard"
        if val != "NULL":
          if val > highhigh:
            self.pList["Alarm Status"] = "High High"
          if val > high:
            self.pList["Alarm Status"] = "High"
          if val < low:
            self.pList["Alarm Status"] = "Low"
          if val < lowlow:
            self.pList["Alarm Status"] = "Low Low"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
      if lowlow != "NULL" and low != "NULL" and high == "NULL" and highhigh == "NULL":
        self.alarmEvaluateType = "Hard"
        if val != "NULL":
          if val > highhigh:
            self.pList["Alarm Status"] = "High High"
          if val < lowlow:
            self.pList["Alarm Status"] = "Low Low"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
      if lowlow == "NULL" and low != "NULL" and high != "NULL" and highhigh == "NULL":
        self.alarmEvaluateType = "Soft"
        if val != "NULL":
          if val > high:
            self.pList["Alarm Status"] = "High"
          if val < low:
            self.pList["Alarm Status"] = "Low"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
      if lowlow == "NULL" and low == "NULL" and high != "NULL" and highhigh == "NULL":
        self.alarmEvaluateType = "High"
        if val != "NULL":
          if val > high:
            self.pList["Alarm Status"] = "High"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
      if lowlow == "NULL" and low != "NULL" and high == "NULL" and highhigh == "NULL":
        self.alarmEvaluateType = "Low"
        if val != "NULL":
          if val < low:
            self.pList["Alarm Status"] = "Low"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
      if lowlow == "NULL" and low == "NULL" and high == "NULL" and highhigh != "NULL":
        self.alarmEvaluateType = "High Hard"
        if val != "NULL":
          if val > highhigh:
            self.pList["Alarm Status"] = "High High"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
      if lowlow != "NULL" and low == "NULL" and high == "NULL" and highhigh == "NULL":
        self.alarmEvaluateType = "Low Hard"
        if val != "NULL":
          if val < lowlow:
            self.pList["Alarm Status"] = "Low Low"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
      if lowlow == "NULL" and low == "NULL" and high != "NULL" and highhigh != "NULL":
        self.alarmEvaluateType = "High Soft and High Hard"
        if val != "NULL":
          if val > highhigh:
            self.pList["Alarm Status"] = "High High"
          if val > high:
            self.pList["Alarm Status"] = "High"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
      if lowlow != "NULL" and low != "NULL" and high == "NULL" and highhigh == "NULL":
        self.alarmEvaluateType = "Low Soft and Low Hard"
        if val != "NULL":
          if val < low:
            self.pList["Alarm Status"] = "Low"
          if val < lowlow:
            self.pList["Alarm Status"] = "Low Low"
          else:
            self.pList["Alarm Status"] = "OK"
        else:
          self.pList["Alarm Status"] = "Invalid"
    print("Updated: pList = {}".format(self.pList))
    if self.pList.get("Alarm Status",u.defaultKey) != "OK" and self.pList.get("Alarm Status",u.defaultKey) != "Invalid" and self.pList.get("Alarm Status",u.defaultKey) != "NULL": # Update global alarm status unless NULL or invalid
      return "Not OK"
    else:
      return "OK"

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
      self.selectedButtonColumnIndicesList.append(-1) # This looks stupid because I'm being safe, initialize to the top row, first object child of each one
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
      #jNew = self.selectedButtonColumnIndices[ind] # Entry in the column
      jNew = self.activeObjectColumnIndicesList[ind] # Entry in the column
      for k in range(0,len(self.objectList[ind+1])): # For each entry in the column to the right
        if self.objectList[ind][jNew].columnIndex==self.objectList[ind+1][k].parentIndices[ind]:
          self.activeObjectColumnIndicesList[ind+1]=self.objectList[ind+1][k].columnIndex  # loop until the end of children of this active click, then the inserting goes at the end of child lists
          break
    # If i+1 then take last parentIndex==columnIndex columnIndex as activeObjectIndicesList[i+1]
    if i < 4:
      for k in range(0,len(self.objectList[i+1])): # For each entry on the right
        # Take the button that was clicked and find the greatest child of it
        if self.objectList[i][j].columnIndex == self.objectList[i+1][k].parentIndices[i]: # Take clicked colInd, if one to right's PI[of mine] == colInd, then set it as the activeObject on right (for file appending purposes)
          self.activeObjectColumnIndicesList[i+1]=self.objectList[i+1][k].columnIndex

class ALARM_OBJECT():
  def __init__(self):
    self.indexStart = 0
    self.indexEnd = 0
    self.column = 0
    self.columnIndex = 0
    self.parentIndices = []
    self.numberChildren = 0
    self.name = "NULL"
    self.value = "NULL"
    self.valueHistory = []
    self.valueHistory.append(self.value)
    self.parameterList = {} # Using a dictionary makes life much easier
    self.parameterListHistory = [] # Every time we update parameterList pass its prior value to history ... let actually accumulating of values take place in alarmLoop if wanted...
    self.color = u.lightgrey_color
    self.alarmStatus = 0
    self.alarm = lambda: ALARM(self);
    self.clicked = 0

  def click(self,clickStat):
    self.clicked = clickStat
    if (clickStat == 0 and self.alarmStatus == 0):
      self.color = u.lightgrey_color
    if (clickStat == 1):
      self.color = u.grey_color
    if (clickStat == 0 and self.alarmStatus == 1):
      self.color = u.red_button_color

  def add_parameter(self,obj1,obj2): # Updates dictionary with new value, appends or edits appropriately, but names are the keys... so be careful
    self.parameterList[obj1.value]=obj2.value

  def add_parameter_history(self,val_append):
    self.parameterListHistory.append(val_append)
    # add a pair to a list of parameter names and values

