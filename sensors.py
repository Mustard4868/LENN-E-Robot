from machine import Pin, time_pulse_us, SoftI2C
from utils import *
import struct, math, time

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

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
        if unit == "mm": distance = int(distance)
        return distance_units

class LineSensor:
    def __init__(self, ir, d1, d2, d3, d4, d5, d6, d7, d8):
        self.ir = Pin(ir, Pin.OUT)
        self.ir.on()

        #self.d1 = Pin(d1, Pin.IN) BROKEN
        #self.d2 = Pin(d2, Pin.IN) BROKEN
        self.d3 = Pin(d3, Pin.IN)
        self.d4 = Pin(d4, Pin.IN)
        self.d5 = Pin(d5, Pin.IN)
        self.d6 = Pin(d6, Pin.IN)
        self.d7 = Pin(d7, Pin.IN)
        #self.d8 = Pin(d8, Pin.IN) BROKEN

        self.average_array = []

    def __getArray(self) -> list:
        """Returns an array of the line sensor values"""
        array = [
            #self.d1.value(),
            #self.d2.value(),
            self.d3.value(),
            self.d4.value(),
            self.d5.value(),
            self.d5.value(), #DUPLICATE BECAUSE OF ODD NUMBER
            self.d6.value(),
            self.d7.value(),
            #self.d8.value()
        ]
        return array
    
    def __movingAverage(self) -> list:

        n = 5

        if len(self.average_array) <= n:
            for i in range(len(self.average_array), n):
                self.average_array.append(self.__getArray())

        self.average_array.pop(0)
        self.average_array.append(self.__getArray())

        sum_array = [0] * len(self.average_array[0])

        for array in self.average_array:
            sum_array = [sum(x) for x in zip(sum_array, array)]

        moving_average_array = [x / len(self.average_array) for x in sum_array]

        #print(moving_average_array)
        return moving_average_array
    
    def getLine(self) -> tuple:
        """left_average, right_average, result"""
        array = self.__movingAverage()
        mid_index = len(array) // 2
        left_half = array[:mid_index]
        right_half = array[mid_index:]
        left_average = sum(left_half)/len(left_half)
        right_average = sum(right_half)/len(right_half)
        result = left_average - right_average
        return left_average, right_average, result

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
    

class esp32_i2c:
    def __init__(self, channel):
        self.channel = channels[channel]

    def __enableChannel(self):
        i2c.writeto(0x70, b"\x00") # First disable all other channels
        i2c.writeto(0x70, self.channel)

class Gyro(esp32_i2c):
    def __init__(self, channel, steps):
        super().__init__(channel)
        self.i2c.writeto_mem(self.channel, 0x6B, bytes([0x01]))
        self.array = []
        self.n = steps

    def getGyroData(self) -> tuple[float, float, float]:
        # set the modified based on the gyro range (need to divide to calculate)
        gr:int = self.read_gyro_range()
        modifier:float = None
        if gr == 0:
            modifier = 131.0
        elif gr == 1:
            modifier = 65.5
        elif gr == 2:
            modifier = 32.8
        elif gr == 3:
            modifier = 16.4
            
        # read data
        data = self.i2c.readfrom_mem(self.address, 0x43, 6) # read 6 bytes (gyro data)
        x:float = (self._translate_pair(data[0], data[1])) / modifier
        y:float = (self._translate_pair(data[2], data[3])) / modifier
        z:float = (self._translate_pair(data[4], data[5])) / modifier
        
        return (x, y, z)
    
    def getMovingAverage(self):
        if len(self.array) < self.n:
            for i in range(len(self.array), self.n):
                self.array.append(self.getGyroData[0])
        
        x = 0
        for item in self.array:
            x = x+item
        return x/self.n
        