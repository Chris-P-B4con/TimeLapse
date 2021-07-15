#!/bin/sh

date = 'date + "%d-%b-%Y %H:%M:%S"'
echo "$(date): Uploading $1 to OneDrive..." >> log.txt
rclone copy -v /home/pi/TimeLapse/$1 onedrive:Test/Pictures 

date = 'date + "%d-%b-%Y %H:%M:%S"'
echo "$(date): Done." >> log.txt

rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
