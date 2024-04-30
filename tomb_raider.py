import time
import subprocess
import pydirectinput



if __name__ == '__main__':
    pydirectinput.FAILSAFE = False

    pydirectinput.press('enter')

    time.sleep(0.5)

    for _ in range(3):
        time.sleep(0.25)
        pydirectinput.press('down')


    time.sleep(0.25)
    pydirectinput.press('enter')

    time.sleep(0.75)


    print('Press R to enter bench mark')
    time.sleep(0.25)
    pydirectinput.keyDown('r')
    time.sleep(0.25)
    pydirectinput.keyUp('r')
    print('end of pressing R')

    time.sleep(20)
    print('started presentmon capture')
    s1 = subprocess.Popen('python presentmon.py')

    time.sleep(62)
    pydirectinput.press('esc')

    time.sleep(0.5)
    pydirectinput.press('esc')

    for _ in range(5):
        time.sleep(0.25)
        pydirectinput.press('up')


    time.sleep(0.5)
    pydirectinput.press('esc')



    pydirectinput.keyDown('ctrl')
    pydirectinput.keyDown('shift')
    pydirectinput.keyDown('alt')
    pydirectinput.keyDown('q')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('shift')
    pydirectinput.keyUp('alt')
    pydirectinput.keyUp('q')

