#!/bin/sh

date = 'date +"%Y-%m-%d %H:%M:%S"'
echo "$(date): Checking free storage..." >> log.txt
df -h | grep /dev/root

date = 'date +"%Y-%m-%d %H:%M:%S"'
echo "$(date): Uploading files to OneDrive..." >> log.txt
{
	{
		sudo rclone copy -v /home/pi/TimeLapse/Pictures/ onedrive:Test/Pictures  --log-file=log.txt 
		date = 'date +"%Y-%m-%d %H:%M:%S"'
	} && {
		echo "$(date): Deleting local pictures..." >> log.txt
		rm Pictures/*.jpg
		date = 'date +"%Y-%m-%d %H:%M:%S"'
		echo "$(date): Done." >> log.txt
		rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
		rclone copy /home/pi/TimeLapse/error.txt onedrive:Test
	}
} || {
	date = 'date +"%Y-%m-%d %H:%M:%S"'
	echo "$(date): Upload failed..." >> log.txt

	rclone copy /home/pi/TimeLapse/log.txt onedrive:Test
	rclone copy /home/pi/TimeLapse/error.txt onedrive:Test
}
