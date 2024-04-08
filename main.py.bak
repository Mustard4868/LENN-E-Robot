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

        self.Magnet = Magnet(signal_pin=23)

        self.LeftEncoder = Encoder("channel 2")
        self.RightEncoder = Encoder("channel 3")

        self.LineSensor = LineSensor(ir=27, d1=26, d2=25, d3=33, d4=32, d5=35, d6=34, d7=39, d8=36)
        self.UltrasonicSensor = UltrasonicSensor(trigger_pin=19, echo_pin=18)
        self.ColorSensor = ColorSensor(s2=12, s3=14, out=13)

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
        for i in range(3, 0, -1):
            print(f"{i} seconds until test.")
            time.sleep(1)
        self.robot.changeState(Forward())

class Forward(State):

    def __init__(self):
        super().__init__()
        self.pid_controller = PIDController(kp = 6, ki = 0, kd = 0.2, setpoint=0)

    def on_enter(self):
        print("Entering Forward State")
        # Reset PID controller when entering the state
        self.pid_controller.reset()

    def execute(self):
        max_speed = 100
        
        while True:
            distance = self.robot.UltrasonicSensor.getDistance(unit="mm")
            left_average, right_average, result = self.robot.LineSensor.getLine()

            if 0 < distance < 100:
                print("Obstacle detected!")
                self.robot.changeState(Stop())
                break
            
            elif left_average > 0.5 and right_average > 0.5:
                left_speed = max_speed
                right_speed = max_speed

            elif left_average < 0.25 and right_average < 0.25:
                left_speed = -0.5 * max_speed
                right_speed = -0.5 * max_speed

            elif result < 0:
                if result < -0.5:
                    left_speed = -0.5 * max_speed
                else: left_speed = 0
                right_speed = 1 * max_speed

            elif result > 0:
                if result > 0.5:
                    right_speed = -0.5 * max_speed
                else: right_speed = 0
                left_speed = 1 * max_speed

            self.robot.LeftMotor.setSpeed(left_speed)
            self.robot.RightMotor.setSpeed(right_speed)
            print(f"{left_average}, {right_average}")

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
        raise NotImplementedError


robot = Robot()
robot.changeState(Idle())
