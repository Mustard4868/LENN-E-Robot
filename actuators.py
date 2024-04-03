from machine import Pin, PWM

class Motor:
    def __init__(self, enable, in_x, in_y):
        self.enable = PWM(Pin(enable), freq=1000)
        self.enable.duty(0)
        self.in_x = Pin(in_x, Pin.OUT)
        self.in_y = Pin(in_y, Pin.OUT)

    def setSpeed(self, speed: int = 0):
        "speed: percentage of 0% power to 100% power or -100% for reverse"
        if speed < -100 or speed > 100:
            raise ValueError("Speed must be between -100 and 100")
        
        if speed < 0:
            self.in_x.value(1)
            self.in_y.value(0)
        else:
            self.in_x.value(0)
            self.in_y.value(1)
        
        min_speed = 40
        if abs(speed) < min_speed and abs(speed) != 0:
            speed = min_speed
        
        pwm_out = 1023 * abs(speed) // 100

        self.enable.duty(pwm_out)

class Magnet:
    def __init__(self, signal_pin):
        self.signal = Pin(signal_pin, Pin.OUT)

    def Set(self, state: bool):
        """state: True for on, False for off"""
        self.signal.value(state)