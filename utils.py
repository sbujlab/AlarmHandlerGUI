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

recentAlarmButton = -1
camguinIDdict = {
    ("mean","ana"),("integral","ana"),
    ("burst","tree"),("mul","tree"),
    ("asym","prefix"),("diff","prefix"),("yield","prefix")
    }
#void camguin(TString ana = "help", TString tree = "mul", TString branch = "asym_vqwk_04_0ch0", TString leaf = "hw_sum", TString cut = "defaultCuts", Int_t overWriteCut = 0, TString histMode = "defaultHist", Int_t stabilityRing = 0, Int_t runNumber = 0, Int_t splitNumber = -1, Int_t nRuns = -1){

# Cameron Alarm Methods

def parse_textfile(fileArray):
  fileArray.mutex.acquire()
  fileArray.filearray.clear()
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

def append_historyList(HL,OL,key):
  freshAlarm = 1
  localStr = "{}".format(OL.objectList[key].name) 
  for hl in HL.historyList: # Loop over all objects, check to see if they are already in the history, and if so then check their time stamp against right now + wait time
    #print("History time: {}, local time: {}, wait time: {}".format(mktime(hl.get("Time",defaultKey)), mktime(localtime()), HL.timeWait))
    if hl.get("Name",defaultKey) == localStr and hl.get("Time",defaultKey) != "NULL" and mktime(hl.get("Time",defaultKey)) > mktime(localtime()) - HL.timeWait:
      freshAlarm = 0
  if freshAlarm == 1:
    tmpDict = {}
    tmpList = []
    tmpDict["Name"] = localStr
    tmpList.append("Name={}".format(localStr))
    for eachKey, eachItem in OL.objectList[key].parameterList.items():
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
  tmpFolderName = ""
  # Make a new unique name
  if HL.filename.rfind("/") == -1:
    tmpFolderName = "history_saves/" + HL.filename[:HL.filename.find(".csv")]
  else:
    tmpFolderName = HL.filename[:HL.filename.rfind("/")+1] + "history_saves/"
  HL.filename = tmpFolderName + HL.filename[HL.filename.rfind("/"):HL.filename.find(".csv")] + "_Save_{}.csv".format(mktime(localtime())) 
  saveFileName = "Alarms Saved to {}".format(HL.filename)
  print(saveFileName)
  # Save the backup
  write_historyFile(HL) 

  # Clear the current history
  HL.filename = tmpFileStore 
  HL.historyList.clear()
  HL.filearray.clear()
  return saveFileName

# FIXME this is updating alarmlist values into OL - is it even needed - pointer logic?
def update_objectList(OL,alarmList):
  # Loop through column 3 (i = 2) and for each parameterList entry check if all column=4 entries have column3[i] as its parent
  # if it does then update it's child [0].value to be == key result
  # if parameterList key doesn't exist in list of col4 then make a new object and make it have name-value
  for key in alarmList.keys():
    OL.objectList[key] = alarmList[key]

def write_textfile(OL,fileArray):
  print("Writing text file to disk - reading ObjectList")
  fileArray.mutex.acquire()
  try: 
    fileArray.filearray.clear()
    # for each in OL.objectList
    #   define the start and stop indices
    #   find all child columns whose start and stop indices lie within
    #   while that condition is true print from left to right
  
    if len(OL.objectList)>0:
      #print("Printing text file, {} items".format(len(OL.keys)))
      # Ordered write based on ordering in OL.keys - should == ordering of button display
      for Title in OL.keys:
        #print("Key: {}".format(Title))
        for key,item in OL.objectList[Title].parameterList.items():
          entryarray = []
        #  print("Name {} = {}".format(key,item))
          entryarray.append(Title)
          entryarray.append(key)
          entryarray.append(item)
        #  print("TEST: {}".format(entryarray))
          fileArray.filearray.append(entryarray)
    else:
      print("ERROR: No data in memory!")
    outFile = open(fileArray.filename,'w+')
    wr = csv.writer(outFile,delimiter=fileArray.delim)
    filearrayrows=zip(*fileArray.filearray)
    wr.writerows(fileArray.filearray)
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

def silence_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    # For it and its children set alarmStatus = "OK"
    if OL.objectList[OL.keys[j]].userSilenceStatus == "Silenced":
      OL.objectList[OL.keys[j]].userSilenceStatus = "Alert" 
      OL.objectList[OL.keys[j]].parameterList["User Silence Status"] = "Alert"
    elif OL.objectList[OL.keys[j]].userSilenceStatus == "Alert":
      OL.objectList[OL.keys[j]].userSilenceStatus = "Silenced" 
      OL.objectList[OL.keys[j]].parameterList["User Silence Status"] = "Silenced"
      OL.objectList[OL.keys[j]].color = yellow_color
    for q in range(0,len(fileArray.filearray)):
      if fileArray.filearray[q][0] == OL.keys[j]: # Update the filearray too
        if fileArray.filearray[q][1] == "User Silence Status":
          fileArray.filearray[q][2] = OL.objectList[OL.keys[j]].userSilenceStatus
  finally:
    fileArray.mutex.release()

