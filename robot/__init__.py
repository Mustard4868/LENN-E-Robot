"""
This is the package for the robot module.

:author:  Mustard4868
:license: The Unlicense

"""

__title__ = 'robot'
__author__ = 'Mustard4868'
__license__ = 'The Unlicense'
__version__ = '0.1.0'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .states import *
from .actuators import *
from .sensors.hcsr04 import HCSR04
from .sensors.tcs3200 import TCS3200

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class Robot(Singleton):
    def __init__(self, test: bool = False) -> None:
        """ !!! CHANGE THE PIN NUMBERS TO THE CORRECT ONES !!! """
        self.UltrasonicSensor = HCSR04(trigger_pin=5, echo_pin=4)
        self.ColorSensor = TCS3200(S0=5, S1=6, S2=7, S3=8, OUT=9)
        self.LeftMotor = Motor(enA=27, in1=26, in2=25)
        self.RightMotor = Motor(enA=22, in1=23, in2=24)

        """ Initialize the state """
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
