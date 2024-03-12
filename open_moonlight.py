import time
import subprocess
import pydirectinput
import ctypes, sys,os

print(ctypes.windll.shell32.IsUserAnAdmin())
# os.popen(
#         'C:/Users/claypool/Desktop/my_test/graph_script/MQP-Graphing-Script/PresentMon-1.9.2-x64.exe -process_name Moonlight.exe -timed 30 -terminate_after_timed -no_top')

# make sure to change the path when pulling in lab vs working at home 
#os.popen(' C:\mqp_moonlight_ff1-22\Moonlight.exe stream "Windows Server" "Desktop"')
os.popen(' C:/test_build/Moonlight.exe stream "Windows Server" "Desktop"')
time.sleep(5)
print("opened moonlight")