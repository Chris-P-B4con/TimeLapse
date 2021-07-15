#!/bin/sh
echo "Uploading $1 to OneDrive..."
rclone copy -v /home/pi/TimeLapse/$1 onedrive:Test/Pictures 

echo "Done."

rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
