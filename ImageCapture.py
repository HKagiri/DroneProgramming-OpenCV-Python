# importing libraries
import cv2 # openCV import
from djitellopy import tello

#connect to the tello (object)
me = tello.Tello()
me.connect()

#print out battery percentage
print(me.get_battery())

#Get Stream
me.streamon()
#loop stream
while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img,(360,240))  # Small frame size for faster processing
    cv2.imshow("Image",img) # window to display result
    cv2.waitKey(1) # Delay of 1 milli_second
