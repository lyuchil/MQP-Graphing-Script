import time
import subprocess
import pydirectinput


if __name__ == '__main__':
    pydirectinput.FAILSAFE = False
    # moving to correct location
    for _ in range(10):
        time.sleep(0.25)
        pydirectinput.press('up')
    print("second mouse move over")
    time.sleep(0.25)
    for _ in range(15):
        time.sleep(0.1)
        pydirectinput.press('left')
    time.sleep(0.25)
    pydirectinput.press('right')
    time.sleep(0.25)
    for _ in range(7):
        time.sleep(0.1)
        pydirectinput.press('down')
    # entering benchmark
    pydirectinput.press('enter')
    time.sleep(0.5)
    pydirectinput.press('enter')

    # wait for benchmark to start
    time.sleep(10.0)

    # start presentmon logging
    print('started presentmon capture')
    s1 = subprocess.Popen('python presentmon.py')

    # # start pm capture ctrl + shift + 1
    # pydirectinput.keyDown('ctrl')
    # pydirectinput.keyDown('shift')
    # pydirectinput.keyDown('1')
    # pydirectinput.keyUp('ctrl')
    # pydirectinput.keyUp('shift')
    # pydirectinput.keyUp('1')

    
    # wait for capture to end
    time.sleep(67.0)
    print('capture ended')
    # exit benchmark and end stream
    pydirectinput.press('esc')
    time.sleep(0.5)
    # select exit
    pydirectinput.press('down')
    time.sleep(0.5)
    pydirectinput.press('down')
    time.sleep(0.5)
    # enter exit menu
    pydirectinput.press('enter')
    time.sleep(0.5)
    # exit
    pydirectinput.press('left')
    time.sleep(0.5)
    # select to quit benchmark
    pydirectinput.press('enter')
    time.sleep(5)
    # close final benchmark result
    pydirectinput.press('enter')
    time.sleep(1)
    # end stream shortcut
    pydirectinput.keyDown('ctrl')
    pydirectinput.keyDown('shift')
    pydirectinput.keyDown('alt')
    pydirectinput.keyDown('q')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('shift')
    pydirectinput.keyUp('alt')
    pydirectinput.keyUp('q')

