#!/bin/bash
#result=`ssh compton@compton -X -tt "echo '~/scripts/printRunStatus EB6'|$SHELL -l"`
#if [[ $result == *"active"* ]]; then
#  echo -en '\e[1;34m'"Compton DAQ is active\n"'\e[0m'
#else
#  echo -en '\e[1;31m'"Compton DAQ is off, restart!\n"'\e[0m'
#fi
python3 ~/alarms/CheckComptonPositions.py $@
