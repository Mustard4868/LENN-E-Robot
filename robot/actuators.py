#from machine import Pin

class Motor():
    def __init__(self, pin):
        Motor_Pin = Pin(pin, Pin.OUT)
        pass


class Magnet():
    def __init__(self, pin):
        pass
#        Magnet_Pin = Pin(pin, Pin.OUT)

    def Enable(self):
        pass
        self.Magnet_Pin.value(1)

    def Disable(self):
#        self.Magnet_Pin.value(0)
        print("Disabled Magnet")


class Servo():
    def __init__(self, pin):
#        Servo_Pin = Pin(pin, Pin.OUT)
        pass