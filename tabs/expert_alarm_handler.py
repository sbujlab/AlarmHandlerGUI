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
from tkinter import simpledialog
from functools import partial
import utils as u

class Callback:
  def __init__(self, func, *args, **kwargs):
    self.func = func
    self.args = args
    self.kwargs = kwargs
  def __call__(self):
    self.func(*self.args,**self.kwargs)

class EXPERT_ALARM_HANDLER(tk.Frame):
  def __init__(self, alarmHandlerWindow, tab, OL, fileArray, alarmLoop):

    self.controlFrame = tk.LabelFrame(tab, text='Alarm Controls', background=u.grey_color)
    self.alarmFrame = tk.LabelFrame(tab, text='Expert Alarm Handler', background=u.lightgrey_color)
    self.columnTitles = ["Kinds","Channel","Type","Parameter","Value"]
    self.colsp = [1,1,1,1,1]
    self.newText = ["New\nKind","New\nChannel","New\nType","New\nParameter","Alarm\nValues"]
    self.controlButtonsText = ["Alarm Status","Toggle Loop","Silence All","Reset GUI"]

    self.alarmColumns = []
    self.initialize_columns(OL)
    self.buttons = []
    self.buttonMenus = []
    self.creatorButtons = []
    self.controlButtons = self.make_control_buttons(OL,fileArray, alarmLoop)
    self.make_screen(OL,fileArray)

  def make_control_buttons(self,OL,fileArray,alarmLoop):
    grid = []
    for i in range(0, len(self.controlButtonsText)):
      # First add the "New Button" button
      newButt = tk.Button(self.controlFrame, text=self.controlButtonsText[i], default='active', justify='center', background=u.lightgrey_color)
      if self.controlButtonsText[i]=="Silence All" and alarmLoop.globalUserAlarmSilence == "Silenced":
        newButt.config(background=u.darkgrey_color)
      #if self.controlButtonsText[i]=="Alarm Status": # FIXME red here too always?
      if self.controlButtonsText[i]=="Alarm Status":
        if alarmLoop.globalAlarmStatus != "OK" and alarmLoop.globalUserAlarmSilence != "Silenced":
          newButt.config(background=u.red_button_color)
        elif alarmLoop.globalAlarmStatus == "OK" and alarmLoop.globalUserAlarmSilence != "Silenced":
          newButt.config(background=u.lightgrey_color)
        elif alarmLoop.globalUserAlarmSilence == "Silenced":
          newButt.config(background=u.darkgrey_color)
      newButt.indices = (i,0)
      newButt.text = self.controlButtonsText[i]
      newButt.config(command = lambda newBut=newButt: self.select_control_buttons(OL,fileArray,alarmLoop,newBut))
      newButt.grid(row = 0, column = i,columnspan=self.colsp[i],padx=10,pady=10,sticky='N')
      grid.append(newButt)
    #self.controlFrame.pack(padx=20,pady=5,anchor='n')
    self.controlFrame.grid(row=0,sticky='NW')
    return grid

  def select_control_buttons(self,OL,fileArray,alarmLoop,but):
    i,j = but.indices
    for k in range(0,len(self.controlButtons)):
      self.controlButtons[k].grid_forget()
    if but.text=="Silence All":
      if alarmLoop.globalUserAlarmSilence == "Alert":
        alarmLoop.globalUserAlarmSilence = "Silenced"
        but.config(background=u.darkgrey_color)
      elif alarmLoop.globalUserAlarmSilence == "Silenced":
        alarmLoop.globalUserAlarmSilence = "Alert"
        but.config(background=u.lightgrey_color)
    if but.text=="Toggle Loop":
      if alarmLoop.globalLoopStatus == "Looping":
        print("Turning off loop")
        alarmLoop.globalLoopStatus = "Paused"
      elif alarmLoop.globalLoopStatus == "Paused":
        print("Turning on loop")
        alarmLoop.globalLoopStatus = "Looping"
        alarmLoop.reset_alarmList(OL)
    if but.text=="Alarm Status":
      if alarmLoop.globalAlarmStatus != "OK": # FIXME red here too always?:
        #and alarmLoop.globalUserAlarmSilence != "Silenced":
        but.config(background=u.red_button_color)
      else:
        but.config(background=u.lightgrey_color)
      for k in range(0,len(u.recentAlarmButtons)):
        OL.selectedButtonColumnIndicesList[k]=u.recentAlarmButtons[k] # Update the currently clicked button index to the alarming one
      self.update_GUI(OL,fileArray)
      for coli in range(0,5):
        if OL.selectedButtonColumnIndicesList[coli] != -1:
          self.refresh_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])
    if but.text=="Reset GUI":
      for k in range(0,len(OL.selectedButtonColumnIndicesList)):
        OL.selectedButtonColumnIndicesList[k]=-1
      self.update_GUI(OL,fileArray)
    self.controlButtons = self.make_control_buttons(OL,fileArray,alarmLoop)

  def make_screen(self,OL,fileArray):
    for i in range(0,len(self.alarmColumns)):
      #self.alarmColumns[i].grid_forget()
      self.alarmColumns[i].destroy()
    self.alarmColumns = []
    self.initialize_columns(OL)
    self.buttons = self.initialize_buttons(OL,fileArray)
    self.creatorButtons = self.initialize_creator_buttons(OL,fileArray)
    self.buttonMenus = self.initialize_menus(OL,fileArray)
    #self.alarmFrame.pack(padx=20,pady=10,anchor='nw')
    self.controlFrame.grid(row=0,sticky='NW')
    self.alarmFrame.grid(row=1,sticky='NW')
    for i in range(0,len(self.buttons)):
      if i == 0: 
        # Only default initialize all entries for column 0 (the Kind column)
        # A refreshed screen should only show the left most column, other columns obtained through clicking or selectedButtonColumnIndicesList
        self.erase_grid_col(i,OL,fileArray,self.creatorButtons[i])
        self.layout_grid_all_col(i,OL,fileArray,self.creatorButtons[i])
      else:
        self.erase_grid_col(i,OL,fileArray,self.creatorButtons[i])

  def initialize_columns(self,OL):
    for i in range(0, len(self.columnTitles)):
      self.alarmColumns.append(tk.LabelFrame(self.alarmFrame, text=self.columnTitles[i], background=u.lightgrey_color))
      self.alarmColumns[i].grid(row=1,column=i,pady=10,padx=10,sticky='N')

  def initialize_column(self,OL,colI):
    self.alarmColumns[colI] = tk.LabelFrame(self.alarmFrame, text=self.columnTitles[colI], background=u.lightgrey_color)
    self.alarmColumns[colI].grid(row=1,column=colI,pady=10,padx=10,sticky='N')
    #self.alarmFrame.pack(padx=20,pady=10,anchor='nw')
    self.alarmFrame.grid(row=1,sticky='NW')

  def initialize_creator_buttons(self,OL,fileArray):
    grid = []
    for i in range(0, len(self.alarmColumns)):
      # First add the "New Button" button
      newButt = tk.Button(self.alarmColumns[i], text=self.newText[i], default='active', justify='center', background=u.lightgrey_color)
      newButt.indices = (i,len(self.buttons[i]))
      if i<4:
        newButt.config(command = lambda newBut=newButt: self.select_add_button(OL,fileArray,newBut))
      grid.append(newButt)
    return grid

  def initialize_buttons(self,OL,fileArray):
    grid = []
    for i in range(0, len(self.alarmColumns)):
      butCol = []
      if len(OL.objectList)>(0):
        for j in range(0,len(OL.objectList[i])):
          # Loop over the list of objects, creating buttons
          butt = tk.Button(self.alarmColumns[i], text=OL.objectList[i][j].value, justify='center', background=OL.objectList[i][j].color) # loop over buttons
          butt.indices = (i,j)
          butt.config(command = lambda but=butt: self.select_button(OL,fileArray,but))
          butCol.append(butt)
      grid.append(butCol)
    return grid

  def initialize_menus(self,OL,fileArray):
    grid = []
    #print("Adding menus, len(self.alarmColumns) = {} times".format(len(self.alarmColumns)))
    for i in range(0, len(self.alarmColumns)):
      #print("Adding menus to {}, len(OL.objectList[{}]) = {} times".format(i,i,len(OL.objectList[i])))
      menuCol = []
      #print("If len(OL.objectList) = {} > 0:".format(len(OL.objectList),0))
      if len(OL.objectList)>(0):
        for j in range(0,len(OL.objectList[i])):
          buttMenu = tk.Menu(self.buttons[i][j], tearoff=0) # Is having the owner be button correct?
          buttMenu.indices = (i,j)
          buttMenu.moveN = 0
          buttMenu.editValue = None
          if i<=2:
            buttMenu.add_command(label = 'Silence', command = lambda butMenu = buttMenu: self.button_silence_menu(OL,fileArray,butMenu))
          buttMenu.add_command(label = 'Edit', command = lambda butMenu = buttMenu: self.button_edit_menu(OL,fileArray,butMenu))
          buttMenu.add_command(label = 'Move', command = lambda butMenu = buttMenu: self.button_move_menu(OL,fileArray,butMenu))
          buttMenu.add_command(label = 'Copy', command = lambda butMenu = buttMenu: self.button_copy_menu(OL,fileArray,butMenu))
          buttMenu.add_command(label = 'Add', command = lambda butMenu = buttMenu: self.button_add_menu(OL,fileArray,butMenu))
          buttMenu.add_command(label = 'Delete', command = lambda butMenu = buttMenu: self.button_delete_menu(OL,fileArray,butMenu))
          self.buttons[i][j].bind("<Button-3>",lambda event, butMenu = buttMenu: self.do_popup(event,butMenu))
          menuCol.append(buttMenu)
      grid.append(menuCol)
    return grid

  def do_popup(self,event,butMenu):
    butMenu.tk_popup(event.x_root,event.y_root,0)

  def layout_grid_all_col(self,colID,OL,fileArray,newButt):
    newButt.grid(row=0,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')
    for i in range(0,len(self.buttons[colID])):
      self.buttons[colID][i].grid(row=i+1,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')
    #self.buttonMenus = self.initialize_menus(OL,fileArray)

  def erase_grid_col(self,colID,OL,fileArray,newButt):
    for i in range(colID,len(self.buttons)):
      self.creatorButtons[i].grid_forget()
      for j in range(0,len(self.buttons[i])):
        self.buttons[i][j].grid_forget()

  def layout_grid_col(self,colID,OL,fileArray,newButts):
    for i in range(colID,len(self.buttons)): 
      self.creatorButtons[i].grid_forget()
      for j in range(0,len(self.buttons[i])):
        self.buttons[i][j].grid_forget()
    for i in range(colID,len(self.buttons)):#NEW
      self.alarmColumns[i].grid_forget() #NEW
    # Want to ask OL which object is clicked
    # Then get the index range that its children live in
    # Then grid those children (and erase prior grid, preserving creatorButton[coldID])
    newButts[colID].grid(row=0,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')
    #print("Adding column {}".format(colID))
    self.alarmColumns[colID].grid(row=1,column=colID,pady=10,padx=10,sticky='N')#NEW
    if colID == 3 and len(self.alarmColumns)>colID+1: #NEW
      #print("Adding column {}".format(colID+1))
      newButts[colID+1].grid(row=0,column=colID+1,columnspan=self.colsp[colID+1],padx=10,pady=10,sticky='N')
      self.alarmColumns[colID+1].grid(row=1,column=colID+1,pady=10,padx=10,sticky='N')#NEW
    #self.alarmFrame.pack(padx=20,pady=10,anchor='nw') #NEW
    self.alarmFrame.grid(row=1,sticky='NW')
    if colID<4:
      for j in range(0,len(OL.objectList[colID])):
        if colID>0 and OL.objectList[colID][j].parentIndices[colID-1]==OL.selectedButtonColumnIndicesList[colID-1]: # If the item on the right has the parent index of the current column equal to the currently selected button's column index, thenactivate it
          self.buttons[colID][j].grid(row=j+1,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')
        if colID == 0:
          self.buttons[colID][j].grid(row=j+1,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')
    if colID==3:
      colID=4
      counter=[]
      for j in range(0,len(OL.objectList[colID-1])):
        counter.append(0)
      for j in range(0,len(OL.objectList[colID])):
        #if OL.objectList[colID][j].parentIndices[colID-1]==OL.selectedButtonColumnIndicesList[colID-1]: # If the item two on the right has the parent index of the current column equal to the currently selected button's column index, thenactivate it
        counter[OL.objectList[colID][j].parentIndices[colID-1]] += 1 # Counts how many times a parent has seen any child
        if OL.objectList[colID][j].parentIndices[colID-2]==OL.selectedButtonColumnIndicesList[colID-2] and counter[OL.objectList[colID][j].parentIndices[colID-1]]==1: # If the item two on the right is the first to have the one of the right's columnIndex as a parent then show it
            self.buttons[colID][j].grid(row=j+1,column=colID,columnspan=self.colsp[colID],padx=10,pady=10,sticky='N')
    #self.buttonMenus = self.initialize_menus(OL,fileArray)

  def refresh_button(self,OL,fileArray,but):
    i,j = but.indices
    OL.selectedButtonColumnIndicesList[i]=j # Update the currently clicked button index
    OL.set_clicked(i,j) # Update that object's color to dark grey
    self.set_button_clicked(OL,fileArray,i,j) # Re-organize the grid and change the non-clicked buttons back to regular light grey
    self.buttons[i][j].config(background=OL.objectList[i][j].color) # Update that button to be the newly update object's new color (could just use but.config)

  def select_button(self,OL,fileArray,but):
    i,j = but.indices
    OL.selectedButtonColumnIndicesList[i]=j # Update the currently clicked button index
    for k in range(0,i): 
      OL.selectedButtonColumnIndicesList[k] = OL.objectList[i][OL.objectList[i][j].parentIndices[k]].columnIndex # FIXME this should fix the incorrect index updating on refresh
    for k in range(i+1,len(OL.selectedButtonColumnIndicesList)): 
      #print("Erasing selectedButtonIndex at {}".format(k))
      OL.selectedButtonColumnIndicesList[k] = -1
    OL.set_clicked(i,j) # Update that object's color to dark grey
    self.set_button_clicked(OL,fileArray,i,j) # Re-organize the grid and change the non-clicked buttons back to regular light grey
    self.buttons[i][j].config(background=OL.objectList[i][j].color) # FIXME redundant? - Update that button to be the newly update object's new color (could just use but.config)

  def update_GUI(self,OL,fileArray):
    fileArray.filearray = u.write_filearray(fileArray)
    OL.objectList = u.create_objects(fileArray)
    self.make_screen(OL,fileArray)

  def select_add_button(self,OL,fileArray,but):
    i,j = but.indices
    fileArray.filearray = u.add_to_filearray(OL,fileArray,but)
    self.update_GUI(OL,fileArray)
    for coli in range(0,i):
      if OL.selectedButtonColumnIndicesList[coli] != -1:
        self.select_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

  def button_silence_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    u.silence_filearray_menu(OL,fileArray,butMenu)
    self.update_GUI(OL,fileArray)
    for coli in range(0,i):
      if OL.selectedButtonColumnIndicesList[coli] != -1:
        self.refresh_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

  def button_edit_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    butMenu.editValue = simpledialog.askstring("Input", "Enter replacement value:",parent = butMenu) 
    if butMenu.editValue != None:
      fileArray.filearray = u.edit_filearray_menu(OL,fileArray,butMenu)
      self.update_GUI(OL,fileArray)
      for coli in range(0,i):
        if OL.selectedButtonColumnIndicesList[coli] != -1:
          self.refresh_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

  def button_move_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    #OL.selectedButtonColumnIndicesList[i]=j # FIXME - try to get menus to persist screen
    butMenu.moveN = simpledialog.askinteger("Input", "Move amount (+ is down)",parent = butMenu, maxvalue=(len(self.buttons[i])-j-1), minvalue=-1*j) #FIXME - limits are for entire button array, not just currently shown one... 
    if butMenu.moveN != 0:
      fileArray.filearray = u.move_filearray_menu(OL,fileArray,butMenu)
      self.update_GUI(OL,fileArray)
      for coli in range(0,i):
        if OL.selectedButtonColumnIndicesList[coli] != -1:
          self.select_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

  def button_copy_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    #OL.selectedButtonColumnIndicesList[i]=j # FIXME - try to get menus to persist screen
    butMenu.copyName = simpledialog.askstring("Input", "New Entry Name",parent = butMenu) 
    if butMenu.moveN != None:
      fileArray.filearray = u.copy_filearray_menu(OL,fileArray,butMenu)
      self.update_GUI(OL,fileArray)
      for coli in range(0,i):
        if OL.selectedButtonColumnIndicesList[coli] != -1:
          self.select_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

  def button_add_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    #OL.selectedButtonColumnIndicesList[i]=j # FIXME - try to get menus to persist screen
    fileArray.filearray = u.add_filearray_menu(OL,fileArray,butMenu)
    self.update_GUI(OL,fileArray)
    for coli in range(0,i):
      if OL.selectedButtonColumnIndicesList[coli] != -1:
        self.select_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

  def button_delete_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    #OL.selectedButtonColumnIndicesList[i]=j # FIXME - try to get menus to persist screen
    fileArray.filearray = u.delete_filearray_menu(OL,fileArray,butMenu)
    self.update_GUI(OL,fileArray)
    for coli in range(i,len(OL.selectedButtonColumnIndicesList)):
      if OL.selectedButtonColumnIndicesList[coli] != -1:
        OL.selectedButtonColumnIndicesList[i] -= 1
    for coli in range(0,i):
      if OL.selectedButtonColumnIndicesList[coli] != -1:
        self.select_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

  def set_button_clicked(self,OL,fileArray,i,j):
    for column in range(0,len(self.buttons)):
      for row in range(0,len(self.buttons[column])):
        self.buttons[column][row].config(background = OL.objectList[column][row].color) # Reset the other buttons that aren't currently the selected ones to their object's color
    self.buttons[i][j].config(background = OL.objectList[i][j].color) # And this one too
    if i<3: 
      self.layout_grid_col(i+1,OL,fileArray,self.creatorButtons)
    self.buttonMenus = self.initialize_menus(OL,fileArray) # FIXME Necessary?

  def refresh_screen(self,OL,fileArray,alarmLoop):
    self.controlButtons = self.make_control_buttons(OL,fileArray, alarmLoop)
    self.update_GUI(OL,fileArray)
    for coli in range(0,len(OL.selectedButtonColumnIndicesList)):
      if OL.selectedButtonColumnIndicesList[coli] != -1:
        self.refresh_button(OL,fileArray,self.buttons[coli][OL.selectedButtonColumnIndicesList[coli]])

