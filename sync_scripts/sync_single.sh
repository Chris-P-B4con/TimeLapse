#!/bin/sh

date '+%d-%b-%Y %H:%M:%S: Uploading...' >> log.txt
rclone copy /home/pi/TimeLapse/$1 $2/$3 &

rclone copy /home/pi/TimeLapse/log.txt $2
rclone copy /home/pi/TimeLapse/error.txt $2
