#!/bin/sh

echo "\n" >> log.txt
echo "++++++++++++++++++++ END OF DAY ++++++++++++++++++++" >> log.txt
date '+%d-%b-%Y %H:%M:%S: Uploading files to OneDrive...' >> log.txt
rclone copy -v /home/pi/TimeLapse/Manual $1/Manual --log-file=log.txt
rclone copy -v /home/pi/TimeLapse/Pictures $1/Pictures  --log-file=log.txt
suc=$?

if [ "$suc" -eq 0 ] || [ "$suc" -eq 9 ]; then
    date '+%d-%b-%Y %H:%M:%S: Done.' >> log.txt
else
    date '+%d-%b-%Y %H:%M:%S: Something went wrong during upload.' >> log.txt
fi

date '+%d-%b-%Y %H:%M:%S: Updating local config files...' >> log.txt
rclone copy $1/config.txt /home/pi/TimeLapse/
if [ $? -eq 0] || [ $? -eq 9 ]; then
    date '+%d-%b-%Y %H:%M:%S: Done' >> log.txt
else 
    date '+%d-%b-%Y %H:%M:%S: Failed to update config.' >> log.txt
fi
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++" >> log.txt
echo "\n" >> log.txt

rclone copy /home/pi/TimeLapse/log.txt $1
rclone copy /home/pi/TimeLapse/error.txt $1
