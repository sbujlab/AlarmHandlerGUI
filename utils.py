'''
Green Monster GUI Revamp
Utilities for the whole program
Code Commissioned 2019-01-16
Code by A.J. Zec
Alarm Handler GUI spinoff
Cameron Clarke 2019-05-28
'''
import tkinter as tk
import subprocess, os
import csv
import alarm_object
from time import gmtime, strftime, localtime, strptime, mktime
from distutils.util import strtobool

green_color = '#3C8373'
lightgrey_color = '#E0E0E0'
lightergrey_color = '#E7E7E7'
grey_color = '#C0C0C0'
darkgrey_color = '#909090' # Maybe swap this for yellow everywhere?
red_button_color = '#9E1A1A'
red_color = '#ff0000'
yellow_color = '#ffff00'
orange_color = '#ff8800'
green_color = '#00ff00'
black_color = '#000000'
white_color = '#ffffff'
defaultKey = "NULL"

recentAlarmButtons = [-1,-1,-1,-1,-1]
camguinIDdict = {
    ("mean","ana"),("integral","ana"),
    ("burst","tree"),("mul","tree"),
    ("asym","prefix"),("diff","prefix"),("yield","prefix")
    }
#void camguin(TString ana = "help", TString tree = "mul", TString branch = "asym_vqwk_04_0ch0", TString leaf = "hw_sum", TString cut = "defaultCuts", Int_t overWriteCut = 0, TString histMode = "defaultHist", Int_t stabilityRing = 0, Int_t runNumber = 0, Int_t splitNumber = -1, Int_t nRuns = -1){

# Cameron Alarm Methods

def parse_textfile(fileArray):
  fileArray.mutex.acquire()
  fileArray.filearray = []
  try:
    with open(fileArray.filename) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=fileArray.delim)
      for row in csv_reader:
        rowList = []
        for col in row:
          rowList.append(col)
        fileArray.filearray.append(rowList)
  except IOError:
    print("Error, no textfile {} found".format(fileArray.filename))
    return []
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

def parse_config(fa):
  fa.mutex.acquire()
  try:
    for each in fa.filearray:
      # Assume the conf file is all single entries per line, '=' separated
      if len(each)==2:
        eachKey = each[0].replace(' ','')
        eachVal = each[1].replace(' ','')
        fa.conf[eachKey] = eachVal
  finally:
    fa.mutex.release()


def update_config(alarmHandlerGUI):
  alarmHandlerGUI.filename = alarmHandlerGUI.conf.conf.get('alarmFilename',defaultKey)
  alarmHandlerGUI.histfilename = alarmHandlerGUI.conf.conf.get('historyFilename',defaultKey)
  alarmHandlerGUI.externalFilename = alarmHandlerGUI.conf.conf.get('externalFilename',defaultKey) # FIXME: make this a list to iterate through
  alarmHandlerGUI.externalParameterFileStaleTime = float(alarmHandlerGUI.conf.conf.get('staleExternalTime',defaultKey))
  alarmHandlerGUI.timeWait = int(alarmHandlerGUI.conf.conf.get('timeWaitHistory',defaultKey))
  alarmHandlerGUI.cooldownLength = int(alarmHandlerGUI.conf.conf.get('alarmCooldownTime',defaultKey))
  alarmHandlerGUI.remoteName = alarmHandlerGUI.conf.conf.get('remoteSoundServer',defaultKey)
  alarmHandlerGUI.showGrid = bool(strtobool(alarmHandlerGUI.conf.conf.get('showGrid',defaultKey)))
  alarmHandlerGUI.alertTheUser = bool(strtobool(alarmHandlerGUI.conf.conf.get('turnSoundOn',defaultKey)))
  alarmHandlerGUI.alertTheUserSound = alarmHandlerGUI.conf.conf.get('defaultAlertSound',defaultKey)
  alarmHandlerGUI.alertTheUserSoundNow = alarmHandlerGUI.conf.conf.get('defaultAlertSound',defaultKey)
  alarmHandlerGUI.includeExpert = bool(strtobool(alarmHandlerGUI.conf.conf.get('includeExpertPage',defaultKey)))

