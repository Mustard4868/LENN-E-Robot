class PIDController:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint  # Desired value
        self.prev_error = 0
        self.integral = 0

    def update(self, process_variable):
        # Error calculation
        error = self.setpoint - process_variable

        # Proportional term
        proportional = self.kp * error

        # Integral term
        self.integral += error
        integral = self.ki * self.integral

        # Derivative term
        derivative = self.kd * (error - self.prev_error)
        self.prev_error = error

        # PID control output
        pid_output = proportional + integral + derivative

        return pid_output

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def reset(self):
        self.prev_error = 0
        self.integral = 0
