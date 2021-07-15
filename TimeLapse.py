import RPi.GPIO as GPIO
import os
import urllib
import subprocess
import sys
import time as tim
import logging

from picamera import PiCamera
from time import sleep, strftime
from pathlib import Path
from datetime import time, datetime, date

def time_in_range(start, end, current):
    return start<= current <= end

def read_config():
    f = open("config.txt", "r")
    for line in f:
        if "interval" in line:
            temp = line.split("=")
            interval = int(temp[-1])
        elif "shooting_days" in line:
            temp = line.split("=")
            shooting_days = temp[-1].split(",")
            shooting_days[-1] = shooting_days[-1].rstrip("\n")
        elif "start_time" in line:
            temp = line.split("=")
            start_time = temp[-1].split(":")
            start_time[-1] = start_time[-1].rstrip("\n")
        elif "stop_time" in line:
            temp = line.split("=")
            stop_time = temp[-1].split(":")
            stop_time[-1] = stop_time[-1].rstrip("\n")
        else:
            continue
    f.close()
    return (interval, shooting_days, start_time, stop_time)

def connect(host="http://google.com"):
    try:
        urllib.urlopen(host)
        return True
    except:
        return False

def sync_script(channel):
    try:
        subprocess.call(['sh', 'sync_scripst/sync_weekly.sh', '>>', 'log.txt'])
    except Exception as e:
	    print("Couldnt upload files.")

def sync_daily():
    try:
	    subprocess.call(['sh','sync_scripst/sync_daily.sh', '>>','log.txt'])
    except:	
	    print("Something went wrong during daily upload.")

def sync_single(file_name):
    try:
    	subprocess.call(['sh', 'sync_scripst/sync_single.sh', str(file_name)])
    except:
	    print("Failed to upload single file.")


def blink_LED(freq, count, LED):
    for i in range(count):
        GPIO.output(LED, GPIO.HIGH)
        sleep(freq)
        GPIO.output(LED, GPIO.LOW)
        sleep(freq)


def quick_pic(channel):
    cur_time = datetime.now()
    GPIO.output(LED_INET, GPIO.HIGH)
    camera.start_preview()
    sleep(2)
    camera.capture("Pictures/Manual_{}.jpg".format(cur_time.strftime("%d-%b-%Y-(%H-%M-%S)")))
    print("Took manual picture at {}".format(cur_time.strftime("%d-%b-%Y-(%H-%M-%S)")))
    GPIO.output(LED_INET, GPIO.LOW)
    camera.stop_preview()

if __name__ == "__main__":
    
    # Create logging instance
    logger = logging.getLogger("TimeLapse")
    fh = logging.FileHandler("errors.txt")
    formatter = logging.Formatter('%(asctime)s = %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Configure RPi GPIOs
    GPIO.setmode(GPIO.BCM)
    BUTTON_PREVIEW = 16
    BUTTON_SYNC = 8
    LED_INET = 23
    GPIO.setup(BUTTON_PREVIEW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_INET, GPIO.OUT)
    GPIO.setup(BUTTON_SYNC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_SYNC, GPIO.FALLING, callback = sync_script, bouncetime=100)
    GPIO.add_event_detect(BUTTON_PREVIEW, GPIO.FALLING, callback = quick_pic, bouncetime=100)

    # Read in config and adjust settings
    interval = 0
    start_time = []
    stop_time = []
    shooting_days = []
    interval, shooting_days, start_time, stop_time = read_config()
    print("==========================")
    print("Starting run at {}".format(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")))

    #Setup camera
    camera = PiCamera()
    camera.resolution = (3280,2464)

    #Ensure internet connection
    print("Checking for internet connection...")
    while not connect():
        blink_LED(0.2, 1, LED_INET)
    print("Done.")

    # Setup Camera preview to adjust focus
    print("Setting up camera...")
    camera.start_preview()
    sleep(2)
    camera.stop_preview()
    print("Done.")

    #Runtime config
    print("Configuring runtime variables...")
    count = 0
    shooting_days = [0,1,2,3,4,5] if len(shooting_days) == 0 else [int(k) for k in shooting_days]
    cur_weekday = date.today().weekday()
    cur_time = datetime.now().time()
    start_time = time(7,0,0) if len(start_time) == 0 else \
        time(int(start_time[0]), int(start_time[1]), int(start_time[2]))
    stop_time = time(20,0,0) if len(stop_time) == 0 else \
        time(int(stop_time[0]), int(stop_time[1]), int(stop_time[2]))
    synced = False
    print("Done.")

    # Ensure folder for Pictures exists and is empty
    print("Creating save space...")
    if not os.path.exists("Pictures"):
        Path("Pictures").mkdir(parents=True)
    print("Done.")

    # Start main loop
    while True:
        if cur_weekday in shooting_days and time_in_range(start_time, stop_time, cur_time):
            cur_time_str = datetime.now().strftime("%d-%b-%Y-(%H-%M-%S)")
            start = tim.time()
            synced = False
            GPIO.output(LED_INET, GPIO.HIGH)
            camera.start_preview()
            sleep(2)
            camera.capture("Pictures/{}.jpg".format(cur_time_str))
            camera.stop_preview()
            print("Picture taken at {}".format(cur_time_str))
            sync_single("Pictures/{}.jpg".format(cur_time_str))
            lost_time = tim.time() - start 
            blink_LED(1, int(interval-lost_time/2), LED_INET)
            GPIO.output(LED_INET, GPIO.LOW)

        # Weekly Upload and deleting of files on Sunday
        elif cur_weekday == 6:
            try:
                print("Sleeping for the day")
                sync_script("Filler")
            except Exception as e:
                logger.exception(e)
                print("Something went wrong with the Upload. Couldnt free data")
            sleep(24*60*60) #24 Hours (should wake up at 5am)


        else:
            if not synced:
                synced = True
                sync_daily()
                print("Updating shooting parameters.")
                interval, shooting_days, start_time, stop_time = read_config()
                print("Going into sleep for 10 hours.")
                GPIO.output(LED_INET, GPIO.LOW)
                sleep(60*60*10)
            else:
                print("Not time to wake yet. Sleeping for 10 more minutes.")
                sleep(600)

        # Update weekday and current time
        cur_weekday, cur_time = date.today().weekday(), datetime.now().time()

