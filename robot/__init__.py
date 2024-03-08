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
from .sensors import *
from .actuators import *

class Robot():
    def __init__(self):

        """ !!! CHANGE THE PIN NUMBERS TO THE CORRECT ONES !!! """
        self.ColorSensor         = ColorSensor(1)
        self.UltraSonicSensor    = UltrasonicSensor(2)
        self.LeftContrastSensor  = ContrastSensor(3)
        self.RightContrastSensor = ContrastSensor(4)

        self.LeftMotor  = Motor(5)
        self.RightMotor = Motor(6)
        self.Servo      = Servo(7)
        self.Magnet     = Magnet(8)

        self.Screen = None
        
        """ Initialize the state """
        self.CurrentState = Idle(self)
        self.CurrentState.on_enter()
        self.CurrentState.execute()

    def ChangeState(self, new_state):
        if not issubclass(new_state, State):
            raise Exception("f{new_state} is not a subclass of State")

        self.CurrentState = new_state      # Change the current state to the new state
        self.CurrentState.on_exit()    # Call the on_exit method of the current state
        self.CurrentState.on_enter()   # Call the on_enter method of the new state
        self.CurrentState.execute()    # Call the execute method of the new state
