#!/bin/sh

date '+%d-%b-%Y %H:%M:%S: Uploading $1 to OneDrive...' >> log.txt
rclone copy -v /home/pi/TimeLapse/$1 onedrive:Test/Pictures 

date '+%d-%b-%Y %H:%M:%S: Done.' >> log.txt

rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
