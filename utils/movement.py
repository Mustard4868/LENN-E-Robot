from machine import Pin

l_motor = Pin(0, Pin.OUT)
r_motor = Pin(1, Pin.OUT)

class Movement:
    def __init__(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y

    def move_x(dir_x):
        while True: l_motor, r_motor = 1
        else: l_motor, r_motor = 0
        
Movement.move_x(1)