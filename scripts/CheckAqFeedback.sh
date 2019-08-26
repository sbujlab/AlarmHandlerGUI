#!/bin/bash
# Aq value from logfile: result=`tail -1000 /adaqfs/home/apar/PREX/japan_feedback/feedbacklog | grep -w "Hall A Aq" | tail -1`
python3 ~/alarms/CheckAqFeedback.py $@
