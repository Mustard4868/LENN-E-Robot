from machine import Pin, time_pulse_us, SoftI2C
from utils import *
import time

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

        self.distance_array = []

    def __getDistance(self, unit = "mm") -> float:
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

    def getDistance(self, unit = "mm") -> float:
        n = 10
        distance_array = self.distance_array
        if len(distance_array) < n:
            for i in range(len(distance_array), n):
                distance_array.append(self.__getDistance())
        
        distance_array.pop(0)
        distance_array.append(self.__getDistance())

        return sum(distance_array)/n
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

        self.average_array = []
        self.junction_array = []

    def __getArray(self) -> list[bool]:
        """
        Reads and returns IR sensor values.
        """
        array = [
            self.d1.value(),
            self.d2.value(),
            self.d3.value(),
            self.d4.value(),
            self.d5.value(),
            self.d6.value(),
            self.d7.value(),
            self.d8.value()
        ]
        return array
    
    def __movingAverage(self) -> list[float]:
        """
        Moving average filter where n is equal to the number of arrays used to calculate the average.
        """
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

        return moving_average_array
    
    def getJunction(self) -> list[str]:
        """
        Returns True when a junction is detected.\n
        Makes use of a moving average, when the moving average sum is equal to 1. A junction should be detected.
        """
        junction_array = []
        while len(junction_array) < 5:

            line_array = self.__movingAverage()
            mix_index = len(line_array) // 2
            left_half = line_array[:mix_index]
            right_half = line_array[mix_index:]

            left_res = sum(left_half)/len(left_half)
            right_res = sum(right_half)/len(right_half)

            if sum(line_array)/len(line_array) == 1:
                junction_array.append("T")
            elif left_res == 1 and right_res != 1:
                junction_array.append("R")
            elif left_res != 1 and right_res == 1:
                junction_array.append("L")
            else:
                junction_array.append("N")

        return junction_array

    
    def getLine(self) -> float:
        """
        Calculates and returns deviation from line using moving average filter.\n
        <0 == Deviation to the left.\n
        >0 == Deviation to the right.    
        """
        array = self.__movingAverage()
        mid_index = len(array) // 2
        left_half = array[:mid_index]
        right_half = array[mid_index:]
        left_average = sum(left_half)/len(left_half)
        right_average = sum(right_half)/len(right_half)
        return (left_average - right_average)

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
        return time_pulse_us(self.out, 0)
    
    def __getGreen(self):
        self.s2.value(1)
        self.s3.value(1)
        return time_pulse_us(self.out, 0)
    
    def __getBlue(self):
        self.s2.value(0)
        self.s3.value(1)
        return time_pulse_us(self.out, 0)
    
    def getRGB(self) -> dict[str, int]:
        """
        Returns a dictionary with the red, green and blue values\n
        Example:\n
            {red: 255, green: 255, blue: 255}
        """
        dictionary = {
            "red": self.__getRed(),
            "green": self.__getGreen(),
            "blue": self.__getBlue()
        }
        return dict(sorted(dictionary.items()))
    
    def getColor(self) -> str:

        n = 20
        total_r, total_g, total_b = 0, 0, 0

        for i in range(n):
            r, g, b = self.getRGB().values()
            total_r += r
            total_g += g
            total_b += b

        avg_r = total_r / n
        avg_g = total_g / n
        avg_b = total_b / n

        rgb = [avg_r, avg_g, avg_b]
        print(rgb)

        r, g, b = rgb

        if r > 0 and g >= 200 and b >= 150:
            return "Black"
        
        elif all(rgb[i] <= 50 for i in range(3)):
            return "White"
        
        elif r < 60 and g >= 125 and b > 100:
            return "Red"
        
        elif r < 60 and g < 125 and b > 100:
            return "Green"
        
        elif r > 125 and g > 80 and b < 100:
            return "Blue"
        
        else:
            return "Undefined"
    
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
        