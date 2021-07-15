#!/bin/sh
echo "Uploading $1 to OneDrive..." >> log.txt
rclone copy -v /home/pi/TimeLapse/$1 onedrive:Test/Pictures 

echo "Done." >> log.txt

rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
