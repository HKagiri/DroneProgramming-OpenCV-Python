import cv2
import numpy as np
from djitellopy import tello

#connect to the tello (object)
me = tello.Tello()
me.connect()

#print out battery percentage
print(me.get_battery())

#Get Stream
me.streamon()
me.takeoff()
#loop stream
cap = cv2.VideoCapture(0)

hsvVals = [0,0,64,179,255,160]
sensors = 3
threshold = 0.2
width, height = 480, 360


sensitivity = 3 # if the number is high less sensitive
weights = [-25, -15, 0, 15, 25] # l, sl, c, sr, r
fSpeed = 15
curve = 0

def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )#hue saturation values BGR to HSV
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def getContours(imgThres, img):
    contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0 :
        biggest  = max(contours, key= cv2.contourArea)
        x,y,w,h = cv2.boundingRect(biggest)
        cx = x + w // 2
        cy = y + h // 2

        cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
        cv2.circle(img, (cx,cy), 10, (0, 255, 255), cv2.FILLED)

    return cx

def getSensorOutput(imgThres, sensors):
    # split using numpy
    imgs = np.hsplit(imgThres, sensors) # width of the image should be divisible by 3
    totalPixels = (img.shape[1] // sensors) * img.shape[0]
    senOut = []

    for x, im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > threshold * totalPixels:
            senOut.append(1)
        else:
            senOut.append(0)
        #cv2.imshow(str(x), im)
    #print(senOut)
    return senOut
def sendCommands(senOut, cx):
    global curve

    ## TRANSLATION ##
    lr = (cx - width // 2) // sensitivity
    lr = int(np.clip(lr, -10, 10))#restrict translation

    if lr < 2  and lr > -2: lr = 0

    #me.send_rc_control(lr, 0, 0, 0)

    ## ROTATION ##
    if   senOut == [1, 0, 0]: curve = weights[0]
    elif senOut == [1, 1, 0]: curve = weights[1]
    elif senOut == [0, 1, 0]: curve = weights[2]
    elif senOut == [0, 1, 1]: curve = weights[3]
    elif senOut == [0, 0, 1]: curve = weights[4]

    elif senOut == [0, 0, 0]: curve = weights[2]
    elif senOut == [1, 1, 1]: curve = weights[2]
    elif senOut == [1, 0, 1]: curve = weights[2]

    # me.send_rc_control(lr, fSpeed, 0, curve)

while True:
    #_, img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img, (width, height))
    img = cv2.flip(img, 0) # flip the image from the drone camera

    imgThres = thresholding(img)
    cx = getContours(imgThres, img) #Translation
    senOut =  getSensorOutput(imgThres, sensors) #Rotation

    sendCommands(senOut, cx)
    cv2.imshow("Output", img)
    cv2.imshow("Path", imgThres)
    cv2.waitKey(1)