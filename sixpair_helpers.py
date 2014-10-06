import serial

class IRLED(object):
    """docstring for IRLED"""
    def __init__(self, port = "/dev/tty.usbmodem1411", baud = 9600, establish_contact = True):

        self.ser = serial.Serial(port, baud)
        self.establish_contact()

    def establish_contact(self):
        while True:
            res = self.ser.read()
            if res == chr(100):
                print "Wrote connection byte"
                self.ser.write(str(unichr(101)))
            if res == chr(102):
                print "Successfully established connection."
                break

    def send_command(self, Throttle, LeftRight, FwdBack):
        res = self.ser.read()
        if res == chr(50):
            self.ser.write(str(unichr(51)))
        if res == chr(52):
            self.ser.write(str(unichr(min(Throttle, 230)))) # 0 - 128
            self.ser.write(str(unichr(LeftRight))) # 0 - 128
            self.ser.write(str(unichr(FwdBack))) # 0 - 128


class JoystickPosition(object):
    """docstring for JOYSTICK_POSITION"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PS3(object):
    """docstring for ClassName"""

    def __init__(self, dev):

        self.device = dev

        self.direction_pad = None
        self.button_pad = None
        self.ps_power_button = None   # 0-depressed; 1-pressed
        self.left_joystick = JoystickPosition(-1,-1)
        self.right_joystick = JoystickPosition(-1,-1)
        self.btn_l2_value = None      # 0-depressed; 255-fully pressed
        self.btn_r2_value = None      # 0-depressed; 255-fully pressed
        self.btn_l1_value = None      # 0-depressed; 255-fully pressed
        self.btn_r1_value = None      # 0-depressed; 255-fully pressed
        self.motor1 = None
        self.motor2 = None
        self.hit = None               # not for sure but appears to be 1 normally, then becomes 2 if the controller is hit
        self.roll  = None             # 0-centered; left-positive; right-negative
        self.pitch = None             # 0-centered; up-positive; down-negative
        self.z_axis = None            # not sure what axis this is. it does change with movement tho

    def update(self):
        # Controller state.
        cs = self.device.ctrl_transfer(0xa1, 0x1, 0x0101, 0, 0x31)

        # print cs

        self.direction_pad = cs[2]
        self.button_pad = cs[3]
        self.ps_power_button = cs[4]   
        self.left_joystick.x = cs[6]
        self.left_joystick.y = cs[7]
        self.right_joystick.x = cs[8]
        self.right_joystick.y = cs[9]
        self.btn_l2_value = cs[18]      
        self.btn_r2_value = cs[19]  
        self.btn_l1_value = cs[20]       
        self.btn_r1_value = cs[21]        
        self.motor1 = cs[28]
        self.motor2 = cs[35]
        self.roll  = cs[42]
        self.pitch = cs[44]  
        # self.z_axis = None  