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

Vacuum_readback_epics = ["VCG1C20ATr","VCG1H00ATr","VCG1H04BTr","VCG1H04CTr","VCG1P02Tr","VIP1H00A","VIP1H00B"]
Vacuum_readback_highs = [5.0e-5,5.0e-5,5.0e-5,5.0e-5,1.0e-6,5.0e-5,5.0e-5]
Vacuum_readback_lows = [1.0e-9,1e-9,1.0e-9,1.0e-9,1.0e-10,1.0e-9,1.0e-9]

AllGood = True
i = 0
while i < len(Vacuum_readback_epics):
  cmds = ['caget', '-t', '-w 1', str(Vacuum_readback_epics[i])]
  cond_out = "NULL"
  cond_out = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') # Needs to be decoded... be careful 
  if "Invalid" in cond_out:
    print("Error, {} not found".format(Vacuum_readback_epics[i]))
    continue
  if Vacuum_readback_lows[i] > float(cond_out) or Vacuum_readback_highs[i] < float(cond_out):
    print("ERROR: Vacuum readback point \n{} = {}\n  Should be < {} and > {}".format(Vacuum_readback_epics[i],cond_out,Vacuum_readback_highs[i],Vacuum_readback_lows[i]))
    AllGood = False
  i = i+1

if AllGood is False:
  print("Please check the vacuum")
else:
  print("OK")
