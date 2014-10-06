import usb.core
import usb.util
import serial
import sys
import struct
from sixpair_helpers import *

"""

100 - Arduino ready
101 - Server ready
102 - Acknowledge connection

50 - Request control State
51 - Control state readdy
52 - Acknowledge ready state (Ready to receive 3 byte update)

"""
        

ir = IRLED()

dev = usb.core.find(idVendor=0x054C, idProduct=0x0268)

if dev is None:
    raise ValueError("Controller not found")

try:
    dev.set_configuration()
except usb.core.USBError:
    print "Controller connection error - try reconnecting."

ps3 = PS3(dev) 

if __name__ == "__main__":

    print "Press PS button to start."

    while True:
        ps3.update()
        if ps3.ps_power_button: 
            break

    while True:
        ps3.update()
        if not ps3.ps_power_button: 
            break


    while True:

        ps3.update()
        ir.send_command(int(ps3.btn_r2_value / 2), int(ps3.left_joystick.x / 2),int( ps3.left_joystick.y / 2))

        print ps3.btn_r2_value, ps3.left_joystick.x, ps3.left_joystick.y

        if ps3.ps_power_button: 
            break   


    print "Control session quit."



        