def write_conf(conf):
  outFile = open(conf.get("alarmConfig",defaultKey) ,'w+')
  wr = csv.writer(outFile,delimiter='=')
  outArray = []
  for key, each in conf.items():
    localAr = []
    key = key + "                          "
    key = key[:20]
    localAr.append(key)
    localAr.append(" "+each)
    outArray.append(localAr)
  if len(conf)!=0:
    filearrayrows=zip(*conf)
    wr.writerows(outArray)

def init_historyList(HL):
  tmpHistList = []
  for each in HL.filearray:
    tmpDict = {}
    for entry in each:
      #print(entry)
      entryPair1, entryPair2 = entry.split(HL.paramDelim,1)
      if entryPair1 == "Time":
        entryPair2 = entryPair2.replace(' ','')
        tmpTimeList = entryPair2[entryPair2.find("(")+1:entryPair2.find(")")]
        tmpTimeList = tmpTimeList.split(',')
        tmpTimeMap = {}
        for ents in tmpTimeList:
          #print(ents)
          a, b = ents.split('=')
          tmpTimeMap[a] = b
        tmpDict[entryPair1] = strptime("{}-{}-{} {}:{}:{}".format(tmpTimeMap["tm_year"],tmpTimeMap["tm_mon"],tmpTimeMap["tm_mday"],tmpTimeMap["tm_hour"],tmpTimeMap["tm_min"],tmpTimeMap["tm_sec"]),"%Y-%m-%d %H:%M:%S")
      else:
        tmpDict[entryPair1] = entryPair2 
    tmpHistList.append(tmpDict)
  return tmpHistList

def append_historyList(HL,OL,i):
  freshAlarm = 1
  localStr = "{}, {}, {}".format(OL.objectList[0][OL.objectList[2][i].parentIndices[0]].value,OL.objectList[1][OL.objectList[2][i].parentIndices[1]].value[:25],OL.objectList[2][i].value[:35]) # FIXME there are better ways to do this...
  for hl in HL.historyList: # Loop over all objects, check to see if they are already in the history, and if so then check their time stamp against right now + wait time
    #print("History time: {}, local time: {}, wait time: {}".format(mktime(hl.get("Time",defaultKey)), mktime(localtime()), HL.timeWait))
    if hl.get("Name",defaultKey) == localStr and hl.get("Time",defaultKey) != "NULL" and mktime(hl.get("Time",defaultKey)) > mktime(localtime()) - HL.timeWait:
      freshAlarm = 0
  if freshAlarm == 1:
    tmpDict = {}
    tmpList = []
    tmpDict["Name"] = localStr
    tmpList.append("Name={}".format(localStr))
    for eachKey, eachItem in OL.objectList[2][i].parameterList.items():
      tmpDict[eachKey] = eachItem
      tmpList.append("{}={}".format(eachKey,eachItem))
    tmpDict["Time"] = localtime()
    tmpList.append("Time={}".format(localtime()))
    HL.historyList.append(tmpDict)
    HL.filearray.append(tmpList)

def write_historyFile(HL):
  outFile = open(HL.filename,'w+')
  wr = csv.writer(outFile,delimiter=HL.delim)
  if len(HL.filearray)!=0:
    filearrayrows=zip(*HL.filearray)
    wr.writerows(HL.filearray)
    return HL.filearray

def backup_clear_hist(HL):
  tmpFileStore = HL.filename
  # Make a new unique name
  tmpFolderName = HL.filename[:HL.filename.rfind("/")+1] + "history_saves"
  HL.filename = tmpFolderName + HL.filename[HL.filename.rfind("/"):HL.filename.find(".csv")] + "_Save_{}.csv".format(mktime(localtime())) 
  saveFileName = "Alarms Saved to {}".format(HL.filename)
  print(saveFileName)
  # Save the backup
  write_historyFile(HL) 

  # Clear the current history
  HL.filename = tmpFileStore 
  HL.historyList = []
  HL.filearray = []
  return saveFileName

# FIXME this is updating alarmlist values into OL
def update_objectList(OL,alarmList):
  # Loop through column 3 (i = 2) and for each parameterList entry check if all column=4 entries have column3[i] as its parent
  # if it does then update it's child [0].value to be == key result
  # if parameterList key doesn't exist in list of col4 then make a new object and make it have name-value
  for key in alarmList.keys():
    OL.objectList[key] = alarmList[key]

