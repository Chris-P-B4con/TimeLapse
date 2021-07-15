#!/bin/sh

date = 'date +"%Y-%m-%d %H:%M:%S"'
echo "$(date): Uploading files to OneDrive..."
rclone copy -v /home/pi/TimeLapse/Pictures onedrive:TimeLapse/Pictures  --log-file=log.txt 
echo "Done."

echo "Updating local config files..."
rclone copy onedrive:TimeLapse/config.txt /home/pi/TimeLapse/
echo "Done"

rclone copy /home/pi/TimeLapse/log.txt onedrive:TimeLapse
rclone copy /home/pi/TimeLapse/error.txt onedrive:TimeLapse