'''
Green Monster GUI Revamp
Containing ADC18s Tab
Code Commissioned 2019-01-16
Code by A.J. Zec
Alarm Handler GUI Update
Cameron Clarke 2019-05-28
'''

import tkinter as tk
from tkinter import ttk
from functools import partial
import utils as u

class Callback:
  def __init__(self, func, *args, **kwargs):
    self.func = func
    self.args = args
    self.kwargs = kwargs
  def __call__(self):
    self.func(*self.args,**self.kwargs)

class ALARM_HANDLER(tk.Frame):
  def __init__(self, tab, OL, fileArray):

    self.alarmFrame = tk.LabelFrame(tab, text='Alarm Handler', background=u.lightgrey_color)
    self.columnTitles = ["Kinds","Channel","Type","Parameter"]
    self.colsp = [1,1,1,2]
    self.newText = ["New\nKind","New\nChannel","New\nType","New\nParameter"]

    self.alarmColumns = []
    self.initialize_columns(OL)
    self.buttons = []
    self.creatorButtons = []
    self.make_screen(OL,fileArray)
    #self.buttons = self.initialize_buttons(OL)
    #self.creatorButtons = self.initialize_creator_buttons(OL,fileArray)
    #self.alarmFrame.pack(padx=20,pady=20,anchor='w')
    #for i in range(0,len(self.buttons)):
    #  if i == 0: # Only default initialize all entries for column 0 (the Kind column)
    #    self.layout_grid_all_col(i,OL,self.creatorButtons[i])
    #  else:
    #    self.layout_grid_col(i,OL,self.creatorButtons[i])


  def make_screen(self,OL,fileArray):
    for i in range(0,len(self.alarmColumns)):
      self.alarmColumns[i].grid_forget()
    self.alarmColumns = []
    self.initialize_columns(OL)
    self.buttons = self.initialize_buttons(OL)
    self.creatorButtons = self.initialize_creator_buttons(OL,fileArray)
    self.alarmFrame.pack(padx=20,pady=20,anchor='w')
    for i in range(0,len(self.buttons)):
      if i == 0: # Only default initialize all entries for column 0 (the Kind column)
        self.erase_grid_col(i,OL,self.creatorButtons[i])
        self.layout_grid_all_col(i,OL,self.creatorButtons[i])
      else:
        #self.layout_grid_col(i,OL,self.creatorButtons[i])
        self.erase_grid_col(i,OL,self.creatorButtons[i])

  def initialize_columns(self,OL):
    for i in range(0, len(self.columnTitles)):
      self.alarmColumns.append(tk.LabelFrame(self.alarmFrame, text=self.columnTitles[i], background=u.lightgrey_color))
      self.alarmColumns[i].grid(row=0,column=i,pady=10,padx=10,sticky='N')

  def initialize_creator_buttons(self,OL,fileArray):
    grid = []
    for i in range(0, len(self.alarmColumns)):
      # First add the "New Button" button
      newButt = tk.Button(self.alarmColumns[i], text=self.newText[i], default='active', justify='center', background=u.lightgrey_color)
      newButt.indices = (i,len(self.buttons[i]))
      newButt.config(command = lambda newBut=newButt: self.select_add_button(OL,fileArray,newBut))
      grid.append(newButt)
    return grid

  def initialize_buttons(self,OL):
    grid = []
    for i in range(0, len(self.alarmColumns)):
      butCol = []
      if len(OL.objectList)>(i): #FIXME this ignores creating a button for the 5th entry, but we will want to make a label/edit box for it
        for j in range(0,len(OL.objectList[i])):
          # Loop over the list of objects, creating buttons
          butt = tk.Button(self.alarmColumns[i], text=OL.objectList[i][j].value, justify='center', background=OL.objectList[i][j].color) # loop over buttons
          butt.indices = (i,j)
          butt.config(command = lambda but=butt: self.select_button(OL,but))
          butCol.append(butt)
      grid.append(butCol)
    return grid

  def layout_grid_all_col(self,colID,OL,newButt):
    newButt.grid(row=0,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')
    for i in range(0,len(self.buttons[colID])):
      self.buttons[colID][i].grid(row=i+1,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')

  def erase_grid_col(self,colID,OL,newButt):
    for i in range(colID,len(self.buttons)):
      self.creatorButtons[i].grid_forget()
      for j in range(0,len(self.buttons[i])):
        self.buttons[i][j].grid_forget()

  def layout_grid_col(self,colID,OL,newButt):
    for i in range(colID,len(self.buttons)):
      self.creatorButtons[i].grid_forget()
      for j in range(0,len(self.buttons[i])):
        self.buttons[i][j].grid_forget()
    # Want to ask OL which object is clicked
    # Then get the index range that its children live in
    # Then grid those children (and erase prior grid, preserving creatorButton[coldID])
    newButt.grid(row=0,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')
    for j in range(0,len(OL.objectList[colID])):
      if OL.objectList[colID][j].parentIndices[colID-1]==OL.selectedButtonColumnIndicesList[colID-1]: # If the item on the right has the parent index of the current column equal to the currently selected button's column index, thenactivate it
        self.buttons[colID][j].grid(row=j+1,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')

  def select_button(self,OL,but):
    i,j = but.indices
    OL.selectedButtonColumnIndicesList[i]=j # Update the currently clicked button index
    print(OL.objectList[i][j].parentIndices)
    OL.set_clicked(i,j) # Update that object's color to dark grey
    self.set_button_clicked(OL,i,j) # Re-organize the grid and change the non-clicked buttons back to regular light grey
    self.buttons[i][j].config(background=OL.objectList[i][j].color) # Update that button to be the newly update object's new color (could just use but.config)

  def select_add_button(self,OL,fileArray,but):
    i,j = but.indices
    #j = len(self.buttons[i]) #- 1 
    #u.append_object(OL,i)
    #FIXME This is the Python way to do it -> #u.insert_object(OL,i)
    fileArray.filearray = u.add_to_filearray(OL,fileArray,but)
    fileArray.filearray = u.write_filearray(fileArray)
    OL.objectList = u.create_objects(fileArray)
    self.make_screen(OL,fileArray)
    for coli in range(0,i):
      self.select_button(OL,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

  def insert_button(self,OL,but,indi):
    i,j = but.indices
    j = OL.selectedButtonColumnIndicesList[i]
    i = indi
    j# = len(self.buttons[i]) #- 1 
    butt = tk.Button(self.alarmColumns[i], text=OL.objectList[i][j].value, justify='center', background=OL.objectList[i][j].color)
    butt.indices = (i,j) #FIXME get the indices right and pass/edit locations of new buttons correctly
    butt.config(command = lambda butte=butt: self.select_button(OL,butte))
    self.buttons[i].insert(j,butt) # FIXME the OL.objectList.parentIndices and columnIndices must be updated now!!
    self.select_button(OL,butt)
    if i==3:
      self.buttons[i][j].grid(row=j+1,column=i,columnspan=2,pady=10,padx=10,sticky='N')
    else:
      self.buttons[i][j].grid(row=j+1,column=i,pady=10,padx=10,sticky='N')
    self.alarmColumns[i].grid(row=0,column=i,pady=10,padx=10,sticky='N')
    self.alarmFrame.pack(padx=20,pady=20,anchor='w')
    #self.insert_button(OL,but,indi+1)

  def append_button(self,OL,but,indi):
    i,j = but.indices
    #j = OL.selectedButtonColumnIndicesList[i]
    i = indi
    j = len(self.buttons[i]) #- 1 
    butt = tk.Button(self.alarmColumns[i], text=OL.objectList[i][j].value, justify='center', background=OL.objectList[i][j].color)
    butt.indices = (i,j) #FIXME get the indices right and pass/edit locations of new buttons correctly
    butt.config(command = lambda butte=butt: self.select_button(OL,butte))
    self.buttons[i].append(butt)
    self.select_button(OL,butt)
    if i==3:
      self.buttons[i][j].grid(row=j+1,column=i,columnspan=2,pady=10,padx=10,sticky='N')
    else:
      self.buttons[i][j].grid(row=j+1,column=i,pady=10,padx=10,sticky='N')
    self.alarmColumns[i].grid(row=0,column=i,pady=10,padx=10,sticky='N')
    self.alarmFrame.pack(padx=20,pady=20,anchor='w')
    
    if indi < len(self.buttons)-1:
      self.append_button(OL,but,indi+1)

  def set_button_clicked(self,OL,i,j):
    for column in range(0,len(self.buttons)):
      for row in range(0,len(self.buttons[column])):
        #if row != OL.selectedButtonColumnIndicesList[column]:
          self.buttons[column][row].config(background = OL.objectList[column][row].color) # Reset the other buttons that aren't currently the selected ones to their object's color
    self.buttons[i][j].config(background = OL.objectList[i][j].color) # And this one too
    if i<3:
      self.layout_grid_col(i+1,OL,self.creatorButtons[i+1])

