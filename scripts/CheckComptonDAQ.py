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
  cmds = ['caget', '-t', '-w 1', 'IBC1H04CRCUR2']
  cond_out = "NULL"
  cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
  if "Invalid" in str(cond_out):
    print("Current-Readback-Invalid")
  elif Decimal(cond_out) > 35.0:
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
    print("Current-Below-35uA")

else: 
  #cmds = ['caget', '-t', '-w 1', 'IGL0I00C1068_DAC06']
  cmds = ['caget', '-t', '-w 1', 'ComptonDSbg1']
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