def notify_acknowledge_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    tmpStat = OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')
    if OL.objectList[OL.keys[j]].parameterList.get("Trip Counter",defaultKey) != defaultKey:
      OL.objectList[OL.keys[j]].parameterList["Trip Counter"] = "0"
    if tmpStat[0] == "Cooldown":
      OL.objectList[OL.keys[j]].userNotifyStatus = "OK" # The user is manually OKing this alarm... 
      OL.objectList[OL.keys[j]].parameterList["User Notify Status"] = "OK"
    else:
      # The user is just now acknowledging, therefore start the cooldown
      OL.objectList[OL.keys[j]].userNotifyStatus = "Cooldown {}".format(int(OL.cooldownLength))
      OL.objectList[OL.keys[j]].parameterList["User Notify Status"] = "Cooldown {}".format(int(OL.cooldownLength))
      OL.objectList[OL.keys[j]].color = orange_color
    for q in range(0,len(fileArray.filearray)):
      if fileArray.filearray[q][0] == OL.keys[j]: # Update the filearray too
        if fileArray.filearray[q][1] == "User Notify Status":
          fileArray.filearray[q][2] = OL.objectList[OL.keys[j]].userNotifyStatus
  finally:
    fileArray.mutex.release()

# FIXME not currently in use outside of depreciated "expert" mode tab
def edit_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    tmpStat = OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')
    # butMenu.editValue
    OL.objectList[OL.keys[j]].parameterList["Value"] = butMenu.editValue
    OL.objectList[OL.keys[j]].value = butMenu.editValue
    for q in range(0,len(fileArray.filearray)):
      if fileArray.filearray[q][0] == key: # Update the filearray too
        if fileArray.filearray[q][1] == "Value":
          fileArray.filearray[q][2] = OL.objectList[OL.keys[j]].value
  finally:
    fileArray.mutex.release()

def subshift(L, start, end, insert_at):
  temp = L[start:end]
  L = L[:start] + L[end:]
  return L[:insert_at] + temp + L[insert_at:]

# FIXME FIXME Start Here FIXME FIXME this method should change for a new OL technique - just change the OL data and let the fileArray printer read OL and continue
def move_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    mvN = butMenu.moveN
    # FIXME do some things here:
    # 1) Shift OL.keys[j] to j+mvN
    # 2) Shift Button Array entry j to j+mvN
    # 3) Find filearray index q where j'th key'd OL item begins and how many elements it has for file_ind_start and stop

    # Shift fileArray down by moveN, make it == the values at tmpFA[moveNind][i]
    # Shift fileArray[+moveNind] up by size of moved bit
    # FIXME file_ind_start = OL.objectList[i][j].indexStart
    # FIXME file_ind_stop = OL.objectList[i][j].indexEnd
    #print("col {}, entry {}, move by {}, start file ind {}, end file ind {}, position to plant into {}".format(i,j,mvN,file_ind_start,file_ind_stop,OL.objectList[i][j+mvN].indexEnd))
    #if mvN>0:
      #FIXME fileArray.filearray = subshift(fileArray.filearray,file_ind_start,file_ind_stop+1,OL.objectList[i][j+mvN].indexEnd-(file_ind_stop-file_ind_start))
    #if mvN<0:
      #FIXME fileArray.filearray = subshift(fileArray.filearray,file_ind_start,file_ind_stop+1,OL.objectList[i][j+mvN].indexStart)
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

# FIXME FIXME this method should change for a new OL technique
def copy_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    copyN = butMenu.copyName
    copyFileArray = []
    # FIXME file_ind_start = OL.objectList[i][j].indexStart
    # FIXME file_ind_stop = OL.objectList[i][j].indexEnd
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

# FIXME FIXME this method should change for a new OL technique
def delete_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    # FIXME file_ind_start = OL.objectList[i][j].indexStart
    # FIXME file_ind_stop = OL.objectList[i][j].indexEnd
    for k in range(file_ind_start,file_ind_stop+1): # +1 is so it will do the first one if both ==
      del fileArray.filearray[file_ind_start]
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

# FIXME FIXME this method should change for a new OL technique
def add_filearray_menu(OL,fileArray,butMenu):
  fileArray.mutex.acquire()
  try:
    i,j = butMenu.indices
    # FIXME file_ind = OL.objectList[i][j].indexEnd+1
    addedLine = []
    #for parent in range(0,i):
      #addedLine.append(OL.objectList[parent][OL.activeObjectColumnIndicesList[parent]].value)
      ######addedLine.append(OL.objectList[parent][OL.selectedButtonColumnIndicesList[parent]].value)
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
      print("Writing file array to disk - generic")
  finally:
    fileArray.mutex.release()
    return fileArray.filearray

