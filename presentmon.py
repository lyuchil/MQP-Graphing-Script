import time
import subprocess
import pydirectinput
import ctypes, sys,os

current_time_ms = int(time.time() * 1_000)
destination_folder = "C:/Users/claypool/Desktop/pm_log_temp"
file_name = f"{current_time_ms}.csv"
commandline = f'C:/Users/claypool/Desktop/my_test/graph_script/MQP-Graphing-Script/PresentMon-1.9.2-x64.exe -output_file ./presentmon_testing/{file_name} -process_name Moonlight.exe -timed 30 -terminate_after_timed -no_top'

os.popen(commandline)

#os.popen(
#         'C:/Users/claypool/Desktop/my_test/graph_script/MQP-Graphing-Script/PresentMon-1.9.2-x64.exe  -output_file    -process_name Moonlight.exe -timed 30 -terminate_after_timed -no_top')

