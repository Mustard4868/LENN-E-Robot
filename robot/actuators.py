import machine, time
from machine import Pin

class Motor():
    def __init__(self, enA, in1, in2):
        enA = Pin(enA, Pin.OUT)
        in1 = Pin(in1, Pin.OUT)
        in2 = Pin(in2, Pin.OUT)

        in1.value(1)
        in2.value(0)
        enA.value(0)
    
    def Test(self) -> None:
        for i in range(0, 100, 1):
            self.SetSpeed(i)
            time.sleep(0.1)
        for i in range(100, -100, -1):
            self.SetSpeed(i)
            time.sleep(0.1)
        for i in range(-100, 0, 1):
            self.SetSpeed(i)
            time.sleep(0.1)

    def SetSpeed(self, percentage) -> None:
        output = abs(int(percentage * 4095 / 100))
        if percentage > 0:
            self.in1.value(1)
            self.in2.value(0)
        elif percentage < 0:
            self.in1.value(0)
            self.in2.value(1)
        self.enA.value(output)

class Magnet():
    def __init__(self, signal_pin):
        self.signal_pin = Pin(signal_pin, Pin.OUT)
        self.signal_pin.value(0)

    def Test(self):
        print("Testing Magnet...")
        self.Enable()
        time.sleep(1)
        self.Disable()
    
    def Enable(self):
        self.signal_pin.value(1)

    def Disable(self):
        self.signal_pin.value(0)