from abc import ABC, abstractmethod

class State(ABC): # Abstract class / SUPERCLASS
    def __init__(self, robot):
        self.robot = robot
        super().__init__

    @abstractmethod
    def on_enter(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass

    @abstractmethod
    def execute(self):
        pass

class Idle(State):
    def on_enter(self):
        self.robot.Magnet.Disable()
        self.robot.Face.Set("idling")

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
