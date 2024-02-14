import time
import subprocess
import pydirectinput
import os




if __name__ == '__main__':
    for _ in range(5):
        time.sleep(1)
        pydirectinput.FAILSAFE = False
        ##move to run
        pydirectinput.moveTo(60, 935)
        time.sleep(0.5)
        # start run
        pydirectinput.click()
        time.sleep(6.5)
        # move to desktop and run
        pydirectinput.moveTo(1000, 500)
        pydirectinput.click()
        time.sleep(0.5)
        # move to start and run
        pydirectinput.moveTo(450, 350)
        pydirectinput.click()
        # launch game
        time.sleep(15.0)  # waiting for stream load fully
        s1 = subprocess.Popen('python war_thunder_keybinds.py')
        s1.wait()

        # make sure moonlight is closed before rerunning
        os.system("taskkill /f /im  Moonlight.exe")
        time.sleep(5.0)







