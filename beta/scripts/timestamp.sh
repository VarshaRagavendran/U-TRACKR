#!/bin/bash

# prints the date every second
while sleep 1; do echo "$(date '+%Y-%m-%d %H:%M:%S')"; done

# prints the date every 200ms, but isn't guaranteed to start at 000 ms
# while sleep 0.2; do echo "$(date '+%Y-%m-%d %H:%M:%S.%N')"; done

# This is not always guaranteed to print out every 200ms, since $(date +%3N) doesn't return fast enough to print out all numbers from 0-999
# An idea was to run a counter from 0-999 that runs every 1 millisecond, and returns the date if divisible by 200ms

# while true
# do
# 	milliSeconds=$(date +%3N)
# 	echo "$milliSeconds"
# 	if [ $milliSeconds -eq "200" ] || [ $milliSeconds -eq "400" ] || [ $milliSeconds -eq "600" ] || [ $milliSeconds -eq "800" ] || [ $milliSeconds -eq "000" ]
# 	then
# 		echo "it works $milliSeconds"
# 	fi
# done