# FIXME this method should change for a new OL technique
def write_textfile(OL,fileArray):
  print("Writing text file to disk")
  fileArray.mutex.acquire()
  try: 
    fileArray.filearray = []
    # for each in OL.objectList
    #   define the start and stop indices
    #   find all child columns whose start and stop indices lie within
    #   while that condition is true print from left to right
  
    if len(OL.objectList)>1:
      i = len(OL.objectList)-1 # i = 5-1 = 4, last column
      for j in range(0,len(OL.objectList[i])): # Take the 5th column and make entries out of all of its parents values, in sequence
        entryarray = []
        parents = OL.objectList[i][j].parentIndices
        for k in range(0,len(parents)):
          entryarray.append(OL.objectList[k][parents[k]].value)
        entryarray.append(OL.objectList[i][j].value)
        fileArray.filearray.append(entryarray)
    outFile = open(fileArray.filename,'w+')
    wr = csv.writer(outFile,delimiter=fileArray.delim)
    filearrayrows=zip(*fileArray.filearray)
    wr.writerows(fileArray.filearray)
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

# Depreciated EXPERT mode command this method should change for a new OL technique

# FIXME this method should change for a new OL technique
def silence_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    # For it and its children set alarmStatus = "OK"
    if OL.objectList[i][j].userSilenceStatus == "Silenced":
      OL.objectList[i][j].userSilenceStatus = "Alert" 
      #OL.objectList[i][j].alarm.userSilenceSelfStatus = "Alert" 
      OL.objectList[2][j].parameterList["User Silence Status"] = "Alert"
    elif OL.objectList[i][j].userSilenceStatus == "Alert":
      OL.objectList[i][j].userSilenceStatus = "Silenced" 
      #OL.objectList[i][j].alarm.userSilenceSelfStatus = "Silenced" 
      OL.objectList[2][j].parameterList["User Silence Status"] = "Silenced"
      OL.objectList[i][j].color = yellow_color
    for q in range(OL.objectList[i][j].indexStart,OL.objectList[i][j].indexEnd+1):
      if fileArray.filearray[q][3] == "User Silence Status": # Update the filearray too
        fileArray.filearray[q][4] = OL.objectList[i][j].userSilenceStatus
  finally:
    fileArray.mutex.release()

# FIXME this method should change for a new OL technique
def notify_acknowledge_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    tmpStat = OL.objectList[i][j].userNotifyStatus.split(' ')
    if OL.objectList[i][j].parameterList.get("Trip Counter",defaultKey) != "NULL":
      OL.objectList[i][j].parameterList["Trip Counter"] = "0"
    if tmpStat[0] == "Cooldown":
      OL.objectList[i][j].userNotifyStatus = "OK" # The user is manually OKing this alarm... 
      OL.objectList[i][j].parameterList["User Notify Status"] = "OK"
      #OL.objectList[i][j].alarm.userNotifySelfStatus = "OK"
    else:
      # The user is just now acknowledging, therefore start the cooldown
      OL.objectList[i][j].userNotifyStatus = "Cooldown {}".format(int(OL.cooldownLength))
      OL.objectList[i][j].parameterList["User Notify Status"] = "Cooldown {}".format(int(OL.cooldownLength))
      #OL.objectList[i][j].alarm.userNotifySelfStatus = "Cooldown {}".format(int(OL.cooldownLength))
      #OL.objectList[i][j].color = yellow_color
    for q in range(OL.objectList[i][j].indexStart,OL.objectList[i][j].indexEnd+1):
      if fileArray.filearray[q][3] == "User Notify Status": # Update the filearray too
        #print("Printing to filearray[{}][{}] User Notify Status = {}".format(q,4,OL.objectList[i][j].userNotifyStatus))
        fileArray.filearray[q][4] = OL.objectList[i][j].userNotifyStatus
  finally:
    fileArray.mutex.release()

# FIXME this method should change for a new OL technique
def edit_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    file_ind_start = OL.objectList[i][j].indexStart
    file_ind_stop = OL.objectList[i][j].indexEnd
    for k in range(file_ind_start,file_ind_stop+1): # +1 is so it will do the first one if both ==
      fileArray.filearray[k][i] = butMenu.editValue # i is the column... where our data word exists
  finally:
    fileArray.mutex.release
    return fileArray.filearray

