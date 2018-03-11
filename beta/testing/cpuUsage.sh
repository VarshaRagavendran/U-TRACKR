#!/bin/bash

# Get number of cores from proc cpuinfo
CORECOUNT=`grep -c ^processor /proc/cpuinfo`
# Use top, skip the first 7 rows, count the sum of the values in column 9 - the CPU column, do some simple rounding at the end. 
CPUUSAGE=`top -bn 1 | awk 'NR>7{s+=$9} END {print s/'$CORECOUNT'}' | awk '{print int($1+0.5)}'`
printf "$CPUUSAGE\n"