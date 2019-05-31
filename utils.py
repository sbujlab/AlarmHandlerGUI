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

def add_object(OL,coli): 
  colLen = len(OL.objectList[coli])
  colIndexInsert = []
  startIndexInsert = []
  endIndexInsert = []
  for i in range(0,len(OL.objectList)):
    colIndexInsert.append(0)
    #colIndexInsert.append(OL.selectedButtonColumnIndicesList[i])
    startIndexInsert.append(0)
    endIndexInsert.append(0)
  clickedIndex = OL.selectedButtonColumnIndicesList[coli-1]
  colIndexInsert[0]=clickedIndex # This is the index below which we start adding our new objects and pusing down
  startIndexInsert[0]=OL.objectList[coli][len(OL.objectList[coli])-1].indexStart+1
  endIndexInsert[0]=OL.objectList[coli][len(OL.objectList[coli])-1].indexEnd+1
  if coli == 0:
    colIndexInsert[coli] = colLen-1
    startIndexInsert[coli] = OL.objectList[coli][colLen-1].indexStart
    endIndexInsert[coli] = OL.objectList[coli][colLen-1].indexEnd
    for i in range(1,len(OL.objectList)):
      tmp = 0
      tmp2 = 0
      tmp3 = 0
      for j in range(0,len(OL.objectList[i])):
        if clickedIndex == OL.objectList[i][j].parentIndices[coli-1]:
          tmp = OL.objectList[i][j].columnIndex
          tmp2 = OL.objectList[i][j].indexStart
          tmp3 = OL.objectList[i][j].indexEnd
      colIndexInsert[i]=tmp #colIndex of one whose parent ID matches)
      startIndexInsert[i]=tmp2
      endIndexInsert[i]=tmp3
  else:
    for i in range(coli,len(OL.objectList)):
      tmp = 0
      tmp2 = 0
      tmp3 = 0
      for j in range(0,len(OL.objectList[i])):
        if clickedIndex == OL.objectList[i][j].parentIndices[coli-1]:
          tmp = OL.objectList[i][j].columnIndex
          tmp2 = OL.objectList[i][j].indexStart
          tmp3 = OL.objectList[i][j].indexEnd
      colIndexInsert.append(tmp) #colIndex of one whose parent ID matches)
      startIndexInsert.append(tmp2)
      endIndexInsert.append(tmp3)

  # + increment the post guys, their column indices change
  #for i in range(coli,len(OL.objectList)):
  #  for j in range(1+colIndexInsert[i],len(OL.objectList[i])-1):
# #     OL.objectList[i][j].columnIndex+=1
  #    OL.objectList[i][j].indexStart+=1
  #    OL.objectList[i][j].indexEnd+=1

  # + increment the pre guys, only their file indices change
  #for i in range(0,coli):
  #  for j in range(OL.selectedButtonColumnIndicesList[i]+1,len(OL.objectList[i])-1):
  #    OL.objectList[i][j].indexStart+=1
  #    OL.objectList[i][j].indexEnd+=1

  # + increment the post guys' parentIndices matrices, as now the coli row has had its post-clicked values ++ed 
  for i in range(coli+1,len(OL.objectList)):
    for j in range(1+colIndexInsert[i],len(OL.objectList[i])-1):
      #if OL.objectList[i][j].parentIndices[coli]>colIndexInsert[i]:
      if OL.objectList[i][j].parentIndices[coli]>=colIndexInsert[i]:
        OL.objectList[i][j].parentIndices[coli] += 1



  newObject = alarm_object.ALARM_OBJECT()
  newObject.indexStart = startIndexInsert[coli]+1
  newObject.indexEnd = startIndexInsert[coli]+2
  newObject.column = coli
  newObject.columnIndex = colIndexInsert[coli]+1

  if coli != 0:
    #if colLen != 0:
    i_index = coli-1
    j_index = OL.selectedButtonColumnIndicesList[i_index]
    #j_index = len(OL.objectList[coli-1])-1
    newObject.parentIndices = OL.objectList[i_index][j_index].parentIndices.copy()
    newObject.parentIndices.append(OL.objectList[i_index][j_index].columnIndex)

  #OL.objectList[coli].insert(colIndexInsert[coli],newObject)
  OL.objectList[coli].insert(colIndexInsert[coli]+1,newObject)
  print("Looping through")
  print(coli)
  #if coli<4:
  #  add_object(OL,coli+1)

  # FIXME FIXME When adding a new parameter or value be sure to add it to the analysis's parameterList and history

  #FIXME : Add new objects into the middle of the array, at the end of the sub-array its parrent, don't append
  # Also need to add objects to the right-> and treat parentIndices correctly

  # Find the currently clicked button on the left
  #   then grab it's list of children in the currently displayed column
  #   then loop through that list of children to find the one that is at the end and obtain its columnIndex
  #   grab all subsequent objects (and buttons to match) and update their column indices++
  #     now, in object (and button) space move to the right, taking and loop through that list of children to find the one that is at the end (of list of children) and obtain its columnIndex
  #     grab all subsequent objects (and buttons) and ++columnIndex (etc.)
  #     


