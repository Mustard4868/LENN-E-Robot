from machine import Pin, time_pulse_us, SoftI2C
from utils import *
import struct, math, time

channels = {
    "channel 1" : b"\x02",
    "channel 2" : b"\x04",
    "channel 3" : b"\x08"
}

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def getDistance(self, unit = "mm") -> float:
        units = {"mm": 1, "cm": 10, "m": 1000}
        self.trigger.value(0)
        time.sleep_us(5)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)

        try:
            pulse_time = time_pulse_us(self.echo, 1, 500*2*30)
        except OSError as ex:
            if ex.args[0] == 110:
                raise OSError("Out of range")
            raise ex
        
        distance = pulse_time * 100 // 582
        distance_units = distance / units[unit]
        return distance_units

class LineSensor:
    def __init__(self, ir, d1, d2, d3, d4, d5, d6, d7, d8):
        self.ir = Pin(ir, Pin.OUT)
        self.ir.on()

        self.d1 = Pin(d1, Pin.IN)
        self.d2 = Pin(d2, Pin.IN)
        self.d3 = Pin(d3, Pin.IN)
        self.d4 = Pin(d4, Pin.IN)
        self.d5 = Pin(d5, Pin.IN)
        self.d6 = Pin(d6, Pin.IN)
        self.d7 = Pin(d7, Pin.IN)
        self.d8 = Pin(d8, Pin.IN)

    def __getArray(self) -> list:
        """Returns an array of the line sensor values"""
        array = []
        sensors = [self.d1, self.d2, self.d3, self.d4, self.d5, self.d6, self.d7, self.d8]
        for sensor in sensors:
            array.append(sensor.value())
        return array
    
class ColorSensor:
    def __init__(self, s2, s3, out):
        self.s2 = Pin(s2, Pin.OUT)
        self.s3 = Pin(s3, Pin.OUT)
        self.out = Pin(out, Pin.IN)

    """
    -------------------------------------
    |   Color   |   R   |   G   |   B   |
    -------------------------------------
    |   Black   |   220 |   232 |   190 |
    |   White   |   17  |   17  |   4   |

    """
    
    def __getRed(self):
        self.s2.value(0)
        self.s3.value(0)
        return 254 - time_pulse_us(self.out, 0)
    
    def __getGreen(self):
        self.s2.value(1)
        self.s3.value(1)
        return 254 - time_pulse_us(self.out, 0)
    
    def __getBlue(self):
        self.s2.value(0)
        self.s3.value(1)
        return 254 - time_pulse_us(self.out, 0)
    
    def getRGB(self) -> dict:
        """
        Returns a dictionary with the red, green and blue values
        red : int, green : int, blue : int

        """
        dictionary = {
            "red": self.__getRed(),
            "green": self.__getGreen(),
            "blue": self.__getBlue()
        }
        return dict(sorted(dictionary.items()))
    
class Encoder:
    def __init__(self, channel):
        self.channel = channels[channel]
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

    def __enableChannel(self):
        self.i2c.writeto(0x70, b"\x00") # First disable all other channels
        self.i2c.writeto(0x70, self.channel)

    def getAngle(self):
        self.__enableChannel()
        data = self.i2c.readfrom_mem(0x70, 0x0E, 2)
        angle_raw = int.from_bytes(data, "big")
        angle_deg = (angle_raw * 360) / 4096

        return angle_deg