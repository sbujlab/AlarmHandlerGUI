#!/bin/bash
export PATH=`echo $PATH | sed 's/:/\n/g' | grep -v "5.34.36" |grep -v ROOT | awk 'NR==1{printf"%s",$1}; NR>1{printf":%s",$1}'`
export LD_LIBRARY_PATH=`echo $LD_LIBRARY_PATH | sed 's/:/\n/g' | grep -v "5.34.36" | grep -v ROOT | awk 'NR==1{printf"%s",$1}; NR>1{printf":%s",$1}'`

export ROOTSYS=/adaqfs/apps/ROOT/6.14-04
#export ROOTSYS=/adaqfs/apps/ROOT/6.16-00

export PATH="${ROOTSYS}/bin:${PATH}"
export LD_LIBRARY_PATH="${ROOTSYS}/lib:${LD_LIBRARY_PATH}"

export QW_DATA=/adaq1/data1/apar/
#setenv QW_ROOTFILES_OLD=/aonl3/work1/apar_OLD/japanOutput
export QW_ROOTFILES=/chafs2/work1/apar/japanOutput

alias root='root -l'
runNum=999999
if [[ $@ -ge 1 ]]
then
  runNum=$1
fi
commandStr="gROOT->LoadMacro(\"/adaqfs/home/apar/PREX/japan/panguin/macros/SyncCheckManually.C\"); SyncCheckManually($runNum); gSystem->Exit(0);"
result=`echo $commandStr | root -b -l 2> /dev/null`
echo "$result"
