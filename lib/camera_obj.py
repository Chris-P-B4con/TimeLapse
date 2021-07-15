import datetime
import time as t
import subprocess
import os
import logging

from picamera import PiCamera
from pathlib import Path
from lib.utils import read_config
from lib.utils import write_to_log

class TimeLapseCam():

    def __init__(self, LED, resolution, interval, shooting_days, start_time, stop_time, path = "Pictures", logg=True):

        self.resolution = resolution
        self.shooting_days = shooting_days
        self.start_time = datetime.time(int(start_time[0]), int(start_time[1]), int(start_time[2]))
        self.stop_time = datetime.time(int(stop_time[0]), int(stop_time[1]), int(stop_time[2]))
        self.interval = interval
        self.LED = LED
        self.save_path = path
        
        # Ensure folder for Pictures exists and is empty
        write_to_log("Creating save space...")
        if not os.path.exists(path):
            Path(path).mkdir(parents=True)
        write_to_log("Done.")

        # Create logging instance
        if logg == True:
            self.logger = logging.getLogger("TimeLapse")
            fh = logging.FileHandler("errors.txt")
            formatter = logging.Formatter('%(asctime)s = %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)   

    def take_picture(self, channel=''):
        start = t.time()
        with PiCamera() as camera:
            camera.resolution = self.resolution
            cur_time_str = datetime.datetime.now().strftime("%d-%b-%Y-(%H-%M-%S)")
            camera.start_preview()
            t.sleep(2)
            camera.capture("Pictures/{}.jpg".format(cur_time_str)) \
                if channel == '' else camera.capture("Pictures/Manual_{}.jpg".format(cur_time_str))
            camera.stop_preview()
            write_to_log("Picture taken at {}".format(cur_time_str))
            self.sync("single",self.save_path + "/" + cur_time_str + ".jpg")
            lost_time = t.time() - start 
            return lost_time
        
    
    def sync(self, subscript, file_name = ""):
        if subscript == "single" and file_name != "":
            try:
               subprocess.call(['sh', 'sync_scripts/sync_single.sh', str(file_name)])
            except Exception as e:
                self.logger.exception(e)
                write_to_log("Something went wrong during single upload.")

        elif subscript == "daily":
            try:
                subprocess.call(['sh','sync_scripts/sync_daily.sh', '>>','log.txt'])
                self.update_config(read_config())
            except Exception as e:
                self.logger.exception(e)
                write_to_log("Something went wrong during daily upload.")
                
        elif subscript == "weekly":
            try:
                subprocess.call(['sh', 'sync_scripts/sync_weekly.sh', '>>', 'log.txt'])
            except Exception as e:
                self.logger.exception(e)
                write_to_log("Something went wrong during weekly upload.")

        else:
            write_to_log("Subscript not found. No uploading")

    def update_config(self, interval="", shooting_days="", start_time="",  stop_time=""):
        if interval != "":
            self.interval = interval
        if start_time != "":
            self.start_time = start_time
        if stop_time != "":
            self.stop_time = stop_time
        if shooting_days != "":
            self.shooting_days = shooting_days
            
    
    

