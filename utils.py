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

def parse_textfile(filename,delim):
  filearray = []
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=delim)
    for row in csv_reader:
      for i in range(len(row)):
        row[i] = int(row[i])
      filearray.append(row)
  return filearray
      
def create_objects(filearray):
  ncolumns = len(filearray[len(filearray)])
  nlines = len(filearray)
  objectList = []
  colRows = []
  line_previous = []
  for i in range(ncolumns):
    objectList.append([]) # Check this
    colRows.append(0)
    line_previous.append("NULL")
  for lineN in range(nlines):
    line = filearray[lineN]
    for column in range(ncolumns):
      if ((line[column] != line_previous[column]) or (line[column] == "NULL")): # This is a new value, so initialize it and store values
        newObject = alarm_object.ALARM_OBJECT # call initializer
        newObject.indexStart = lineN
        newObject.indexEnd = lineN
        newObject.column = column
        newObject.columnIndex = colRow[column]
        newObject.identifier = "Name"
        newObject.value = line[column]
        newObject.add_parameter(identifier,value)
        newObject.color = lightgrey_color
        newObject.alarm_status = green
        objectList[column].append(newObject)
        for indices in range(1,column): # for parent objects grab their index (assuming my parent was the most recently added one to the object list)
          objectList[column][colRow[column]].parent_index[indices]=objectList[indices][objectList[indices].size()].columnIndex
        if column==4:
          objectList[3][parent_index[3]].add_parameter(objectList[4][colRow[4]].value,objectList[5][colRow[5]].value)
        colRow[column] += 1
        for colN in range(column+1,len(line)): # Tell the sub-types not to care if they are repeat values
          line_previous[colN]="NULL"
      else:
        objectList[column][colRow[column]].indexEnd=lineN
      line_previous[column]=line[column]

  return objectList

