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
red_button_color = '#9E1A1A'

# Cameron Alarm Methods

def parse_textfile(fileArray):
  fileArray.filearray = []
  with open(fileArray.filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=fileArray.delim)
    for row in csv_reader:
      rowList = []
      for col in row:
        rowList.append(col)
      fileArray.filearray.append(rowList)
  return fileArray.filearray

def write_textfile(OL,fileArray):
  fileArray.filearray = []
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
      fileArray.filearray.append(entryarray)
  outFile = open(fileArray.filename,'w+')
  wr = csv.writer(outFile,delimiter=fileArray.delim)
  filearrayrows=zip(*fileArray.filearray)
  wr.writerows(fileArray.filearray)
  return fileArray.filearray

def add_to_filearray(OL,fileArray,but):
  i,j = but.indices
  print("Column:")
  print(i)
  j = OL.activeObjectColumnIndicesList[i]
  print("Column index:")
  print(j)
  file_ind = OL.objectList[i][j].indexEnd+1
  print("File index:")
  print(file_ind)
  addedLine = []
  for parent in range(0,i):
    addedLine.append(OL.objectList[parent][OL.activeObjectColumnIndicesList[parent]].value)
  for child in range(i,len(OL.objectList)):
    addedLine.append("NULL")
  print("Added Line:")
  print(addedLine)
  fileArray.filearray.insert(file_ind,addedLine)
  print("adding to file array")
  for i in range(0,len(fileArray.filearray)):
    print(fileArray.filearray[i])
  return fileArray.filearray

def write_filearray(fileArray):
  outFile = open(fileArray.filename,'w+')
  wr = csv.writer(outFile,delimiter=fileArray.delim)
  filearrayrows=zip(*fileArray.filearray)
  wr.writerows(fileArray.filearray)
  print("writing file array")
  for i in range(0,len(fileArray.filearray)):
    print(fileArray.filearray[i])
  return fileArray.filearray

def create_objects(fileArray):
  if len(fileArray.filearray)>0: 
    ncolumns = len(fileArray.filearray[len(fileArray.filearray)-1]) # FIXME should this just be hardcoded to 5 layers or should I keep it generic??
  nlines = len(fileArray.filearray)
  localObjectList = []
  colRow = []
  line_previous = []
  for i in range(0,ncolumns):
    localObjectList.append([]) # Check this
    colRow.append(0)
    line_previous.append("NULL")
  for lineN in range(0,nlines):
    line = fileArray.filearray[lineN]
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
      else:
        localObjectList[column][colRow[column]-1].indexEnd=lineN
      line_previous[column]=line[column]
  print("generating object list")
  for i in range(len(localObjectList)):
    for j in range(len(localObjectList[i])):
      print("Val: {}, startIndex: {}, endIndex: {}".format(localObjectList[i][j].value,localObjectList[i][j].indexStart,localObjectList[i][j].indexEnd))
  return localObjectList
  
def append_object(OL,coli): 

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
  if coli != 0:
    #if colLen != 0:
    i_index = coli-1
    j_index = OL.selectedButtonColumnIndicesList[i_index]
    #j_index = len(OL.objectList[coli-1])-1
    newObject.parentIndices = OL.objectList[i_index][j_index].parentIndices.copy()
    newObject.parentIndices.append(OL.objectList[i_index][j_index].columnIndex)
  OL.objectList[coli].append(newObject)

  if coli < len(OL.objectList)-1:
    append_object(OL,coli+1)

def insert_object(OL,coli): 
  colLen = len(OL.objectList[coli])
  originalLengthColumn = OL.selectedColumnButtonLengthList[coli]
  insertColumnsLocations = OL.activeObjectColumnIndicesList.copy() # These are the locations (++) we will be inserting new objects (and buttons)

  #colIndexInsert = []
  #startIndexInsert = []
  #endIndexInsert = []
  #for i in range(0,len(OL.objectList)):  # Fill from 0, but use from coli
  #  colIndexInsert.append(insertColumnsLocations[i]+1)
  #  startIndexInsert.append(OL.objectList[i][insertColumnsLocations[i]].indexEnd+1)
  #  endIndexInsert.append(OL.objectList[i][insertColumnsLocations[i]].indexEnd+2)
  # Go through the items whose children contain the affected (moved down) objects and update their start and endIndex+1, for row 3 (analyses) update parameter list with new NULL parameter in correct placement
  # Go through the items which are moved down and move them down, also if their parent was moved down then update parentIndices+1
  # Go through columns and insert new objects in the new colIndex position, give parentIndices appropriately for updated information
  for j in range(insertColumnsLocations[coli]+1,len(OL.objectList[coli])): # Rows below first new button
    OL.objectList[coli][j].columnIndex += 1
    OL.objectList[coli][j].indexStart += 1
    OL.objectList[coli][j].indexEnd += 1
  for i in range(coli+1,len(OL.objectList)): # Rows to the right, below right buttons, update parent indices too
    for j in range(insertColumnsLocations[i]+1,len(OL.objectList[i])):
      OL.objectList[i][j].columnIndex += 1
      OL.objectList[i][j].indexStart += 1
      OL.objectList[i][j].indexEnd += 1
      OL.objectList[i][j].parentIndices[i-1] += 1
  for i in range(0,coli): # Rows to the left, left of and below selected location
    OL.objectList[i][insertColumnsLocations[i]].indexEnd += 1
    OL.objectList[i][insertColumnsLocations[i]].numberChildren += 1
    for j in range(insertColumnsLocations[i]+1,len(OL.objectList[i])):
      OL.objectList[i][j].indexEnd += 1

  newObjects = []
  for i in range(coli,len(OL.objectList)):
    newObjects.append(alarm_object.ALARM_OBJECT())
    newObjects[i-coli].indexStart = OL.objectList[i][insertColumnsLocations[i]].indexEnd + 1
    newObjects[i-coli].indexEnd = OL.objectList[i][insertColumnsLocations[i]].indexEnd + 2
    newObjects[i-coli].column = i
    newObjects[i-coli].columnIndex = insertColumnsLocations[i]+1 # Sketchy FIXME
    if coli>0:
      newObjects[i-coli].parentIndices = OL.objectList[i-1][insertColumnsLocations[i-1]].parentIndices.copy()
      if i>coli:
        newObjects[i-coli].parentIndices.append(OL.objectList[i-1][insertColumnsLocations[i-1]].columnIndex+1)
      else:
        newObjects[i-coli].parentIndices.append(OL.objectList[i-1][insertColumnsLocations[i-1]].columnIndex)

  for i in range(coli,len(OL.objectList)):
    OL.selectedButtonColumnIndicesList[i]+=1
    OL.selectedColumnButtonLengthList[i]+=1
    OL.activeObjectColumnIndicesList[i]+=1
  for i in range(coli,len(OL.objectList)):
    OL.objectList[i].insert(insertColumnsLocations[i]+1,newObjects[i-coli])

  print("Looping through column")
  print(coli)
  print("values of objectList: ")
  for i in range (0,len(OL.objectList)):
    for j in range (0,len(OL.objectList[i])):
      print("Val: {}, columnIndex: {}, parentIndices: {}".format(OL.objectList[i][j].value,OL.objectList[i][j].columnIndex,OL.objectList[i][j].parentIndices))


