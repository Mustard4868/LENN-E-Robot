class Sensor:
    def __init__(self, sensor):
        self.sensor = sensor

    class ColorSensor():
        def __init__(self, pin):
            self.pin = pin

        def GetColor(self):
            raise NotImplementedError
    
    class UltrasonicSensor():
        def __init__(self, pin):
            self.pin = pin

        def GetDistance(self):
            raise NotImplementedError
        
    class ContrastSensor():
        def __init__(self, pin):
            self.pin = pin

        def GetContrast(self):
            raise NotImplementedError