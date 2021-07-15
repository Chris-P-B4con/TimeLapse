#!/bin/sh
echo "Uploading $1 to OneDrive..."
rclone copy -v /home/pi/TimeLapse/$1 onedrive:TimeLapse/Pictures 

echo "Done."

rclone copy /home/pi/TimeLapse/log.txt onedrive:TimeLapse
