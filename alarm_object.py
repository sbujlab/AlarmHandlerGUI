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

class ALARM_LOOP():
  def __init__(self,alarmHandlerGUI):
    self.alarmHandlerGUI = alarmHandlerGUI
    self.globalAlarmStatus = 0 # Start in non-alarmed state
    self.globalLoopStatus = 1 # Start in looping state
    
  def alarm_loop(self):
    if (self.globalLoopStatus==1):
      self.alarmHandlerGUI.win.after(10000,self.alarm_loop) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
      print("waited 10 seconds")
      #u.write_textfile(self.OL,self.fileArray)

class ALARM():
  def __init__(self,myAO):
    self.alarmName = myAO.name
    #self.runNumber = os.getenv($RUNNUM)
    self.pList = myAO.parameterList # FIXME FIXME FIXME test and prove that this is true!!! This parameterList is built out of the object's parameter list which is built out of the values of all objects, so editing them here edits them everywhere - be careful!! FIXME - to edit all of objectLists' values it may be necessary to make the constituent local objects into arrays so the pointer logic works
    self.alarmAnalysisReturn = None
    self.alarmErrorReturn = None
    self.alarmType = self.pList.get("Alarm Type",u.defaultKey)
    self.alarm_analysis = lambda myAOhere = myAO: self.do_alarm_analysis(myAOhere)
    self.alarm_evaluate = lambda myAOhere = myAO: self.do_alarm_evaluat(myAOhere)

    #subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None)
    def do_alarm_analysis(self,myAO):
      if "Camguin" in self.alarmType: # Alarm Type is the parameter (level 4 object) which keeps track of what analysis to do
        #Standard form: ./camguin.C(string "type of analysis" (rms), string "tree" (mul), string "branch" (asym_vqwk_04_0ch0), string "leaf" (hw_sum), string "cuts" (defaultCuts), int overWriteCut (0, boolean to overwrite default cuts), string "histMode" (defaultHist, doesn't rebin), int runNumber ($RUNNUM), int nRuns ($NRUNS), double data (0.0))
        subprocess("root -L camguin_C.so({},{},{},{},{},{},{},{},{},{},{})".format(self.pList["Analysis"],self.pList["Tree"],self.pList["Branch"],self.pList["Leaf"],self.pList["Cuts"],int(self.pList["Ignore Event Cuts"]),self.pList["Hist Rebinning"],int(self.pList["Stability Ring Length"]),self.runNumber,1,0.0), stdout=self.alarmAnalysisReturn, stderr=self.alarmErrorReturn, timeout=30)
        # Parse alarm return values into results and determine alarm status upadte
        # Use dictionaries to map the return string names and values into the parameter list values
        #self.do_alarm_valuate(self,myAO)

      if "Japan" in self.alarmType: # Alarm Type is the parameter (level 4 object) which keeps track of what analysis to do
        # Read the JAPAN output text file, parse each line, compare with current alarm object's dictionaries, update object's values, evaluate status, continue
        pass




        #for camguinID in u.camguinIDdict: 
        #  if camguinID in self.name:   # Name is the analysis (level 3 object) which keeps track of what the analysis will do (mean_asym_bpm, rms_diff_sams, etc..)
        #    self.camguinDict[u.camguinIDdict[camguinID]] = camguinID # i.e. if "mean" is in descriptor then 
        #if self.pList["Cuts"]:
        #  self.camguinDict["Cuts"] = self.pList["Cuts"]:
                                                                     # the "ana" dict entry == "mean" now
      #if "CODA" in self.alarmType:

#    def do_alarm_evaluate(self,myAO):

    #myAO.indexStart = 0
    #myAO.indexEnd = 0
    #myAO.column = 0
    #myAO.columnIndex = 0
    #myAO.parentIndices = []
    #myAO.numberChildren = 0
    #myAO.name = "NULL"
    #myAO.value = "NULL"
    #myAO.valueHistory = []
    #myAO.valueHistory.append(self.value)
    #myAO.parameterList = {} # Using a dictionary makes life much easier
    #myAO.parameterListHistory = {} # Every time we update parameterList pass its prior value to history ... let actually accumulating of values take place in alarmLoop if wanted...
    #myAO.color = u.lightgrey_color
    #myAO.alarmStatus = 0
    #myAO.clicked = 0


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
    self.clicked = 0

  def click(self,clickStat):
    self.clicked = clickStat
    if (clickStat == 0 and self.alarmStatus == 0):
      self.color = u.lightgrey_color
    if (clickStat == 1):
      self.color = u.grey_color
    if (clickStat == 0 and self.alarmStatus == 1):
      self.color = u.red_button_color

  def add_parameter(self,val1,val2): # Updates dictionary with new value, appends or edits appropriately, but names are the keys... so be careful
    self.parameterList[val1]=val2

  def add_parameter_history(self,val_append):
    self.parameterListHistory.append(val_append)
    # add a pair to a list of parameter names and values

