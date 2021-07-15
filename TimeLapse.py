from lib.camera_obj import TimeLapseCam
import RPi.GPIO as GPIO
from lib import utils

from time import sleep
from datetime import datetime, date

# GPIO PIN MAPPING
BUTTON_PREVIEW = 16
BUTTON_SYNC = 8
LED_INET = 23

def setup():
   
    print("Reading in Config and setting up camera...")
    interval, shooting_days, start_time, stop_time = utils.read_config()
    camera = TimeLapseCam(LED_INET, (3280,2464), interval, shooting_days, start_time, stop_time)
    print("Done.")


    # Configure RPi GPIOs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PREVIEW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_INET, GPIO.OUT)
    GPIO.setup(BUTTON_SYNC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_SYNC, GPIO.FALLING, callback = utils.sync_script, bouncetime=100)
    GPIO.add_event_detect(BUTTON_PREVIEW, GPIO.FALLING, callback = camera.take_picture, bouncetime=100)

    #Ensure internet connection
    print("Checking for internet connection...")
    while not utils.connect():
        camera.blink_LED(0.2, 1, LED_INET)
    print("Done.")

    #Runtime config
    cur_weekday = date.today().weekday()
    cur_time = datetime.now().time()

    return camera, cur_weekday, cur_time

if __name__ == "__main__":
    
    print("==========================")
    print("Starting run at {}".format(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")))
    camera, cur_weekday, cur_time = setup()
    synced = False

    # Start main loop
    while True:
        if str(cur_weekday) in camera.shooting_days and utils.time_in_range(camera.start_time, camera.stop_time, cur_time):
	    synced = False
            lost_time = camera.take_picture()
            camera.blink_LED(1, int(camera.interval-lost_time/2))
            GPIO.output(camera.LED, GPIO.LOW)
            print("Failed to take intervall picture.")

        # Weekly Upload and deleting of files on Sunday
        elif cur_weekday not in camera.shooting_days:
	    print("Going to sleep for the day.")
            camera.sync("weekly")
            sleep(24*60*60) #24 Hours (should wake up at 5am)

        else:
            if not synced:
                synced = True
                camera.sync("daily")
                print("Updating shooting parameters.")
                interval, shooting_days, start_time, stop_time = utils.read_config()
                print("Going into sleep for 10 hours.")
                GPIO.output(LED_INET, GPIO.LOW)
                sleep(60*60*10)
            else:
                print("Not time to wake yet. Sleeping for 10 more minutes.")
                sleep(600)

        # Update weekday and current time
        cur_weekday, cur_time = date.today().weekday(), datetime.now().time()
