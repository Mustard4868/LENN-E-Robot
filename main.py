from actuators import *
from sensors import *
from pid_controller import *
import time

class Robot:
    """
    !!! DO NOT MAKE ANY CHANGES TO THIS CLASS !!!\n
    Robot class for LENN-E Robot.\n
    This class initializes all the sensors and actuators of the robot.\n
    Use the State class to control the robot.\n
    """
    def __init__(self):
        self.LeftMotor = Motor(enable=15, in_x=2, in_y=4)
        self.RightMotor = Motor(enable=5, in_x=16, in_y=17)

        self.Magnet = Magnet(signal_pin=14)

        self.LeftEncoder = Encoder("channel 2")
        self.RightEncoder = Encoder("channel 3")

        self.LineSensor = LineSensor(ir=27, d1=26, d2=25, d3=33, d4=32, d5=35, d6=34, d7=39, d8=36)
        self.UltrasonicSensor = UltrasonicSensor(trigger_pin=19, echo_pin=18)
        self.ColorSensor = ColorSensor(s2=12, s3=13, out=23)

    def changeState(self, state):
        self.current_state = state
        self.current_state.on_enter()
        self.current_state.execute()

class State:
    def __init__(self):
        self.robot = Robot()
    
    def on_enter(self) -> None:
        pass

    def execute(self) -> None:
        pass

class Idle(State):
    def __init__(self):
        super().__init__()
    
    def on_enter(self):
        print("Entering Idle State")
        self.robot.LeftMotor.setSpeed(0)
        self.robot.RightMotor.setSpeed(0)
        self.robot.Magnet.Set(False)
    
    def execute(self):
        print("Executing Idle State")
        for i in range(3, 0, -1):
            print(f"{i} seconds until test.")
            time.sleep(1)
        self.robot.changeState(Forward())

class Forward(State):
    def __init__(self):
        super().__init__()

    def on_enter(self):
        print("Entering Test State")

    def execute(self):
        self.robot.LeftMotor.setSpeed(100)
        self.robot.RightMotor.setSpeed(100)    
        
        while True:
            distance = self.robot.UltrasonicSensor.getDistance(unit="mm")

            array = self.robot.LineSensor.__getArray()
            mid_index = len(array) // 2
            left_half = array[:mid_index]
            right_half = array[mid_index:]
            left_average = sum(left_half)/len(left_half)
            right_average = sum(right_half)/len(right_half)
            result = left_average - right_average

            if 0 < distance < 100:
                print("Obstacle detected!")
                self.robot.changeState(Stop())
                break

            elif result < 0:
                self.robot.LeftMotor.setSpeed(0)
                self.robot.RightMotor.setSpeed(100)
            elif result > 0:
                self.robot.LeftMotor.setSpeed(100)
                self.robot.RightMotor.setSpeed(0)

            print(f"Distance: {distance} mm | Array average: {result}")

class Stop(State):
    def __init__(self):
        super().__init__()

    def on_enter(self):
        print("Entering Stop State")

    def execute(self):
        self.robot.LeftMotor.setSpeed(0)
        self.robot.RightMotor.setSpeed(0)

class Approach(State):
    def __init__(self):
        super().__init__()

    def on_enter(self):
        print("Entering Approach State")

    def execute(self):
        while True:
            distance = self.robot.UltrasonicSensor.getDistance(unit="mm")
            self.robot.LeftMotor.setSpeed(distance)
            self.robot.RightMotor.setSpeed(distance)
            if distance < 2:
                self.robot.Magnet.Set(True)
                self.robot.changeState(Stop())
                break

robot = Robot()
robot.changeState(Idle())