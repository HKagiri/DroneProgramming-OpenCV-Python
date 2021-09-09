from djitellopy import tello

import time
import cv2
import KeyPressModule as kp
#initialize the module
kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

global img #Making variable image global
me.streamon() #Get Stream

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
    if kp.getKey("q"): me.land(); time.sleep(3)

    # Take-Off Inputs
    if kp.getKey("e"): me.takeoff()

    if kp.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img) #save image
        time.sleep(0.3) #reduce the amount of images with a delay to one image

    return [lr, fb, ud, yv]



while True:
    #print(kp.getKey("s"))
    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    #Image Capture
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))  # Small frame size for faster processing
    cv2.imshow("Image", img)  # window to display result
    cv2.waitKey(1)  # Delay of 1 milli_second

