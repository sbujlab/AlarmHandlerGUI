#Injector PQB,Hall A Aq,Feedback Status,Value,Feedback-Off
#Injector PQB,Hall A Aq,Feedback Status,Alarm Status,Feedback-Off
#Injector PQB,Hall A Aq,Feedback Status,User Silence Status,Alert
#Injector PQB,Hall A Aq,Feedback Status,User Notify Status,Feedback-Off
#Injector PQB,Hall A Aq,Feedback Status,Script Name,CheckAqFeedback.sh
#Injector PQB,Hall A Aq,Feedback Status,Case Argument,IBC1H04CRCUR2
#Injector PQB,Hall A Aq,Feedback Status,Case Value,Beam-Above-35uA
#Injector PQB,Hall A Aq,Feedback Status,Exactly Beam-Above-35uA,Feedback-On
#Injector PQB,Hall A Aq,Feedback Status,Trip Limit,1
#Injector PQB,Hall A Aq,Feedback Status,Trip Counter,0
#Injector PQB,Hall A Aq,Feedback Status,Alarm Type,BASH

import os
import time
import subprocess
import socket
from argparse import ArgumentParser
from datetime import datetime
from decimal import Decimal

parser = ArgumentParser()
parser.add_argument("arg", nargs='?', type=str, help="Input Flag", default="NULL")
args = vars(parser.parse_args())



#Aq="`tail -1000 /adaqfs/home/apar/PREX/japan_feedback/feedbacklog | grep -w \"Hall A Aq\" | tail -1`"
if args['arg'] != "NULL":
  cmds = ['caget', '-t', '-w 1', 'IBC3H00CRCUR4']
  cond_out = "NULL"
  cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
  if "Invalid" in str(cond_out):
    print("Current-Readback-Invalid")
  elif Decimal(cond_out) > 3.0:
    #print("{}".format(cond_out))
    if args['arg'] != "NULL":
      cmds = ['sh','/adaqfs/home/apar/scripts/printRunStatus','EB1']
      cond_out = "NULL"
      cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
      if "active" in str(cond_out):
        #print("{}".format(cond_out))
        print("EB-Active")
      else:
        print("Invalid")
  else:
    print("Current-Below-3uA")

else: 
  #cmds = ['caget', '-t', '-w 1', 'IGL0I00C1068_DAC06']
  cmds = ['caget', '-t', '-w 1', 'BCM3H04_AsymMean']
  cond_out = "NULL"
  cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
  if "Invalid" in str(cond_out):
    print("Readback-Invalid")
  else:
    print("{}".format(cond_out))
  #if os.path.exists("/adaqfs/home/apar/PREX/japan_feedback/feedbacklog") and (time.time() - os.path.getmtime("/adaqfs/home/apar/PREX/japan_feedback/feedbacklog")) < 30:
  #  print("Feedback-On")
  #if os.path.exists("/adaqfs/home/apar/PREX/japan_feedback/feedbacklog") and (time.time() - os.path.getmtime("/adaqfs/home/apar/PREX/japan_feedback/feedbacklog")) > 30:
  #  print("Feedback-Off")