def create_objects(fileArray,cooldownLength):
  ncolumns = 0
  if len(fileArray.filearray)>0: 
    ncolumns = len(fileArray.filearray[len(fileArray.filearray)-1]) # FIXME should this just be hardcoded to 3 layers or should I keep it generic??
  nlines = len(fileArray.filearray)
  if fileArray.filearray == [] or fileArray.filearray == [[]] or fileArray.filearray == None:
    nlines = 0
    ncolumns = 0 # Sanity Check
    print("Error: Empty alarm file given to Parity Alarm Handler")
    return None
  localObjectList = {}
  for lineN in range(0,nlines):
    line = fileArray.filearray[lineN]
    if len(line) != ncolumns:
      print("Error, line {} = {} has the wrong number of entries for alarm handling parsing".format(lineN,line))
      return None
    if line[0] not in localObjectList.keys():
      newObject = alarm_object.ALARM_OBJECT() # call initializer
      newObject.name = line[0]
      localObjectList[line[0]] = newObject
    localObjectList[line[0]].parameterList[line[1]]=line[2] # Set object named line[0] parameter named line[1] equal to value held in line[2]
  for key in localObjectList.keys():
    localObjectList[key].polish_alarm_object()
    #localObjectList[key].alarm = alarm_object.ALARM(localObjectList[key]) # NEW ALARM defined here per new object in middle column
  return localObjectList

def create_objects_keys(fileArray):
  ncolumns = 0
  if len(fileArray.filearray)>0: 
    ncolumns = len(fileArray.filearray[len(fileArray.filearray)-1]) # FIXME should this just be hardcoded to 3 layers or should I keep it generic??
  nlines = len(fileArray.filearray)
  if fileArray.filearray == [] or fileArray.filearray == [[]] or fileArray.filearray == None:
    nlines = 0
    ncolumns = 0 # Sanity Check
    print("Error: Empty alarm file given to Parity Alarm Handler")
    return None
  localKeyDict = {}
  localKeyList = []
  for lineN in range(0,nlines):
    line = fileArray.filearray[lineN]
    if len(line) != ncolumns:
      print("Error, line {} = {} has the wrong number of entries for alarm handling parsing".format(lineN,line))
      return None
    if line[0] not in localKeyDict.keys():
      localKeyDict[line[0]] = line[0]
      localKeyList.append(line[0])
  return localKeyList
  
# FIXME is this method OK? Appears to be actually
def update_extra_filearray(fileArray,extraFileArray):
  # Update the extra file array with whatever contents it happens to have on disk at the moment
  extraFileArray = alarm_object.FILE_ARRAY(extraFileArray.filename,extraFileArray.delim)
  fileArray.mutex.acquire()
  try: 
    if extraFileArray != None and len(extraFileArray.filearray) != 0:
      nColumns = len(extraFileArray.filearray[0])
      if nColumns != 0: # Then we have the correct format
        for i in range (0,len(extraFileArray.filearray)): # Check each line of extra array
          print("Reading extra fileArray {}, line {} = {}".format(extraFileArray.filename,i,extraFileArray.filearray[i]))
          # Check original file for contents matching comparison file, if first (nColumns-1) columns can find a match then update, if not then append into the section with first (nColumns-2)/2/1 columns
          edittedEntry = False
          insertSpot = len(fileArray.filearray)
          for j in range (0,len(extraFileArray.filearray[i])-1):
            filled = [-1] * (nColumns-1)
            for k in range (0,len(fileArray.filearray)): # Check each line of original array
              if len(fileArray.filearray[k])>j and extraFileArray.filearray[i][j] == fileArray.filearray[k][j]: 
                # Then this entry has already been included in the main object list
                #print("Entry in extra fileArray {} being overwritten, line {} = {}".format(extraFileArray.filearray[i][j],i,extraFileArray.filearray[i]))
                #print("fileArray.filearay[{}] contains {}".format(k,extraFileArray.filearray[i][j]))
                if extraFileArray.filearray[i][0:(nColumns-1)] == fileArray.filearray[k][0:(nColumns-1)]: # only update for the case that I'm exactly replacing
                  fileArray.filearray[k][(nColumns-1)] = extraFileArray.filearray[i][(nColumns-1)] 
                  edittedEntry = True
                if extraFileArray.filearray[i][0:(nColumns-2)] == fileArray.filearray[k][0:(nColumns-2)]:
                  insertSpot = k+1 # Update insertSpot for each entry with (nColumns-2)th level ana name matching
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

