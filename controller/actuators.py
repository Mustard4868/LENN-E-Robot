import machine, time
from machine import Pin

class Motor():
    def __init__(self, enA, in1, in2):
        self.enA = Pin(enA, Pin.OUT)
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)

        self.in1.value(1)
        self.in2.value(0)
        self.enA.value(0)

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

    def Enable(self) -> None:
        self.signal_pin.value(1)

    def Disable(self) -> None:
        self.signal_pin.value(0)

class Display():
    def __init__(self, S, P, I):
        self.S = Pin(S, Pin.OUT)


    def Clear(self) -> None:
        raise NotImplementedError
    
    def Write(self) -> None:
        raise NotImplementedError