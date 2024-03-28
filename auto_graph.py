import time
import subprocess
import ctypes, sys,os

pm_folder = "C:/Users/claypool/Desktop/pm_logger_mqp_23-24"
log_folder = "C:/Users/claypool/Desktop/local_logger_mqp23-24"

def get_recent_file(folder_path):
    files = [os.path.join(folder_path, x) for x in os.listdir(folder_path) if x.endswith(".csv")]
    newest = max(files , key = os.path.getctime)
    return newest


pm = get_recent_file(pm_folder)
log = get_recent_file(log_folder)

# manually change it 
title = "E-Policy-QMon-NJ"

commandline = f'python graphing.py --log {log} --pm {pm} --title {title}'

s1 = subprocess.Popen(commandline)



