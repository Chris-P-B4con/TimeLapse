#!/bin/sh

date = 'date +"%Y-%m-%d %H:%M:%S"'
echo "$(date): Uploading files to OneDrive..."
rclone copy -v /home/pi/TimeLapse/Pictures onedrive:Test/Pictures  --log-file=log.txt 
echo "Done."

echo "Updating local config files..."
rclone copy onedrive:Test/config.txt /home/pi/TimeLapse/
echo "Done"

rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
rclone copy /home/pi/TimeLapse/error.txt onedrive:Test
