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
import bclient as bclient
import os
import time
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
    #print("Initializing, adding alarm list pList = {}".format(alarmHandlerGUI.OL.objectList[2][i].alarm.pList))
    self.globalAlarmStatus = "OK" # Start in non-alarmed state
    self.checkExternalStatus = True # Check the externalAlarms.csv file
    self.globalLoopStatus = "Looping" # Start in looping state
    self.globalUserAlarmSilence = "Alert"
    self.userNotifyLoop = USER_NOTIFY(self)
    self.userNotifyLoop.user_notify_loop(self,alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI)
    
  def ok_notify_check(self,checkNotifyStatus):
    checkedStat = "OK"
    if checkNotifyStatus != "OK":
      if checkNotifyStatus.split(' ')[0] == "Cooldown":
        #print("Checked if we are in a countdown, we are, status = {}".format(checkNotifyStatus))
        checkedStat = "OK"
      else:
        #print("Checked if we are in a countdown, we are not, status = {}".format(checkNotifyStatus))
        checkedStat = checkNotifyStatus
    return checkedStat

  def ok_notify_update(checkNotifyStatus,reduction):
    checkedStat = "OK"
    if checkNotifyStatus != "OK":
      tmpCheck = checkNotifyStatus.split(' ')
      if tmpCheck[0] == "Cooldown":
        if tmpCheck[1] != '':
          checkedStat = "Cooldown {}".format(int(tmpCheck[1])-reduction)
        if int(tmpCheck[1]) <= reduction:
          checkedStat = "OK" # Reset
      else:
        checkedStat = checkNotifyStatus
    return checkedStat
  
  def reset_alarmList(self,OL):
    self.alarmList = []
    for i in range(0,len(OL.objectList[2])):
      self.alarmList.append(OL.objectList[2][i].alarm)
      #print("Updated alarm lists == {}".format(self.alarmList[i].pList))

  def alarm_loop(self,alarmHandlerGUI):
    if (self.globalLoopStatus=="Looping"):
      print("Waited 10 seconds, analyzing alarms")
      if os.path.exists(alarmHandlerGUI.externalFilename) and self.checkExternalStatus == True and (time.time() - os.path.getmtime(alarmHandlerGUI.externalFilename)) < 300000: # 5 minute wait time for external to update FIXME paramter file
        #print("Adding External alarms from {}".format(alarmHandlerGUI.externalFileArray.filename))
        u.update_extra_filearray(alarmHandlerGUI.fileArray,alarmHandlerGUI.externalFileArray)
        alarmHandlerGUI.OL.objectList = u.create_objects(alarmHandlerGUI.fileArray,alarmHandlerGUI.OL.cooldownLength)
        self.reset_alarmList(alarmHandlerGUI.OL)
        u.write_textfile(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray) #FIXME Do this here?
      else:
        print("No extra alarm files found")
      localStat = "OK"
      for i in range (0,len(self.alarmList)):
        self.alarmList[i].alarm_analysis()
        self.alarmList[i].alarm_evaluate()
        # Check if the alarm is alarming and has not been "OK"ed by the user acknowledge
        #print("Checking alarm {} alarm status = {}, silence status = {}, and user acknowledge = {}".format(i,self.alarmList[i].alarmSelfStatus,self.alarmList[i].userSilenceSelfStatus,self.ok_notify_check(self.alarmList[i].userNotifySelfStatus)))
        # If the userNotifyStatus is NULL (i.e. not set) then the alarm handler will just read it and move on with its life
        if self.ok_notify_check(self.alarmList[i].userNotifySelfStatus) != "OK" and self.alarmList[i].userSilenceSelfStatus == "Alert":
          # Just let the method I wrote take care of determining global alarm status
          self.globalAlarmStatus = self.alarmList[i].userNotifySelfStatus
          localStat = self.alarmList[i].userNotifySelfStatus
      if localStat == "OK":
        self.globalAlarmStatus = "OK"
      else:
        print("Global Alarm Alarmed")
        #print("After: Parameter list value for \"Value\" updated to be {}".format(self.alarmList[i].pList.get("Value",u.defaultKey)))
      u.update_objectList(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,self.alarmList)
      u.write_textfile(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray) #FIXME Do this here?
      if alarmHandlerGUI.tabs.get("Alarm Handler",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
      if alarmHandlerGUI.tabs.get("Grid Alarm Handler",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Grid Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
      if alarmHandlerGUI.tabs.get("Expert Alarm Handler",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Expert Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
      alarmHandlerGUI.masterAlarmButton.destroy()
      if alarmHandlerGUI.alarmLoop.globalAlarmStatus == "OK":
        alarmHandlerGUI.masterAlarmImage = tk.PhotoImage(file='ok.ppm').subsample(2)
        alarmHandlerGUI.masterAlarmButton = tk.Label(alarmHandlerGUI.win, image=alarmHandlerGUI.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
        alarmHandlerGUI.masterAlarmButton.image = tk.PhotoImage(file='ok.ppm').subsample(2)
      if alarmHandlerGUI.alarmLoop.globalAlarmStatus != "OK":
        #alarmHandlerGUI.alarmClient.sendPacket("2")
        #self.userNotifyLoop.update_user_notify_status(alarmHandlerGUI.OL)
        alarmHandlerGUI.masterAlarmImage = tk.PhotoImage(file='alarm.ppm').subsample(2)
        alarmHandlerGUI.masterAlarmButton = tk.Label(alarmHandlerGUI.win, image=alarmHandlerGUI.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
        alarmHandlerGUI.masterAlarmButton.image = tk.PhotoImage(file='alarm.ppm').subsample(2)
      alarmHandlerGUI.masterAlarmButton.grid(rowspan=3, row=1, column=0, padx=5, pady=10, sticky='NESW')
      alarmHandlerGUI.masterAlarmButton.bind("<Button-1>", alarmHandlerGUI.update_show_alarms)
      alarmHandlerGUI.win.after(10000,self.alarm_loop, alarmHandlerGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
    if (self.globalLoopStatus=="Paused"):
      alarmHandlerGUI.win.after(10000,self.alarm_loop, alarmHandlerGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
      print("In sleep mode: waited 10 seconds to try to check alarm status again")

class USER_NOTIFY():
  def __init__(self,alarmLoop):
    pass

  def user_notify_loop(self,alarmLoop,OL,fileArray,alarmHandlerGUI):
    #if alarmHandlerGUI.tabs.get("Alarm Handler",u.defaultKey) != u.defaultKey:
    #  alarmHandlerGUI.tabs["Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
    #if alarmHandlerGUI.tabs.get("Grid Alarm Handler",u.defaultKey) != u.defaultKey:
    #  alarmHandlerGUI.tabs["Grid Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
    #if alarmHandlerGUI.tabs.get("Expert Alarm Handler",u.defaultKey) != u.defaultKey:
    #  alarmHandlerGUI.tabs["Expert Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
    if (alarmLoop.globalLoopStatus=="Looping"):
      self.update_user_notify_status(alarmLoop,OL,fileArray) # Assumes OK, checks each OL.objectList[2] entry for its notify status, continues
      if alarmHandlerGUI.alertTheUser == True and alarmLoop.globalAlarmStatus != "OK": # globalAlarmStatus determined by these set acknowledged stati
        try:
          alarmHandlerGUI.alarmClient.sendPacket("2") # Have a case series here for passing different packets based on different alarm stati
        except:
          print("Alarm Sound Server not running\nPlease Launch an instance on the EPICS computer\nssh hacuser@hacweb7, cd parity-alarms, ./bserver&")
      # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
      alarmHandlerGUI.win.after(1000*OL.cooldownReduction,self.user_notify_loop, alarmLoop,OL,fileArray,alarmHandlerGUI) 
    else:                                                                                     
      # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful) - Wait longer if paused, no need to overkill # FIXME Probably use the global cooldownReduction wait time for this
      alarmHandlerGUI.win.after(1000*10*OL.cooldownReduction,self.user_notify_loop, alarmLoop,OL,fileArray,alarmHandlerGUI) 

  def update_user_notify_status(self,alarmLoop,OL,fileArray):
    for e in range(0,len(OL.objectList[2])):
      tmpUNS = "OK" # Assume its ok, then update with the alarmList's "self" values
      if OL.objectList[2][e].userNotifyStatus != "OK":
        tmpCheck = OL.objectList[2][e].userNotifyStatus.split(' ')
        if tmpCheck[0] == "Cooldown":
          if tmpCheck[1] != '':
            print("In cooldown save region - actually cooling down")
            tmpUNS = "Cooldown {}".format(int(tmpCheck[1])-OL.cooldownReduction)
          if int(tmpCheck[1]) <= OL.cooldownReduction:
            tmpUNS = "OK" # Reset upond 2nd click
            print("In cooldown save region - cooldown over, now we're OK")
        else: # it isn't a Cooldown # array, so just take the 0th element
          tmpUNS = tmpCheck[0]
        #print("COOL: Saving to file [{}][{}] userNotifyStatus = {}".format(2,e,tmpUNS))
        OL.objectList[2][e].parameterList["User Notify Status"] = tmpUNS
        OL.objectList[2][e].userNotifyStatus = tmpUNS
        OL.objectList[2][e].alarm.userNotifySelfStatus = tmpUNS
        for t in range(OL.objectList[2][e].indexStart,OL.objectList[2][e].indexEnd+1):
          if fileArray.filearray[t][3] == "User Notify Status":
            fileArray.filearray[t][4] = tmpUNS
            # Update the object list all children's user notify status
      

class ALARM():
  def __init__(self,myAO):
    #self.alarmName = myAO.name
    #self.runNumber = os.getenv($RUNNUM)
    self.pList = myAO.parameterList # FIXME FIXME FIXME test and prove that this is true!!! This parameterList is built out of the object's parameter list which is built out of the values of all objects, so editing them here edits them everywhere - be careful!! FIXME - to edit all of objectLists' values it may be necessary to make the constituent local objects into arrays so the pointer logic works
    #print("Initializing: pList = {}".format(self.pList))
    self.alarmAnalysisReturn = None
    self.alarmErrorReturn = None
    self.alarmSelfStatus = myAO.alarmStatus
    self.userNotifySelfStatus = myAO.userNotifyStatus
    self.userSilenceSelfStatus = myAO.userSilenceStatus
    self.alarmType = self.pList.get("Alarm Type",u.defaultKey)
    self.alarmEvaluateType = "Exactly" # Default alarm criteria is whether the value is not-null and otherwise is defined on context from given parameterList entries
    # Do I need to make a lambda initialized instance of the alarm action per event? I don't think this matters like it did for button context menu placements.... especially since these actions are being taken by the alarm handler in a loop over objectList
    #print("Initializing new alarm for object {} {}, name = {}".format(myAO.column,myAO.columnIndex,myAO.name+" "+myAO.value))
    self.alarm_analysis = lambda myAOhere = myAO: self.do_alarm_analysis(myAOhere)
    self.alarm_evaluate = lambda myAOhere = myAO: self.do_alarm_evaluate(myAOhere) # Just keep this stub here in case

  def do_alarm_analysis(self,myAO):
    #print("Trying alarm analysis for object {} {}, name = {}, = {}".format(myAO.column,myAO.columnIndex,myAO.name+" "+myAO.value,self.pList))
    if "Camguin" in self.alarmType: # Alarm Type is the parameter (level 4 object) which keeps track of what analysis to do
      subprocess("root -L camguin_C.so({},{},{},{},{},{},{},{},{},{},{})".format(self.pList["Analysis"],self.pList["Tree"],self.pList["Branch"],self.pList["Leaf"],self.pList["Cuts"],int(self.pList["Ignore Event Cuts"]),self.pList["Hist Rebinning"],int(self.pList["Stability Ring Length"]),self.runNumber,1,0.0), stdout=self.alarmAnalysisReturn, stderr=self.alarmErrorReturn, timeout=30)

    if "EPICS" in self.alarmType:
      if self.pList.get("Variable Name"):
        cmds = ['caget', '-t', self.pList["Variable Name"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful #FIXME
        #print("EPICS: Doing alarm analysis for object {} {}, name = {}".format(myAO.column,myAO.columnIndex,myAO.name+" "+myAO.value))
        print("The epics output for variable {} is {}".format(self.pList["Variable Name"],cond_out))
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          #print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.pList["Variable Name"]))
          cond_out = "NULL"
        self.pList["Value"] = cond_out
      else: # User didn't have "Value" in their parameter list, add it and make it init to NULL
        self.pList["Variable Name"] = "NULL"
        self.pList["Value"] = "NULL"
      #print("Parameter list value for \"Value\" updated to be {}".format(self.pList["Value"]))

    if "External" in self.alarmType: # Alarm Type is the parameter (level 4 object) which keeps track of what analysis to do
      # Read the external output text file, parse each line, compare with current alarm object's dictionaries, update object's values, evaluate status, continue
      pass

  def do_alarm_evaluate(self,myAO):
    # Consider making a candidate list of possible key words, but for now stick to hard-coded names... 
    #print("Updating: pList = {}".format(self.pList))
    val = self.pList.get("Value",u.defaultKey)
    lowlow = self.pList.get("Low Low",u.defaultKey)
    low = self.pList.get("Low",u.defaultKey)
    high = self.pList.get("High",u.defaultKey)
    highhigh = self.pList.get("High High",u.defaultKey)
    exactly = self.pList.get("Exactly",u.defaultKey)
    print("Value = {}, high = {}".format(val, high))
    #valD = Decimal(val)
    #highD = Decimal(high)
    #if valD > highD:
    #  print("Value is > high")
    #if not u.is_number(str(val)): # Then we are not dealing with a number alarm - for now just return false
    if self.pList.get("Exactly",u.defaultKey) != u.defaultKey: # Then we are not dealing with a number alarm - for now just return false
      #print("ERROR: Assume alarms values can only be numbers for now")
      pass
      #if exactly != "NULL" and val != exactly:
      #  self.pList["Alarm Status"] = "Exactly"
      #else:
      #  self.pList["Alarm Status"] = "OK"
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
    if val != "NULL":
      if low != "NULL" and val < low:
        self.pList["Alarm Status"] = "Low"
      elif lowlow != "NULL" and val < lowlow:
        self.pList["Alarm Status"] = "LowLow"
      elif high != "NULL" and val > high:
        print("Updating status to high")
        self.pList["Alarm Status"] = "High"
      elif highhigh != "NULL" and val > highhigh:
        self.pList["Alarm Status"] = "HighHigh"
      elif exactly != "NULL" and val != exactly:
        self.pList["Alarm Status"] = "Exactly"
      else:
        self.pList["Alarm Status"] = "OK"
    else:
      val = "NULL"
      self.pList["Alarm Status"] = "OK"
    #print("Updated: pList = {}".format(self.pList))
    if self.pList.get("Alarm Status",u.defaultKey) != "OK" and self.pList.get("Alarm Status",u.defaultKey) != "Invalid" and self.pList.get("Alarm Status",u.defaultKey) != "NULL": # Update global alarm status unless NULL or invalid
      self.alarmSelfStatus = self.pList.get("Alarm Status",u.defaultKey)
      myAO.alarmStatus = self.pList.get("Alarm Status",u.defaultKey)
      print("Alarm status updated to be {}".format(myAO.alarmStatus))
      # If the alarm is alarming and we aren't in cooldown the update user status
      if self.pList.get("Alarm Status",u.defaultKey) != "OK" and self.pList.get("User Notify Status",u.defaultKey).split(' ')[0] != "Cooldown":
        self.userNotifySelfStatus = self.pList.get("Alarm Status",u.defaultKey)
        myAO.userNotifyStatus = self.pList.get("Alarm Status",u.defaultKey)
        print("User Notify Status updated to be {}".format(myAO.userNotifyStatus))
        self.pList["User Notify Status"] = self.pList.get("Alarm Status",u.defaultKey)
        #print("COOLER: Editing value of User Notify Status to = {}".format(myAO.userNotifyStatus))
      myAO.userSilenceStatus = self.pList.get("User Silence Status",u.defaultKey)
      if myAO.userSilenceStatus != "Silenced":
        myAO.color = u.red_color
      elif myAO.userSilenceStatus == "Silenced":
        myAO.color = u.darkgrey_color # Still indicate that it is off, but not red now
      for k in range(0,len(myAO.parentIndices)):
        u.recentAlarmButtons[k] = myAO.parentIndices[k]
      u.recentAlarmButtons[myAO.column] = myAO.columnIndex
      return "Not OK"
    else:
      print("Alarm OK")
      self.alarmSelfStatus = self.pList.get("Alarm Status",u.defaultKey)
      #self.userNotifySelfStatus = self.pList.get("User Notify Status",u.defaultKey)
      # FIXME needed? # myAO.userNotifyStatus = self.pList.get("User Notify Status",u.defaultKey)
      #myAO.userSilenceStatus = self.pList.get("User Silence Status",u.defaultKey)
      myAO.alarmStatus = "OK"
      myAO.color = u.lightgrey_color
      return "OK"

class FILE_ARRAY():
  def __init__(self,filen,delimiter):
    self.filename = filen
    self.delim = delimiter
    self.filearray = u.parse_textfile(self)

class OBJECT_LIST():
  def __init__(self,fileArray,cooldownLength):
    self.objectList = u.create_objects(fileArray,cooldownLength)
    self.currentlySelectedButton = -1
    self.displayPList = 0
    self.cooldownLength = cooldownLength # Wait a minute before alarming again
    self.cooldownReduction = 2
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
          self.activeObjectColumnIndicesList[ind+1]=self.objectList[ind+1][k].columnIndex  
          # loop until the end of children of this active click, then the inserting goes at the end of child lists
          # FIXME is this why only last entry in a set of children will trigger parent's alarm status?
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
    self.alarmStatus = "OK"
    self.userSilenceStatus = "Alert"
    self.userNotifyStatus = "OK"
    self.cooldownLength = 60 # Default initialize, will be overwritten later
    #self.parameterList["User Silence Status"] = self.userSilenceStatus
    self.alarm = lambda: ALARM(self);
    self.clicked = 0

  def click(self,clickStat):
    self.clicked = clickStat
    if (clickStat == 0 and self.alarmStatus == "OK"):
      self.color = u.lightgrey_color
    if (clickStat == 1 and self.alarmStatus == "OK"):
      self.color = u.grey_color
    #if (clickStat == 0 and self.alarmStatus == 1):
    if self.alarmStatus != "OK":
      self.color = self.color #FIXME col #3 still == red problem?
    #if self.alarmStatus != "OK" and self.userSilenceStatus == "Alert":
    #  self.color = u.red_color
    #if self.userSilenceStatus == "Silenced":
    #  self.color = u.darkgrey_color

  def add_parameter(self,obj1,obj2): # Updates dictionary with new value, appends or edits appropriately, but names are the keys... so be careful
    self.parameterList[obj1.value]=obj2.value

  def add_parameter_history(self,val_append):
    self.parameterListHistory.append(val_append)
    # add a pair to a list of parameter names and values

