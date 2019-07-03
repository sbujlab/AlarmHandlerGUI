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
import utils as u
from time import gmtime, strftime, localtime

class ALARM_HISTORY(tk.Frame):
  def __init__(self, alarmHandlerWindow, tab, OL, fileArray, alarmLoop, HL):

    # The Alarm History is a page that will store information of previous alarms in Labels.
    
    # The kinds of alarms to display should be any alarm status that takes place, and the conditions for adding an alarm at the bottom of the list should be contingent upon that information not being superfluous.
    # An alarm which blinks on and off should not be added to the alarm handler many times, but instead we should utilize the UserNotifyStatus as our indicator of alarm. 
    # i.e. every time that the UserNotifyStatus turns not OK and not countdown then we want to add a new entry to our alarm handler
    # Silenced Alarms should be ignored.

    # The information should store the entire parameter list, though the information that is displayed at top level should be the 3 level name, the alarm status violation and the comparator that failed the test, and the time at which the alarm was initiated.

    # The routine should look exactly like the alarm_object Global Alarm Status decision loop, but instead of one global alarm status it will pick out each fresh alarm (that is not othewise currently active/non-user notify accepted) and add it to the list (a history text file).
    # The History Text file will be read after each checking/writing loop and used to display the alarm history on the screen. The top level details are put into the TLabel and the extra details are put into an information panel for the user to select (similar to the parameterList panel in other windows, but based on history, not an active alarm object)
    # An active alarm should be red, and allow the user to interact with that alarm similar to the alarm handler page (red, green, yellow, orange buttons mimicked).
    # An inactive alarm should still persist permenantly in full-history mode, but only the most recent N alarms should be displayed in default display mode. The Full-history mode should be a scrollable TFrame (basically just a redraw of truncated history to include full file contents).
    # The alarm history list is an independent alarmHistory object which contains just a historyArray file, owned by the main program (like the alarm_object and filearray lists for simplicity), which is comprised of a list of lists, where the columns are [parameter = value] pairs and the rows are individual history entries.
### class HISTORY_LIST():
###  def __init__(self,filen,delimiter,pdelimiter):
###    self.filename = filen
###    self.delim = delimiter
###    self.paramDelim = pdelimiter
###    self.filearray = u.parse_textfile(self) # Reads text file just like fileArray, same names so Python doesn't know the difference
###    self.historyList = u.init_historyList(self)

