#!/bin/sh

date '+%d-%b-%Y %H:%M:%S: Checking free storage...' >> log.txt
df -h | grep /dev/root

success = 1
date '+%d-%b-%Y %H:%M:%S: Uploading files to OneDrive...' >> log.txt

rclone copy -v /home/pi/TimeLapse/Manual $1/Manual --log-file=log.txt
rclone copy -v /home/pi/TimeLapse/Pictures/ $1/Pictures  --log-file=log.txt 
if [$? -eq 0] || [$? -eq 9]
then
	date '+%d-%b-%Y %H:%M:%S: Deleting local pictures...' >> log.txt
	rm Pictures/*.jpg
	date '+%d-%b-%Y %H:%M:%S: Done.' >> log.txt
else 
	date '+%d-%b-%Y %H:%M:%S: Upload failed...' >> log.txt
fi
rclone copy /home/pi/TimeLapse/log.txt $1
rclone copy /home/pi/TimeLapse/error.txt $1
