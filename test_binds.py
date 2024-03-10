import time
import subprocess
import pydirectinput


if __name__ == '__main__':
    pydirectinput.FAILSAFE = False
    time.sleep(2)
    s1 = subprocess.Popen('python presentmon.py')
    time.sleep(18.0)
    # end stream shortcut
    pydirectinput.keyDown('ctrl')
    pydirectinput.keyDown('shift')
    pydirectinput.keyDown('alt')
    pydirectinput.keyDown('q')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('shift')
    pydirectinput.keyUp('alt')
    pydirectinput.keyUp('q')
