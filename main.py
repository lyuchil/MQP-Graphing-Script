import time
import subprocess
import pydirectinput
import ctypes, sys,os
import time 


if __name__ == '__main__':

    # open admin command prompt before running the script 
    # otherwise everything crashes
    tempVal = 0
    for _ in range(5):
        tempVal = 0
        f = open("tag.txt", "r+")
        tempVal = int(f.readline())
        
        print(type(tempVal))
        f.close()

        f = open("tag.txt", "w")
        tempVal = tempVal+1
        tempValString = str(tempVal)
        f.write(tempVal)

        f.close()
    



    

    # # launches moonlight
    # s1 = subprocess.Popen('python open_moonlight.py')
    # s1.wait()

    # # make sure moonlight stream is open
    # time.sleep(5)

    # # opens benchmark in wt
    # s2 = subprocess.Popen('python war_thunder_keybinds.py')
    # s2.wait()

    # # rename and match files
    # s3 = subprocess.Popen('python match_file.py')  
    # s3.wait()


    #for loop

    #open moonlight (with cmdline)
    #open presentmon (with cmdline)
    #open game with moonlight
    #run benchmark
    #start presentmon capture

    # for _ in range(5):
    #     time.sleep(1)
    #     pydirectinput.FAILSAFE = False
    #     ##move to run
    #     pydirectinput.moveTo(60, 935)
    #     time.sleep(0.5)
    #     # start run
    #     pydirectinput.click()
    #     time.sleep(6.5)
    #     # move to desktop and run
    #     pydirectinput.moveTo(1000, 500)
    #     pydirectinput.click()
    #     time.sleep(0.5)
    #     # move to start and run
    #     pydirectinput.moveTo(450, 350)
    #     pydirectinput.click()
    #     # launch game
    #     time.sleep(15.0)  # waiting for stream load fully
    #     s1 = subprocess.Popen('python war_thunder_keybinds.py')
    #     s1.wait()

    #     # make sure moonlight is closed before rerunning
    #     os.system("taskkill /f /im  Moonlight.exe")
    #     time.sleep(5.0)







