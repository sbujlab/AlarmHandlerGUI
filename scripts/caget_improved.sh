#!/bin/bash

epics_text_file="/adaqfs/home/apar/alarms/epics_text/tmp_out_${1}.txt"
#epics_text_file="./tmp_out_${1}.txt"
if [ ! -e $epics_text_file ]; 
then
  echo "${1} --- Invalid channel name" >> $epics_text_file &
  sleep 0.1
fi
caget -t $1 >> $epics_text_file &
sleep 0.1
cat $epics_text_file | tail -1
rm -f $epics_text_file
