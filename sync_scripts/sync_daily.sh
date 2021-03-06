#!/bin/sh

date '+%d-%b-%Y %H:%M:%S: Uploading files to OneDrive...' >> log.txt
rclone copy -v /home/pi/TimeLapse/Pictures $1/Pictures  --log-file=log.txt

date '+%d-%b-%Y %H:%M:%S: Updating local config files...' >> log.txt
rclone copy $1/config.txt /home/pi/TimeLapse/
date '+%d-%b-%Y %H:%M:%S: Done' >> log.txt

rclone copy /home/pi/TimeLapse/log.txt $1
rclone copy /home/pi/TimeLapse/error.txt $1