def subshift(L, start, end, insert_at):
  temp = L[start:end]
  L = L[:start] + L[end:]
  return L[:insert_at] + temp + L[insert_at:]

# FIXME this method should change for a new OL technique - just change the OL data and let the fileArray printer read OL and continue
def move_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    mvN = butMenu.moveN
    # Shift fileArray down by moveN, make it == the values at tmpFA[moveNind][i]
    # Shift fileArray[+moveNind] up by size of moved bit
    file_ind_start = OL.objectList[i][j].indexStart
    file_ind_stop = OL.objectList[i][j].indexEnd
    #print("col {}, entry {}, move by {}, start file ind {}, end file ind {}, position to plant into {}".format(i,j,mvN,file_ind_start,file_ind_stop,OL.objectList[i][j+mvN].indexEnd))
    #inplace_shift(fileArray.filearray,file_ind_start,file_ind_stop-file_ind_start+1,file_ind_distance+file_ind_start)
    if mvN>0:
      #fileArray.filearray = subshift(fileArray.filearray,file_ind_start,file_ind_stop+1,OL.objectList[i][j+mvN].indexEnd)
      fileArray.filearray = subshift(fileArray.filearray,file_ind_start,file_ind_stop+1,OL.objectList[i][j+mvN].indexEnd-(file_ind_stop-file_ind_start))
    if mvN<0:
      fileArray.filearray = subshift(fileArray.filearray,file_ind_start,file_ind_stop+1,OL.objectList[i][j+mvN].indexStart)
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

# FIXME this method should change for a new OL technique
def copy_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    copyN = butMenu.copyName
    copyFileArray = []
    file_ind_start = OL.objectList[i][j].indexStart
    file_ind_stop = OL.objectList[i][j].indexEnd
    #print("col {}, entry {}, copy newName = {}, start file ind {}, end file ind {}".format(i,j,copyN,file_ind_start,file_ind_stop))
    if copyN != None:
      for l in range(file_ind_start,file_ind_stop+1):
        copyFileArray.append(fileArray.filearray[l].copy())
      for h in range(0,len(copyFileArray)):
        copyFileArray[h][i] = copyN
    for k in reversed(range(0,len(copyFileArray))):
      fileArray.filearray.insert(file_ind_stop+1,copyFileArray[k])
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

# FIXME this method should change for a new OL technique
def delete_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    file_ind_start = OL.objectList[i][j].indexStart
    file_ind_stop = OL.objectList[i][j].indexEnd
    for k in range(file_ind_start,file_ind_stop+1): # +1 is so it will do the first one if both ==
      del fileArray.filearray[file_ind_start]
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

# FIXME this method should change for a new OL technique
def add_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    file_ind = OL.objectList[i][j].indexEnd+1
    addedLine = []
    for parent in range(0,i):
      addedLine.append(OL.objectList[parent][OL.activeObjectColumnIndicesList[parent]].value)
      #addedLine.append(OL.objectList[parent][OL.selectedButtonColumnIndicesList[parent]].value)
    for child in range(i,len(OL.objectList)):
      addedLine.append("NULL")
    fileArray.filearray.insert(file_ind,addedLine)
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

def write_filearray(fileArray):
  fileArray.mutex.acquire()
  try:
    outFile = open(fileArray.filename,'w+')
    wr = csv.writer(outFile,delimiter=fileArray.delim)
    if len(fileArray.filearray)!=0:
      filearrayrows=zip(*fileArray.filearray)
      wr.writerows(fileArray.filearray)
      print("Writing file array to disk")
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

