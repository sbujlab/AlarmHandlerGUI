'''
Green Monster GUI Revamp
Utilities for the whole program
Code Commissioned 2019-01-16
Code by A.J. Zec
Alarm Handler GUI spinoff
Cameron Clarke 2019-05-28
'''
import tkinter as tk
from ctypes import cdll
import subprocess, os
import csv
import alarm_object

green_color = '#3C8373'
lightgrey_color = '#E0E0E0'
grey_color = '#C0C0C0'

SOCK_OK = 0; SOCK_ERROR = -1

COMMAND_HAPTB = 1000; COMMAND_BMW = 2000
COMMAND_FDBK = 3000; COMMAND_HAPADC = 4000
COMMAND_SCAN = 5000; COMMAND_ALARM = 6000
COMMAND_VQWK = 7000

Crate_CH   = 0; Crate_LHRS = 1
Crate_RHRS = 2; Crate_INJ  = 3
Crate_Test = 4

def set_text(entry, text):
  entry.delete(0, tk.END)
  entry.insert(0, str(text))
  return entry

def pass_params_to_c():
  f = open('transfer.txt', 'w+')
  f.write('This is the message\n')
  f.write('And the reply')
  f.close()

  lib = cdll.LoadLibrary('./libs/libTestClass.so')
  obj = lib.init(2, 4000, 4006, 423, 5493, 585)
  lib.print_params(obj)
  
def send_command(crate_num, packet):
  lib = cdll.LoadLibrary('cfSock/libcfSockCli.so')

  f = open('transfer.txt', 'w+')
  for i in  range(5, 7):
    f.write(str(packet[i]) + '\n')
  f.close()

  err_flag = lib.GMSockCommand(crate_num, packet[0], packet[1], packet[2], packet[3], packet[4])

  ind = 0; reply = []
  fin = open('reply.txt')
  for line in fin.readlines():
    if ind < 5: reply += [int(line)]
    else: reply += [str(line)]
    ind += 1
  fin.close()

  os.remove('reply.txt')

  return err_flag, reply 
  


# Cameron Alarm Methods

#def parse_textfile(fAlarmHandler):
#  fAlarmHandler.filearray = []
#  with open(fAlarmHandler.filename) as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter=fAlarmHandler.delim)
#    for row in csv_reader:
#      fAlarmHandler.filearray.append(row)
#  #return filearray

def create_objects(filearray):
  #ncolumns = len(filearray[0]) # FIXME array 0?
  ncolumns = len(filearray[len(filearray)-1]) # FIXME array 0?
  nlines = len(filearray)
  objectList = []
  colRow = []
  line_previous = []
  for i in range(0,ncolumns):
    objectList.append([]) # Check this
    colRow.append(0)
    line_previous.append("NULL")
  for lineN in range(0,nlines):
    line = filearray[lineN]
    isnew = 0
    for column in range(0,ncolumns):
      if (isnew == 1 or (line[column] != line_previous[column]) or (line[column] == "NULL")): # This is a new value, so initialize it and store values
        isnew = 1
        colRow[column] += 1
        newObject = alarm_object.ALARM_OBJECT() # call initializer
        newObject.indexStart = lineN
        newObject.indexEnd = lineN
        newObject.parentIndices = []
        newObject.column = column
        newObject.columnIndex = colRow[column]-1
        newObject.identifier = "Name"
        newObject.value = line[column]
        newObject.add_parameter(newObject.identifier,newObject.value)          # FIXME having its own name in its parameter list is probably not needed....
        newObject.add_parameter_history(newObject.identifier,newObject.value)
        newObject.color = lightgrey_color
        newObject.alarm_status = 0
        objectList[column].append(newObject)
        if column != 0:
          for indices in range(0,column): # for parent objects grab their index (assuming my parent was the most recently added one to the object list)
            objectList[column][colRow[column]-1].parentIndices.append(0)
            objectList[column][colRow[column]-1].parentIndices[indices] = objectList[indices][len(objectList[indices])-1].columnIndex
        # FIXME try to find a way to catalogue the following children in a level 2 object
        if (column==4 and isnew==1):
          objectList[2][objectList[column][colRow[2]-1].parentIndices[2]].add_parameter(objectList[3][colRow[3]-1].value,objectList[4][colRow[4]-1].value)
          objectList[2][objectList[column][colRow[2]-1].parentIndices[2]].add_parameter_history(objectList[3][colRow[3]-1].value,objectList[4][colRow[4]-1].value)
          #objectList[2][colRow[2]-1].add_parameter(objectList[3][colRow[3]-1].value,objectList[4][colRow[4]-1].value)
        if (column==4 and isnew!=1):
          objectList[2][objectList[column][colRow[2]-1].parentIndices[2]].add_parameter_history(objectList[3][colRow[3]-1].value,objectList[4][colRow[4]-1].value)
        #for colN in range(column+1,len(line)): # Tell the sub-types not to care if they are repeat values
        #  line_previous[colN]="NULL"
      else:
        objectList[column][colRow[column]-1].indexEnd=lineN
      line_previous[column]=line[column]
  return objectList
  

def add_object(objList,coli):
  colLen = len(objList[coli])
  lastIndexCol = objList[coli][colLen-1].indexEnd
  newObject = alarm_object.ALARM_OBJECT()
  newObject.indexStart = lastIndexCol+1
  newObject.indexEnd = lastIndexCol+1
  newObject.column = coli
  newObject.columnIndex = colLen-1
  # objList.write_object(newObject) # fixme - do this method next
  objList[coli].append(newObject)

def alarm_loop():
  pass
  # Loop over the global objectData and call data updating methods
