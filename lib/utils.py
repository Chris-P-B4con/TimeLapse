import urllib
import subprocess


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