# FIXME FIXME this method needs to change a lot to use a streamlined object and OL definition
def create_objects(fileArray,cooldownLength):
  ncolumns = 0
  if len(fileArray.filearray)>0: 
    ncolumns = len(fileArray.filearray[len(fileArray.filearray)-1]) # FIXME should this just be hardcoded to 5 layers or should I keep it generic??
  nlines = len(fileArray.filearray)
  if fileArray.filearray == [] or fileArray.filearray == [[]] or fileArray.filearray == None:
    nlines = 0
    ncolumns = 0 # Sanity Check
    print("Error: Empty alarm file given to Parity Alarm Handler")
  localObjectList = {}
  for lineN in range(0,nlines):
    line = fileArray.filearray[lineN]
    if len(line) != ncolumns:
      print("Error, line {} = {} has the wrong number of entries for alarm handling parsing".format(lineN,line))
      return None
    if line[0] is not in localObjectList.keys():
      newObject = alarm_object.ALARM_OBJECT() # call initializer
      localObjectList[line[0]] = newObject
    localObjectList[line[0]].parameterList[line[1]]=line[2] # Set object named line[0] parameter named line[1] equal to value held in line[2]
  for key in localObjectList.keys():
    # FIXME uses ALARM_OBJECT to declare an ALARM... why???
    # FIXME FIXME should probably have a call to a method to polish alarm to read parameterList and fill the gaps based on alarm's necessary logics
    localObjectList[key].polish_alarm_object()
    #localObjectList[key].alarm = alarm_object.ALARM(localObjectList[key]) # NEW ALARM defined here per new object in middle column
  return localObjectList


def create_objects_keys(fileArray):
  nlines = len(fileArray.filearray)
  if fileArray.filearray == [] or fileArray.filearray == [[]] or fileArray.filearray == None:
    nlines = 0
    ncolumns = 0 # Sanity Check
    print("Error: Empty alarm file given to Parity Alarm Handler")
  localKeyDict = {}
  localKeyList = []
  for lineN in range(0,nlines):
    line = fileArray.filearray[lineN]
    if len(line) != ncolumns:
      print("Error, line {} = {} has the wrong number of entries for alarm handling parsing".format(lineN,line))
      return None
    if line[0] is not in localKeyDict.keys():
      localKeyDict[line[0]] = line[0]
      localKeyList.append(line[0])
  return localKeyList
  
# FIXME is this method OK? Appears to be actually
def update_extra_filearray(fileArray,extraFileArray):
  # Update the extra file array with whatever contents it happens to have on disk at the moment
  extraFileArray = alarm_object.FILE_ARRAY(extraFileArray.filename,extraFileArray.delim)
  fileArray.mutex.acquire()
  try: 

    if extraFileArray != None: # Then we have the correct format
      for i in range (0,len(extraFileArray.filearray)): # Check each line of extra array
        print("Reading extra fileArray {}, line {} = {}".format(extraFileArray.filename,i,extraFileArray.filearray[i]))
        # Check original file for contents matching comparison file, if first 4 columns can find a match then update, if not then append into the section with first 3/2/1 columns
        edittedEntry = False
        insertSpot = len(fileArray.filearray)
        for j in range (0,len(extraFileArray.filearray[i])-1):
          filled = [-1] * 4
          for k in range (0,len(fileArray.filearray)): # Check each line of original array
            if len(fileArray.filearray[k])>j and extraFileArray.filearray[i][j] == fileArray.filearray[k][j]: 
              # Then this entry has already been included in the main object list
              #print("Entry in extra fileArray {} being overwritten, line {} = {}".format(extraFileArray.filearray[i][j],i,extraFileArray.filearray[i]))
              #print("fileArray.filearay[{}] contains {}".format(k,extraFileArray.filearray[i][j]))
              if extraFileArray.filearray[i][0:4] == fileArray.filearray[k][0:4]: # only update for the case that I'm exactly replacing
                fileArray.filearray[k][4] = extraFileArray.filearray[i][4] 
                edittedEntry = True
              if extraFileArray.filearray[i][0:3] == fileArray.filearray[k][0:3]:
                insertSpot = k+1 # Update insertSpot for each entry with 3th level ana name matching
          if edittedEntry == False:
            if insertSpot == len(fileArray.filearray):
              #print("Appending {} below {}".format(extraFileArray.filearray[i],fileArray.filearray[len(fileArray.filearray)-1]))
              fileArray.filearray.append(extraFileArray.filearray[i])
            else:
              fileArray.filearray.insert(insertSpot,extraFileArray.filearray[i])
              #print("Inserting {} below {}".format(extraFileArray.filearray[i],fileArray.filearray[indices[x]]))
  finally:
    fileArray.mutex.release()

def is_number(s):
  try:
    complex(s) # for int, long, float and complex
  except ValueError:
    return False
  return True

