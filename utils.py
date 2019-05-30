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

green_color = '#3C8373'
lightgrey_color = '#E0E0E0'
grey_color = '#C0C0C0'

# Cameron Alarm Methods

def parse_textfile(filename,delim):
  filearray = []
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=delim)
    for row in csv_reader:
      rowList = []
      for col in row:
        rowList.append(col)
      filearray.append(rowList)
  return filearray

def write_textfile(OL,filename,delim):
  filearray = []
  # for each in OL.objectList
  #   define the start and stop indices
  #   find all child columns whose start and stop indices lie within
  #   while that condition is true print from left to right
  if len(OL.objectList)>1:
    i = len(OL.objectList)-1
    for j in range(0,len(OL.objectList[i])): # Take the 5th column and make objects out of all of its parents, in sequence
      entryarray = []
      parents = OL.objectList[i][j].parentIndices
      for k in range(0,len(parents)):
        entryarray.append(OL.objectList[k][parents[k]].value)
      entryarray.append(OL.objectList[i][j].value)
      filearray.append(entryarray)
  outFile = open(filename,'w+')
  wr = csv.writer(outFile,delimiter=delim)
  filearrayrows=zip(*filearray)
  wr.writerows(filearray)
  return filearray

def create_objects(filearray):
  ncolumns = 5
  #if len(filearray)>0: 
  #  ncolumns = len(filearray[len(filearray)-1]) # FIXME should this just be hardcoded to 5 layers or should I keep it generic??
  nlines = len(filearray)
  localObjectList = []
  colRow = []
  line_previous = []
  for i in range(0,ncolumns):
    localObjectList.append([]) # Check this
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
        localObjectList[column].append(newObject)
        if column != 0:
          for indices in range(0,column): # for parent objects grab their index (assuming my parent was the most recently added one to the object list)
            localObjectList[column][colRow[column]-1].parentIndices.append(0)
            localObjectList[column][colRow[column]-1].parentIndices[indices] = localObjectList[indices][len(localObjectList[indices])-1].columnIndex
        # FIXME try to find a way to catalogue the following children in a level 2 object
        if (column==4 and isnew==1):
          localObjectList[2][localObjectList[column][colRow[2]-1].parentIndices[2]].add_parameter(localObjectList[3][colRow[3]-1].value,localObjectList[4][colRow[4]-1].value)
          localObjectList[2][localObjectList[column][colRow[2]-1].parentIndices[2]].add_parameter_history(localObjectList[3][colRow[3]-1].value,localObjectList[4][colRow[4]-1].value)
          #localObjectList[2][colRow[2]-1].add_parameter(localObjectList[3][colRow[3]-1].value,localObjectList[4][colRow[4]-1].value)
        if (column==4 and isnew!=1):
          localObjectList[2][localObjectList[column][colRow[2]-1].parentIndices[2]].add_parameter_history(localObjectList[3][colRow[3]-1].value,localObjectList[4][colRow[4]-1].value)
        #for colN in range(column+1,len(line)): # Tell the sub-types not to care if they are repeat values
        #  line_previous[colN]="NULL"
      else:
        localObjectList[column][colRow[column]-1].indexEnd=lineN
      line_previous[column]=line[column]
  return localObjectList
  

def add_object(OL,coli):
  colLen = len(OL.objectList[coli])
  if colLen>0:
    lastIndexCol = OL.objectList[coli][colLen-1].indexEnd+1
  else:
    lastIndexCol = 0 # This is the first object of any row
  newObject = alarm_object.ALARM_OBJECT()
  newObject.indexStart = lastIndexCol
  newObject.indexEnd = lastIndexCol
  newObject.column = coli
  newObject.columnIndex = colLen
  if coli!=0:
    if colLen!=0:
      #newObject.parentIndices = OL.objectList[coli][colLen-1].parentIndices # FIXME this needs to be done inteligently
      tempPI = OL.objectList[coli-1][len(OL.objectList[coli-1])-1].parentIndices
      newObject.parentIndices = tempPI.append(OL.objectList[coli-1][len(OL.objectList[coli-1])-1].columnIndex)
    # because the lastIndexCol will be non-addressable in event of this is the first thing added to the column, in which case we need to know which parent was actually activated to generate this column
    else:
      pass
  # OL.objectList.write_object(newObject) # fixme - do this method next
  OL.objectList[coli].append(newObject)

