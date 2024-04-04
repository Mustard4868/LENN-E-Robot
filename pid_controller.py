class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, delta_t=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.delta_t = delta_t
        self.error_prev = 0
        self.error_acc = 0

    def calculate(self, e):
        # PID algorithm
        P = self.kp * e
        I = self.error_acc + self.ki * e * self.delta_t
        D = self.kd * (e - self.error_prev) / self.delta_t

        output = P + I + D

        # Update error values for the next iteration
        self.error_prev = e
        self.error_acc = I

        return output
