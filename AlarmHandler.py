'''
Alarm Handler GUI Revamp
Code Commissioned 2019-01-04
Code by A.J. Zec
Greyed and Alarmed by Cameron
  2019-05-28
'''

import tkinter as tk
from tkinter import ttk
import os
import webbrowser

import csv
import alarm_object
import tabs.alarm_handler as alarm_handler
import tabs.alarm_history as alarm_history
import utils as u

class AlarmHandler:

    def __init__(self):
        os.environ["TCL_LIBRARY"] = "/lib64/tcl8.5/"
        self.win = tk.Tk()
        self.win.title("Continuous Aggregate Monitor: Alarm Handler")
        self.win.configure(background=u.lightgrey_color)
        self.adc_options_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.bm_test_setting = tk.StringVar()
        self.clean_setting = tk.StringVar()
        self.get_alarm_handler_style()
        self.filename = "/adaqfs/home/apar/bin/alarm.csv"
        self.delim = ','
        self.filearray = None
        #self.objectList = None 
        self.parse_textfile()
        self.objectList = u.create_objects(self.filearray) 
        #self.create_objects()
        self.fGlobalAlarmStatus = 0 # Start in non-alarmed state
        self.fGlobalLoopStatus = 1 # Start in looping state
        self.create_widgets()

    def parse_textfile(self):
      self.filearray = []
      with open(self.filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=self.delim)
        for row in csv_reader:
          rowList = []
          for col in row:
            rowList.append(col)
          self.filearray.append(rowList)
  #return filearray

    def create_self_objects(self):
      #ncolumns = len(self.filearray[0]) # FIXME array 0?
      ncolumns = len(self.filearray[len(self.filearray)-1]) # FIXME array 0?
      nlines = len(self.filearray)
      self.objectList = []
      colRow = []
      line_previous = []
      for i in range(0,ncolumns):
        self.objectList.append([]) # Check this
        colRow.append(0)
        line_previous.append("NULL")
      for lineN in range(0,nlines):
        line = self.filearray[lineN]
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
            newObject.color = u.lightgrey_color
            newObject.alarm_status = 0
            self.objectList[column].append(newObject)
            if column != 0:
              for indices in range(0,column): # for parent objects grab their index (assuming my parent was the most recently added one to the object list)
                self.objectList[column][colRow[column]-1].parentIndices.append(0)
                self.objectList[column][colRow[column]-1].parentIndices[indices] = self.objectList[indices][len(self.objectList[indices])-1].columnIndex
            # FIXME try to find a way to catalogue the following children in a level 2 object
              if (column==4 and isnew==1):
                self.objectList[2][self.objectList[column][colRow[2]-1].parentIndices[2]].add_parameter(self.objectList[3][colRow[3]-1].value,self.objectList[4][colRow[4]-1].value)
                self.objectList[2][self.objectList[column][colRow[2]-1].parentIndices[2]].add_parameter_history(self.objectList[3][colRow[3]-1].value,self.objectList[4][colRow[4]-1].value)
                #self.objectList[2][colRow[2]-1].add_parameter(self.objectList[3][colRow[3]-1].value,self.objectList[4][colRow[4]-1].value)
              if (column==4 and isnew!=1):
                self.objectList[2][self.objectList[column][colRow[2]-1].parentIndices[2]].add_parameter_history(self.objectList[3][colRow[3]-1].value,self.objectList[4][colRow[4]-1].value)
            #for colN in range(column+1,len(line)): # Tell the sub-types not to care if they are repeat values
            #  line_previous[colN]="NULL"
          else:
            self.objectList[column][colRow[column]-1].indexEnd=lineN
          line_previous[column]=line[column]
      #return self.objectList


#for i
#  bool isnew = false 
#  for j
#    if(line[i][j] != line[i-1][j])
#      isnew = true
#    if (isnew == true)
#      do stuff
#  isnew = false
#  } 
#}

    def get_alarm_handler_style(self):
        style = ttk.Style()
        style.theme_create("alarm_handler", parent="alt", settings={
            "TNotebook": {"configure": {"background": u.lightgrey_color}},
            "TNotebook.Tab": {"configure": {"background": u.lightgrey_color}}})
        style.theme_use("alarm_handler")

    def quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    def educate_yourself(self, event):
      webbrowser.open_new(r"https://en.wikipedia.org/wiki/Green_Monster")

#    def alarm_handler_tab(self, expt_tab):
#        tab_control = ttk.Notebook(expt_tab)
#        tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER)]
#        for title, fn in tab_titles:
#            sub_tab = ttk.Frame(tab_control, width=800, height=600, style="My.TFrame")
#            tab_control.add(sub_tab, text=title)
#            fn(sub_tab)
#        tab_control.grid(row=0, column=0, columnspan=2)
#
#    def alarm_history_tab(self, expt_tab):
#        tab_control = ttk.Notebook(expt_tab)
#        tab_titles = [('Alarm History', alarm_history.ALARM_HISTORY)]
#        for title, fn in tab_titles:
#            sub_tab = ttk.Frame(tab_control, width=800, height=600, style="My.TFrame")
#            tab_control.add(sub_tab, text=title)
#            fn(sub_tab)
#        tab_control.grid(row=0, column=0, columnspan=2)

    def create_widgets(self):
        gui_style = ttk.Style()
        gui_style.configure('My.TButton', foreground=u.lightgrey_color)
        gui_style.configure('My.TFrame', background=u.lightgrey_color)

        tab_control = ttk.Notebook(self.win)
        #tab_titles = [('Alarm Handler', self.alarm_handler_tab),('Alarm History', self.alarm_history_tab)]
        tab_titles = [('Alarm Handler', alarm_handler.ALARM_HANDLER),('Alarm History', alarm_history.ALARM_HISTORY)]
        for title, fn in tab_titles:
            tab = ttk.Frame(tab_control, width=800, height=600, style="My.TFrame")
            tab_control.add(tab, text=title)
            fn(tab,self.objectList)
        tab_control.grid(row=0, column=0, columnspan=2)
        fenway = tk.PhotoImage(file='gm.ppm')
        fenway_pahk = tk.Label(self.win, image=fenway, cursor="hand2", bg=u.lightgrey_color)
        fenway_pahk.image = fenway
        fenway_pahk.grid(row=1, column=0, padx=5, pady=10, sticky='SW')
        fenway_pahk.bind("<Button-1>", self.educate_yourself)
        tk.Button(self.win, text='QUIT', command=quit, background=u.lightgrey_color, width=20, height=4).grid(
            row=1, column=1, padx=15, pady=5, sticky='SE')

alarm_handler_GUI = AlarmHandler()
alarm_handler_GUI.win.mainloop()
