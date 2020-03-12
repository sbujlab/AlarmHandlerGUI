#!/bin/tcsh
echo "\nThe most recent run in progress is"
set runNum=`~/scripts/getRunNumber`
echo "Run number:    $runNum"
echo "Slug number:   `rcnd $runNum slug`"
echo "Run condition: `rcnd $runNum run_type`"
echo "Target type:   `rcnd $runNum target_type`"
echo "User comment:  `rcnd $runNum user_comment`"
