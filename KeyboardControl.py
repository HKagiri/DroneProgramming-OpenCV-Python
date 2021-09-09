from djitellopy import tello
from time import sleep

import KeyPressModule as kp
#initialize the module
kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

def getKeyInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    # Roll Inputs
    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    # Pitch Inputs
    if kp.getKey("UP"):fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    # Throttle Inputs
    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    # Yaw Inputs
    if kp.getKey("a"): yv = -speed
    elif kp.getKey("d"): yv = speed

    # Land Inputs
    if kp.getKey("q"): me.land()

    # Take-Off Inputs
    if kp.getKey("e"): me.takeoff()

    return [lr, fb, ud, yv]



while True:
    #print(kp.getKey("s"))
    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)

