import time

from robot.actuators import *
from robot.sensors.hcsr04 import *
from robot.sensors.tcs3200 import * 

class Test():
    def __init__(self):
        #self.UltrasonicSensor = HCSR04(trigger_pin=5, echo_pin=4)
        #self.ColorSensor = TCS3200(S0=5, S1=6, S2=7, S3=8, OUT=9)
        self.LeftMotor = Motor(enA=27, in1=26, in2=25)
        #self.RightMotor = Motor(6)
        #self.Magnet = Magnet(8)

    def PrintValues(self):
        print(self.UltrasonicSensor.distance_mm())
        print(self.ColorSensor.rgb())

    def TestMotors(self):
        self.LeftMotor.SetSpeed(100)
        time.sleep(2)
        self.LeftMotor.SetSpeed(0)
        time.sleep(2)
        self.LeftMotor.SetSpeed(-100)
        time.sleep(2)
        self.LeftMotor.SetSpeed(0)

if __name__ == "__main__":
    Test = Test()
    while True:
        Test.TestMotors()