from abc import ABC, abstractmethod
from main import Robot

class State(ABC): # Abstract class / SUPERCLASS
    def __init__(self):
        self.Robot = Robot
        super().__init__()

    @abstractmethod
    def on_enter(self):
        print("Entered {self.__class__.__name__}")

    @abstractmethod
    def on_exit(self):
        print("Exiting {self.__class__.__name__}")

    @abstractmethod
    def execute(self):
        pass

class Idle(State):
    def on_enter(self):
        """Turn off all actuators"""
        self.LeftMotor.SetSpeed(0)
        self.RightMotor.SetSpeed(0)
        self.Magnet.Disable()

    def on_exit(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

class Move(State):
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

class MoveLeft(State):
    def on_enter(self):
        raise NotImplementedError

    def on_exit(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
    
class MoveRight(State):
    def on_enter(self):
        raise NotImplementedError

    def on_exit(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
