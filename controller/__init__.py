"""
This is the package for the robot module.

:author:  Mustard4868
:license: The Unlicense

"""

__title__ = 'robot'
__author__ = 'Mustard4868'
__license__ = 'The Unlicense'
__version__ = '0.1.0'

#from pkgutil import extend_path
#__path__ = extend_path(__path__, __name__)

from .states import *
from .actuators import *
from .sensors import *

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class Robot(Singleton):
    def __init__(self, test: bool = False) -> None:
        """
        Robot class for LENN-E Robot.
        test: bool = False // If True, the robot will enter test mode.
        """
        State(self)
        
        # Sensors
        self.UltrasonicSensor = HCSR04(trigger_pin=19, echo_pin=18)
        self.ColorSensor = TCS3200(S2=1, S3=3, OUT=23) # S2 = TX0, S3 = RX0
        self.LineSensor = HCS301(d1=26, d2=25, d3=33, d4=32, d5=35, d6=34, d7=39, d8=36, IR=27) # d7 = VN, d8 = VP

        # Actuators
        self.Magnet = Magnet(signal_pin=14)
        self.LeftMotor = Motor(enA=15, in1=2, in2=4)
        self.RightMotor = Motor(enA=5, in1=16, in2=17) # in1 = RX2, in2 = TX2

        # Initialize the state
        self.CurrentState = Idle(self)
        self.CurrentState.on_enter()
        self.CurrentState.execute()
        
    def ChangeState(self, new_state) -> None:
        if not issubclass(new_state, State):
            raise Exception("f{new_state} is not a subclass of State")

        self.CurrentState = new_state  # Change the current state to the new state
        self.CurrentState.on_exit()    # Call the on_exit method of the current state
        self.CurrentState.on_enter()   # Call the on_enter method of the new state
        self.CurrentState.execute()    # Call the execute method of the new state

    def Test(self) -> None:
        self.LeftMotor.Test()
        self.RightMotor.Test()
