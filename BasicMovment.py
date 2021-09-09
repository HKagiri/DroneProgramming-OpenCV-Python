# importing libraries

from djitellopy import tello
from time import sleep


#connect to the tello (object)

me = tello.Tello()
me.connect()

#print out battery percentage
print(me.get_battery())
#Take off
me.takeoff()
#print out send command (-100 to 100)
me.send_rc_control(0,50,0,0)
#Delay
sleep(2)
me.send_rc_control(0,0,0,30)
#Delay
sleep(2)
# print out send command (-100 to 100)
me.send_rc_control(0,0, 0, 0)
#land
me.land()

