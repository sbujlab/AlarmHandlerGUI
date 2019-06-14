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

class ALARM_HANDLER(tk.Frame):
  def __init__(self, alarmHandlerWindow, tab, OL, fileArray, alarmLoop):

    self.controlFrame = tk.LabelFrame(tab, text='Alarm Handler', background=u.grey_color)
    self.alarmFrame = tk.LabelFrame(tab, text='Alarm Handler Viewer', background=u.lightgrey_color)
    self.rowTitles = ["Alarms","ctd.","ctd.","ctd."]
    self.NperCol = 8
    self.colsp = [1,1,1,1]
    self.controlButtonsText = ["Alarm Status","Toggle Loop","Silence All","Refresh GUI"]

    self.alarmRows = []
    self.initialize_rows(OL)
    self.buttons = []
    self.buttonMenus = []
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
    self.controlFrame.pack(padx=20,pady=5,anchor='n')
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
      self.update_GUI(OL,fileArray)
    self.controlButtons = self.make_control_buttons(OL,fileArray,alarmLoop)

  def make_screen(self,OL,fileArray):
    for i in range(0,len(self.alarmRows)):
      #self.alarmRows[i].grid_forget()
      self.alarmRows[i].destroy()
    self.alarmRows = []
    self.initialize_rows(OL)
    self.buttons = self.initialize_buttons(OL,fileArray)
    self.buttonMenus = self.initialize_menus(OL,fileArray)
    self.alarmFrame.pack(padx=20,pady=10,anchor='nw')

  def initialize_rows(self,OL):
    for i in range(0, len(self.rowTitles)):
      self.alarmRows.append(tk.LabelFrame(self.alarmFrame, text=self.rowTitles[i], background=u.lightgrey_color))
      self.alarmRows[i].grid(column=0,row=i,pady=10,padx=10,sticky='N')

  def initialize_row(self,OL,rowI):
    self.alarmRows[rowI] = tk.LabelFrame(self.alarmFrame, text=self.rowTitles[rowI], background=u.lightgrey_color)
    self.alarmRows[rowI].grid(column=0,row=rowI,pady=10,padx=10,sticky='N')
    self.alarmFrame.pack(padx=20,pady=10,anchor='nw')

  def initialize_buttons(self,OL,fileArray): # Needs a short row to contain [name = value, alarm status = type, alarm stat !OK, user silence stat, alarm stat OK], context menu displays full parameter list
    grid = []
    if len(OL.objectList)>(2) and len(OL.objectList[2])>0:
      for i in range(0,len(OL.objectList[2])):
        # Loop over the list of objects, creating buttons
        butt = tk.Button(self.alarmRows[int(1.0*i/self.NperCol)], text=OL.objectList[2][i].value, justify='center', background=OL.objectList[2][i].color) # loop over buttons
        butt.indices = (int(1.0*i/self.NperCol),i)
        butt.config(command = lambda but=butt: self.select_button(OL,fileArray,but))
        grid.append(butt)
      grid.append(grid)
    return grid

  def initialize_menus(self,OL,fileArray):
    grid = []
    #print("Adding menus, len(self.alarmRows) = {} times".format(len(self.alarmRows)))
    for i in range(0, len(self.buttons)):
      if len(OL.objectList[2])>=i:
        buttMenu = tk.Menu(self.buttons[i], tearoff=0) # Is having the owner be button correct?
        buttMenu.indices = (i,OL.objectList[2][i].columnIndex)
        buttMenu.moveN = 0
        buttMenu.editValue = None
        buttMenu.add_command(label = 'Information', command = lambda butMenu = buttMenu: self.button_information_menu(OL,fileArray,butMenu))
        buttMenu.add_command(label = 'Silence', command = lambda butMenu = buttMenu: self.button_silence_menu(OL,fileArray,butMenu))
        self.buttons[i].bind("<Button-3>",lambda event, butMenu = buttMenu: self.do_popup(event,butMenu))
      grid.append(buttMenu)
    return grid

  def do_popup(self,event,butMenu):
    butMenu.tk_popup(event.x_root,event.y_root,0)

  def layout_grid_all_row(self,rowID,OL,fileArray,newButt):
    newButt.grid(row=0,column=rowID,columnspan=self.rowsp[rowID],padx=10,pady=10,sticky='N')
    for i in range(0,len(self.buttons)):
      # FIXME Put the int() mod math to place buttons in a given row here
      self.buttons[i].grid(row=i,column=rowID,columnspan=self.rowsp[rowID],padx=10,pady=10,sticky='N')
    #self.buttonMenus = self.initialize_menus(OL,fileArray)

  def erase_grid_row(self,rowID,OL,fileArray,newButt):
    # FIXME rowID is not being parsed correctly here !!
    for i in range(rowID,len(self.buttons)):
      self.buttons[i].grid_forget()

  def layout_grid_row(self,rowID,OL,fileArray):
    # FIXME Put the int() mod math to place buttons in a given row here
    for i in range(rowID,len(self.buttons)): 
      self.buttons[i].grid_forget()
    for j in range(rowID,len(self.buttons)):#NEW
      self.alarmRows[j].grid_forget() #NEW
    # Want to ask OL which object is clicked
    # Then get the index range that its children live in
    # Then grid those children (and erase prior grid, preserving creatorButton[rowdID])
    #print("Adding row {}".format(rowID))
    self.alarmRows[rowID].grid(column=0,row=rowID,pady=10,padx=10,sticky='N')#NEW
    if rowID == 3 and len(self.alarmRows)>rowID+1: #NEW
      #print("Adding row {}".format(rowID+1))
      self.alarmRows[rowID+1].grid(column=0,row=rowID+1,pady=10,padx=10,sticky='N')#NEW
    self.alarmFrame.pack(padx=20,pady=10,anchor='nw') #NEW

  def refresh_button(self,OL,fileArray,but):
    i,j = but.indices
    OL.set_clicked(i,j) # Update that object's color to dark grey
    self.buttons[i].config(background=OL.objectList[i][j].color) # Update that button to be the newly update object's new color (could just use but.config)

  def select_button(self,OL,fileArray,but):
    i,j = but.indices
    OL.set_clicked(i,j) # Update that object's color to dark grey
    self.buttons[i].config(background=OL.objectList[i][j].color) # Update that button to be the newly update object's new color (could just use but.config)

  def update_GUI(self,OL,fileArray):
    fileArray.filearray = u.write_filearray(fileArray)
    OL.objectList = u.create_objects(fileArray)
    self.make_screen(OL,fileArray)

  def button_silence_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    u.silence_filearray_menu(OL,fileArray,butMenu)
    self.update_GUI(OL,fileArray)

  def refresh_screen(self,OL,fileArray,alarmLoop):
    self.controlButtons = self.make_control_buttons(OL,fileArray, alarmLoop)
    self.update_GUI(OL,fileArray)

