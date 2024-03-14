from machine import Pin

class Motor():
    def __init__(self, enA, in1, in2):
        enA = Pin(enA, Pin.OUT)
        in1 = Pin(in1, Pin.IN)
        in2 = Pin(in2, Pin.IN)

        in1.value(1)
        in2.value(0)
        enA.value(0)
    
    def SetSpeed(self, percentage):
        output = abs(int(percentage * 4095 / 100))
        if percentage > 0:
            self.in1.value(1)
            self.in2.value(0)
        elif percentage < 0:
            self.in1.value(0)
            self.in2.value(1)
        self.enA.value(output)


class Magnet():
    def __init__(self, pin):
        Magnet_Pin = Pin(pin, Pin.OUT)

    def Enable(self):
        self.Magnet_Pin.value(1)
        print("Enabled Magnet")

    def Disable(self):
        self.Magnet_Pin.value(0)
        print("Disabled Magnet")


class Servo():
    def __init__(self, pin):
#        Servo_Pin = Pin(pin, Pin.OUT)
        pass