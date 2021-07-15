#!/bin/sh

date '+%d-%b-%Y %H:%M:%S: Checking free storage...' >> log.txt
df -h | grep /dev/root

date '+%d-%b-%Y %H:%M:%S: Uploading files to OneDrive...' >> log.txt
{
	{
		rclone copy -v /home/pi/TimeLapse/Pictures/ onedrive:Test/Pictures  --log-file=log.txt 
	} && {
		date '+%d-%b-%Y %H:%M:%S: Deleting local pictures...' >> log.txt
		rm Pictures/*.jpg
		date '+%d-%b-%Y %H:%M:%S: Done.' >> log.txt
		rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
		rclone copy /home/pi/TimeLapse/error.txt onedrive:Test
	}
} || {
	date '+%d-%b-%Y %H:%M:%S: Upload failed...' >> log.txt

	rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
	rclone copy /home/pi/TimeLapse/error.txt onedrive:Test
}
