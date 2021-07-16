#!/bin/sh

date '+%d-%b-%Y %H:%M:%S: Uploading...' >> log.txt
rclone copy -v /home/pi/TimeLapse/$1 $2/Pictures 

date '+%d-%b-%Y %H:%M:%S: Done.' >> log.txt

rclone copy /home/pi/TimeLapse/log.txt $2
