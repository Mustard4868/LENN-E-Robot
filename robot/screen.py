import adafruit_displayio_sh1106
from machine import I2C, Pin

class Screen():
    def __init__(self, SDA, SCL):
        self.SDA = SDA
        self.SCL = SCL
        i2c = I2C(-1, Pin(self.SDA), Pin(self.SCL)) # SDA, SCL

    def Set(self, ctx):
        raise NotImplementedError

    def Clear(self):
        raise NotImplementedError