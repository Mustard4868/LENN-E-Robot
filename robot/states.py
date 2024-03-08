class State: # Abstract class / SUPERCLASS
    def __init__(self):
        raise Exception("You cannot initialize this class")

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def execute(self):
        pass

class Idle(State):
    def on_enter(self):
        raise NotImplementedError

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
