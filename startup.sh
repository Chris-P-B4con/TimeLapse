#! /bin/sh
if [ -z "$STY" ]; then exec screen -dm -S TimeLapse /bin/bash "$0"; fi
python /home/pi/TimeLapse/TimeLapse.py >> /home/pi/TimeLapse/log.txt

