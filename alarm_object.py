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
import gc
from decimal import Decimal
from threading import Thread, Lock

# EPICS
import logging
import rcdb
import subprocess
import socket
from datetime import datetime

class ALARM_LOOP_MONITOR():
  def __init__(self,alarmHandlerGUI):
    self.nLoops = 1
    self.Monitor = True
    #self.alarm_loop_monitor(alarmHandlerGUI)

  def alarm_loop_monitor(self,alarmHandlerGUI):
    if (alarmHandlerGUI.alarmLoop.globalLoopStatus=="Looping"):
      #if self.Monitor:
      #  self.Monitor = False
      #else:
      #  self.Monitor = True
      # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful) - 30 second loop
      if alarmHandlerGUI.alarmLoop.userNotifyLoop.nLoops <= self.nLoops and self.nLoops>10 and self.Monitor:
        print("\n\nALERT ALERT: Alarm handler notification loop has been stale for 1 minute\n\nRebooting alarm loops - Probably you should just reboot the alarm handler entirely now\n\n")
        self.nLoops = alarmHandlerGUI.alarmLoop.userNotifyLoop.nLoops
        alarmHandlerGUI.win.after(1000*alarmHandlerGUI.OL.cooldownReduction,alarmHandlerGUI.alarmLoop.userNotifyLoop.user_notify_loop, alarmHandlerGUI.alarmLoop,alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI)
        alarmHandlerGUI.win.after(10000,alarmHandlerGUI.alarmLoop.alarm_loop,alarmHandlerGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
      else: 
        if self.Monitor:
          print("\n\nAlarm Handler Health Check passed: 60 second loop's Notify Counter # = {}, notify loop's counter # = {}, should not be the same\n\n".format(self.nLoops,alarmHandlerGUI.alarmLoop.userNotifyLoop.nLoops))
          self.nLoops = alarmHandlerGUI.alarmLoop.userNotifyLoop.nLoops
      alarmHandlerGUI.win.after(30000*alarmHandlerGUI.OL.cooldownReduction,self.alarm_loop_monitor,alarmHandlerGUI)

class ALARM_LOOP_GUI():
  def __init__(self,alarmHandlerGUI):
    pass

  def GUI_loop(self,alarmHandlerGUI):
    gc.collect()
    del gc.garbage[:]
    if (alarmHandlerGUI.alarmLoop.globalLoopStatus=="Looping"):
      print("Waited 10 seconds, refreshing GUI")
      u.update_objectList(alarmHandlerGUI.OL,alarmHandlerGUI.alarmLoop.alarmList)
      u.write_textfile(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray) #FIXME Do this here?
      if alarmHandlerGUI.tabs.get("Alarm Handler",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      if alarmHandlerGUI.tabs.get("Grid Alarm Handler",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Grid Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      if alarmHandlerGUI.tabs.get("Expert Alarm Handler",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Expert Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      if alarmHandlerGUI.tabs.get("Active Alarm Handler",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Active Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      if alarmHandlerGUI.tabs.get("Alarm History",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Alarm History"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      if alarmHandlerGUI.tabs.get("Settings",u.defaultKey) != u.defaultKey:
        alarmHandlerGUI.tabs["Settings"].refresh_screen(alarmHandlerGUI)
      alarmHandlerGUI.masterAlarmButton.destroy()
      if alarmHandlerGUI.alarmLoop.globalAlarmStatus == "OK":
        alarmHandlerGUI.masterAlarmImage = tk.PhotoImage(file='ok.ppm').subsample(2)
        alarmHandlerGUI.masterAlarmButton = tk.Label(alarmHandlerGUI.win, image=alarmHandlerGUI.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
        alarmHandlerGUI.masterAlarmButton.image = tk.PhotoImage(file='ok.ppm').subsample(2)
      if alarmHandlerGUI.alarmLoop.globalAlarmStatus != "OK":
        alarmHandlerGUI.masterAlarmImage = tk.PhotoImage(file='alarm.ppm').subsample(2)
        alarmHandlerGUI.masterAlarmButton = tk.Label(alarmHandlerGUI.win, image=alarmHandlerGUI.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
        alarmHandlerGUI.masterAlarmButton.image = tk.PhotoImage(file='alarm.ppm').subsample(2)
      alarmHandlerGUI.masterAlarmButton.grid(rowspan=3, row=1, column=0, padx=5, pady=10, sticky='NESW')
      alarmHandlerGUI.masterAlarmButton.bind("<Button-1>", alarmHandlerGUI.update_show_alarms)
      alarmHandlerGUI.win.after(5000,self.GUI_loop, alarmHandlerGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
    if (alarmHandlerGUI.alarmLoop.globalLoopStatus=="Paused"):
      alarmHandlerGUI.win.after(5000,self.GUI_loop, alarmHandlerGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
      print("In sleep mode: waited 5 seconds to refresh GUI again")
    gc.collect()
    del gc.garbage[:]

class ALARM_LOOP():
  def __init__(self,alarmHandlerGUI):
    self.alarmList = alarmHandlerGUI.OL.objectList
    #print("Initializing, adding alarm list parameterList = {}".format(alarmHandlerGUI.OL.objectList[i].alarm.parameterList))
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
  

  def doExternal(self,alarmHandlerGUI):
    if os.path.exists(alarmHandlerGUI.externalFilename) and self.checkExternalStatus == True and (time.time() - os.path.getmtime(alarmHandlerGUI.externalFilename)) < alarmHandlerGUI.externalParameterFileStaleTime:
      #print("Adding External alarms from {}".format(alarmHandlerGUI.externalFileArray.filename))
      u.update_extra_filearray(alarmHandlerGUI.fileArray,alarmHandlerGUI.externalFileArray)
      alarmHandlerGUI.OL.objectList = u.create_objects(alarmHandlerGUI.fileArray,alarmHandlerGUI.OL.cooldownLength) # FIXME Necessary?
      self.alarmList = alarmHandlerGUI.OL.objectList
      gc.collect()
      del gc.garbage[:]
      u.write_textfile(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray) #FIXME Do this here?
    else:
      print("No extra alarm files found")

  def doAlarmChecking(self,alarmHandlerGUI):
    print("\n - Global Alarm Status: ")
    localAlStat = 0
    for alrm in self.alarmList.values():
    # FIXME This is what I want to replace the above line with, using the object list dictionary of ALARM_OBJECT rather than their ALARMs
  # for i in range (0,len(alarmHandlerGUI.OL.objectList)):
      Thread(target=alrm.alarm_analysis).start()
      if alrm.parameterList["Alarm Status"] != "OK":
        print(" -- Alarm {}: {}, {} = {}".format(alrm.parameterList["Alarm Status"],alrm.name,alrm.value,alrm.parameterList["Value"]))
        localAlStat += 1
      Thread(target=alrm.alarm_evaluate).start()
      # Check if the alarm is alarming and has not been "OK"ed by the user acknowledge
      #print("Checking alarm {} alarm status = {}, silence status = {}, and user acknowledge = {}".format(i,alrm.alarmSelfStatus,alrm.userSilenceSelfStatus,self.ok_notify_check(alrm.userNotifySelfStatus)))
      # If the userNotifyStatus is NULL (i.e. not set) then the alarm handler will just read it and move on with its life
      if self.globalUserAlarmSilence == "Alert" and self.ok_notify_check(alrm.userNotifySelfStatus) != "OK" and alrm.userSilenceSelfStatus == "Alert":
        # Just let the method I wrote take care of determining global alarm status
        self.globalAlarmStatus = alrm.userNotifySelfStatus # Update global alarm status
        u.append_historyList(alarmHandlerGUI.HL,alarmHandlerGUI.OL,i) # Update Alarm History
        localStat = alrm.userNotifySelfStatus
    if localAlStat == 0:
      print(' -- '+'\x1b[1;1;32m'+'Alarms all OK '+'\x1b[0m'+'\n')
    else:
      print(' -- '+'\x1b[1;1;31m'+'{} alarms triggered '.format(localAlStat)+'\x1b[0m'+'\n')

  def alarm_loop(self,alarmHandlerGUI):
    if (self.globalLoopStatus=="Looping"):
      print("Waited 10 seconds, analyzing alarms")
      Thread(self.doExternal(alarmHandlerGUI)).start()
      localStat = "OK"
      self.doAlarmChecking(alarmHandlerGUI)
      if localStat == "OK":
        self.globalAlarmStatus = "OK"
      else:
        print("Global Alarm Alarmed")
      u.update_objectList(alarmHandlerGUI.OL,self.alarmList)
      u.write_historyFile(alarmHandlerGUI.HL)
      #u.write_textfile(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray) #FIXME Do this here?
      #if alarmHandlerGUI.tabs.get("Alarm Handler",u.defaultKey) != u.defaultKey:
      #  alarmHandlerGUI.tabs["Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      #if alarmHandlerGUI.tabs.get("Grid Alarm Handler",u.defaultKey) != u.defaultKey:
      #  alarmHandlerGUI.tabs["Grid Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      #if alarmHandlerGUI.tabs.get("Expert Alarm Handler",u.defaultKey) != u.defaultKey:
      #  alarmHandlerGUI.tabs["Expert Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      #if alarmHandlerGUI.tabs.get("Active Alarm Handler",u.defaultKey) != u.defaultKey:
      #  alarmHandlerGUI.tabs["Active Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      #if alarmHandlerGUI.tabs.get("Alarm History",u.defaultKey) != u.defaultKey:
      #  alarmHandlerGUI.tabs["Alarm History"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop,alarmHandlerGUI.HL)
      #if alarmHandlerGUI.tabs.get("Settings",u.defaultKey) != u.defaultKey:
      #  alarmHandlerGUI.tabs["Settings"].refresh_screen(alarmHandlerGUI)
      #alarmHandlerGUI.masterAlarmButton.destroy()
      #if alarmHandlerGUI.alarmLoop.globalAlarmStatus == "OK":
      #  alarmHandlerGUI.masterAlarmImage = tk.PhotoImage(file='ok.ppm').subsample(2)
      #  alarmHandlerGUI.masterAlarmButton = tk.Label(alarmHandlerGUI.win, image=alarmHandlerGUI.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
      #  alarmHandlerGUI.masterAlarmButton.image = tk.PhotoImage(file='ok.ppm').subsample(2)
      #if alarmHandlerGUI.alarmLoop.globalAlarmStatus != "OK":
      #  #alarmHandlerGUI.alarmClient.sendPacket("2")
      #  #self.userNotifyLoop.update_user_notify_status(alarmHandlerGUI.OL)
      #  alarmHandlerGUI.masterAlarmImage = tk.PhotoImage(file='alarm.ppm').subsample(2)
      #  alarmHandlerGUI.masterAlarmButton = tk.Label(alarmHandlerGUI.win, image=alarmHandlerGUI.masterAlarmImage, cursor="hand2", bg=u.lightgrey_color)
      #  alarmHandlerGUI.masterAlarmButton.image = tk.PhotoImage(file='alarm.ppm').subsample(2)
      #alarmHandlerGUI.masterAlarmButton.grid(rowspan=3, row=1, column=0, padx=5, pady=10, sticky='NESW')
      #alarmHandlerGUI.masterAlarmButton.bind("<Button-1>", alarmHandlerGUI.update_show_alarms)
      alarmHandlerGUI.win.after(10000,self.alarm_loop, alarmHandlerGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
    if (self.globalLoopStatus=="Paused"):
      alarmHandlerGUI.win.after(10000,self.alarm_loop, alarmHandlerGUI) # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
      print("In sleep mode: waited 10 seconds to try to check alarm status again")

class USER_NOTIFY():
  def __init__(self,alarmLoop):
    self.nLoops = 0

  def user_notify_loop(self,alarmLoop,OL,fileArray,alarmHandlerGUI):
    self.nLoops = self.nLoops + 1
    #if alarmHandlerGUI.tabs.get("Alarm Handler",u.defaultKey) != u.defaultKey:
    #  alarmHandlerGUI.tabs["Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
    #if alarmHandlerGUI.tabs.get("Grid Alarm Handler",u.defaultKey) != u.defaultKey:
    #  alarmHandlerGUI.tabs["Grid Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
    #if alarmHandlerGUI.tabs.get("Expert Alarm Handler",u.defaultKey) != u.defaultKey:
    #  alarmHandlerGUI.tabs["Expert Alarm Handler"].refresh_screen(alarmHandlerGUI.OL,alarmHandlerGUI.fileArray,alarmHandlerGUI.alarmLoop)
    localStat = "OK"
    alarmHandlerGUI.alertTheUserSoundNow = alarmHandlerGUI.alertTheUserSound # Default = 7 every restart of loop
    for alrm in alarmLoop.alarmList.values():
      alrm.alarm_evaluate()
      # Check if the alarm is alarming and has not been "OK"ed by the user acknowledge
      #print("Checking alarm {} alarm status = {}, silence status = {}, and user acknowledge = {}".format(i,alrm.alarmSelfStatus,alrm.userSilenceSelfStatus,alarmLoop.ok_notify_check(alrm.userNotifySelfStatus)))
      # If the userNotifyStatus is NULL (i.e. not set) then the alarm handler will just read it and move on with its life
      if alarmLoop.globalUserAlarmSilence == "Alert" and alarmLoop.ok_notify_check(alrm.userNotifySelfStatus) != "OK" and alrm.userSilenceSelfStatus == "Alert":
        # Just let the method I wrote take care of determining global alarm status
        print("Alert status = {}".format(alrm.alertSound))
        alarmLoop.globalAlarmStatus = alrm.userNotifySelfStatus # Update global alarm status
        if alrm.alertSound != alarmHandlerGUI.alertTheUserSound:
          alarmHandlerGUI.alertTheUserSoundNow = alrm.alertSound # Update global alarm sound
        u.append_historyList(alarmHandlerGUI.HL,alarmHandlerGUI.OL,i) # Update Alarm History
        localStat = alrm.userNotifySelfStatus
    if localStat == "OK":
      alarmLoop.globalAlarmStatus = "OK"
    else:
      print("Global Alarm Alarmed")
    if (alarmLoop.globalLoopStatus=="Looping" and alarmLoop.globalUserAlarmSilence == "Alert"):
      self.update_user_notify_status(alarmLoop,OL,fileArray) # Assumes OK, checks each OL.objectList[2] entry for its notify status, continues
      if alarmHandlerGUI.alertTheUser == True and alarmLoop.globalAlarmStatus != "OK": # globalAlarmStatus determined by these set acknowledged stati
        try:
          if alarmHandlerGUI.alertTheUserSoundNow != alarmHandlerGUI.alertTheUserSound:
            alarmHandlerGUI.alarmClient.sendPacket(alarmHandlerGUI.alertTheUserSoundNow) 
          else:
            alarmHandlerGUI.alarmClient.sendPacket(alarmHandlerGUI.alertTheUserSound)
        except:
          print("Alarm Sound Server not running\nPlease Launch an instance on the EPICS computer\nssh hacuser@hacweb7, cd parity-alarms, ./bserver&")
      # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful)
      alarmHandlerGUI.win.after(1000*OL.cooldownReduction,self.user_notify_loop, alarmLoop,OL,fileArray,alarmHandlerGUI) 
    else:                                                                                     
      # Recursion loop here - splits off a new instance of this function and finishes the one currently running (be careful) - Wait longer if paused, no need to overkill 
      alarmHandlerGUI.win.after(1000*OL.cooldownReduction,self.user_notify_loop, alarmLoop,OL,fileArray,alarmHandlerGUI) 

  # FIXME - uses old index notation to keep track of notify status in fileArray/objectList data
  def update_user_notify_status(self,alarmLoop,OL,fileArray):
    for key in OL.objectList.keys():
      tmpUNS = "OK" # Assume its ok, then update with the alarmList's "self" values
      if OL.objectList[key].userNotifyStatus != "OK":
        tmpCheck = OL.objectList[key].userNotifyStatus.split(' ')
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
        OL.objectList[key].parameterList["User Notify Status"] = tmpUNS
        OL.objectList[key].userNotifyStatus = tmpUNS
        OL.objectList[key].alarm.userNotifySelfStatus = tmpUNS
        # FIXME Depreciated - no longer have the ability to silence a chunk - no more chunks
        #for t in range(OL.objectList[key].indexStart,OL.objectList[key].indexEnd+1):
        #  if fileArray.filearray[t][3] == "User Notify Status":
        #    fileArray.filearray[t][4] = tmpUNS
        #    # Update the object list all children's user notify status
      
class FILE_ARRAY():
  def __init__(self,filen,delimiter):
    self.mutex = Lock()
    self.filename = filen
    self.delim = delimiter
    self.conf = {}
    self.filearray = u.parse_textfile(self)

class HISTORY_LIST():
  def __init__(self,filen,delimiter,pdelimiter,time):
    self.mutex = Lock()
    self.currentHist = -1
    self.displayPList = 0
    self.timeWait = time
    self.filename = filen
    self.delim = delimiter
    self.paramDelim = pdelimiter
    self.filearray = u.parse_textfile(self) # Reads text file just like fileArray, same names so Python doesn't know the difference
    self.historyList = u.init_historyList(self)

# FIXME The Object List class is full of old features that need to be removed and streamlined
class OBJECT_LIST():
  def __init__(self,fileArray,cooldownLength):
    self.objectList = u.create_objects(fileArray,cooldownLength)
    self.keys = u.create_objects_keys(fileArray)
    self.currentlySelectedButton = -1
    self.displayPList = 0
    self.cooldownLength = cooldownLength # Wait a minute before alarming again
    # FIXME this time step should be from the config file too
    self.cooldownReduction = 2
    # These three lists need to be removed and just use self.currentlySelectedButton...
    self.selectedButtonColumnIndicesList = []
    self.activeObjectColumnIndicesList = [] # This stores the location where insertion will take place
    self.selectedColumnButtonLengthList = [] # This is the thing to store the number of buttons that should be displayed -> == the number of children of the parent clicked button
    for key in self.keys: # Look in the list of columns of objects, neglect final row
      self.selectedButtonColumnIndicesList.append(-1) # This looks stupid because I'm being safe, initialize to the top row, first object child of each one
      self.activeObjectColumnIndicesList.append(0) # This looks stupid because I'm being safe, initialize to the top row, first object child of each one
      self.selectedColumnButtonLengthList.append(0) # Safety initialization
    self.activeObjectColumnIndicesList[0]=self.objectList[0][len(self.objectList[0])-1].columnIndex
    self.selectedColumnButtonLengthList[0] = len(self.objectList[0]) # Initialize first column length to be just the number there

  # FIXME Depreciated chunk clicking feature here - replace with just click...
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
          # FIXME is this why only last entry in a set of children will trigger parent's alarm status in expert mode?
          break
    # If i+1 then take last parentIndex==columnIndex columnIndex as activeObjectIndicesList[i+1]
    if i < 4:
      for k in range(0,len(self.objectList[i+1])): # For each entry on the right
        # Take the button that was clicked and find the greatest child of it
        if self.objectList[i][j].columnIndex == self.objectList[i+1][k].parentIndices[i]: # Take clicked colInd, if one to right's PI[of mine] == colInd, then set it as the activeObject on right (for file appending purposes)
          self.activeObjectColumnIndicesList[i+1]=self.objectList[i+1][k].columnIndex

class ALARM_OBJECT():
  def __init__(self):
    # Needed parameters
    self.name = "NULL"
    self.value = "NULL"
    self.parameterList = {} # Using a dictionary makes life much easier
    self.color = u.lightgrey_color
    self.alarmStatus = "OK"
    self.userSilenceStatus = "Alert"
    self.userNotifyStatus = "OK"
    # Should come from the config file?
    self.alertSound = "7"
    self.cooldownLength = 60 # Default initialize, will be overwritten later
    #self.parameterList["User Silence Status"] = self.userSilenceStatus
    #self.alarm = lambda: ALARM(self);
    self.clicked = 0

    # FIXME Depreciated
    self.indexStart = 0
    self.indexEnd = 0
    self.column = 0
    self.columnIndex = 0
    self.parentIndices = []
    self.numberChildren = 0
    self.parameterListHistory = [] # Every time we update parameterList pass its prior value to history ... let actually accumulating of values take place in alarmLoop if wanted...
    self.valueHistory = []
    self.valueHistory.append(self.value)

    # Old "ALARM" Class initializer remnants
    self.alarmAnalysisReturn = None # For camguin outputs to stdout to catch
    self.alarmErrorReturn = None
    self.runNumber = 0
    self.alarmType = self.parameterList.get("Alarm Type",u.defaultKey)
    # Default alarm criteria is whether the value is not-null and otherwise is defined on context from given parameterList entries
    self.alarmEvaluateType = "Exactly" 
    # Do I need to make a lambda initialized instance of the alarm action per event? I don't think this matters like it did for button context menu placements.... especially since these actions are being taken by the alarm handler in a loop over objectList
    #print("Initializing new alarm for object {} {}, name = {}".format(self.column,self.columnIndex,self.name+" "+self.value))
    self.alarm_analysis = lambda myAO = self: self.do_alarm_analysis(myAO)
    self.alarm_evaluate = lambda myAO = self: self.do_alarm_evaluate(myAO) # Just keep this stub here in case

  def click(self,clickStat):
    self.clicked = clickStat
    if (clickStat == 0 and self.alarmStatus == "OK"):
      self.color = u.lightgrey_color
    if (clickStat == 1 and self.alarmStatus == "OK"):
      self.color = u.grey_color
    #if (clickStat == 0 and self.alarmStatus == 1):
    if self.alarmStatus != "OK":
      self.color = self.color #FIXME col #3 still == red problem in expert mode? 
    #if self.alarmStatus != "OK" and self.userSilenceStatus == "Alert":
    #  self.color = u.red_color
    #if self.userSilenceStatus == "Silenced":
    #  self.color = u.darkgrey_color

  def add_parameter(self,obj1,obj2): # Updates dictionary with new value, appends or edits appropriately, but names are the keys... so be careful
    self.parameterList[obj1.value]=obj2.value

  def add_parameter_history(self,val_append):
    self.parameterListHistory.append(val_append)
    # add a pair to a list of parameter names and values

  def polish_alarm_object(self):
    # Silence status
    if "User Silence Status" not in self.parameterList:
      self.parameterList["User Silence Status"] = "Alert"
    self.userSilenceStatus = self.parameterList["User Silence Status"]
    if self.alarmStatus != "OK" and self.userSilenceStatus == "Alert":
      self.color = u.red_color
    elif self.userSilenceStatus == "Silenced":
      self.color = u.yellow_color
    elif self.alarmStatus == "OK" and self.userSilenceStatus != "Silenced":
      self.color = u.lightgrey_color

    # Alarm status
    if "Alarm Status" not in self.parameterList:
      self.parameterList["Alarm Status"] = "OK"
    self.alarmStatus = self.parameterList["Alarm Status"]
    if self.alarmStatus != "OK"
      self.color = u.red_color
    if self.userSilenceStatus == "Silenced":
      self.color = u.yellow_color

    if "User Notify Status" not in self.parameterList:
      self.parameterList["User Notify Status"] = "OK"
    self.userNotifyStatus = self.parameterList["User Notify Status"]
    if self.userSilenceStatus = "Silenced":
      self.parameterList["User Notify Status"] = "OK"
    elif self.alarmStatus != "OK" and self.userNotifyStatus.split(' ')[0] != "Cooldown":
      self.parameterList["User Notify Status"] = self.alarmStatus
    else:
      self.parameterList["User Notify Status"] = self.value
    self.userNotifyStatus = self.parameterList["User Notify Status"]

  def do_alarm_analysis(self):
    if "Camguin" in self.alarmType: # Alarm Type is the parameter (level 4 object) which keeps track of what analysis to do
      subprocess("root -L camguin_C.so({},{},{},{},{},{},{},{},{},{},{})".format(self.parameterList["Analysis"],self.parameterList["Tree"],self.parameterList["Branch"],self.parameterList["Leaf"],self.parameterList["Cuts"],int(self.parameterList["Ignore Event Cuts"]),self.parameterList["Hist Rebinning"],int(self.parameterList["Stability Ring Length"]),self.runNumber,1,0.0), stdout=self.alarmAnalysisReturn, stderr=self.alarmErrorReturn, timeout=30)

    # FIXME Bash and EPICS are basically the same - find a way to merge them
    if "BASH" in self.alarmType: # Alarm Type parameter (level 4) for indicating that the return value is some special bash script
      if self.parameterList.get("Script Name",u.defaultKey) != "NULL":
        #print("Checking Script = {}".format(self.parameterList.get("Script Name",u.defaultKey)))
        cmds = [self.parameterList.get("Script Name",u.defaultKey)]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Command not found." in str(cond_out): # Then the Script was invalid
          print("Error: command {} not found".format(self.parameterList.get("Script Name",u.defaultKey)))
          cond_out = "NULL"
        self.parameterList["Value"] = cond_out
      if self.parameterList.get("Threshold Variable Name",u.defaultKey) != "NULL" and self.parameterList.get("Script Name",u.defaultKey) != "NULL":
        cmds = [self.parameterList.get("Script Name",u.defaultKey),self.parameterList.get("Threshold Variable Name",u.defaultKey)]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Command not found." in str(cond_out): # Then the Script was invalid
          print("Error: command {} not found".format(self.parameterList.get("Script Name",u.defaultKey)))
          cond_out = u.defaultKey
          
        self.parameterList["Threshold Value"] = cond_out
      if self.parameterList.get("Threshold 2 Variable Name",u.defaultKey) != "NULL" and self.parameterList.get("Script Name",u.defaultKey) != "NULL":
        cmds = [self.parameterList.get("Script Name",u.defaultKey),self.parameterList.get("Threshold 2 Variable Name",u.defaultKey)]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Command not found." in str(cond_out): # Then the Script was invalid
          print("Error: command {} not found".format(self.parameterList.get("Script Name",u.defaultKey)))
          cond_out = u.defaultKey
          
        self.parameterList["Threshold 2 Value"] = cond_out
      if self.parameterList.get("Case Variable Name",u.defaultKey) != "NULL" and self.parameterList.get("Script Name",u.defaultKey) != "NULL":
        cmds = [self.parameterList.get("Script Name",u.defaultKey),self.parameterList.get("Case Variable Name",u.defaultKey)]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Command not found." in str(cond_out): # Then the Script was invalid
          print("Error: command {} not found".format(self.parameterList.get("Script Name",u.defaultKey)))
          cond_out = "BAD"
          
        self.parameterList["Case Value"] = cond_out
      if self.parameterList.get("Double Case Variable Name",u.defaultKey) != "NULL" and self.parameterList.get("Script Name",u.defaultKey) != "NULL":
        cmds = [self.parameterList.get("Script Name",u.defaultKey),self.parameterList.get("Double Case Variable Name",u.defaultKey)]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Command not found." in str(cond_out): # Then the epics Script was invalid
          print("Error: command {} not found".format(self.parameterList.get("Script Name",u.defaultKey)))
          cond_out = "BAD"
        self.parameterList["Double Case Value"] = cond_out
      if (self.parameterList.get("Same Value Comparator",u.defaultKey) != "NULL" or self.parameterList.get("Same Value Comparator {}".format(self.parameterList.get("Case Value",u.defaultKey)),u.defaultKey) != "NULL" or self.parameterList.get("Same Value Comparator {}".format(self.parameterList.get("Double Case Value",u.defaultKey)),u.defaultKey) != "NULL") and self.parameterList.get("Script Name",u.defaultKey) != "NULL":
        cmds = [self.parameterList.get("Script Name",u.defaultKey)]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Command not found." in str(cond_out): # Then the Script was invalid
          print("Error: command {} not found".format(self.parameterList.get("Script Name",u.defaultKey)))
          cond_out = "BAD"
          
        if self.parameterList.get("Same Value Comparator",u.defaultKey) != "NULL":
          self.parameterList["Same Value Comparator 2"] = self.parameterList["Same Value Comparator"]
          self.parameterList["Same Value Comparator"] = cond_out
        if self.parameterList.get("Same Value Comparator {}".format(self.parameterList.get("Case Value",u.defaultKey)),u.defaultKey) != "NULL":
          self.parameterList["Same Value Comparator 2 {}".format(self.parameterList.get("Case Value",u.defaultKey))] = self.parameterList["Same Value Comparator {}".format(self.parameterList.get("Case Value",u.defaultKey))]
          self.parameterList["Same Value Comparator {}".format(self.parameterList.get("Case Value",u.defaultKey))] = cond_out
        if self.parameterList.get("Same Value Comparator {}".format(self.parameterList.get("Double Case Value",u.defaultKey)),u.defaultKey) != "NULL":
          self.parameterList["Same Value Comparator 2 {}".format(self.parameterList.get("Double Case Value",u.defaultKey))] = self.parameterList["Same Value Comparator {}".format(self.parameterList.get("Double Case Value",u.defaultKey))]
          self.parameterList["Same Value Comparator {}".format(self.parameterList.get("Double Case Value",u.defaultKey))] = cond_out

    if "CODA" in self.alarmType or "RCND" in self.alarmType or "RCDB" in self.alarmType or "PVDB" in self.alarmType:
      # TEMP FIXME Do the CODA on/taking good data (split = 0, EB alive) here... why not?
      #CODAonAlarm = "NULL"
      #CODAonAlarmReturn = "NULL"
      #subprocess("./checkIfRun", shell=True, stdout=CODAonAlarm, stderr=CODAonAlarmReturn, timeout=10)
      runNumber = 0
      if self.parameterList.get("Run Number",u.defaultKey) != 0 and self.parameterList.get("Run Number",u.defaultKey) != "NULL":
        runNumber = self.parameterList.get("Run Number")
      else:
        runNumber = self.get_run_number()
      new_runNumber = self.get_run_number()
      if runNumber != new_runNumber: # Then this is a new run, update new run type alarms
        print("Original run number = {}, New Run number = {}".format(self.runNumber,new_runNumber))
        if self.parameterList.get("Variable Name",u.defaultKey) == "Run Number":
          self.parameterList["Low"] = self.runNumber
          self.parameterList["Value"] = new_runNumber # Update the run number
        if self.parameterList.get("Variable Name",u.defaultKey) == "Run Start Time":
          self.parameterList["Start Time"] = int(time.time())
          self.parameterList["Value"] = 0# int(time.time()) # Update the time value
          self.parameterList["High"] = 80*60 #int(time.time()) + 80*60
        self.runNumber = new_runNumber
        self.parameterList["Run Number"] = new_runNumber
      else:
        if self.parameterList.get("Variable Name",u.defaultKey) == "Run Start Time" and self.parameterList.get("Start Time",u.defaultKey) != "NULL":
          self.parameterList["Value"] = int(time.time()) - int(self.parameterList.get("Start Time",u.defaultKey)) # Update the time value
        
      if self.parameterList.get("Variable Name",u.defaultKey) != "Run Start Time" and self.parameterList.get("Variable Name",u.defaultKey) != "Run Number": # Else update other alarms
        cmds = ['rcnd',self.runNumber,self.parameterList["Variable BName"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Decoding...
        self.parameterList["Value"] = cond_out

    if "EPICS" in self.alarmType:
      if self.parameterList.get("Variable Name",u.defaultKey) != "NULL":
        #print("Checking EPICs variable = {}".format(self.parameterList.get("Variable Name",u.defaultKey)))
        cmds = ['caget', '-t', '-w 1', self.parameterList["Variable Name"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        #print("The epics output for variable {} is {}".format(self.parameterList["Variable Name"],cond_out))
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.parameterList["Variable Name"]))
          cond_out = "NULL"
        self.parameterList["Value"] = cond_out
      elif self.parameterList.get("IOC Alarm List Name",u.defaultKey) != "NULL":
        #print("Checking EPICs variable = {}".format(self.parameterList.get("Variable Name",u.defaultKey)))
        listNames = ['.B1','.B2','.B3','.B4','.B5','.B6','.B7','.B8','.B9','.BA']
        cond_out = "NULL"
        cmds = ["NULL"]
        if self.parameterList.get("Current Variable",u.defaultKey) != "NULL":
          cmds = ['caget', '-t', '-w 1', self.parameterList["Current Variable"]]
          cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.parameterList.get("Variable Name",u.defaultKey)))
          cond_out = "NULL"
        elif u.is_number(cond_out) and Decimal(cond_out) > 35.0:
          for eachName in listNames:
            cmds = ['caget', '-t', '-w 1', self.parameterList["IOC Alarm List Name"]+eachName]
            cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
            if cond_out == "1":
              self.parameterList["Value"] = cond_out;
            #print("The epics output for variable {} is {}".format(self.parameterList["Variable Name"],cond_out))
          if "Invalid" in str(cond_out): # Then the epics variable was invalid
            print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.parameterList.get("Variable Name",u.defaultKey)))
            cond_out = "NULL"
          self.parameterList["Value"] = cond_out
        else: 
          self.parameterList["Value"] = "0"
      else: # User didn't have "Value" in their parameter list, add it and make it init to NULL
        self.parameterList["Variable Name"] = "NULL"
        self.parameterList["Value"] = "NULL"
      if self.parameterList.get("Difference Reference Variable Name",u.defaultKey) != "NULL":
        #print("Checking EPICs variable = {}".format(self.parameterList.get("Difference Reference Variable Name",u.defaultKey)))
        cmds = ['caget', '-t', '-w 1', self.parameterList["Difference Reference Variable Name"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        #print("The epics output for variable {} is {}".format(self.parameterList["Variable Name"],cond_out))
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.parameterList["Difference Reference Variable Name"]))
          cond_out = "NULL"
        self.parameterList["Difference Reference Value"] = cond_out
        if self.parameterList.get("Value",u.defaultKey) != "NULL" and self.parameterList.get("Difference Reference Value") != "NULL":
          # FIXME HACKED this to just go ahead and take the difference here. Reference value is now only stored in file for user knowledge
          self.parameterList["Value"] = str(Decimal(self.parameterList["Value"]) - Decimal(self.parameterList["Difference Reference Value"]))
      #else: # User didn't have "Value" in their parameter list, add it and make it init to NULL
      #  self.parameterList["Difference Reference Variable Name"] = "NULL"
      #  self.parameterList["Difference Reference Value"] = "NULL"
      if self.parameterList.get("Threshold Variable Name",u.defaultKey) != "NULL":
        cmds = ['caget', '-t', '-w 1', self.parameterList["Threshold Variable Name"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.parameterList["Threshold Variable Name"]))
          cond_out = u.defaultKey
        self.parameterList["Threshold Value"] = cond_out
      if self.parameterList.get("Threshold 2 Variable Name",u.defaultKey) != "NULL":
        cmds = ['caget', '-t', '-w 1', self.parameterList["Threshold 2 Variable Name"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.parameterList["Threshold 2 Variable Name"]))
          cond_out = u.defaultKey
        self.parameterList["Threshold 2 Value"] = cond_out
      if self.parameterList.get("Case Variable Name",u.defaultKey) != "NULL":
        cmds = ['caget', '-t', '-w 1', self.parameterList["Case Variable Name"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.parameterList["Case Variable Name"]))
          cond_out = "BAD"
        self.parameterList["Case Value"] = cond_out
      #else: # User didn't have "Value" in their parameter list, add it and make it init to NULL
      #  self.parameterList["Case Variable Name"] = "NULL"
      #  self.parameterList["Case Value"] = "NULL"
      if self.parameterList.get("Double Case Variable Name",u.defaultKey) != "NULL":
        cmds = ['caget', '-t', '-w 1', self.parameterList["Double Case Variable Name"]]
        cond_out = "NULL"
        cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
        if "Invalid" in str(cond_out): # Then the epics variable was invalid
          print("ERROR Invalid epics channel, check with caget again:\t {}".format(self.parameterList["Double Case Variable Name"]))
          cond_out = "BAD"
        self.parameterList["Double Case Value"] = cond_out
      #else: # User didn't have "Value" in their parameter list, add it and make it init to NULL
      #  self.parameterList["Double Case Variable Name"] = "NULL"
      #  self.parameterList["Double Case Value"] = "NULL"

      #print("Parameter list value for \"Value\" updated to be {}".format(self.parameterList["Value"]))

    if "External" in self.alarmType: # Alarm Type is the parameter (level 4 object) which keeps track of what analysis to do
      # Read the external output text file, parse each line, compare with current alarm object's dictionaries, update object's values, evaluate status, continue
      pass

  def get_run_number(self):
    cmds = ['rcnd']
    cond_out = "NULL"
    cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
    lines = cond_out.split('\n')
    runNumber = 0
    for linei in lines:
      if ":" not in linei:
        continue
      if len(linei.split(':')) < 2:
        continue
      if linei.split(':')[0].replace(' ','') == "Lastrun":
        runNumber = linei.split(':')[1].replace(' ','')
    return runNumber

  def do_alarm_evaluate(self):
    # Consider making a candidate list of possible key words, but for now stick to hard-coded names... 
    #print("Updating: parameterList = {}".format(self.parameterList))
    val = self.parameterList.get("Value",u.defaultKey)
    threshold = self.parameterList.get("Threshold Variable Name",u.defaultKey)
    thresholdValue = self.parameterList.get("Threshold Value",u.defaultKey)
    thresholdLow = self.parameterList.get("Threshold Low",u.defaultKey)
    thresholdHigh = self.parameterList.get("Threshold High",u.defaultKey)
    threshold2 = self.parameterList.get("Threshold 2 Variable Name",u.defaultKey)
    threshold2Value = self.parameterList.get("Threshold 2 Value",u.defaultKey)
    threshold2Low = self.parameterList.get("Threshold 2 Low",u.defaultKey)
    threshold2High = self.parameterList.get("Threshold 2 High",u.defaultKey)
    case = self.parameterList.get("Case Variable Name",u.defaultKey)
    caseValue = self.parameterList.get("Case Value","BAD")
    case2nd = self.parameterList.get("Double Case Variable Name",u.defaultKey)
    case2ndValue = self.parameterList.get("Double Case Value","BAD")
    differenceReference = self.parameterList.get("Difference Reference Variable Name",u.defaultKey)
    differenceReferenceValue = self.parameterList.get("Difference Reference Value",u.defaultKey)

    tripLimit = self.parameterList.get("Trip Limit",u.defaultKey)
    if u.is_number(tripLimit):
      tripLimit = int(tripLimit)
    tripCounter = self.parameterList.get("Trip Counter",u.defaultKey)
    if u.is_number(tripCounter):
      tripCounter = int(tripCounter)

    lowlowStr = "Low Low"
    lowStr = "Low"
    highStr = "High"
    highhighStr = "High High"
    exactlyStr = "Exactly"
    comparatorStr = "Same Value Comparator"
    comparatorStr2 = "Same Value Comparator 2"
    differenceLowStr = "Difference Low"
    differenceHighStr = "Difference High"
    lowlow = u.defaultKey
    low = u.defaultKey
    high = u.defaultKey
    highhigh = u.defaultKey
    exactly = u.defaultKey
    comparator = u.defaultKey
    comparator2 = u.defaultKey
    differenceLow = u.defaultKey
    differenceHigh = u.defaultKey
    # Done initializing

    if case2nd != u.defaultKey and case2ndValue != "BAD" and case != u.defaultKey and caseValue != "BAD": # Then we have a double case determining which set of limits to use
      lowlowStr = "Low Low "+caseValue+" "+case2ndValue
      lowStr = "Low "+caseValue+" "+case2ndValue
      highStr = "High "+caseValue+" "+case2ndValue
      highhighStr = "High High "+caseValue+" "+case2ndValue
      exactlyStr = "Exactly "+caseValue+" "+case2ndValue
      comparatorStr = "Same Value Comparator"+caseValue+" "+case2ndValue
      comparatorStr2 = "Same Value Comparator 2 "+caseValue+" "+case2ndValue
      differenceLowStr = "Difference Low "+caseValue+" "+case2ndValue
      differenceHighStr = "Difference High "+caseValue+" "+case2ndValue
      lowlow = self.parameterList.get("Low Low "+caseValue+" "+case2ndValue,u.defaultKey) # Assume the user knows what the case's return values can be and names their cased limits as such
      low = self.parameterList.get("Low "+caseValue+" "+case2ndValue,u.defaultKey) 
      high = self.parameterList.get("High "+caseValue+" "+case2ndValue,u.defaultKey) 
      highhigh = self.parameterList.get("High High "+caseValue+" "+case2ndValue,u.defaultKey) 
      exactly = self.parameterList.get("Exactly "+caseValue+" "+case2ndValue,u.defaultKey) 
      comparator = self.parameterList.get("Same Value Comparator "+caseValue+" "+case2ndValue,u.defaultKey) 
      comparator2 = self.parameterList.get("Same Value Comparator 2 "+caseValue+" "+case2ndValue,u.defaultKey) 
      differenceLow = self.parameterList.get("Difference Low "+caseValue+" "+case2ndValue,u.defaultKey) 
      differenceHigh = self.parameterList.get("Difference High "+caseValue+" "+case2ndValue,u.defaultKey) 
      # Now get the default, non-cased values and catch any general case free values too
      if lowlow == u.defaultKey: 
        lowlow = self.parameterList.get("Low Low",u.defaultKey)
      if low == u.defaultKey:  
        low = self.parameterList.get("Low",u.defaultKey)
      if high == u.defaultKey:  
        high = self.parameterList.get("High",u.defaultKey)
      if highhigh == u.defaultKey:  
        highhigh = self.parameterList.get("High High",u.defaultKey)
      if exactly == u.defaultKey:  
        exactly = self.parameterList.get("Exactly",u.defaultKey)
      if comparator == u.defaultKey:  
        comparator = self.parameterList.get("Same Value Comparator",u.defaultKey)
      if comparator2 == u.defaultKey:  
        comparator2 = self.parameterList.get("Same Value Comparator 2",u.defaultKey)
      if differenceLow == u.defaultKey:  
        differenceLow = self.parameterList.get("Difference Low",u.defaultKey)
      if differenceHigh == u.defaultKey:  
        differenceHigh = self.parameterList.get("Difference High",u.defaultKey)
    # FIXME vastly redundant ELSE condition here... just make them from the top?
    elif case != u.defaultKey and caseValue != "BAD": # Then we have a single case determining which set of limits to use
      lowlowStr = "Low Low "+caseValue
      lowStr = "Low "+caseValue
      highStr = "High "+caseValue
      highhighStr = "High High "+caseValue
      exactlyStr = "Exactly "+caseValue
      comparatorStr = "Same Value Comparator "+caseValue
      comparatorStr2 = "Same Value Comparator 2 "+caseValue
      differenceLowStr = "Difference Low "+caseValue
      differenceHighStr = "Difference High "+caseValue
      lowlow = self.parameterList.get("Low Low "+caseValue,u.defaultKey) # Assume the user knows what the case's return values can be and names their cased limits as such
      low = self.parameterList.get("Low "+caseValue,u.defaultKey) 
      high = self.parameterList.get("High "+caseValue,u.defaultKey) 
      highhigh = self.parameterList.get("High High "+caseValue,u.defaultKey) 
      exactly = self.parameterList.get("Exactly "+caseValue,u.defaultKey) 
      comparator = self.parameterList.get("Same Value Comparator "+caseValue,u.defaultKey) 
      comparator2 = self.parameterList.get("Same Value Comparator 2 "+caseValue,u.defaultKey) 
      differenceLow = self.parameterList.get("Difference Low "+caseValue,u.defaultKey) 
      differenceHigh = self.parameterList.get("Difference High "+caseValue,u.defaultKey) 
    # Now get the default, non-cased values and catch any general case free values too
    if lowlow == u.defaultKey: 
      lowlow = self.parameterList.get("Low Low",u.defaultKey)
    if low == u.defaultKey:  
      low = self.parameterList.get("Low",u.defaultKey)
    if high == u.defaultKey:  
      high = self.parameterList.get("High",u.defaultKey)
    if highhigh == u.defaultKey:  
      highhigh = self.parameterList.get("High High",u.defaultKey)
    if exactly == u.defaultKey:  
      exactly = self.parameterList.get("Exactly",u.defaultKey)
    if comparator == u.defaultKey:  
      comparator = self.parameterList.get("Same Value Comparator",u.defaultKey)
    if comparator2 == u.defaultKey:  
      comparator2 = self.parameterList.get("Same Value Comparator 2",u.defaultKey)
    if differenceLow == u.defaultKey:  
      differenceLow = self.parameterList.get("Difference Low",u.defaultKey)
    if differenceHigh == u.defaultKey:  
      differenceHigh = self.parameterList.get("Difference High",u.defaultKey)
    #print("Value = {}, high = {}".format(val, high))
    #valD = Decimal(val)
    #highD = Decimal(high)
    #if valD > highD:
    #  print("Value is > high")
    #if not u.is_number(str(val)): # Then we are not dealing with a number alarm - for now just return false
    if self.parameterList.get(exactlyStr,u.defaultKey) != u.defaultKey: # Then we are not dealing with a number alarm - for now just return false
      #print("ERROR: Assume alarms values can only be numbers for now")
      #if exactly != "NULL" and val != exactly:
      #  self.parameterList["Alarm Status"] = "Exactly"
      #else:
      #  self.parameterList["Alarm Status"] = "OK"
      pass
    elif self.parameterList.get(comparatorStr,u.defaultKey) != u.defaultKey: # Then we are not dealing with a number alarm - for now just return false
      #print("ERROR: Assume alarms values can only be numbers for now")
      pass
    elif self.parameterList.get(comparatorStr2,u.defaultKey) != u.defaultKey: # Then we are not dealing with a number alarm - for now just return false
      #print("ERROR: Assume alarms values can only be numbers for now")
      pass
    else:
      if u.is_number(str(val)):
        val = Decimal(self.parameterList.get("Value",u.defaultKey))
      if u.is_number(str(thresholdValue)):
        thresholdValue = Decimal(self.parameterList.get("Threshold Value",u.defaultKey))
      if u.is_number(str(thresholdLow)):
        thresholdLow = Decimal(self.parameterList.get("Threshold Low",u.defaultKey))
      if u.is_number(str(thresholdHigh)):
        thresholdHigh = Decimal(self.parameterList.get("Threshold High",u.defaultKey))
      if u.is_number(str(threshold2Value)):
        threshold2Value = Decimal(self.parameterList.get("Threshold 2 Value",u.defaultKey))
      if u.is_number(str(threshold2Low)):
        threshold2Low = Decimal(self.parameterList.get("Threshold 2 Low",u.defaultKey))
      if u.is_number(str(threshold2High)):
        threshold2High = Decimal(self.parameterList.get("Threshold 2 High",u.defaultKey))
      #if u.is_number(str(differenceReferenceValue)) and differenceReferenceValue != u.defaultKey:
      #  differenceReferenceValue = Decimal(self.parameterList.get("Difference Reference Value",u.defaultKey))
      if u.is_number(str(lowlow)): # And now check the other ones too
        lowlow = Decimal(self.parameterList.get(lowlowStr,u.defaultKey))
      if u.is_number(str(low)):
        low = Decimal(self.parameterList.get(lowStr,u.defaultKey))
      if u.is_number(str(high)):
        high = Decimal(self.parameterList.get(highStr,u.defaultKey))
      if u.is_number(str(highhigh)):
        highhigh = Decimal(self.parameterList.get(highhighStr,u.defaultKey))
      if u.is_number(str(differenceLow)):
        differenceLow = Decimal(self.parameterList.get(differenceLowStr,u.defaultKey))
      if u.is_number(str(differenceHigh)):
        differenceHigh = Decimal(self.parameterList.get(differenceHighStr,u.defaultKey))
    if val != "NULL":
      if low != "NULL" and u.is_number(low) and u.is_number(val) and val < low:
      #if low != "NULL" and u.is_number(low) and u.is_number(val) and val < "TEST":
      #if low != "NULL":
      #  if u.is_number(low):
      #    if u.is_number(val):
      #      if val < low:
        self.parameterList["Alarm Status"] = lowStr
              #print("Alarm {} Low".format(val))
      elif lowlow != "NULL" and u.is_number(lowlow) and u.is_number(val) and val < lowlow:
        self.parameterList["Alarm Status"] = lowlowStr
      elif high != "NULL" and u.is_number(high) and u.is_number(val) and val > high:
        #print("Updating status to high")
        self.parameterList["Alarm Status"] = highStr
      elif highhigh != "NULL" and u.is_number(highhigh) and u.is_number(val) and val > highhigh:
        self.parameterList["Alarm Status"] = highhighStr
      #elif differenceLow != "NULL" and differenceReferenceValue != "NULL" and val != "NULL" and u.is_number(differenceLow) and u.is_number(val) and u.is_number(differenceReferenceValue) and ((val - differenceReferenceValue) < differenceLow):
      #  self.parameterList["Alarm Status"] = differenceLowStr
      #elif differenceHigh != "NULL" and differenceReferenceValue != "NULL" and val != "NULL" and u.is_number(differenceHigh) and u.is_number(differenceReferenceValue) and u.is_number(val) and ((val - differenceReferenceValue) > differenceHigh):
      #  self.parameterList["Alarm Status"] = differenceHighStr
      elif exactly != "NULL" and val != exactly:
        self.parameterList["Alarm Status"] = exactlyStr
      elif comparator != "NULL" and comparator2 != "NULL" and (val == comparator and val == comparator2): # Comparator wants to check if its not exactly
        # FIXME This assumes the comparator is only ever used for Aq feedback
        self.parameterList["Alarm Status"] = "Value is Static!"
      else:
        self.parameterList["Alarm Status"] = "OK"
      # If the thresholds conditions are NOT met then erase prior alarm status, else let that Alert status propagate forward
      if threshold != u.defaultKey and thresholdValue != u.defaultKey and ((thresholdLow != u.defaultKey and thresholdValue < thresholdLow) or (thresholdHigh != u.defaultKey and thresholdValue > thresholdHigh)):
        self.parameterList["Alarm Status"] = "OK"
        #print("Alarm {} OK, checked against {} = {}. Is < {} threshold, therefore alarm is OK".format(val,threshold,thresholdValue,thresholdLow))
      if threshold2 != u.defaultKey and threshold2Value != u.defaultKey and ((threshold2Low != u.defaultKey and threshold2Value < threshold2Low) or (threshold2High != u.defaultKey and threshold2Value > threshold2High)):
        self.parameterList["Alarm Status"] = "OK"
        #print("Alarm {} OK, checked against {} = {}. Is < {} threshold2, therefore alarm is OK".format(val,threshold2,threshold2Value,threshold2Low))
      if tripCounter != "NULL" and tripLimit != "NULL" and tripCounter < tripLimit and self.parameterList.get("Alarm Status",u.defaultKey) != "OK":
        #print("Not OK: Less than, Trip counter = {}, trip limit = {}".format(tripCounter, tripLimit))
        # The alarm has not surpassed the limit
        self.parameterList["Alarm Status"] = "OK"
        self.parameterList["Trip Counter"] = str(tripCounter + 1)
      elif tripCounter != "NULL" and tripLimit != "NULL" and tripCounter >= tripLimit and self.parameterList.get("Alarm Status",u.defaultKey) != "OK":
        #print("Not OK: Greater than, Trip counter = {}, trip limit = {}".format(tripCounter, tripLimit))
        # The alarm has surpassed the limit
        self.parameterList["Trip Counter"] = str(tripCounter + 1)
      elif tripCounter != "NULL" and tripLimit != "NULL":
        #print("OK: Trip counter = {}, trip limit = {}".format(tripCounter, tripLimit))
        # We have an OK alarm status and should reset the counter
        self.parameterList["Trip Counter"] = "0"
    else:
      val = "NULL"
      self.parameterList["Alarm Status"] = "OK"
    #print("Updated: parameterList = {}".format(self.parameterList))
    if self.parameterList.get("Alarm Status",u.defaultKey) != "OK" and self.parameterList.get("Alarm Status",u.defaultKey) != "Invalid" and self.parameterList.get("Alarm Status",u.defaultKey) != "NULL": # Update global alarm status unless NULL or invalid
      self.alertSound = self.parameterList.get("Alert Sound","7")
      self.alarmSelfStatus = self.parameterList.get("Alarm Status",u.defaultKey)
      # If the alarm is alarming and we aren't in cooldown the update user status
      if self.parameterList.get("Alarm Status",u.defaultKey) != "OK" and self.parameterList.get("User Notify Status",u.defaultKey).split(' ')[0] != "Cooldown":
        self.userNotifySelfStatus = self.parameterList.get("Alarm Status",u.defaultKey)
        self.parameterList["User Notify Status"] = self.parameterList.get("Alarm Status",u.defaultKey)
      self.userSilenceStatus = self.parameterList.get("User Silence Status",u.defaultKey)
      if self.userSilenceStatus != "Silenced":
        self.color = u.red_color
      elif self.userSilenceStatus == "Silenced":
        self.color = u.darkgrey_color # Still indicate that it is off, but not red now
      for k in range(0,len(self.parentIndices)):
        u.recentAlarmButtons[k] = self.parentIndices[k]
      u.recentAlarmButtons[self.column] = self.columnIndex
      return "Not OK"
    else:
      #print("Alarm OK")
      self.alarmSelfStatus = self.parameterList.get("Alarm Status",u.defaultKey)
      #self.userNotifySelfStatus = self.parameterList.get("User Notify Status",u.defaultKey)
      self.alarmStatus = "OK"
      self.color = u.lightgrey_color
      return "OK"

