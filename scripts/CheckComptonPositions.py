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

y_expected = 0.48
y_expected_tolerance = 0.12
readback_epics = ["IPM1P02A.XPOS","IPM1P02A.YPOS","IPM1P02B.XPOS","IPM1P02B.YPOS"]
readback_values = [0.0,0.0,0.0,0.0]
#readback_points = [0.0,0.0,0.0,0.9]
#readback_tolerances = [0.50,0.50,0.50,0.50]
#readback_points = [-0.25,0.55,0.0,0.48]
#readback_tolerances = [0.075,0.075,0.10,0.05]

AllGood = True
i = 0

cmds = ['caget', '-t', '-w 1', 'COMPTON_PW1PCAV_ca']
comptonPower = "NULL"
comptonPower = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
cmds = ['caget', '-t', '-w 1', 'IBC1H04CRCUR2']
beamCurrent = "NULL"
beamCurrent = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 


while i < len(readback_epics):

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
  ##if abs(readback_points[i]-float(cond_out)) > readback_tolerances[i]:
    #print("ERROR: Channel {} = {}mm\n- This is more than {}mm away\n- It is {}mm away".format(readback_epics[i],cond_out,readback_tolerances[i], (float(cond_out)-readback_points[i])))
  ##  AllGood = False
  readback_values[i] = float(cond_out)
  i = i+1

if abs( (readback_values[1] + readback_values[3])/2.0 - y_expected ) > y_expected_tolerance:
 # print("Positions are (2Ay, 2By): (" + str(readback_values[1]) + ", " + str(readback_values[3]) + ")")
  print("Compton Lock bad in Y")
  AllGood = False

if AllGood is False:
  print("Check Compton Lock")
else:
  print("OK")
