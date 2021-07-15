#!/bin/sh

date '+%d-%b-%Y %H:%M:%S: Uploading files to OneDrive...' >> log.txt
rclone copy -v /home/pi/TimeLapse/Pictures onedrive:Test/Pictures  --log-file=log.txt

date '+%d-%b-%Y %H:%M:%S: Updating local config files...' >> log.txt
rclone copy onedrive:Test/config.txt /home/pi/TimeLapse/
date '+%d-%b-%Y %H:%M:%S: Done' >> log.txt

rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
rclone copy /home/pi/TimeLapse/error.txt onedrive:Test
