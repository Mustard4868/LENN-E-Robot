import time as t

class Timer():
    def __init__(self):
        pass

    def Wait(time: int = None):
        """time: time in ms"""
        if not time:
            raise ValueError("Time must be greater than 0")
        else:
            start_time = t.time()
            while True:
                if start_time + time == t.time():
                    break
            return True

Timer = Timer()
Timer.Wait(10)