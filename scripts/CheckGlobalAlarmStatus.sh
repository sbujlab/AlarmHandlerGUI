#!/bin/bash
#echo "Most recent alarm history entry:"
#echo " = `cat ~/alarms/alarmHistory.csv | tail -1`"
echo ""
status=`cat ~/alarms/alarm.csv | grep "Alarm Status" | grep -v "OK"`
if [[ $status == '' ]]; then echo "All Alarms OK"; else echo "Global Alarm Alarmed"; cat ~/alarms/alarm.csv | grep "Alarm Status" | grep -v "OK"; fi
