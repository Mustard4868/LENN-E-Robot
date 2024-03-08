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
        
        """ Initialize the state """
        self.CurrentState = Idle()

    def ChangeState(self, new_state):
        if not issubclass(new_state, State):
            raise Exception("f{new_state} is not a subclass of State")

        self.current_state.on_exit(self)    # Call the on_exit method of the current state
        self.current_state = new_state      # Change the current state to the new state
        self.current_state.on_enter(self)   # Call the on_enter method of the new state
        self.current_state.execute(self)    # Call the execute method of the new state
