from os import read
import urllib
import subprocess
import RPi.GPIO as GPIO
import time as t
import datetime

def time_in_range(start, end, current):
    return start<= current <= end

def read_config():
    f = open("config.txt", "r")
    params = {}
    for line in f:
        if "interval" in line:
            temp = line.split("=")
            params['interval'] = int(temp[-1])
        elif "shooting_days" in line:
            temp = line.split("=")
            params["shooting_days"] = temp[-1].split(",")
            params["shooting_days"][-1] = params["shooting_days"][-1].rstrip("\n")
        elif "start_time" in line:
            temp = line.split("=")
            params["start_time"] = temp[-1].split(":")
            params["start_time"][-1] = params["start_time"][-1].rstrip("\n")
        elif "stop_time" in line:
            temp = line.split("=")
            params["stop_time"] = temp[-1].split(":")
            params["stop_time"][-1] = params["stop_time"][-1].rstrip("\n")
        elif "save_path" in line:
            temp = line.split("=")
            params["save_path"] = temp[-1].rstrip("\n")
        elif "onedrive_folder" in line:
            temp = line.split("=")
            params["onedrive_folder"] = temp[-1].rstrip("\n")
        else:
            continue

    f.close()
    return params

def connect(host="http://google.com"):
    try:
        urllib.urlopen(host)
        return True
    except:
        return False

def sync_script(channel):
    try:
        subprocess.call(['sh', 'sync_scripts/sync_weekly.sh', '>>', 'log.txt'])
    except Exception as e:
	    print("Couldnt upload files.")


def blink_LED(freq, count, LED):
    for i in range(count):
        GPIO.output(LED, GPIO.HIGH)
        t.sleep(freq)
        GPIO.output(LED, GPIO.LOW)
        t.sleep(freq)

def write_to_log(text, t_bool = True, log_file='log.txt'):
    cur_time_str = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(cur_time_str + ": " + text + "\n") if t_bool else \
            f.write("\n\n" + text + "\n")
