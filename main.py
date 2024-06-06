from actuators import *
from sensors import *
from mapping import *
from utils.mpu6050 import *
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
        """ CLASS INITIALIZERS """
        self.LeftMotor = Motor(enable=15, in_x=2, in_y=4)
        self.RightMotor = Motor(enable=5, in_x=17, in_y=16)

        self.Magnet = Magnet(signal_pin=23)

        self.LineSensor = LineSensor(ir=27, d1=26, d2=25, d3=33, d4=32, d5=35, d6=34, d7=39, d8=36)
        self.UltrasonicSensor = UltrasonicSensor(trigger_pin=19, echo_pin=18)
        self.ColorSensor = ColorSensor(s2=12, s3=14, out=13)

        """ VARIABLES """
        self.starting_point = (0, 0)
        self.target_point = (10, 14)

        # Target points for the colored boxes to go.
        self.red_target = (10, 14)
        self.green_target = (10, 12)
        self.blue_target = (10, 10)
        self.black_target = (10, 8)

        self.carrying = False # Is the robot carrying a payload?
        self.current_position_index = 0

        self.path = bfs_shortest_path(self.starting_point, self.target_point) # Set initial path to start mission.

        self.junctions = getJunctions(self.path)

    def changeState(self, state) -> None:
        """
        Change the current state of the robot.\n
        Can only be a class that inherits from metaclass: "State"
        """
        self.current_state = state
        self.current_state.on_enter()
        self.current_state.execute()

    def cleanup(self) -> None:
        """
        Disables all actuators and exits the program.
        """
        self.Magnet.Set(False)
        self.LeftMotor.setSpeed(0)
        self.RightMotor.setSpeed(0)

class State:
    def __init__(self):
        self.robot = Robot()
    
    def on_enter(self) -> None:
        pass

    def execute(self) -> None:
        pass

    def cleanup(self) -> None:
        """
        Same as Robot.cleanup() without exiting the program.\n
        Use this function to clean up from within the state machine.\n
        !!! DO NOT USE OUTSIDE OF A STATE CLASS !!!       
        """
        self.robot.LeftMotor.setSpeed(0)
        self.robot.RightMotor.setSpeed(0)
        self.robot.Magnet.Set(False)

class Idle(State):
    def __init__(self):
        super().__init__()
    
    def on_enter(self):
        print("Entering Idle State")
        self.cleanup()
    
    def execute(self):
        for i in range(1, 0, -1):
            #print(f"{i} seconds until test.")
            time.sleep(1)
        self.robot.changeState(Forward())

class Forward(State):
    def __init__(self):
        super().__init__()
        self.pid_controller = PIDController(kp=1.5, ki=0.0001, kd=0.999, setpoint=0)

    def on_enter(self):
        print("Entering Forward State")
        self.pid_controller.reset()

    def execute(self):
        max_speed = 100

        while True:
            distance = self.robot.UltrasonicSensor.getDistance(unit="mm")
            result = self.robot.LineSensor.getLine()
            print(result)

            getJunction = self.robot.LineSensor.getJunction()
            if all(x == getJunction[0] for x in getJunction):
                if getJunction[0] != "N":
                    pass

            if distance < 0:
                if not self.robot.carrying:
                    self.robot.changeState(Detect())
                else:
                    self.robot.changeState(Turn(180))
                break

            if sum(self.robot.LineSensor.__movingAverage()) == 0:
                self.robot.changeState(Turn(180))
                break
            else:
                correction = self.pid_controller.compute(result)
                base_speed = max_speed
                left_speed = base_speed - correction*100
                right_speed = base_speed + correction*100

            # Set rounded integer for motor speed within limits -100 to 100
            self.robot.LeftMotor.setSpeed(round(max(min(left_speed, max_speed), -max_speed)))
            self.robot.RightMotor.setSpeed(round(max(min(right_speed, max_speed), -max_speed)))

class Turn(State):
    def __init__(self, heading):
        super().__init__()
        self.heading = heading

    def on_enter(self) -> None:
        print(f"Entering Turn State: {self.heading} deg.")
        robot.LeftMotor.setSpeed(0)
        robot.RightMotor.setSpeed(0)

    def execute(self) -> None:
        start_time = time.time()
        multiplier = 1
        if self.heading < 0:
            multiplier = -1

        while start_time + abs(self.heading/60) > time.time():
            self.robot.LeftMotor.setSpeed(50 * multiplier)
            self.robot.RightMotor.setSpeed(-50 * multiplier)

        self.robot.LeftMotor.setSpeed(0)
        self.robot.RightMotor.setSpeed(0)
        self.robot.changeState(Forward())

class Detect(State):
    def __init__(self):
        super().__init__()
        self.pid_controller = PIDController(kp=1.5, ki=0.0001, kd=0.999, setpoint=0)

    def on_enter(self):
        print("Entering Detect State")
        if not self.robot.carrying:
            self.cleanup()
        else:
            print("Robot is carrying a payload.\nUnable to detect type of obstacle, moving on.")
            self.robot.changeState(Turn(180))

    def execute(self):
        max_speed = 50 # Half the max speed to ensure a slow acceleration towards the box.
        zero_limit = 10 # This is what the ultrasonic sensor measures when the robot is in contact with the box.

        self.pid_controller.reset()

        start_time = time.time()

        while start_time + 3 > time.time():
            result = self.robot.LineSensor.getLine()

            correction = self.pid_controller.compute(result)
            base_speed = 50 # Slow down robot when it gets closer to the box.
            left_speed = base_speed - correction*100
            right_speed = base_speed + correction*100

            self.robot.LeftMotor.setSpeed(round(max(min(left_speed, max_speed), -max_speed)))
            self.robot.RightMotor.setSpeed(round(max(min(right_speed, max_speed), -max_speed)))
        
        """ Logic for determining color and selecting new path. """

        self.cleanup()
        while True:
            color = self.robot.ColorSensor.getColor()
            if color != "Undefined":
                break

        if color == "Red":
            self.robot.target_point = self.robot.red_target
        elif color == "Green":
            self.robot.target_point = self.robot.green_target
        elif color == "Blue":
            self.robot.target_point = self.robot.blue_target
        elif color == "Black":
            self.robot.target_point = self.robot.black_target
        else:
            raise Exception("Something went wrong!")

        self.robot.Magnet.Set(True)
        self.robot.changeState(Turn(180)) # Turn 180 degrees and continue mission.
            
class Stop(State):
    def __init__(self):
        super().__init__()

    def on_enter(self):
        print("Entering Stop State")

    def execute(self):
        self.cleanup()

while True:
    try:
        robot = Robot()
        robot.changeState(Idle())
        break
    except KeyboardInterrupt as e:
        print(f"Exiting program from main loop: {e}")
        robot.cleanup()
        break