### def init_historyList(HL):
### def append_historyList(HL,OL,i):
### def write_historyFile(HL):


    self.controlFrame = tk.LabelFrame(tab, text='Alarm Controls', background=u.grey_color)
    self.alarmFrame = tk.LabelFrame(tab, text="Alarm History Viewer\nWait {} minutes before duplicating".format(HL.timeWait/60), background=u.lightgrey_color, font = ('Helvetica 14 bold'))
    self.pDataFrame = tk.LabelFrame(tab, text='Alarm Parameter Display', background=u.white_color)
    self.pDataFrame.disp = []
    self.colTitles = {0:"Saved Alarms"}
    self.NperCol = 8
    HL.displayPList = 0
    self.colsp = 3
    self.controlButtonsText = ["Backup History","Alarm Info"]
    self.CBTextSuffix1 = ["\nClear Current","\nShow Parameters"]
    self.CBTextSuffix2 = ["\nClear Current","\nHide Parameters"]

    self.alarmCols = []
    self.initialize_cols(HL)
    self.displayFrames = []
    self.buttonMenus = []
    self.controlButtons = self.make_control_buttons(OL,HL)
    self.make_screen(OL,HL)

  def make_control_buttons(self,OL,HL):
    grid = []
    for i in range(0, len(self.controlButtonsText)):
      newButt = tk.Button(self.controlFrame, text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix1[i]), default='active', justify='center', font = ('Helvetica 14 bold'),background=u.lightgrey_color)
      if self.controlButtonsText[i]=="Alarm Info":
      # Alarm Info
        if HL.displayPList == 0:
          newButt.config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix1[i]))
        else:
          newButt.config(text="{}{}".format(self.controlButtonsText[i],self.CBTextSuffix2[i]))
      newButt.indices = (i,0)
      newButt.config(command = lambda newBut=newButt: self.select_control_buttons(OL,HL,newBut))
      newButt.grid(row = 0, column = i,columnspan=1,padx=10,pady=10,sticky='W')
      grid.append(newButt)
    self.controlFrame.grid(columnspan=2, column=0, row=0, sticky='NW')
    return grid

  def select_control_buttons(self,OL,HL,but):
    i,j = but.indices
    for k in range(0,len(self.controlButtons)):
      self.controlButtons[k].grid_forget()
    if but.cget('text')=="{}{}".format(self.controlButtonsText[0],self.CBTextSuffix1[0]): 
      u.backup_clear_hist(HL)
      HL.currentHist = -1
      HL.displayPList = 0
      for each in self.controlButtons:
        each.destroy()
      self.controlButtons = self.make_control_buttons(OL,HL)
      self.update_GUI(OL,HL)
      return
    if but.cget('text')=="{}{}".format(self.controlButtonsText[1],self.CBTextSuffix1[1]): 
      # Alarm Info
      if HL.currentHist != -1:
        #Show parameters of currently selected button, else do nothing
        but.config(text="{}{}".format(self.controlButtonsText[1],self.CBTextSuffix2[1]))
        self.display_parameter_list(OL,HL,HL.currentHist)
        self.pDataFrame.grid(column=1,row=1, sticky='NE')
    elif but.cget('text')=="{}{}".format(self.controlButtonsText[1],self.CBTextSuffix2[1]):
      # Hide parameters
      but.config(text="{}{}".format(self.controlButtonsText[1],self.CBTextSuffix1[1]))
      HL.displayPList = 0
      self.erase_pDataFrame()
    for each in self.controlButtons:
      each.destroy()
    self.controlButtons = self.make_control_buttons(OL,HL)

  def make_screen(self,OL,HL):
    for i in range(0,len(self.alarmCols)):
      self.alarmCols[i].destroy()
    self.alarmCols = []
    self.initialize_cols(HL)
    for each in self.displayFrames:
      each.destroy()
    self.displayFrames = self.initialize_displayFrames(OL,HL)
    for each in self.buttonMenus:
      each.destroy()
    self.buttonMenus = self.initialize_menus(OL,HL)
    self.alarmFrame.grid_forget()
    self.alarmFrame.grid(column=0, row=1, sticky='NW')
    self.erase_pDataFrame()
    if HL.currentHist != -1 and HL.displayPList == 1:
      self.display_parameter_list(OL,HL,HL.currentHist)
      self.pDataFrame.grid(column=1,row=1, sticky='NE')
    self.erase_grid_all_col()
    self.layout_grid_all_col(HL)

  def initialize_cols(self,HL):
    for i in range(0, int(1.0*len(HL.historyList)/self.NperCol)+1):
      self.alarmCols.append(tk.LabelFrame(self.alarmFrame, text=self.colTitles.get(i,"ctd."), background=u.lightgrey_color))
      self.alarmCols[i].grid(column=i,row=0,pady=10,padx=10,sticky='N')


  def initialize_displayFrames(self,OL,HL): # Needs a short row to contain [name = value, alarm status = type, alarm stat !OK, user silence stat, alarm stat OK], context menu displays full parameter list
    lgrid = []
    if len(HL.historyList)>0 and HL.historyList != []:
      for i in range(0,len(HL.historyList)):
        # Loop over the list of objects, creating displayFrames
        disp = tk.LabelFrame(self.alarmCols[int(1.0*i/self.NperCol)], text=HL.historyList[i].get("Name",u.defaultKey), font=('Helvetica 10'), background=u.lightgrey_color)
        lgrid.append(disp)

        disp.statbutt = tk.Button(lgrid[i], text="{}".format(HL.historyList[i].get("Alarm Status",u.defaultKey)), justify='center', background=u.white_color) # loop over displayFrames
        disp.statbutt.indices = (0,i)
        disp.statbutt.config(command = lambda but=disp.statbutt: self.select_disp_button(OL,HL,but))
        disp.statbutt.grid(row=0,column=0,sticky='W')

        disp.butt = tk.Button(lgrid[i], text="Value = {}".format(HL.historyList[i].get("Value",u.defaultKey)), justify='center', background=u.lightgrey_color) # loop over displayFrames
        disp.butt.indices = (0,i)
        disp.butt.config(command = lambda but=disp.butt: self.select_disp_button(OL,HL,but))
        disp.butt.grid(row=0,column=1,sticky='EW')

        disp.timebutt = tk.Button(lgrid[i], text="Time = {}".format(strftime("%Y-%m-%d %H:%M:%S",HL.historyList[i].get("Time",u.defaultKey))), justify='center', background=u.white_color) # loop over displayFrames
        disp.timebutt.indices = (0,i)
        disp.timebutt.config(command = lambda but=disp.timebutt: self.select_disp_button(OL,HL,but))
        disp.timebutt.grid(row=0,column=2,sticky='E')
    else:
      disp = tk.Label(self.alarmCols[0], text="No Alarms stored in History", font=('Helvetica 12'), background=u.lightgrey_color)
      disp.grid()
      lgrid.append(disp)
    return lgrid

  def initialize_menus(self,OL,HL):
    grid = []
    for i in range(0, len(self.displayFrames)):
      if len(HL.historyList)>=i and self.displayFrames[i]['text'] != "No Alarms stored in History":
        buttMenu = tk.Menu(self.displayFrames[i].butt, tearoff=0) 
        buttMenu.indices = (0,i)
        buttMenu.moveN = 0
        buttMenu.editValue = None
        buttMenu.add_command(label = 'Information', command = lambda butMenu = buttMenu: self.button_information_menu(OL,HL,butMenu))
        self.displayFrames[i].butt.bind("<Button-3>",lambda event, butMenu = buttMenu: self.do_popup(event,butMenu))
        self.displayFrames[i].statbutt.bind("<Button-3>",lambda event, butMenu = buttMenu: self.do_popup(event,butMenu))
        self.displayFrames[i].timebutt.bind("<Button-3>",lambda event, butMenu = buttMenu: self.do_popup(event,butMenu))
        grid.append(buttMenu)
    return grid

  def do_popup(self,event,butMenu):
    butMenu.tk_popup(event.x_root,event.y_root,0)

  def layout_grid_all_col(self,HL):
    for i in range(0,len(self.displayFrames)):
      self.displayFrames[i].grid(column=int(1.0*i/self.NperCol),row=i%self.NperCol,columnspan=self.colsp,padx=0,pady=0,sticky='EW')

  def erase_grid_all_col(self):
    for i in range(0,len(self.displayFrames)):
      self.displayFrames[i].grid_forget()

  def select_disp_button(self,OL,HL,but):
    i,j = but.indices
    self.displayFrames[HL.currentHist].grid_forget()
    self.displayFrames[HL.currentHist].butt.grid_forget()
    self.displayFrames[HL.currentHist].butt.config(background=u.lightgrey_color)
    self.displayFrames[HL.currentHist].butt.grid(row=0,column=1,sticky='EW')
    self.displayFrames[HL.currentHist].grid(column=int(1.0*HL.currentHist/self.NperCol),row=HL.currentHist%self.NperCol,columnspan=self.colsp,padx=0,pady=0,sticky='EW')
    HL.currentHist = j
    #for k in range (0, len(self.displayFrames)):
    #  self.displayFrames[k].grid_forget()
    #  self.displayFrames[k].butt.config(background=u.lightgrey_color)
    #  self.displayFrames[k].butt.grid(row=0,column=1,sticky='EW')
    #  self.displayFrames[k].grid(column=int(1.0*k/self.NperCol),row=k%self.NperCol,columnspan=self.colsp,padx=0,pady=0,sticky='EW')
    self.displayFrames[j].grid_forget()
    self.displayFrames[j].butt.grid_forget()
    self.displayFrames[j].butt.config(background=u.grey_color)
    self.displayFrames[j].butt.grid(row=0,column=1,sticky='EW')
    self.displayFrames[j].grid(column=int(1.0*j/self.NperCol),row=j%self.NperCol,columnspan=self.colsp,padx=0,pady=0,sticky='EW')
    self.erase_pDataFrame()
    if HL.currentHist != -1 and HL.displayPList == 1:
      self.display_parameter_list(OL,HL,HL.currentHist)
      self.pDataFrame.grid(column=1,row=1, sticky='NE')

  def erase_pDataFrame(self):
    for k in range(0,len(self.pDataFrame.disp)):
      self.pDataFrame.disp[k].grid_forget()
    self.pDataFrame.grid_forget()

  def update_GUI(self,OL,HL):
    self.make_screen(OL,HL)

  def display_parameter_list(self,OL,HL,j):
    if j >= len(HL.historyList):
      return
    self.erase_pDataFrame()
    self.pDataFrame.disp = []
    HL.displayPList = 1
    localPlist = HL.historyList[j].copy()
    #self.pDataFrame.pack(padx=20,pady=10,anchor='nw')
    self.pDataFrame.grid(column=1,row=1,sticky='NW')
    k = 0
    for key in localPlist:
      if key == "Time":
        self.pDataFrame.disp.append(tk.Label(self.pDataFrame, text="{} = {}".format(key,strftime("%Y-%m-%d %H:%M:%S",localPlist[key])), background=u.lightgrey_color)) # FIXME want red alarm full label frame?
      else:
        self.pDataFrame.disp.append(tk.Label(self.pDataFrame, text="{} = {}".format(key, localPlist[key]), background=u.lightgrey_color)) # FIXME want red alarm full label frame?
      self.pDataFrame.disp[k].grid(row=k,column=0,padx=5,pady=5,sticky='W')
      k+=1

  def button_information_menu(self,OL,HL,butMenu):
    i,j = butMenu.indices
    self.select_disp_button(OL,HL,butMenu)
    self.display_parameter_list(OL,HL,j)
    self.controlButtons[1].grid_forget()
    self.controlButtons[1].config(text="{}{}".format(self.controlButtonsText[1],self.CBTextSuffix2[1]))
    self.controlButtons[1].grid(row = 0, column = 1,columnspan=1,padx=10,pady=10,sticky='N')

  def refresh_screen(self,OL,fileArray,alarmLoop,HL):
    for each in self.controlButtons:
      each.destroy()
    self.controlButtons = self.make_control_buttons(OL,HL)
    self.update_GUI(OL,HL)

