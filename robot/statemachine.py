class State:
    def __init__(self, name):
        self.name = name

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def execute(self):
        pass


class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def transition_to(self, new_state):
        if self.current_state:
            self.current_state.on_exit()
        self.current_state = new_state
        self.current_state.on_enter()

    def execute_current_state(self):
        self.current_state.execute()


class MovementState(State):
    def on_enter(self):
        print("Entering State A")

    def on_exit(self):
        print("Exiting State A")

    def execute(self):
        print("State A is executing")
        # State transition logic
        # For example:
        # if some_condition:
        #     self.state_machine.transition_to
