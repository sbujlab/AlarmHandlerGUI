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

cmdsA = ['caget', '-t', '-w 1', 'IBC1H04CRCUR2']
cond_outA = "NULL"
cond_outA = subprocess.Popen(cmdsA, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
cmdsC = ['caget', '-t', '-w 1', 'IBC3H00CRCUR4']
cond_outC = "NULL"
cond_outC = subprocess.Popen(cmdsC, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
if "Invalid" in str(cond_outA) or "Invalid" in str(cond_outC):
  print("Current-Readback-Invalid")
elif Decimal(cond_outA) > 50.0 or Decimal(cond_outC)>3.0:
  #print("{}".format(cond_out))
  cmds = ['sh','/adaqfs/home/apar/scripts/printRunStatus','EB1']
  cond_out = "NULL"
  cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
  if "active" in str(cond_out): # The DAQ should be on
    #print("{}".format(cond_out))
    print("OK")
  else:
    print("Start-the-Parity-DAQ!")
else:
  print("OK") # We don't have enough current to do feedback

