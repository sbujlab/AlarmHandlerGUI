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
import bclient as bclient
import utils as u

class ALARM_HANDLER(tk.Frame):
  def __init__(self, alarmHandlerWindow, tab, OL, fileArray, alarmLoop, HL, **kwargs):
    # Original bunch of LabelFrame contents
    self.controlFrame = tk.LabelFrame(tab, text='Alarm Controls', background=u.grey_color)
    self.alarmFrame = tk.LabelFrame(tab, text='Alarm Handler Viewer', background=u.lightgrey_color)
#    self.aFrame = tk.Frame(self.alarmFrame, background=u.lightgrey_color)
    self.pDataFrame = tk.LabelFrame(tab, text='Alarm Parameter Display', background=u.white_color)
    self.pDataFrame.disp = []
    self.colTitles = {0:"Alarms"}
    self.NperCol = 11
    # FIXME NperCol1 should change if the first column has some larger, special entries
    self.NperCol1 = 11
    OL.currentlySelectedButton = -1
    OL.displayPList = 0
    OL.displayPListN = -1
    self.colsp = 2
    self.remoteName = alarmHandlerWindow.remoteName
    self.HBchecked = 0
    self.controlButtonsText = ["Alarm Status","Alarm Checker","Silencer","Test Sound","Alarm Info"]
    self.CBTextSuffix1 = ["\nFind Alarm","\nPause" ,"\nSilence","\nHeartbeat: Start","\nShow Parameters"]
    self.CBTextSuffix2 = ["\nFind Alarm","\nUnpause","\nUnsilence","\n-1","\nHide Parameters"]

    self.alarmCols = []
    #self.initialize_cols(OL)
    self.displayFrames = []
    self.buttonMenus = []
    self.controlButtons = self.make_control_buttons(OL,fileArray, alarmLoop)
    self.make_screen(OL,fileArray, **kwargs)


  def update_layout(self):
    self.aFrame.update_idletasks()
    self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    self.canvas.yview('moveto', '0.0')
    self.canvas.xview('moveto', '0.0')
    self.aFrame.size = self.alarmFrame.grid_size()

  def on_configure(self, event):
    w, h = event.width, event.height
    natural = self.frame.winfo_reqwidth()
    self.canvas.itemconfigure('inner', width=w if w > natural else natural)
    self.canvas.configure(scrollregion=self.canvas.bbox('all'))


  def make_control_buttons(self,OL,fileArray,alarmLoop):
    grid = []
    for i in range(0, len(self.controlButtonsText)):
      newButt = tk.Button(self.controlFrame, text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix1[i]), default='active', justify='center', font = ('Helvetica 14 bold'),background=u.lightgrey_color)
      if self.controlButtonsText[i]=="Alarm Checker" and alarmLoop.globalLoopStatus != "Looping":
        newButt.config(background=u.yellow_color)
        newButt.config(fg=u.black_color)
        newButt.config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix2[i]))
      if self.controlButtonsText[i]=="Silencer" and alarmLoop.globalUserAlarmSilence == "Silenced":
        newButt.config(background=u.yellow_color)
        newButt.config(fg=u.black_color)
        newButt.config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix2[i]))
      if self.controlButtonsText[i]=="Alarm Status":
        if alarmLoop.globalAlarmStatus != "OK" and alarmLoop.globalUserAlarmSilence != "Silenced":
          newButt.config(background=u.red_color)
          newButt.config(fg=u.white_color)
        elif alarmLoop.globalAlarmStatus == "OK" and alarmLoop.globalUserAlarmSilence != "Silenced":
          newButt.config(fg=u.black_color)
          newButt.config(background=u.lightgrey_color)
        elif alarmLoop.globalUserAlarmSilence == "Silenced": 
          newButt.config(fg=u.black_color)
          newButt.config(background=u.yellow_color)
        if alarmLoop.globalLoopStatus != "Looping":
          newButt.config(fg=u.black_color)
          newButt.config(background=u.yellow_color)
      if self.controlButtonsText[i]=="Test Sound":
      # Alarm Test
        newButt.config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix1[i]))
      if self.controlButtonsText[i]=="Alarm Info":
      # Alarm Info
        if OL.displayPList == 0:
          newButt.config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix1[i]))
        else:
          newButt.config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix2[i]))
      newButt.indices = (i,0)
      newButt.config(command = lambda newBut=newButt: self.select_control_buttons(OL,fileArray,alarmLoop,newBut))
      newButt.grid(row = 0, column = i,columnspan=1,padx=5,pady=5,sticky='W')
      grid.append(newButt)
    self.controlFrame.grid(columnspan=2, column=0, row=0, sticky='NW')
    return grid

  def update_control_buttons(self,OL,fileArray,alarmLoop):
