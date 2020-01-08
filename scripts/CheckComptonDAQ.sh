#!/bin/bash
# Aq value from logfile: result=`tail -1000 /adaqfs/home/apar/PREX/japan_feedback/feedbacklog | grep -w "Hall A Aq" | tail -1`
#vim /adaqfs/home/apar/PREX/japan_feedback/feedbacklog -c ":q!" 
export TCL_LIBRARY="/adaqfs/coda/2.6.2/common/lib/tcl7.4"
python3 /adaqfs/home/apar/alarms/AlarmHandlerGUI/scripts/CheckComptonDAQ.py $@
