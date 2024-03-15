from abc import ABC, abstractmethod
from main import Robot

class State(ABC): # Abstract class / SUPERCLASS
    def __init__(self):
        self.Robot = Robot
        super().__init__()

    @abstractmethod
    def on_enter(self) -> None:
        """ abstract method: execute this code upon state entry """
        print("Entered {self.__class__.__name__}")

    @abstractmethod
    def on_exit(self) -> None:
        """ abstract method: execute this code when exiting state """
        print("Exiting {self.__class__.__name__}")

    @abstractmethod
    def execute(self) -> None:
        """ abstract method: execute this code during state """
        print("Exiting {self.__class__.__name__}")

class Idle(State):
    def on_enter(self):
        # disable all actuators
        self.LeftMotor.SetSpeed(0)
        self.RightMotor.SetSpeed(0)
        self.Magnet.Disable()

    def on_exit(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

class MoveForward(State):
    def on_enter(self):
        raise NotImplementedError

    def on_exit(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
    
class MoveStop(State):
    def on_enter(self):
        raise NotImplementedError

    def on_exit(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

class ForwardTurnLeft(State):
    def on_enter(self):
        raise NotImplementedError

    def on_exit(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
    
class ForwardTurnRight(State):
    def on_enter(self):
        raise NotImplementedError

    def on_exit(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
    
class AxisTurnLeft(State):
    def on_enter(self):
        raise NotImplementedError
    
    def on_exit(self):
        raise NotImplementedError
    
    def execute(self):
        raise NotImplementedError
    
class AxisTurnRight(State):
    def on_enter(self):
        raise NotImplementedError
    
    def on_exit(self):
        raise NotImplementedError
    
    def execute(self):
        raise NotImplementedError