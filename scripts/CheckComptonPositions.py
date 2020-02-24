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

readback_epics = ["IPM1P02A.XPOS","IPM1P02A.YPOS","IPM1P02B.XPOS","IPM1P02B.YPOS"]
readback_points = [-0.3,0.5,0.0,0.5]
readback_tolerances = [0.100,0.10,0.15,0.10]
#readback_points = [-0.25,0.55,0.0,0.48]
#readback_tolerances = [0.075,0.075,0.10,0.05]

AllGood = True
i = 0


while i < len(readback_epics):

  cmds = ['caget', '-t', '-w 1', 'COMPTON_PW1PCAV_ca']
  comptonPower = "NULL"
  comptonPower = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
  cmds = ['caget', '-t', '-w 1', 'IBC1H04CRCUR2']
  beamCurrent = "NULL"
  beamCurrent = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 

  if float(beamCurrent)<50.0 or float(comptonPower)<1000.0:
    if i == len(readback_epics):
      print("OK")
    i = i+1
    continue

  cmds = ['caget', '-t', '-w 1', str(readback_epics[i])]
  cond_out = "NULL"
  cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
  if "Invalid" in cond_out:
    print("Error, {} not found".format(readback_epics[i]))
    continue
  if abs(readback_points[i]-float(cond_out)) > readback_tolerances[i]:
    print("ERROR: Channel {} = {}mm\n- This is more than {}mm away\n- It is {}mm away".format(readback_epics[i],cond_out,readback_tolerances[i], (float(cond_out)-readback_points[i])))
    AllGood = False
  i = i+1

if AllGood is False:
  print("Please check the Compton Lock")
else:
  print("OK")
