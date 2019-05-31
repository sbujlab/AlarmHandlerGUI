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
import utils as u

class ALARM_HISTORY(tk.Frame):
  def __init__(self, tab, OL, fileArray):

    i = 0
