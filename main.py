import robot

def main():

    class LENN_E:
        def __init__(self):
            self.movement = robot.Movement(self)
            self.sensor = robot.Sensor(self)

        def __str__(self):
            return "LENN-E"

        def __repr__(self):
            return "LENN-E"

        def __eq__(self, other):
            return isinstance(other, LENN_E)

        def __ne__(self, other):
            return not self.__eq__(other)
        
if __name__ == "__main__":
    main()