#!/bin/tcsh
echo "\nThe most recent run in progress is"
set runNum=`~/scripts/getRunNumber`
echo "Run: $runNum  -  Slug: `rcnd $runNum slug`"
echo "Condition: `rcnd $runNum run_type`  -  Target: `rcnd $runNum target_type`"
echo "User comment: `rcnd $runNum user_comment`"
