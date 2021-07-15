#!/bin/sh

date = 'date +"%Y-%m-%d %H:%M:%S"'
echo "$(date): Checking free storage..."
df -h | grep /dev/root

date = 'date +"%Y-%m-%d %H:%M:%S"'
echo "$(date): Uploading files to OneDrive..."
{
	{
		rclone copy -v /home/pi/TimeLapse/Pictures onedrive:TimeLapse/Pictures  --log-file=log.txt 
		date = 'date +"%Y-%m-%d %H:%M:%S"'
	} && {
		echo "$(date): Deleting local pictures..."
		rm Pictures/*.jpg
		date = 'date +"%Y-%m-%d %H:%M:%S"'
		echo "$(date): Done."
		rclone copy /home/pi/TimeLapse/log.txt onedrive:TimeLapse
		rclone copy /home/pi/TimeLapse/error.txt onedrive:TimeLapse
	}
} || {
	date = 'date +"%Y-%m-%d %H:%M:%S"'
	echo "$(date): Upload failed..."

	rclone copy /home/pi/TimeLapse/log.txt onedrive:TimeLapse
	rclone copy /home/pi/TimeLapse/error.txt onedrive:TimeLapse
}
