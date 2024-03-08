from machine import Pin

class ColorSensor():
    def __init__(self, pin):
        self.pin = pin

    def GetColor(self):
        raise NotImplementedError

class UltrasonicSensor():
    def __init__(self, pin):
        self.pin = pin
        US_Pin = Pin(pin, Pin.IN)

    def GetDistance(self):
        raise NotImplementedError
        
class ContrastSensor():
    def __init__(self, pin):
        self.pin = pin

    def GetContrast(self):
        raise NotImplementedError