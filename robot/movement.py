class Movement:
    def __init__(self, robot):
        self.robot = robot

    def MoveForward(self, speed):
        raise NotImplementedError
    
    def MoveBackward(self, speed):
        raise NotImplementedError
    
    def TurnLeft(self, speed):
        raise NotImplementedError
    
    def TurnRight(self, speed):
        raise NotImplementedError