#    self.controlButtons
    for i in range(0, len(self.controlButtons)):
      #newButt = tk.Button(self.controlFrame, text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix1[i]), default='active', justify='center', font = ('Helvetica 14 bold'),background=u.lightgrey_color)
      if self.controlButtonsText[i]=="Alarm Checker" and alarmLoop.globalLoopStatus != "Looping":
        self.controlButtons[i].config(background=u.yellow_color)
        self.controlButtons[i].config(fg=u.black_color)
        self.controlButtons[i].config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix2[i]))
      if self.controlButtonsText[i]=="Silencer" and alarmLoop.globalUserAlarmSilence == "Silenced":
        self.controlButtons[i].config(background=u.yellow_color)
        self.controlButtons[i].config(fg=u.black_color)
        self.controlButtons[i].config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix2[i]))
      if self.controlButtonsText[i]=="Alarm Status":
        if alarmLoop.globalAlarmStatus != "OK" and alarmLoop.globalUserAlarmSilence != "Silenced":
          self.controlButtons[i].config(background=u.red_color)
          self.controlButtons[i].config(fg=u.white_color)
        elif alarmLoop.globalAlarmStatus == "OK" and alarmLoop.globalUserAlarmSilence != "Silenced":
          self.controlButtons[i].config(fg=u.black_color)
          self.controlButtons[i].config(background=u.lightgrey_color)
        elif alarmLoop.globalUserAlarmSilence == "Silenced": 
          self.controlButtons[i].config(fg=u.black_color)
          self.controlButtons[i].config(background=u.yellow_color)
        if alarmLoop.globalLoopStatus != "Looping":
          self.controlButtons[i].config(fg=u.black_color)
          self.controlButtons[i].config(background=u.yellow_color)
      if self.controlButtonsText[i]=="Test Sound":
        if self.HBchecked == 0:
          self.CBTextSuffix2[i] = self.CBTextSuffix1[i] # Grab prior value
          self.CBTextSuffix1[i] = "\nHeartbeat: {}".format(alarmLoop.userNotifyLoop.nLoops%1000)
          print("{}{}".format(self.CBTextSuffix1[i],self.CBTextSuffix2[i]))
        if self.CBTextSuffix2[i] == self.CBTextSuffix1[i]:
          self.controlButtons[i].config(background=u.red_color)
          self.controlButtons[i].config(fg=u.white_color)
          self.controlButtons[i].config(text="{}{}".format(self.controlButtonsText[i],"\nERROR, Loop Died, PLEASE REBOOT"))
          bclient.sockClient(self.remoteName).sendPacket("7") 
        else: 
          self.controlButtons[i].config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix1[i]))
        self.HBchecked = 0
      if self.controlButtonsText[i]=="Alarm Info":
      # Alarm Info
        if OL.displayPList == 0:
          self.controlButtons[i].config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix1[i]))
        else:
          self.controlButtons[i].config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix2[i]))
      #self.controlButtons[i].indices = (i,0)
      #self.controlButtons[i].config(command = lambda newBut=self.controlButtons[i]: self.select_control_buttons(OL,fileArray,alarmLoop,newBut))

  def select_control_buttons(self,OL,fileArray,alarmLoop,but):
    i,j = but.indices
    #for k in range(0,len(self.controlButtons)):
      #self.controlButtons[k].grid_forget()
    if but.cget('text')=="{}{}".format(self.controlButtonsText[2],self.CBTextSuffix1[2]):# and alarmLoop.globalUserAlarmSilence == "Alert": 
      # Silenced All
      alarmLoop.globalUserAlarmSilence = "Silenced"
      but.config(background=u.yellow_color)
      but.config(text="{}{}".format(self.controlButtonsText[2],self.CBTextSuffix2[2]))
      self.controlButtons[0].config(background=u.yellow_color)
    elif but.cget('text')=="{}{}".format(self.controlButtonsText[2],self.CBTextSuffix2[2]):# and alarmLoop.globalUserAlarmSilence == "Silenced":
      alarmLoop.globalUserAlarmSilence = "Alert"
      but.config(background=u.lightgrey_color)
      but.config(text="{}{}".format(self.controlButtonsText[2],self.CBTextSuffix1[2]))
      if alarmLoop.globalAlarmStatus != "OK":
        self.controlButtons[0].config(background=u.red_color)
      else:
        self.controlButtons[0].config(background=u.lightgrey_color)
    if but.cget('text')==self.controlButtonsText[1]+self.CBTextSuffix1[1] and alarmLoop.globalLoopStatus == "Looping": 
      # Paused Loop
      print("Turning off loop")
      alarmLoop.globalLoopStatus = "Paused"
      but.config(background=u.yellow_color)
      but.config(text="{}{}".format(self.controlButtonsText[1],self.CBTextSuffix2[1]))
    elif but.cget('text')=="{}{}".format(self.controlButtonsText[1],self.CBTextSuffix2[1]) and alarmLoop.globalLoopStatus == "Paused":
      print("Turning on loop")
      alarmLoop.globalLoopStatus = "Looping"
      # FIXME FIXME necessary?
      alarmLoop.alarmList = OL.objectList
      #gc.collect()
      #del gc.garbage[:]
      but.config(background=u.lightgrey_color)
      but.config(text="{}{}".format(self.controlButtonsText[1],self.CBTextSuffix1[1]))
    if but.cget('text')=="{}{}".format(self.controlButtonsText[0],self.CBTextSuffix1[0]): 
      # Alarm Go To Control Button
      if alarmLoop.globalAlarmStatus != "OK" and alarmLoop.globalUserAlarmSilence != "Silenced":
        but.config(background=u.red_color)
      elif alarmLoop.globalAlarmStatus != "OK" and alarmLoop.globalUserAlarmSilence == "Silenced":
        but.config(background=u.yellow_color)
      elif alarmLoop.globalAlarmStatus == "OK":
        but.config(background=u.lightgrey_color)
      OL.currentlySelectedButton=u.recentAlarmButton # Update the currently clicked button index to the alarming one
      if OL.currentlySelectedButton != -1:
        self.select_button(OL,fileArray,self.displayFrames[OL.currentlySelectedButton].butt)
      #self.update_GUI(OL,fileArray)
    if but.cget('text')=="{}{}".format(self.controlButtonsText[3],self.CBTextSuffix1[3]): 
      but.config(text="{}{}".format(self.controlButtonsText[3],self.CBTextSuffix1[3]))
      bclient.sockClient(self.remoteName).sendPacket("7") 
    if but.cget('text')=="{}{}".format(self.controlButtonsText[4],self.CBTextSuffix1[4]): 
      # Alarm Info
      if OL.currentlySelectedButton != -1:
        #Show parameters of currently selected button, else do nothing
        but.config(text="{}{}".format(self.controlButtonsText[4],self.CBTextSuffix2[4]))
        self.display_parameter_list(OL,fileArray,2,OL.currentlySelectedButton)
        self.pDataFrame.grid(column=1,row=1, sticky='NE')
    elif but.cget('text')=="{}{}".format(self.controlButtonsText[4],self.CBTextSuffix2[4]):
      # Hide parameters
      but.config(text="{}{}".format(self.controlButtonsText[4],self.CBTextSuffix1[4]))
      #OL.currentlySelectedButton = -1
      OL.displayPList = 0
      self.erase_pDataFrame()
      self.update_GUI(OL,fileArray)
    #for each in self.controlButtons:
    #  each.destroy()
    #self.controlButtons = self.make_control_buttons(OL,fileArray,alarmLoop)
    self.HBchecked = 1
    self.update_control_buttons(OL,fileArray,alarmLoop)

  def make_screen(self,OL,fileArray):
    #tk.Frame.__init__(self.alarmFrame, tab, width=2000, height=2000, **kwargs)  # holds canvas & scrollbars
    self.alarmFrame.grid_rowconfigure(0, weight=1)
    self.alarmFrame.grid_columnconfigure(0, weight=1)
    #FIXME Arbitrarily chose width = 850 and height = 750 because it looks good
    self.canvas = tk.Canvas(self.alarmFrame, width=850, height=750, bd=0, highlightthickness=0)
    self.hScroll = tk.Scrollbar(self.alarmFrame, orient='horizontal',
        command=self.canvas.xview)
    self.hScroll.grid(row=1, column=0, sticky='we')
    self.vScroll = tk.Scrollbar(self.alarmFrame, orient='vertical',
        command=self.canvas.yview)
    self.vScroll.grid(row=0, column=1, sticky='ns')
    self.canvas.grid(row=0, column=0, sticky='nsew')
    self.canvas.configure(xscrollcommand=self.hScroll.set,
        yscrollcommand=self.vScroll.set)

    self.aFrame = tk.Frame(self.canvas, width=1850, height=1750, bd=2)
    self.aFrame.grid_columnconfigure(0, weight=1)
    self.canvas.create_window(0, 0, window=self.aFrame, anchor='nw', tags='inner')
    # OLD
    for i in range(0,len(self.alarmCols)):
      self.alarmCols[i].destroy()
    self.alarmCols = []
    self.initialize_cols(OL)
    for each in self.displayFrames:
      each.destroy()
    self.displayFrames = self.initialize_displayFrames(OL,fileArray)
    for each in self.buttonMenus:
      each.destroy()
    self.buttonMenus = self.initialize_menus(OL,fileArray)
    self.alarmFrame.grid_forget()
    self.alarmFrame.grid(column=0, row=1, sticky='NW')
    self.erase_pDataFrame()
    if OL.currentlySelectedButton != -1 and OL.displayPList == 1:
      self.display_parameter_list(OL,fileArray,2,OL.currentlySelectedButton)
      self.pDataFrame.grid(column=1,row=1, sticky='NE')
    self.erase_grid_all_col()
    self.layout_grid_all_col(OL,fileArray)
    if OL.currentlySelectedButton != -1:
      self.select_button(OL,fileArray,self.displayFrames[OL.currentlySelectedButton].butt)
    #print("currently selected button = {}".format(OL.currentlySelectedButton))

    # NEW
    self.update_layout()
    self.canvas.bind('<Configure>', self.on_configure)


  def initialize_cols(self,OL):
    for i in range(0, int(1.0*(len(OL.keys)+(self.NperCol-self.NperCol1))/(self.NperCol))+1):
      self.alarmCols.append(tk.LabelFrame(self.aFrame, text=self.colTitles.get(i,"ctd."), background=u.lightgrey_color))
      self.alarmCols[i].grid(column=i,row=0,padx=5,pady=5,sticky='N')

  def update_displayFrame(self,OL,localBut):
    i,j = localBut.indices
    self.displayFrames[j].butt.config(text="{}".format(OL.objectList[OL.keys[j]].parameterList.get("Value",u.defaultKey))) # loop over displayFrames
    #self.displayFrames[j].butt.config(text="Value = {}".format(OL.objectList[OL.keys[j]].parameterList.get("Value",u.defaultKey))) # loop over displayFrames
    #self.displayFrames[j].butt.grid_forget()
    #self.displayFrames[j].radioButGreen.grid_forget()
    #self.displayFrames[j].radioButRed.grid_forget()
    #self.displayFrames[j].radioButYellow.grid_forget()
    #self.displayFrames[j].radioButOrange.grid_forget()

    #self.displayFrames[j].alarmStatus = 0
    #self.displayFrames[j].greenAlarmStatus = 0
    #self.displayFrames[j].userNotifyStatus = 0
    #self.displayFrames[j].userSilenceStatus = 0

    self.displayFrames[j].redStat.set(0)
    self.displayFrames[j].orangeStat.set(0)
    self.displayFrames[j].yellowStat.set(0)
    self.displayFrames[j].greenStat.set(0)

    #self.displayFrames[j].butt.grid(row=0,column=1,sticky='E')
    if OL.objectList[OL.keys[j]].userNotifyStatus != "OK" and OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')[0] != "Cooldown" and OL.objectList[OL.keys[j]].userSilenceStatus != "Silenced":
      # Then we are alarmed
      self.displayFrames[j].radioButGreen.grid_forget()
      self.displayFrames[j].radioButYellow.grid_forget()
      self.displayFrames[j].radioButOrange.grid_forget()
      # THIS WAS ALREADY HERE... FIXME:
      self.displayFrames[j].alarmStatus = 0
      self.displayFrames[j].radioButRed.grid(row=0,column=0,padx=5,sticky='W')
      self.displayFrames[j].radioButRed.config(text=OL.objectList[OL.keys[j]].alarmStatus, value = self.displayFrames[j].alarmStatus)
      # Reset
      self.displayFrames[j].userNotifyStatus = 1
      self.displayFrames[j].userSilenceStatus = 1
      self.displayFrames[j].greenAlarmStatus = 1
    if OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')[0] == "Cooldown" and OL.objectList[OL.keys[j]].userSilenceStatus != "Silenced":
      self.displayFrames[j].radioButGreen.grid_forget()
      self.displayFrames[j].radioButRed.grid_forget()
      self.displayFrames[j].radioButYellow.grid_forget()
      self.displayFrames[j].radioButOrange.grid(row=0,column=0,padx=5,sticky='W')
      self.displayFrames[j].userNotifyStatus = 0
      self.displayFrames[j].radioButOrange.config(text=OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')[1], value = self.displayFrames[j].userNotifyStatus)
      # Reset
      self.displayFrames[j].alarmStatus = 1
      self.displayFrames[j].userSilenceStatus = 1
      self.displayFrames[j].greenAlarmStatus = 1
    # Silence takes precedent over alarm and over notify/acknowledge
    if OL.objectList[OL.keys[j]].userSilenceStatus == "Silenced":
      self.displayFrames[j].radioButGreen.grid_forget()
      self.displayFrames[j].radioButRed.grid_forget()
      self.displayFrames[j].radioButOrange.grid_forget()
      #self.displayFrames[j].radioButYellow.grid_forget()
      self.displayFrames[j].radioButYellow.grid(row=0,column=0,padx=5,sticky='W')
      self.displayFrames[j].userSilenceStatus = 0
      if OL.objectList[OL.keys[j]].alarmStatus == "OK":
        self.displayFrames[j].radioButYellow.config(text=OL.objectList[OL.keys[j]].userSilenceStatus, value = self.displayFrames[j].userSilenceStatus)
      if OL.objectList[OL.keys[j]].alarmStatus != "OK":
        self.displayFrames[j].radioButYellow.config(text=OL.objectList[OL.keys[j]].userNotifyStatus, value = self.displayFrames[j].userSilenceStatus)
      # Reset
      self.displayFrames[j].alarmStatus = 1
      self.displayFrames[j].userNotifyStatus = 1
      self.displayFrames[j].greenAlarmStatus = 1
    if OL.objectList[OL.keys[j]].alarmStatus == "OK" and OL.objectList[OL.keys[j]].userSilenceStatus != "Silenced" and OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')[0] == "OK":
      # Then we are all GOOD :)
      # Add check on userNotifyStatus so that the user will keep seeing the alarm indicator on even after the alarm itself has disappeared
      #if self.displayFrames[j].greenAlarmStatus != 0:
      # Then erase all and start a new green one, else do nothing
      self.displayFrames[j].radioButRed.grid_forget()
      self.displayFrames[j].radioButYellow.grid_forget()
      self.displayFrames[j].radioButOrange.grid_forget()
      self.displayFrames[j].radioButGreen.grid(row=0,column=0,padx=5,sticky='W')
      self.displayFrames[j].greenAlarmStatus = 0
      self.displayFrames[j].radioButGreen.config(text='   ', value = self.displayFrames[j].greenAlarmStatus)
      # Reset
      self.displayFrames[j].alarmStatus = 1
      self.displayFrames[j].userNotifyStatus = 1
      self.displayFrames[j].userSilenceStatus = 1
    



  def initialize_displayFrames(self,OL,fileArray): # Needs a short row to contain [name = value, alarm status = type, alarm stat !OK, user silence stat, alarm stat OK], context menu displays full parameter list
    lgrid = []
    if len(OL.objectList)>0:
      for key in OL.keys:
        i = OL.objectList[key].index
        # Loop over the list of objects, creating displayFrames
        localStr = "{}".format(key)
        # Write a string that is composed of the three levels - Top, second, and Name, with some useful formating.
        if len(localStr) > 30:
          localStr = "{}\n{}".format(key[:25],key[25:])
        perCol = self.NperCol
        if i < self.NperCol:
          perCol = self.NperCol1
          disp = tk.LabelFrame(self.alarmCols[int(1.0*((i)/perCol))], text=localStr, font=('Helvetica 8'), background=u.lightgrey_color) 
        else:
          disp = tk.LabelFrame(self.alarmCols[int(1.0*((i+self.NperCol-self.NperCol1)/perCol))], text=localStr, font=('Helvetica 8'), background=u.lightgrey_color) 
        disp.redStat = tk.IntVar()
        disp.orangeStat = tk.IntVar()
        disp.yellowStat = tk.IntVar()
        disp.greenStat = tk.IntVar()
        disp.redStat.set(0)
        disp.orangeStat.set(0)
        disp.yellowStat.set(0)
        disp.greenStat.set(0)
        disp.alarmStatus = 0
        disp.greenAlarmStatus = 0
        disp.userNotifyStatus = 0
        disp.userSilenceStatus = 0
        if OL.objectList[key].alarmStatus != "OK":
          disp.alarmStatus = 0
          disp.greenAlarmStatus = 1
        if OL.objectList[key].userSilenceStatus != "Alert":
          disp.userSilenceStatus = 0 
        if OL.objectList[key].userSilenceStatus != "Silenced" and OL.objectList[key].userNotifyStatus.split(' ')[0] == "Cooldown":
          # Not silenced, and in Cooldown time period, then show this button instead
          disp.userNotifyStatus = 0
        lgrid.append(disp)

        disp.butt = tk.Button(lgrid[i], text="Value = {}".format(OL.objectList[key].parameterList.get("Value",u.defaultKey)), justify='center', background=u.lightgrey_color) # loop over displayFrames
        #disp.butt = tk.Button(lgrid[i], text="{}".format(OL.objectList[key].parameterList.get("Value",u.defaultKey)), justify='center', background=u.lightgrey_color) # loop over displayFrames
        #disp.butt = tk.Button(lgrid[i], text="Value = {}".format(OL.objectList[key].parameterList.get("Value",u.defaultKey)), justify='center', background=OL.objectList[key].color) # loop over displayFrames
        disp.butt.indices = (2,i)
        disp.butt.config(command = lambda but=disp.butt: self.select_disp_button(OL,fileArray,but))
        disp.butt.grid(row=0,column=1,sticky='E')
        disp.radioButRed = tk.Radiobutton(lgrid[i], text=OL.objectList[key].alarmStatus, indicatoron=False, justify='left', value=lgrid[i].alarmStatus, variable=lgrid[i].redStat, fg=u.white_color, bg=u.lightgrey_color,
            activebackground=u.grey_color, activeforeground=u.black_color, selectcolor = u.red_color, highlightbackground=u.red_color, highlightcolor=u.red_color, highlightthickness=1)
        disp.radioButRed.indices = (2,i)
        disp.radioButRed.config(command = lambda radRed=disp.radioButRed: self.select_red_button(OL,fileArray,radRed))
        disp.radioButOrange = tk.Radiobutton(lgrid[i], text=OL.objectList[key].userNotifyStatus, indicatoron=False, justify='center', value=lgrid[i].userNotifyStatus, variable=lgrid[i].orangeStat, fg=u.black_color, bg=u.lightgrey_color,
            activebackground=u.grey_color, activeforeground=u.black_color, selectcolor = u.orange_color, highlightbackground=u.orange_color, highlightcolor=u.orange_color, highlightthickness=1)
        disp.radioButOrange.indices = (2,i)
        disp.radioButOrange.config(command = lambda radOrange=disp.radioButOrange: self.select_orange_button(OL,fileArray,radOrange))
        disp.radioButYellow = tk.Radiobutton(lgrid[i], text=OL.objectList[key].userSilenceStatus, indicatoron=False, justify='center', value=lgrid[i].userSilenceStatus, variable=lgrid[i].yellowStat, fg=u.black_color, bg=u.lightgrey_color,
            activebackground=u.grey_color, activeforeground=u.black_color, selectcolor = u.yellow_color, highlightbackground=u.yellow_color, highlightcolor=u.yellow_color, highlightthickness=1)
        disp.radioButYellow.indices = (2,i)
        disp.radioButYellow.config(command = lambda radYellow=disp.radioButYellow: self.select_yellow_button(OL,fileArray,radYellow))
        disp.radioButGreen = tk.Radiobutton(lgrid[i], text=OL.objectList[key].alarmStatus, indicatoron=False, justify='right', value=lgrid[i].greenAlarmStatus, variable=lgrid[i].greenStat, fg=u.black_color, bg=u.lightgrey_color,
            activebackground=u.grey_color, activeforeground=u.black_color, selectcolor = u.green_color, highlightbackground=u.green_color, highlightcolor=u.green_color, highlightthickness=1)
        disp.radioButGreen.indices = (2,i)
        #print("OL 2,{} alarm status = {}".format(i,OL.objectList[key].alarmStatus))
        disp.radioButGreen.config(command = lambda radGreen=disp.radioButGreen: self.select_green_button(OL,fileArray,radGreen))
        #if (OL.objectList[key].alarmStatus != "OK" or (OL.objectList[key].userNotifyStatus.split(' ')[0] != "OK" and OL.objectList[key].userNotifyStatus.split(' ')[0] != "Cooldown")) and OL.objectList[key].userSilenceStatus != "Silenced":
        if OL.objectList[key].userNotifyStatus != "OK" and OL.objectList[key].userNotifyStatus.split(' ')[0] != "Cooldown" and OL.objectList[key].userSilenceStatus != "Silenced":
          disp.alarmStatus = 0
          disp.radioButRed.grid(row=0,column=0,padx=5,sticky='W')
          disp.radioButRed.config(text=OL.objectList[key].alarmStatus, value = disp.alarmStatus)
        if OL.objectList[key].userNotifyStatus.split(' ')[0] == "Cooldown" and OL.objectList[key].userSilenceStatus != "Silenced":
          disp.radioButOrange.grid(row=0,column=0,padx=5,sticky='W')
          disp.radioButOrange.config(text=OL.objectList[key].userNotifyStatus.split(' ')[1])
        # Silence takes precedent over alarm and over notify/acknowledge
        if OL.objectList[key].alarmStatus == "OK" and OL.objectList[key].userSilenceStatus == "Silenced":
          disp.radioButYellow.grid(row=0,column=0,padx=5,sticky='W')
          disp.radioButYellow.config(text=OL.objectList[key].userSilenceStatus)
        if OL.objectList[key].alarmStatus != "OK" and OL.objectList[key].userSilenceStatus == "Silenced":
          disp.radioButYellow.grid(row=0,column=0,padx=5,sticky='W')
          disp.radioButYellow.config(text=OL.objectList[key].userNotifyStatus)
          #disp.radioButYellow.config(text=OL.objectList[key].alarmStatus)
        if OL.objectList[key].alarmStatus == "OK" and OL.objectList[key].userSilenceStatus != "Silenced" and OL.objectList[key].userNotifyStatus.split(' ')[0] == "OK":
          # Add check on userNotifyStatus so that the user will keep seeing the alarm indicator on even after the alarm itself has disappeared
          disp.radioButGreen.grid(row=0,column=0,padx=5,sticky='W')
          disp.radioButGreen.config(text='   ')
    return lgrid

  def initialize_menus(self,OL,fileArray):
    grid = []
    #print("Adding menus, len(self.alarmCols) = {} times".format(len(self.alarmCols)))
    for i in range(0, len(self.displayFrames)):
      if len(OL.keys)>=i:
        buttMenu = tk.Menu(self.displayFrames[i].butt, tearoff=0) # Is having the owner be button correct?
        buttMenu.indices = (2,OL.objectList[OL.keys[i]].index)
        buttMenu.moveN = 0
        buttMenu.editValue = None
        buttMenu.add_command(label = 'Information', command = lambda butMenu = buttMenu: self.button_information_menu(OL,fileArray,butMenu))
        buttMenu.add_command(label = 'Acknowledge Alarm', command = lambda butMenu = buttMenu: self.button_notify_acknowledge_menu(OL,fileArray,butMenu))
        buttMenu.add_command(label = 'Silence', command = lambda butMenu = buttMenu: self.button_silence_menu(OL,fileArray,butMenu))
        self.displayFrames[i].butt.bind("<Button-3>",lambda event, butMenu = buttMenu: self.do_popup(event,butMenu))
        grid.append(buttMenu)
    return grid

  def do_popup(self,event,butMenu):
    butMenu.tk_popup(event.x_root,event.y_root,0)

  def layout_grid_all_col(self,OL,fileArray):
    for i in range(0,len(self.displayFrames)):
      perCol = self.NperCol
      if i < self.NperCol1:
        perCol = self.NperCol1
        self.displayFrames[i].grid(column=int(1.0*(i)/perCol),row=i%perCol,columnspan=self.colsp,padx=5,pady=5,sticky='EW')
      else:
        self.displayFrames[i].grid(column=int(1.0*(i+self.NperCol-self.NperCol1)/perCol),row=i%perCol,columnspan=self.colsp,padx=5,pady=5,sticky='EW')
    #self.buttonMenus = self.initialize_menus(OL,fileArray)

  def erase_grid_all_col(self):
    for i in range(0,len(self.displayFrames)):
      self.displayFrames[i].grid_forget()

  def erase_pDataFrame(self):
    for k in range(0,len(self.pDataFrame.disp)):
      self.pDataFrame.disp[k].grid_forget()
    self.pDataFrame.grid_forget()

  def refresh_button(self,OL,fileArray,but):
    i,j = but.indices
    OL.set_clicked(i,j) # Update that object's color to dark grey
    #if i==2:
    OL.currentlySelectedButton=OL.objectList[OL.keys[j]].index
    #self.set_button_clicked(OL,fileArray,i,j) # Re-organize the grid and change the non-clicked buttons back to regular light grey
    #self.buttons[i][j].config(background=OL.objectList[OL.keys[j]].color) # Update that button to be the newly update object's new color (could just use but.config)

  def select_button(self,OL,fileArray,but):
    i,j = but.indices
    OL.currentlySelectedButton = j
    OL.set_clicked(i,j) # Update that object's color to dark grey
    for k in range(0,len(self.displayFrames)):
      if k == j:
        self.displayFrames[k].butt.config(background=u.darkgrey_color) 
      else:
        self.displayFrames[k].butt.config(background=u.lightgrey_color) 
    if OL.currentlySelectedButton != -1 and OL.displayPList == 1:
      self.display_parameter_list(OL,fileArray,2,OL.currentlySelectedButton)
      self.pDataFrame.grid(column=1,row=1, sticky='NE')
    #self.displayFrames[j].config(background=OL.objectList[OL.keys[j]].color) # Update that button to be the newly update object's new color (could just use but.config)

  def select_disp_button(self,OL,fileArray,but):
    i,j = but.indices
    self.select_button(OL,fileArray,but)
    #self.update_GUI(OL,fileArray)

  def select_red_button(self,OL,fileArray,but):
    i,j = but.indices
    self.select_button(OL,fileArray,but)
    # Add a feature where clicking the red button counts as an alarm acknowledge
    self.displayFrames[j].greenAlarmStatus = 1
    u.notify_acknowledge_filearray_menu(OL,fileArray,but)
    alStat = 0 # Always maintain buttons in activated state, just hide them
    but.config(value=alStat)
    self.update_displayFrame(OL,but)
    self.select_button(OL,fileArray,but)
    #self.update_GUI(OL,fileArray)

  def select_orange_button(self,OL,fileArray,but):
    i,j = but.indices
    #self.select_button(OL,fileArray,but)
    self.displayFrames[j].alarmStatus = 1
    self.displayFrames[j].userSilenceStatus = 1
    self.displayFrames[j].greenAlarmStatus = 1
    # If the user has acknowledged the alarm then we will be in a cooldown state and this button is visible, now if the user clicks again they will force->"OK" the userNotifyStatus to skip the cooldown period 
    u.notify_acknowledge_filearray_menu(OL,fileArray,but)
    # FIXME FIXME this set of OL manipulations should just be inside above line... right?
    OL.objectList[OL.keys[j]].userNotifyStatus = OL.objectList[OL.keys[j]].alarmStatus #"OK"
    OL.objectList[OL.keys[j]].parameterList["User Notify Status"] = OL.objectList[OL.keys[j]].alarmStatus #"OK"
    OL.objectList[OL.keys[j]].alarmStatus = OL.objectList[OL.keys[j]].alarmStatus #"OK"
    OL.objectList[OL.keys[j]].parameterList["Alarm Status"] = OL.objectList[OL.keys[j]].alarmStatus #"OK"
    notStat = 0 # Always maintain buttons in activated state, just hide them
    but.config(value=notStat)
    self.update_displayFrame(OL,but)
    self.select_button(OL,fileArray,but)
    #self.update_GUI(OL,fileArray)

  def select_yellow_button(self,OL,fileArray,but):
    i,j = but.indices
    #self.select_button(OL,fileArray,but)
    self.displayFrames[j].alarmStatus = 1
    self.displayFrames[j].userNotifyStatus = 1
    self.displayFrames[j].greenAlarmStatus = 1
    u.silence_filearray_menu(OL,fileArray,but)
    silStat = 0 # Always maintain buttons in activated state, just hide them
    but.config(value=silStat)
    self.update_displayFrame(OL,but)
    self.select_button(OL,fileArray,but)
    #self.update_GUI(OL,fileArray)

  def select_green_button(self,OL,fileArray,but):
    i,j = but.indices
    self.select_button(OL,fileArray,but)
    alStat = 0 # Always maintain buttons in activated state, just hide them
    but.config(value=alStat)
    #self.update_GUI(OL,fileArray)

  def update_GUI(self,OL,fileArray):
    # FIXME FIXME is this filearray refresh actually needed?
    #fileArray.filearray = u.write_filearray(fileArray)

    #OL.objectList = u.create_objects(fileArray,OL.cooldownLength)
    #self.make_screen(OL,fileArray)
    # NEW
    #for i in range(0,len(self.alarmCols)):
    #  self.alarmCols[i].destroy()
    #self.alarmCols = []
    #self.initialize_cols(OL)
    for each in self.displayFrames:
      localBut = each.butt
      self.update_displayFrame(OL,localBut)
      #each.destroy()
    #self.displayFrames = self.initialize_displayFrames(OL,fileArray)
    ####for each in self.buttonMenus:
    ####  each.destroy()
    ####self.buttonMenus = self.initialize_menus(OL,fileArray)
    #self.alarmFrame.grid_forget()
    #self.alarmFrame.grid(column=0, row=1, sticky='NW')
    #self.erase_pDataFrame()
    if OL.currentlySelectedButton != -1 and OL.displayPList == 1:
      self.display_parameter_list(OL,fileArray,2,OL.currentlySelectedButton)
    #  self.pDataFrame.grid(column=1,row=1, sticky='NE')
    #self.erase_grid_all_col()
    #self.layout_grid_all_col(OL,fileArray)
    if OL.currentlySelectedButton != -1:
      self.select_button(OL,fileArray,self.displayFrames[OL.currentlySelectedButton].butt)
    #print("currently selected button = {}".format(OL.currentlySelectedButton))

  def display_parameter_list(self,OL,fileArray,i,j):
    #self.pDataFrame.pack(padx=20,pady=10,anchor='nw')
    OL.displayPList = 1
    if j != OL.displayPListN:
      self.erase_pDataFrame()
      self.pDataFrame.grid(column=1,row=1,sticky='NW')
    else:
      for k in range(0,len(self.pDataFrame.disp)):
        self.pDataFrame.disp[k].grid_forget()
    self.pDataFrame.disp = []
    localPlist = OL.objectList[OL.keys[j]].parameterList.copy()
    k = 0
    for key in localPlist:
      self.pDataFrame.disp.append(tk.Label(self.pDataFrame, text="{} = {}".format(key, localPlist[key]), background=u.lightgrey_color)) 
      self.pDataFrame.disp[k].grid(row=k,column=0,padx=5,pady=5,sticky='W')
      k+=1
    OL.displayPListN = j


  def button_information_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    self.select_button(OL,fileArray,self.displayFrames[j].butt)
    self.display_parameter_list(OL,fileArray,i,j)
    #self.controlButtons[4].grid_forget()
    self.controlButtons[4].config(text="{}{}".format(self.controlButtonsText[4],self.CBTextSuffix2[4]))
    #self.controlButtons[4].grid(row = 0, column = 3,columnspan=1,padx=5,pady=5,sticky='W')
    ####self.update_GUI(OL,fileArray)

  def button_silence_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    #self.select_button(OL,fileArray,self.displayFrames[j].butt)
    self.displayFrames[j].alarmStatus = 1
    self.displayFrames[j].userNotifyStatus = 1
    self.displayFrames[j].greenAlarmStatus = 1
    u.silence_filearray_menu(OL,fileArray,butMenu)
    self.update_displayFrame(OL,self.displayFrames[j].radioButYellow)
    self.select_button(OL,fileArray,self.displayFrames[j].butt)
    #self.update_GUI(OL,fileArray)

  def button_notify_acknowledge_menu(self,OL,fileArray,butMenu):
    i,j = butMenu.indices
    self.select_button(OL,fileArray,self.displayFrames[j].butt)
    if OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')[0] != "Cooldown" and OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')[0] != "OK":
      self.displayFrames[j].greenAlarmStatus = 1
      u.notify_acknowledge_filearray_menu(OL,fileArray,butMenu)
    elif OL.objectList[OL.keys[j]].userNotifyStatus.split(' ')[0] == "Cooldown":
      u.notify_acknowledge_filearray_menu(OL,fileArray,butMenu)
      OL.objectList[OL.keys[j]].userNotifyStatus = OL.objectList[OL.keys[j]].alarmStatus #"OK"
      OL.objectList[OL.keys[j]].parameterList["User Notify Status"] = OL.objectList[OL.keys[j]].alarmStatus #"OK"
      OL.objectList[OL.keys[j]].alarmStatus = OL.objectList[OL.keys[j]].alarmStatus #"OK"
      OL.objectList[OL.keys[j]].parameterList["Alarm Status"] = OL.objectList[OL.keys[j]].alarmStatus #"OK"
    self.update_displayFrame(OL,self.displayFrames[j].radioButGreen)
    self.select_button(OL,fileArray,self.displayFrames[j].butt)
    #self.update_GUI(OL,fileArray)

  def refresh_screen(self,OL,fileArray,alarmLoop,HL):
    #for each in self.controlButtons:
    #  each.destroy()
    #self.controlButtons = self.make_control_buttons(OL,fileArray, alarmLoop)
    self.update_control_buttons(OL,fileArray,alarmLoop)
    self.update_GUI(OL,fileArray)
    if OL.currentlySelectedButton != -1:
      self.refresh_button(OL,fileArray,self.displayFrames[OL.currentlySelectedButton].butt)

