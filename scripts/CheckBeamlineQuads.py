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

Magnet_set_epics = ["MQK1H01.BDL","MQO1H02.BDL","MQM1H02.BDL","MQO1H03.BDL","MQO1H03A.BDL","MQA1H04.BDL"]
Magnet_set_points = [-11520.5,7563.26,-7286.23,7601.64,7657.7,-6100.9]
Magnet_set_points_tolerances = [1.0,1.0,1.0,1.0,1.0,1.0]
Magnet_readback_epics = ["MQK1H01M","MQO1H02M","MQM1H02M","MQO1H03M","MQO1H03AM","MQA1H04M"]
Magnet_readback_points = [-1.32967,46.5788,-42.5495,42.7773,41.5018,-0.750732]
Magnet_readback_tolerances = [15.0,15.0,15.0,15.0,15.0,15.0]

AllGood = True
i = 0
cmds = ['caget', '-t', '-w 1', 'IBC1H04CRCUR2']
cond_out = "NULL"
cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
if "Invalid" in cond_out:
  print("ERROR: BCM readback invalid")
elif float(cond_out) > 10.0: 
  while i < len(Magnet_set_epics):
    #cmds = ['caget', '-t', '-w 1', 'IGL0I00C1068_DAC06']
    cmds = ['caget', '-t', '-w 1', str(Magnet_set_epics[i])]
    cond_out = "NULL"
    cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
    if "Invalid" in cond_out:
      print("Error, {} not found".format(Magnet_set_epics[i]))
      continue
    if abs(Magnet_set_points[i] - float(cond_out)) > Magnet_set_points_tolerances[i]:
      #print("ERROR: Magnet set point {} = {} -> Not equal to correct value of {} +- {}".format(Magnet_set_epics[i],cond_out,Magnet_set_points[i],Magnet_set_points_tolerances[i]))
      AllGood = False

 
    cmds = ['caget', '-t', '-w 1', str(Magnet_readback_epics[i])]
    cond_out = "NULL"
    cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
    if "Invalid" in cond_out:
      print("Error, {} not found".format(Magnet_readback_epics[i]))
      AllGood = False
      continue
    if 100.0*abs(Magnet_readback_points[i]-float(cond_out))/(Magnet_readback_points[i]) > Magnet_readback_tolerances[i]:
      #print("ERROR: Magnet readback point \n{} = {}\n  This is more than {} % away\n  Correct value is {}\n  It is {} % away".format(Magnet_readback_epics[i],cond_out,Magnet_readback_tolerances[i],Magnet_readback_points[i], 100*(Magnet_readback_points[i]-float(cond_out))/Magnet_readback_points[i]))
      AllGood = False
    i = i+1

if AllGood is False:
  print("Please check the Beamline Quad magnet set \npoints and readbacks.")
else:
  print("OK")
