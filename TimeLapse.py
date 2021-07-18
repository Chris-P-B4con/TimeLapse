import RPi.GPIO as GPIO
import os, glob

from lib import utils
from lib.camera_obj import TimeLapseCam
from time import sleep
from datetime import datetime, date, time, timedelta

# GPIO PIN MAPPING
BUTTON_PREVIEW = 16
BUTTON_SYNC = 8
LED_INET = 23

def setup():
   
    utils.write_to_log("Reading in Config and setting up camera...")
    params = utils.read_config()
    params["resolution"] = (3280,2464)
    params["LED"] = LED_INET
    camera = TimeLapseCam(params)
    utils.write_to_log("Done.")

    # Configure RPi GPIOs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PREVIEW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_INET, GPIO.OUT)
    GPIO.setup(BUTTON_SYNC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_SYNC, GPIO.FALLING, callback = camera.preview, bouncetime=100)
    GPIO.add_event_detect(BUTTON_PREVIEW, GPIO.FALLING, callback = camera.take_picture, bouncetime=100)

    #Ensure internet connection
    utils.write_to_log("Checking for internet connection...")
    while not utils.connect():
        utils.blink_LED(0.2, 1, LED_INET)
    utils.write_to_log("Done.")

    #Runtime config
    utils.write_to_log("Checking last pictures for timestamp...")
    if os.path.exists(camera.save_path):
        cur_time = datetime.now()
        pictures = glob.glob(os.path.join("Pictures",'*.{}'.format('jpg')))
        pictures = [datetime.strptime(i, "Pictures/%d-%b-%Y-(%H-%M-%S).jpg") for i in pictures]
        pictures = sorted(pictures, key= lambda x: (cur_time-x).total_seconds())
        last_picture = pictures[0]
        if (cur_time-last_picture).total_seconds() < camera.interval:
            utils.write_to_log("Last picture was {}. sleeping for {}".format(last_picture, camera.interval-(cur_time-last_picture).total_seconds()))
            sleep(camera.interval - (cur_time-last_picture).total_seconds())
    cur_time = datetime.now().time()
    cur_weekday = date.today().weekday()
    

    return camera, cur_weekday, cur_time

if __name__ == "__main__":
    
    utils.write_to_log("======================================", False)
    utils.write_to_log("Starting run at {}".format(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")))
    camera, cur_weekday, cur_time = setup()
    synced = True

    # Start main loop
    while True:

        # If current time is one of shooting days and in time intervall
        if str(cur_weekday) in camera.shooting_days and utils.time_in_range(camera.start_time, camera.stop_time, cur_time):
            synced = False
            GPIO.output(camera.LED, GPIO.HIGH)
            lost_time = camera.take_picture()
            utils.blink_LED(1, int((camera.interval-lost_time)/2), camera.LED)
            GPIO.output(camera.LED, GPIO.LOW)

        # Weekly Upload and deleting of files on Sunday
        elif str(cur_weekday) not in camera.shooting_days:
            utils.write_to_log("Going to sleep for the day.")
            camera.sync("weekly")

            # Calculate difference between now and next shooting time for sleep
            now = datetime.now()
            next_shoot = now + timedelta(days=1)
            next_shoot = next_shoot.replace(hour=camera.start_time.hour-1, minute=camera.start_time.minute, second=camera.start_time.second)
            sleep((next_shoot-now).total_seconds()) #24 Hours (should wake up at start_time - 1 Hour)

        # End of Workday or before start of workday
        else:
            # Sync once after the day and sleep longer
            if not synced:
                synced = True
                utils.write_to_log("Updating time lapse parameters and going to sleep for {} hours.".format(camera.sleep_time/60/60))
                camera.sync("daily")
                params = utils.read_config()
                camera.update_config(params)
                GPIO.output(LED_INET, GPIO.LOW)

                # Calculate difference between now and next shooting time for sleep
                now = datetime.now()
                next_shoot = now + timedelta(days=1)
                next_shoot = next_shoot.replace(hour=camera.start_time.hour-1, minute=camera.start_time.minute-10, second=camera.start_time.second)
                sleep((next_shoot - now).total_seconds())
            
            # Reduce sleeping interval to not miss start time
            else:
                utils.write_to_log("Waking up...")
                utils.blink_LED(2, int(15), camera.LED)

        # Update weekday and current time
        cur_weekday, cur_time = date.today().weekday(), datetime.now().time()
