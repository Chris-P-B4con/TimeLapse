import RPi.GPIO as GPIO

from lib import utils
from lib.camera_obj import TimeLapseCam
from time import sleep
from datetime import datetime, date

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
    GPIO.add_event_detect(BUTTON_SYNC, GPIO.FALLING, callback = utils.sync_script, bouncetime=100)
    GPIO.add_event_detect(BUTTON_PREVIEW, GPIO.FALLING, callback = camera.take_picture, bouncetime=100)

    #Ensure internet connection
    utils.write_to_log("Checking for internet connection...")
    while not utils.connect():
        utils.blink_LED(0.2, 1, LED_INET)
    utils.write_to_log("Done.")

    #Runtime config
    cur_weekday = date.today().weekday()
    cur_time = datetime.now().time()

    return camera, cur_weekday, cur_time

if __name__ == "__main__":
    
    utils.write_to_log("======================================", False)
    utils.write_to_log("Starting run at {}".format(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")))
    camera, cur_weekday, cur_time = setup()
    synced = True

    # Start main loop
    while True:
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
            sleep(24*60*60) #24 Hours (should wake up at 5am)

        else:
            if cur_time > camera.stop_time:
                synced = True
                utils.write_to_log("Updating time lapse parameters and going to sleep for {} hours.".format(camera.sleep_time))
                camera.sync("daily")
                params = utils.read_config()
                camera.update_config(params)
                GPIO.output(LED_INET, GPIO.LOW)
                sleep(camera.sleep_time)
            else:
                utils.write_to_log("Not time to wake yet. Sleeping for 10 more minutes.")
                utils.blink_LED(2, int(camera.sleep_time/120), camera.LED)

        # Update weekday and current time
        cur_weekday, cur_time = date.today().weekday(), datetime.now().time()
